# vim: ts=4 sw=4 noexpandtab
"""Sample module.

This is a the ModManager In Game Admin module

===== Config =====
 # Sets the prefix for all in game commands
 mm_iga.cmdPrefix "!"

 # Dynamic command binding take the following form:
 mm_iga.addCmdBinding "<privilege>|<alias>:<command>"

 # The default command Bindings
 mm_iga.addCmdBinding "k|kick:iga kick"
 mm_iga.addCmdBinding "b|ban:iga ban"
 mm_iga.addCmdBinding "m|map:map"
 mm_iga.addCmdBinding "s|switch:bf2cc switchplayer"
 mm_iga.addCmdBinding "w|warn:iga warn"
 mm_iga.addCmdBinding "r|restart:exec admin.restartMap"
 mm_iga.addCmdBinding "n|next:exec admin.runNextLevel"
 mm_iga.addCmdBinding "l|list:exec admin.listPlayers"

 # Adding admins takes the following form:
 mm_iga.addAdmin "<profileid|cdkeyhash>:<privilege1>,<privilege2>,...<privilegeX>"

 # The special privilege "all" allows the admin access to all commands

 # The message displayed when an player trys to use IGA but is not recognised as an admin
 mm_iga.notAdminMessage "Sorry %s you are not registered as an admin!"

 # The message displayed when an admin tries to use a command they are not authorised for
 mm_iga.notAuthedMessage "Sorry %s you are not permitted use the command %s"
	
 # The automatic authorisation level used for IGA admins
 mm_iga.authLevel 100
 
===== Rcon commands =====
 # List the current commands
 iga listCmds
 
 # Add a new command
 iga addCmd <cmd> <priv|alias1[...|aliasX]>
 
 # Remove a command and all its aliases
 iga delCmd <cmd>
 
 # List IGA admins
 iga listAdmins
 
 # Add a new IGA admin, priviledges are a comma seperate list of privileges
 iga addAdmin <profileid|cdkeyhash|name> <privs1,priv2...privX>
 
 # Remove an IGA admin and all their priviledges
 iga delAdmin <profileid|cdkeyhash|name>

===== History =====
 v1.7 - 12/10/2011:
 Added BFP4F Support

 v1.6 - 16/01/2009:
 Added warning reason support to kick and ban player
 
 v1.5 - 28/11/2008:
 Added support for replaceable arguments in all commands e.g.
 tk|tkwarn:iga warn %arg1% 'Dont team kill %arg1% or you will be banned next time!'
 
 v1.4 - 20/10/2008:
 Added preconfigured warning messages and replacements
 
 v1.3 - 20/08/2008:
 The automatic rcon auth handler now uses a "random" password for auth which is valid for a very limited time frame to prevent direct use of "rcon login"
 Fixed missing unregister for rcon cmd handlers
 Removed superfluous warning for iga alias on restart

 v1.2 - 31/07/2008:
 Stipped channel prefixes so commands work in all channels

 v1.1 - 28/06/2007:
 Now uses wildcard player determination

 v1.0 - 08/02/2007:
 Initial version

Copyright (c)2008 Multiplay
Author: Steven 'Killing' Hartland
"""

import bf2
import host
import mm_utils

# Set the version of your module here
__version__ = 1.7

# Set the required module versions here
__required_modules__ = {
	'modmanager': 1.7
}

# Does this module support reload ( are all its reference closed on shutdown? )
__supports_reload__ = True

# Sets which games this module supports
__supported_games__ = {
	'bf2': True,
	'bf2142': True,
	'bfheroes': True,
	'bfp4f': True
}

# Set the description of your module here
__description__ = "In Game Admin v%s" % __version__

# Add all your configuration options here
configDefaults = {
	'cmdPrefix': '!',
	'cmdBindings':
	[
		'k|kick:iga kick',
		'b|ban:iga ban',
		'm|map:map',
		's|switch:bf2cc switchplayer',
		'w|warn:iga warn',
		'r|restart:admin.restartMap',
		'n|next:admin.runNextLevel',
		'l|list:admin.listPlayers',
	],
	'admins': [],
	'notAdminMessage': 'Sorry %s you are not registered as an admin!',
	'notAuthedMessage': 'Sorry %s you are not permitted use the command %s',
	'warnings':
	[
      	'tk|team killing:%action% %player% stop Team Killing!',
      	'lang|language:%action% %player% stop using Bad Language!',
		'vh|vehicle whore:%action% %player% stop Stealing/Shooting Teammates Vehicles!',
		'hp|high ping:%action% %player% High Ping!',
		'spam|spamming:%action% %player% stop Spamming Messages!',
		'i|idle:%action% %player% for being Idle!',
		'sp|Cheating Stats:%action% %player% stop Stat Padding!',
		'mr|make room for admin:%action% %player% to make room for an Admin',
		'nv|name violation:%action% %player% for Name Violation!',
	],
	'warningPrefix': '[%admin%] ',
	'warningAction': 'Warning',
	'authLevel': 100,
}

class InGameAdmin( object ):

	def __init__( self, modManager ):
		# ModManager reference
		self.mm = modManager

		# Internal shutdown state
		self.__state = 0
		self.__igacmds = {}
		self.__warnings = {}
		self.__admins = {}
		self.__privs = { 'all': True }

		# Our internal commands
		self.__cmds = {
			# Cmd methods
			'listCmds': { 'method': self.cmdListCmds, 'level': 10 },
			'addCmd': { 'method': self.cmdAddCmd, 'args': '<cmd> <priv|alias1[...|aliasX]>', 'level': 30 },
			'delCmd': { 'method': self.cmdDelCmd, 'args': '<cmd>', 'level': 30 },

			# Admin methods
			'listAdmins': { 'method': self.cmdListAdmins, 'level': 10 },
			'addAdmin': { 'method': self.cmdAddAdmin, 'args': '<profileid|cdkeyhash|name> <privs>', 'level': 30 },
			'delAdmin': { 'method': self.cmdDelAdmin, 'args': '<profileid|cdkeyhash|name>', 'level': 30 },

			# Extended methods
			'kick': { 'method': self.cmdKickPlayer, 'level': 5 },
			'ban': { 'method': self.cmdBanPlayer, 'level': 5 },
			'warn': { 'method': self.cmdWarnPlayer, 'level': 2 },
		}

		# Add any static initialisation here.
		# Note: Handler registration should not be done here
		# but instead in the init() method

	def cmdKickPlayer( self, ctx, cmd ):
		"""Kick a player from the server with a message."""
		self.mm.rcon().kickPlayer( ctx, cmd, True );
		( playerid, reason ) = mm_utils.largs( cmd, None, 2, '' )
		reason = reason.lower()
		if self.__warnings.has_key( reason ):
			# message shortcut replace
			reason = self.__warnings[reason]
			self.mm.rcon().kickPlayer( ctx, ( "'%s' '%s'" ) % ( playerid, reason ) , True )
		else:
			self.mm.rcon().kickPlayer( ctx, cmd, True )

	def cmdBanPlayer( self, ctx, cmd ):
		"""Ban a player for a specified time period from the server with a message."""
		( playerid, banReason, banPeriod ) = mm_utils.largs( cmd, None, 3, '' )
		banReason = banReason.lower()
		if self.__warnings.has_key( banReason ):
			# message shortcut replace
			banReason = self.__warnings[banReason]
			self.mm.rcon().banPlayer( ctx, ( "'%s' '%s' '%s'" ) % ( playerid, banPeriod, banReason ) , True )
		else:
			self.mm.rcon().banPlayer( ctx, cmd, True )

	def cmdWarnPlayer( self, ctx, cmd ):
		"""Send a message to a specific player."""
		( playerid, msg ) = mm_utils.largs( cmd, None, 2, '' )

		player = mm_utils.find_player( playerid, True )

		if player is None:
			ctx.write( 'Error: player %s not found\n' % playerid )
			self.mm.error( "Failed to find player %s" % playerid )
		else:
			lmsg = msg.lower()
			if self.__warnings.has_key( lmsg ):
				# message shortcut replace
				msg = self.__warnings[lmsg]

			msg = self.__config['warningPrefix'] + msg
			msg = msg.replace( '%player%', player.getName().strip( ' ' ) );
			msg = msg.replace( '%action%', self.__config['warningAction'] );
			msg = msg.replace( '%admin%', ctx.bf2ccClient.adminName );

			mm_utils.msg_player( player.index, msg )
			ctx.write( 'Chat sent to player %s\n' % playerid )

	def cmdExec( self, ctx, cmd ):
		"""Execute a Announcer sub command."""
		return mm_utils.exec_subcmd( self.mm, self.__cmds, ctx, cmd )

	def runCmd( self, playerid, cmd, args ):
		"""Runs an admin command."""
		ctx = self.mm.getRconContext( playerid )
		if not ctx.authedLevel:
			# Automatically log the player in
			ctx.autoLogin = "%d:%d" % ( playerid, int( host.timer_getWallTime() ) )
			self.mm.runRconCommand( playerid, "login %s" % ctx.autoLogin )
			ctx.autoLogin = "" # Prevent future logins
			logout = True
		else:
			logout = False

		if -1 != cmd.find( '%arg' ):
			# Have replacement params so iterate through replacing
			args_list = mm_utils.largs( args, None, 0, '', True )
			for i in range( len( args_list ) ):
				arg_name = ( "%%arg%s%%" % ( i + 1 ) );
				cmd = cmd.replace( arg_name, args_list[i] )
			args = ""
		ret = self.mm.runRconCommand( playerid, "%s %s" % ( cmd, args ) )

		# Automatically log the player in
		if logout:
			self.mm.runRconCommand( playerid, "logout" )

		return ret
		
		
	def onChatMessage( self, playerid, text, channel, flags ):
		"""Check for in game commands."""
		if 1 != self.__state:
			return 0

		try:
			# Strip channel prefixes so commands can be used in all channels
			text = mm_utils.MsgChannels.named[channel].stripPrefix( text )
			self.mm.debug( 2, "Chat[%d]: '%s'" % ( playerid, text ) )
			player = bf2.playerManager.getPlayerByIndex( playerid )
			if player:
				prefix = self.__config['cmdPrefix']
				if text.startswith( prefix ):
					# We have a potential command
					( cmd, args ) = mm_utils.largs( text[len(prefix):], None, 2, '', True )
					self.mm.debug( 2, "CMD?: '%s' '%s'" % ( cmd, args ) )
					if cmd in self.__igacmds:
						# We have a command
						cdkeyhash = mm_utils.get_cd_key_hash( player )
						profileid = str( player.getProfileId() )
						playername = player.getName()
						admins = self.__admins
						self.mm.debug( 2, "Looking for: %s, %s, %s" % ( cdkeyhash, profileid, playername ) )
						if cdkeyhash in admins:
							# User is an admin
							admin = cdkeyhash
						elif profileid in admins:
							# User is an admin
							admin = profileid
						elif playername in admins:
							# User is an admin
							admin = playername
						else:
							# User is not an admin
							mm_utils.msg_player( player.index, self.__config['notAdminMessage'] % ( playername ) )
							return

						# User is an admin
						details = self.__igacmds[cmd]
						if details['priv'] in admins[admin] or 'all' in admins[admin]:
							self.runCmd( playerid, details['cmd'], args )
						else:
							mm_utils.msg_player( player.index, self.__config['notAuthedMessage'] % ( playername, cmd ) )
		except:
			self.mm.error( "Oops bad", True )


	def inGameAuth( self, ctx, cmd ):
		""" In Game Authentication handler.

		This authorises a user based on the their hash or profileid's presence in our admins list.
		"""
		password = cmd.strip()

		# Note: we dont log failures as there may be more auth handlers
		if ctx.isInGame():
			player = bf2.playerManager.getPlayerByIndex( ctx.player )
			cdkeyhash = mm_utils.get_cd_key_hash( player )
			profileid = str( player.getProfileId() )
			playername = player.getName()
			admins = self.__admins
			if cdkeyhash in admins:
				# User is an admin
				admin = cdkeyhash
			elif profileid in admins:
				# User is an admin
				admin = profileid
			elif playername in admins:
				# User is an admin
				admin = playername
			else:
				# User is not an admin
				return 0
			
			try:
				self.mm.warn( "inGameAuth: %s == %s" %  ( password, ctx.autoLogin ) )
				if "" != password and password == ctx.autoLogin:
					return self.__config['authLevel']
			except:
				self.mm.warn( "inGameAuth: %s ( no autoLogin )" %  password )

		return 0

	def inGameAllowed( self, ctx, details ):
		"""In Game method allowed handler.

		Checks to see if the user is allowed to use the method.
		"""
		if ctx.authedLevel >= details['level']:
			return True
		else:
			return False

	def cmdListCmds( self, ctx, cmd ):
		"""Lists the commands available via IGA."""
		i = 0
		for priv in self.__privs.keys():
			if 'all' != priv:
				aliases = self.__privs[priv]
				ctx.write( "Priv '%s' => Command '%s', aliases: %s\n" % ( priv, self.__igacmds[priv]['cmd'], ", ".join( aliases )  ) )
				i = i + 1
		ctx.write( "%d IGA Commands\n" % ( i ) )

	def cmdListAdmins( self, ctx, cmd ):
		"""Lists the Admins and their privs known to IGA."""
		i = 0
		for admin in self.__admins.keys():
			ctx.write( "Admin '%s' privileges: %s\n" % ( admin, ", ".join( self.__admins[admin] )  ) )
			i = i + 1
		ctx.write( "%d IGA Admins\n" % ( i ) )

	def cmdAddCmd( self, ctx, cmd ):
		"""Adds a command into our supported commands set."""
		( command, aliases_str ) = mm_utils.largs( cmd, None, 2, '' )
		return self.__addCmd( ctx, command, aliases_str )

	def __addCmd( self, ctx, aliases_str, cmd ):
		"""Adds a command into our supported commands set."""
		aliases = aliases_str.strip( '"\' ' ).split( '|' )
		priv = aliases[0]
		for alias in aliases:
			if alias in self.__igacmds and cmd != self.__igacmds[alias]['cmd']:
				msg = "IGA: cmd '%s' overrides alias '%s' for cmd '%s'\n" % ( cmd, alias, self.__igacmds[alias]['cmd'] )
				self.mm.warn( msg )
				if ctx is not None:
					ctx.write( msg )
			self.__igacmds[alias] = { 'cmd': cmd, 'priv': priv }

		if priv in self.__privs:
			msg = "IGA: cmd '%s' overrides privilege '%s' for cmd '%s'\n" % ( cmd, priv, self.__igacmds[priv]['cmd'] )
			self.mm.warn( msg )
			if ctx is not None:
				ctx.write( msg )
		self.__privs[priv] = aliases

	def __addWarn( self, ctx, aliases_str, msg ):
		"""Adds a warning into our supported warnings set."""
		aliases = aliases_str.strip( '"\'' ).split( '|' )
		for alias in aliases:
			if alias in self.__warnings and msg != self.__warnings[alias]:
				msg = "IGA: warning '%s' overrides alias '%s' for warning '%s'\n" % ( msg, alias, self.__warnings[alias] )
				self.mm.warn( msg )
				if ctx is not None:
					ctx.write( msg )
			self.mm.info( "added: %s = %s" % ( alias, msg ) )
			self.__warnings[alias] = msg

	def cmdDelCmd( self, ctx, cmd ):
		"""Adds a command into our supported commands set."""
		if cmd in self.__privs:
			aliases = self.__privs[cmd]
			for alias in aliases:
				del self.__privs[alias]
			msg = "Command '%s' removed\n" % ( cmd )
			self.mm.warn( msg )
			if ctx is not None:
				ctx.write( msg )
		else:
			msg = "IGA: cmd '%s' doesn't exist\n" % ( cmd )
			self.mm.warn( msg )
			if ctx is not None:
				ctx.write( msg )


	def cmdAddAdmin( self, ctx, cmd ):
		"""Adds an admin into our authorised admin set."""
		( admin, privs_str ) = mm_utils.largs( cmd, None, 2, '' )
		return self.__addAdmin( ctx, admin, privs_str )
		
	def __addAdmin( self, ctx, admin, privs_str ):
		"""Adds an admin into our authorised admin set."""
		privs = {}
		for priv in privs_str.strip( '"\' ' ).split( ',' ):
			if priv in self.__privs:
				# valid priv
				privs[priv] = True
			else:
				# invalid priv
				msg = "IGA: invalid privaledge '%s' requested for admin '%s'\n" % ( priv, admin )
				self.mm.warn( msg )
				if ctx is not None:
					ctx.write( msg )

		self.__admins[admin] = privs

		msg = "Admin '%s' added" % admin
		self.mm.info( msg )
		if ctx is not None:
			ctx.write( msg )

	def cmdDelAdmin( self, ctx, cmd ):
		"""Removes an admin into our authorised admin set."""
		return self.__delAdmin( ctx, cmd.strip( '"\' ' ) )

	def __delAdmin( self, ctx, admin ):
		"""Removes an admin into our authorised admin set."""
		if admin in self.__admins:
			del self.__admins[admin]
			msg = "Admin '%s' removed\n" % admin
			self.mm.info( msg )
			if ctx is not None:
				ctx.write( msg )
		else:
			msg = "Admin '%s' doesnt exist\n" % admin
			self.mm.warn( msg )
			if ctx is not None:
				ctx.write( msg )

	def init( self ):
		"""Provides default initialisation."""

		# Load the configuration
		self.__config = self.mm.getModuleConfig( configDefaults )

		# Load in the commands
		for line in self.__config['cmdBindings']:
			try:
				( aliases_str, cmd ) = line.strip( '"\' ' ).split( ':', 1 )
				self.__addCmd( None, aliases_str, cmd )
			except:
				self.mm.error( "IGA: Invalid command binding '%s'" % line )

		# Load in the admins
		for line in self.__config['admins']:
			try:
				( admin, privs_str ) = line.strip( '"\' ' ).split( ':', 1 )
				self.__addAdmin( None, admin, privs_str )
			except:
				self.mm.error( "IGA: Invalid admin '%s'" % line )

		# Load in the warnings
		for line in self.__config['warnings']:
			try:
				( aliases_str, warn ) = line.split( ':', 1 )
				self.__addWarn( None, aliases_str, warn )
			except:
				self.mm.error( "IGA: Invalid warning '%s'" % line )

		# Register your game handlers and provide any
		# other dynamic initialisation here
		self.mm.registerRconAuthHandler( self.inGameAuth, self.inGameAllowed )

		if 0 == self.__state:
			# Register your host handlers here
			host.registerHandler( 'ChatMessage', self.onChatMessage, 1 )

		# Register our rcon command handlers
		self.mm.registerRconCmdHandler( 'iga', { 'method': self.cmdExec, 'subcmds': self.__cmds, 'level': 1 } )

		# Update to the running state
		self.__state = 1

	def shutdown( self ):
		"""Shutdown and stop processing."""

		# Unregister game handlers and do any other
		# other actions to ensure your module no longer affects
		# the game in anyway
		self.mm.unregisterRconAuthHandler( self.inGameAuth )

		# Unregister our rcon command handlers
		self.mm.unregisterRconCmdHandler( 'iga' )

		# Flag as shutdown as there is currently way to:
		# host.unregisterHandler
		self.__state = 2

	def update( self ):
		"""Process and update.
		Note: This is called VERY often processing in here should
		be kept to an absolute minimum.
		"""
		pass

def mm_load( modManager ):
	"""Creates and returns your object."""
	return InGameAdmin( modManager )
