# vim: ts=4 sw=4 noexpandtab
"""Slot reserver system

This is a slot reserver ModManager module.

It works by kicking people when the reserved slots limit is reached, hence keeping the slots open for "registered" players ( mm_reserver.addProfileId 11111 ).
If all registered players are in the server then no slots are kept open.

This is by no means optimium but without the ability to password the server on the fly or to know when a "registered" player is attempting to join there are no other ways.
Due to this please only use this module if absolultely required and keep the reservedSlots to a minimum.

This module is very much still '''BETA''' due to some missing functionality in the BattleField 2 servers itself.

===== Config =====
 # The number of slots to reserver
 mm_reserver.reservedSlots 1
 
 # The delay after messaging the player before they are kicked
 mm_reserver.kickDelay 5
 
 # The kick mode used:
 # 1: On spawn ( default: tells the player why they are being kicked )
 # 2: On connect ( kicks as soon as the player attempts to connect )
 mm_reserver.kickMode 2
 
 # The kick type used:
 # 1: rcon
 mm_reserver.kickType 1
 
 # The message used
 mm_reserver.kickReason "Reserved slots reached"
 
 # The private password to be used on the server when reserved slots are required
 mm_reserver.privatePassword ""

 # Add profileids to the reserved list
 mm_reserver.addProfileId 11111
 mm_reserver.addProfileId 22222

===== Notes =====
* On ranked servers the maximum number of slots that can be reserved is 20% of the total slots available
* Punkbuster kick is not currently supported
* The private password is currently only effective on none ranked servers

===== History =====
 v0.8 - 12/10/2011:
 Added BFP4F Support

 v0.7 - 30/08/2006:
 Added supported games

 v0.6 - 19/08/2006:
 Corrected unescaped literal % in warning for too high reserved slots

 v0.5 - 02/08/2006:
 Replaced kickMessage with kickReason
 Now uses banmanager.kickPlayer hence requires MM v1.2
 
 v0.4 - 02/08/2005:
 Default kick mode is now Kick on Connect ( no message ) to prevent message
 spam on busy servers until private messaging is fixed
 
 v0.3 - 02/08/2005:
 Corrected kicking already playing players on spawn
 
 v0.2 - 01/07/2005:
 Added a private password option
 
 v0.1 - 28/06/2005:
 Initial version

Copyright (c)2008 Multiplay
Author: Steven 'Killing' Hartland
"""

import bf2
import host
import mm_utils

__version__ = 0.8

__required_modules__ = {
	'modmanager': 1.6
}

__supports_reload__ = True

__supported_games__ = {
	'bf2': True,
	'bf2142': True,
	'bfheroes': False,
	'bfp4f': False
}

__description__ = "ModManager Reserver v%s" % __version__

class KickMode:
	onSpawn = 1
	onConnect = 2

# Add all your configuration options here
configDefaults = {
	'reservedSlots': 1,
	'privatePassword': '',
	'kickDelay': 5,
	'kickMode': KickMode.onConnect,
	'kickType': mm_utils.KickBanType.rcon,
	'profileIds': [],
	'kickReason': "Reserved slots reached"
}

class Reserver( object ):

	def __init__( self, modManager ):
		# ModManager reference
		self.mm = modManager

		# Internal shutdown state
		self.__state = 0

		# Your rcon commands go here:
		self.__cmds = {
			'addProfileId': { 'method': self.cmdAddProfileId, 'args': '<profileid>', 'level': 30 },
			'removeProfileId': { 'method': self.cmdRemoveProfileId, 'args': '<profileid>', 'level': 30 },
			#'listPlayers': { 'method': self.cmdListPlayers },
			'listProfileIds': { 'method': self.cmdListProfileIds, 'level': 30 },
			'setPassword': { 'method': self.cmdSetPassword, 'level': 30 }
		}

	def cmdExec( self, ctx, cmd ):
		"""Execute a Reserver sub command."""

		# Note: The Python doc above is used for help / description
		# messages in rcon if not overriden
		return mm_utils.exec_subcmd( self.mm, self.__cmds, ctx, cmd )

	def cmdSetPassword( self, ctx, cmd ):
		"""Sets the Private Password."""

		self.__config['privatePassword'] = cmd

		ctx.write( "Private Password updated\nSave your config to make this permanent!\n" )
		self.mm.info( "Admin '%s' set the private password" % ctx.getName() )
		return 1

	def cmdAddProfileId( self, ctx, cmd ):
		"""Adds the profileid to the list of reserved ids"""

		self.mm.debug( 2, "Adding profileid '%s'" % cmd )
		try:
			profileid = int( cmd )
		except TypeError:
			ctx.write( "Invalid profileid '%s'" % cmd )
			return 0

		self.__config['profileIds'].append( profileid )
		self.__profileIds[profileid] = 1
		ctx.write( "Added profileid '%d' to the reserved list\nSave your config to make this permanent!\n" % profileid )
		return 1

	def cmdRemoveProfileId( self, ctx, cmd ):
		"""Remove the profileid from the list of reserved ids"""

		self.mm.debug( 2, "Remove profileid '%s'" % cmd )
		try:
			profileid = int( cmd )
		except TypeError:
			ctx.write( "Invalid profileid '%s'" % cmd )
			return 0
		del self.__profileIds[profileid]
		self.__config['profileIds'] = self.__profileIds.keys()
		ctx.write( "Removed profileid '%d' to the reserved list\nSave your config to make this permanent!\n" % profileid )
		return 1

	def cmdListPlayers( self, ctx, cmd ):
		"""List the players and their profileids."""
		players = bf2.playerManager.getPlayers()
		if not players:
			ctx.write( "No connected players\n" )
		else:
			ctx.write( "ProfileId: Name\n" )
			for player in players:
				ctx.write( "%d: %s\n" % ( player.getProfileId(), player.getName() ) )

	def cmdListProfileIds( self, ctx, cmd ):
		"""List the currently reserved profileids."""
		if not self.__profileIds:
			ctx.write( "No reserved ProfileIds set\n" )
		else:
			ctx.write( "ProfileId\n" )
			for profileid in self.__profileIds:
				ctx.write( "%d\n" % profileid )

	def onPlayerConnect( self, player ):
		"""Kick the player if required."""
		if 1 != self.__state:
			return 0

		# Need to check due to changes
		if self.__config['kickMode'] == KickMode.onConnect:
			self.__checkPlayer( player )

		# Flag that this player has just connected
		player.mmSpawned = False

		return self.__updateServerPassword()

	def onPlayerDisconnect( self, player ):
		"""Remove player from reserved list."""
		if 1 != self.__state:
			return 0

		if self.__reservedPlayers.has_key( player.index ):
			del self.__reservedPlayers[player.index]

		return self.__updateServerPassword()

	def onPlayerSpawn( self, player, soldier ):
		"""Kick the player if required."""
		if 1 != self.__state:
			return 0

		# Need to check due to changes
		if not player.mmSpawned:
			player.mmSpawned = True
			# N.B. two part if to ensure config changes work appropriatly
			if self.__config['kickMode'] == KickMode.onSpawn:
				self.__checkPlayer( player )		

	def __updateServerPassword( self ):
		"""Sets or removes the password on the server depending on the state."""
		if not host.ss_getParam('ranked') and self.__config['privatePassword']:
			# We can password the server as its not ranked
			( needed_slots, remaining_slots ) = self.__neededRemainingSlots()
			if not needed_slots:
				# dont need any reserved slots remove the password
				host.rcon_invoke( 'sv.password ""' )
			else:
				host.rcon_invoke( 'sv.password "%s"' % self.__config['privatePassword'] )

		return 1

	def __neededRemainingSlots( self ):
		"""Returns the number of needed slots."""
		needed_slots = len( self.__profileIds ) - len( self.__reservedPlayers )
		if not needed_slots:
			# all reserved playerid's are already playing ignore
			return ( 0, 0 )

		# Find the min number of slots we need to reserve
		if self.__config['reservedSlots'] < needed_slots:
			needed_slots = self.__config['reservedSlots']

		remaining_slots = bf2.serverSettings.getMaxPlayers() - bf2.playerManager.getNumberOfPlayers()
		self.mm.debug( 3, "R-Need: %d, %d" % ( needed_slots, remaining_slots ) )
		return ( needed_slots, remaining_slots )

	def __checkPlayer( self, player ):
		"""Check to see if this player should be allowed."""
		( needed_slots, remaining_slots ) = self.__neededRemainingSlots()
		if not needed_slots:
			# dont need any reserved slots
			return 1

		if needed_slots > remaining_slots:
			# We need to reserve this slot
			if self.__profileIds.has_key( player.getProfileId() ):
				# Player is in the reserved list let them in
				self.__reservedPlayers[player.index] = player
				return 1
			else:
				# Player was not in the reserved list say by by
				return self.__kickPlayer( player, remaining_slots, needed_slots )
		return 1

	def __kickPlayer( self, player, remaining_slots, needed_slots ):
		"""Kick the player."""
		if self.__config['kickMode'] == KickMode.onSpawn:
			# Inform the player why they are being kicked
			# delay then kick them
			self.mm.banManager().kickPlayer( player, self.__config['kickReason'], self.__config['kickDelay'], self.__config['kickType'] )
		else:
			# No point informing them they wont see it
			self.mm.banManager().kickPlayerNow( player, self.__config['kickType'] )

		return 1

	def init( self ):
		"""Provides default initialisation."""

		# Load the configuration
		self.__config = self.mm.getModuleConfig( configDefaults )
		self.__profileIds = dict.fromkeys( self.__config['profileIds'], 1 )
		self.__newPlayers = {}
		self.__reservedPlayers = {}

		if host.ss_getParam('ranked'):
			# Max of 20%
			max_reserved = ( host.ss_getParam( 'maxPlayers' ) * 0.2 )
			if self.__config['reservedSlots'] > max_reserved:
				self.mm.warn( "Max reserved slots is 20%% of maxPlayers on ranked servers, setting to %d" % max_reserved )
				self.__config['reservedSlots'] = max_reserved

		# Register your game handlers and provide any
		# other dynamic initialisation here
		if 0 == self.__state:
			host.registerHandler( 'PlayerSpawn', self.onPlayerSpawn, 1 )
			host.registerHandler( 'PlayerConnect', self.onPlayerConnect, 1 )
			host.registerHandler( 'PlayerDisconnect', self.onPlayerDisconnect, 1 )

		# Register our rcon command handlers
		self.mm.registerRconCmdHandler( 'reserver', { 'method': self.cmdExec, 'subcmds': self.__cmds, 'level': 1 } )

		# Update to the running state
		self.__state = 1

	def shutdown( self ):
		"""Shutdown and stop processing."""

		# Unregister game handlers and do any other
		# other actions to ensure your module no longer affects
		# the game in anyway
		self.mm.unregisterRconCmdHandler( 'reserver' )

		# Flag as shutdown as there is currently way to:
		# host.unregisterHandler
		self.__state = 2

def mm_load( modManager ):
	"""Creates your object."""
	return Reserver( modManager )
