# vim: ts=4 sw=4 noexpandtab
"""Player Kicker.

This is a Player Kicker ModManager module it kicks high ping,
low ping and idle players.

===== Config =====
 # The maximum ping before violation is triggered ( 0 = disabled )
 mm_kicker.maxPing 250
 
 # The minimum ping before violation is triggered ( 0 = disabled )
 mm_kicker.minPing 0
 
 # The minimum score before players are kicked ( 0 = disabled )
 mm_kicker.negScoreKick -15
 
 # The number of ping violations before a player is kicked
 mm_kicker.pingLimit 8
 
 # The maximum time a player can be idle before being kicked ( 0 = disabled )
 mm_kicker.idleLimit 300
 
 # Ignore idle players while waiting for min players to start a round
 mm_kicker.idleIgnoreNotStarted 1
 
 # The delay on map start before samples at taken
 mm_kicker.initDelay 60
 
 # The period over which samples are considered
 mm_kicker.samplePeriod 120
 
 # The delay applied to position information to prevent cheating
 mm_kicker.positionDelay 120
 
 # The time between samples
 mm_kicker.sampleRate 10
 
 # The type of kick used:
 # 1: rcon
 mm_kicker.kickType 1
 
 # The delay after informing the player before they are kicked / banned
 mm_kicker.kickDelay 5
 
 # Add a word which if said will result in a ban word violation
 mm_kicker.addBanWord "newbee"
 mm_kicker.addBanWord "badman"
 
 # Add a pattern which if matched will result in a ban word violation
 mm_kicker.addBanPattern ".*bee"
 
 # The number of ban word violations before a player is banned
 mm_kicker.banLimit 1
 
 # Add a word which if said will result in a kick word violation
 mm_kicker.addKickWord "killer"
 mm_kicker.addKickWord "upety"
 
 # Add a pattern which if matched will result in a kick word violation
 mm_kicker.addKickPattern ".*ller"
 mm_kicker.addKickPattern "Kill.*"
 
 # The number of kick word violations before a player is kicked
 mm_kicker.kickLimit 3
 
 # The period a ban lasts for
 mm_kicker.banPeriod "Round"
 
 # The ban reason used when a player is banned
 mm_kicker.banWordReason "Using bad / racist language"
 
 # The message displayed to a player when they are kicked
 mm_kicker.kickWordReason "Using bad / racist language"
 
 # The message displayed to a player when they are warned about bad / ban words
 mm_kicker.warnWordMessage "WARNING: Please refrain from using bad / racist language on this server '%s'"
 
 # Enable chat checks, set to 0 to disable them
 mm_kicker.enableChatChecks 1

===== Notes =====
* All times are in seconds
* It is recommended you use addBanWord and addKickWord instead of patterns as it is much more efficient
* When changing messages ensure that any replacement parameters are maintained e.g. %s

===== History =====
 v2.6 - 12/10/2011:
 Added BFP4F Support

 v2.5 - 01/05/2008:
 Updated to use configured kickType in all places and added banType option
 
 v2.4 - 18/02/2008:
 Fixed chat checks failing

 v2.3 - 28/10/2007:
 Added checks for invalid kick and ban patterns
 
 v2.2 - 30/08/2006:
 Added supported games
 
 v2.1 - 22/02/2006:
 Removed kickMessage as its now handled via mm_banmanager
 Now uses banmanager.kickPlayer hence requires MM v1.2
 Replaced kickWordMessage with kickWordReason
 
 v2.0 - 15/02/2006:
 Now uses self.mm.banManager().<method>
 Now requires ModManager version 1.1
 Config option banWordMessage removed and replaced with banWordReason for ban manager compatibility
 
 v1.9 - 23/08/2005:
 Corrected round check
 Changed default negative kick to -15
 Upated ban checks to corrected variable name
 Now only switches dead players if the game is in progress.
 
 v1.8 - 14/08/2005:
 Added idleIgnoreNotStarted defaults to 1 which means idle kicks are disabled
 while the round has not started ( below min players to start )
 Disabled enhanced debug in main kick routine
 Now detects bad language in the first word of dead messages
 Added negative score kick
 
 v1.7 - 12/08/2005:
 Fixed typo's in "message" variables ensure ur modmanager.con is correct
 
 v1.6 - 11/08/2005:
 Fixed Max / Min ping warnings for ranked servers
 
 v1.5 - 08/08/2005:
 Added control point checks to idle detection
 Added bullets fired checks to idle detection
 Added error checking to main player check method
 
 v1.4 - 02/08/2005:
 maxPing and idleLimit checks can now be disabled by setting their values to 0
 Added enableChatChecks, set to 0 to disable all chat checks
 
 v1.3 - 02/08/2005:
 Fixes for initial bad word in team say.
 High / low ping expiry corrected.
 Default pingLimit is now 8
 
 v1.2 - 30/07/2005:
 Added bad word checks
 Updated to use one structure stored on the player
 
 v1.1 - 29/07/2005:
 Added idle checks
 Renamed from mm_ping_picker -> mm_kicker
 
 v1.0 - 01/07/2005:
 Initial version

Copyright (c)2008 Multiplay
Author: Steven 'Killing' Hartland
"""

import bf2
import host
import mm_utils
import re

__version__ = 2.6

__required_modules__ = {
	'modmanager': 1.6
}

__supports_reload__ = True

__supported_games__ = {
	'bf2': True,
	'bf2142': True,
	'bfheroes': True,
	'bfp4f': True
}

__description__ = "ModManager Player Kicker v%s" % __version__

class KickReason:
	highPing = 'ping too high'
	lowPing = 'ping too low'
	idle = 'idler'
	negScore = 'negative score'

# Add all your configuration options here
configDefaults = {
	'maxPing': 250,
	'minPing': 0,
	'pingLimit': 8,
	'idleLimit': 300,
	'idleIgnoreNotStarted': 1,
	'initDelay': 60,
	'samplePeriod': 120,
	'sampleRate': 10,
	'positionDelay': 120,
	'negScoreKick': -15,
	'kickType': mm_utils.KickBanType.rcon,
	'kickDelay': 5,
	'banType': mm_utils.BanMethod.key,

	# Chat Spam
	'chatSpamLimit': 5,
	'chatSpamPeriod': 5,
	'chatSpamBanReason': "Chat spam",
	'chatSpamBanPeriod': 'Round',

	# Bad Words
	'banWords': [],
	'banPatterns': [],
	'banLimit': 1,
	'banPeriod': 'Round',
	'banWordReason': "Using bad / racist language",
	'kickWords': [],
	'kickPatterns': [],
	'kickLimit': 3,
	'kickWordReason': "Using bad / racist language",
	'warnWordMessage': "WARNING: Please refrain from using bad / racist language on this server '%s'",
	'enableChatChecks': 1
}

class KickerInfo( object ):
	def __init__( self ):
		self.highPing = []
		self.lowPing = []
		self.posHistory = []
		self.kickWordWarnings = 0
		self.banWordWarnings = 0
		self.idleTime = 0
		self.lastPos = ( 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 )
		self.lastScore = 0
		self.lastCheck = self.connectedAt = host.timer_getWallTime()
		self.lastBulletsFired = 0
		self.chatSpamCheck = []
 
	def roundReset( self ):
		"""Resets data that is round dependent."""
		self.posHistory = []
		self.highPing = []
		self.lowPing = []

	def safePos( self ):
		"""Return a cheat safe position."""
		return self.posHistory[0]['pos']

class Kicker( object ):

	def __init__( self, modManager ):
		# ModManager reference
		self.mm = modManager
		self.__state = 0

		# Our internal commands
		self.__cmds = {
			# Global methods
			'listWords': { 'method': self.cmdListWords, 'level': 10 },

			# Ban word methods
			'addBanWord': { 'method': self.cmdAddBanWord, 'args': '<word>', 'level': 30 },
			'removeBanWord': { 'method': self.cmdRemoveBanWord, 'args': '<word>', 'level': 30 },
			'clearBanWords': { 'method': self.cmdClearBanWords, 'level': 30 },

			# Ban pattern methods
			'addBanPattern': { 'method': self.cmdAddBanPattern, 'args': '<word>', 'level': 30 },
			'removeBanPattern': { 'method': self.cmdRemoveBanPattern, 'args': '<word>', 'level': 30 },
			'clearBanPatterns': { 'method': self.cmdClearBanPatterns, 'level': 30 },

			# Kick word methods
			'addKickWord': { 'method': self.cmdAddKickWord, 'args': '<word>', 'level': 30 },
			'removeKickWord': { 'method': self.cmdRemoveKickWord, 'args': '<word>', 'level': 30 },
			'clearKickWords': { 'method': self.cmdClearKickWords, 'level': 30 },

			# Kick pattern methods
			'addKickPattern': { 'method': self.cmdAddKickPattern, 'args': '<word>', 'level': 30 },
			'removeKickPattern': { 'method': self.cmdRemoveKickPattern, 'args': '<word>', 'level': 30 },
			'clearKickPatterns': { 'method': self.cmdClearKickPatterns, 'level': 30 }
		}

	def cmdExec( self, ctx, cmd ):
		"""Execute a Kicker sub command."""

		# Note: The Python doc above is used for help / description
		# messages in rcon if not overriden
		return mm_utils.exec_subcmd( self.mm, self.__cmds, ctx, cmd )

	def cmdListWords( self, ctx, cmd ):
		"""List the current ban / kick words."""

		if self.__banWords:
			idx = 0
			ctx.write( 'Ban words:\n' )
			for msg in self.__banWords:
				ctx.write( "#%d: '%s'\n" % ( idx, msg ) )
				idx += 1
			ctx.write( '\n' )
		else:
			ctx.write( 'No ban words\n' )

		if self.__banPatterns:
			idx = 0
			ctx.write( 'Ban patterns:\n' )
			for msg in self.__banPatterns:
				ctx.write( "#%d: '%s'\n" % ( idx, msg ) )
				idx += 1
			ctx.write( '\n' )
		else:
			ctx.write( 'No ban patterns\n' )

		if self.__kickWords:
			ctx.write( 'Kick words:\n' )
			idx = 0
			for msg in self.__kickWords:
				ctx.write( "#%d: '%s'\n" % ( idx, msg ) )
				idx += 1
		else:
			ctx.write( 'No kick words\n' )

		if self.__kickPatterns:
			idx = 0
			ctx.write( 'Kick patterns:\n' )
			for msg in self.__kickPatterns:
				ctx.write( "#%d: '%s'\n" % ( idx, msg ) )
				idx += 1
			ctx.write( '\n' )
		else:
			ctx.write( 'No kick patterns\n' )

		return 1

	#
	# Ban word methods
	#

	def cmdAddBanWord( self, ctx, cmd ):
		"""Add a word which if said will get a player ban."""
		word = cmd.strip( '" ' ).lower()
		self.__banWords[word] = len( self.__kickWords )
		self.mm.addParam( 'banWords', word )

		ctx.write( "Ban word '%s' added\n" % word )

		return 1

	def cmdRemoveBanWord( self, ctx, cmd ):
		"""Remove a word for the ban list."""
		word = cmd.strip( '" ' ).lower()
		if not self.__banWords.has_key( word ):
			msg = "Invalid ban word '%s' (not found)" % word
			self.mm.info( msg )
			ctx.write( msg )
			return 0

		self.mm.removeParam( 'banWords', self.__banWords[word] )
		del self.__banWords[word]
		ctx.write( "Ban word '%s' removed\n" % word )

		return 1

	def cmdClearBanWords( self, ctx, cmd ):
		"""Removes all ban words."""
		self.__banWords = {}

		self.mm.setParam( 'banWords', [] )

		ctx.write( "All ban words removed\n" )

		return 1

	#
	# Ban pattern methods
	#

	def cmdAddBanPattern( self, ctx, cmd ):
		"""Add a patten which if said will get a player ban."""
		pattern = cmd.strip( '" ' ).lower()
		try:
			self.__banPatterns[pattern] = [ re.compile( pattern ), len( self.__banPatterns )  ]
			self.mm.addParam( 'banPatterns', pattern )

			ctx.write( "Ban pattern '%s' added\n" % pattern )

		except:
			msg = "Invalid ban pattern '%s' added\n" % pattern
			ctx.write( msg )
			self.mm.error( msg )

		return 1

	def cmdRemoveBanPattern( self, ctx, cmd ):
		"""Remove a pattern for the ban list."""
		pattern = cmd.strip( '" ' ).lower()
		if not self.__banPatterns.has_key( pattern ):
			msg = "Invalid ban pattern '%s' (not found)" % pattern
			self.mm.info( msg )
			ctx.write( msg )
			return 0

		( re, idx ) = self.__banPatterns[pattern]
		self.mm.removeParam( 'banPatterns', idx )
		del self.__banPatterns[pattern]
		ctx.write( "Ban pattern '%s' removed\n" % pattern )

		return 1

	def cmdClearBanPatterns( self, ctx, cmd ):
		"""Removes all ban patterns."""
		self.__banPatterns = {}

		self.mm.setParam( 'banPatterns', [] )

		ctx.write( "All ban patterns removed\n" )

		return 1

	#
	# Kick word methods
	#

	def cmdAddKickWord( self, ctx, cmd ):
		"""Add a word which if said will get a player warn / kicked / ban."""
		word = cmd.strip( '" ' ).lower()
		self.__kickWords[word] = len( self.__kickWords )
		self.mm.addParam( 'kickWords', word )

		ctx.write( "Kick word '%s' added\n" % word )

		return 1

	def cmdRemoveKickWord( self, ctx, cmd ):
		"""Remove a word for the kick list."""
		word = cmd.strip( '" ' ).lower()
		if not self.__kickWords.has_key( word ):
			msg = "Invalid kick word '%s' (not found)" % word
			self.mm.info( msg )
			ctx.write( msg )
			return 0

		self.mm.removeParam( 'kickWords', self.__kickWords[word] )
		del self.__kickWords[word]
		ctx.write( "Kick word '%s' removed\n" % word )

		return 1

	def cmdClearKickWords( self, ctx, cmd ):
		"""Removes all kick words."""
		self.__kickWords = {}

		self.mm.setParam( 'kickWords', [] )

		ctx.write( "All kick words removed\n" )

		return 1

	#
	# Kick pattern methods
	#

	def cmdAddKickPattern( self, ctx, cmd ):
		"""Add a patten which if said will get a player warn / kicked / ban."""
		pattern = cmd.strip( '" ' ).lower()

		try:
			self.__kickPatterns[pattern] = [ re.compile( pattern ), len( self.__kickPatterns ) ]
			self.mm.addParam( 'kickPatterns', pattern )

			ctx.write( "Kick pattern '%s' added\n" % pattern )

		except:
			msg = "Invalid kick pattern '%s' added\n" % pattern
			ctx.write( msg )
			self.mm.error( msg )

		return 1

	def cmdRemoveKickPattern( self, ctx, cmd ):
		"""Remove a pattern for the kick pattern list."""
		word = cmd.strip( '" ' ).lower()
		if not self.__kickPatterns.has_key( word ):
			msg = "Invalid kick pattern '%s' (not found)" % word
			self.mm.info( msg )
			ctx.write( msg )
			return 0

		( re, idx ) = self.__kickPatterns[word]
		self.mm.removeParam( 'kickPatterns', idx )
		del self.__kickPatterns[word]
		ctx.write( "Kick pattern '%s' removed\n" % word )

		return 1

	def cmdClearKickPatterns( self, ctx, cmd ):
		"""Removes all kick patterns."""
		self.__kickPatterns = {}

		self.mm.setParam( 'kickPatterns', [] )

		ctx.write( "All kick patterns removed\n" )

		return 1


	def __kickPlayer( self, player, reason ):
		"""Kick the player for the given reason."""
		return self.mm.banManager().kickPlayer( player, reason, self.__config['kickDelay'], self.__config['kickType'] )

	def checkPlayers( self, params=None ):
		"""Check players for ping violations and update advanced player info"""
		try:
			self.mm.debug( 2, "K-Check" )
			if not self.mm.gamePlaying:
				# not playing atm ignore
				#self.mm.debug( 2, "K-NP" )
				return

			# We are playing
			ping_limit = self.__config['pingLimit']
			idle_limit = self.__config['idleLimit']		
			max_ping = self.__config['maxPing']
			min_ping = self.__config['minPing']
			neg_score = self.__config['negScoreKick']
			now = host.timer_getWallTime()
			expire = now - self.__config['samplePeriod']
			pos_delay = now - self.__config['positionDelay']
			team1_cp = 0
			team2_cp = 0

			# ignore idle checks or not?
			if not self.mm.roundStarted and self.__config['idleIgnoreNotStarted']:
				ignoreIdle = True
			else:
				ignoreIdle = False

			#self.mm.debug( 2, "K-II: %s" % ignoreIdle )

			# find out how many control points each team has
			for cp in bf2.objectManager.getObjectsOfType( 'dice.hfe.world.ObjectTemplate.ControlPoint' ):
				if 1 == cp.cp_getParam( "team" ):
					team1_cp += 1
				else:
					team2_cp += 1

			for player in bf2.playerManager.getPlayers():
				try:
					if not player.isConnected():
						# Players still connecting ignore
						continue

					kicker_info = self.playerKickerInfo( player )

					# Expire old info
					kicker_info.highPing = filter( lambda time: time > expire, kicker_info.highPing )
					kicker_info.lowPing = filter( lambda time: time > expire, kicker_info.lowPing )
					kicker_info.posHistory = filter( lambda details: details['time'] > expire, kicker_info.posHistory )

					# check ping
					ping = player.getPing()
					if max_ping and ping > max_ping:
						#self.mm.debug( 4, "K-HI: player %s %d > %d" % ( player.getName(), ping, max_ping ) )
						kicker_info.highPing.append( now )
						# Now check limits
						if ping_limit <= len( kicker_info.highPing ):
							self.mm.debug( 4, "K-2HI: player %s" % player.getName() )
							return self.__kickPlayer( player, KickReason.highPing )

					elif ping < min_ping:
						#self.mm.debug( 4, "K-LOW: player %s %d < %d" % ( player.getName(), ping, min_ping ) )
						kicker_info.lowPing.append( now )
						# Now check limits
						if ping_limit <= len( kicker_info.lowPing ):
							self.mm.debug( 4, "K-2LOW: player %s" % player.getName() )
							return self.__kickPlayer( player, KickReason.lowPing )

					# Check score
					cscore = player.score.score
					if neg_score and neg_score >= cscore:
						#self.mm.debug( 4, "K-NEG: player %s" % player.getName() )
						return self.__kickPlayer( player, KickReason.negScore )

					# check idle
					total_bullets_fired = 0
					veh = player.getVehicle()
					( cx, cy, cz ) = veh.getPosition()
					( ca, cp, cr ) = veh.getRotation()
					if ignoreIdle:
						# Game is not really playing and idleIgnoreNotStarted is set
						kicker_info.idleTime = 0

					elif kicker_info.lastScore == cscore:
						# score is still the same
						#self.mm.debug( 4, "K-NS: player %s %d == %d" % ( player.getName(), kicker_info.lastScore, cscore ) )
						playerCanMove = True
						if not player.isAlive():
							# Player is dead can the spawn?
							if 1 == player.getTeam():
								if 0 == team1_cp:
									playerCanMove = False
							else:
								if 0 == team2_cp:
									playerCanMove = False

						if playerCanMove:
							# they can move, check player position
							( lx, ly, lz, la, lp, lr ) = kicker_info.lastPos
							#self.mm.debug( 4, "K-CM: player %s [%f,%f,%f->%f,%f,%f] => [%f,%f,%f->%f,%f,%f]" % ( player.getName(), lx, ly, lz, la, lp, lr, cx, cy, cz, ca, cp, cr ) )

							if cx == lx and cy == ly and cz == lz and ca == la and cp == lp and cr == lr:
								# player hasnt moved
								# finally check to see if they have fired
								bulletsFired = player.score.bulletsFired
								for f in bulletsFired:
									total_bullets_fired += f[1]

								if kicker_info.lastBulletsFired == total_bullets_fired:
									#self.mm.debug( 4, "K-IDLE: player %s (%d == %d)" % ( player.getName(), kicker_info.lastBulletsFired, total_bullets_fired ) )
									kicker_info.idleTime += ( now - kicker_info.lastCheck )
									# Now check limits
									if idle_limit and idle_limit <= kicker_info.idleTime:
										#self.mm.debug( 4, "K-2IDLE: player %s" % player.getName() )
										return self.__kickPlayer( player, KickReason.idle )
								else:
									# player fired
									kicker_info.idleTime = 0
							else:
								# player moved
								kicker_info.idleTime = 0
						else:
							# player cant move
							kicker_info.idleTime = 0
					else:
						# player scored
						kicker_info.idleTime = 0

					# update our last details
					kicker_info.lastCheck = now
					kicker_info.lastScore = cscore
					kicker_info.lastPos = ( cx, cy, cz, ca, cp, cr )
					kicker_info.lastBulletsFired = total_bullets_fired
					kicker_info.posHistory.append( { 'time': now, 'pos': ( cx, cy, cz ), 'rot': ( ca, cp, cr ) } )
				except:
					try:
						player_name = player.getName()
					except:
						player_name = 'unknown'
					self.mm.error( "Failed to check player '%s'" % player_name, True )
		except:
			self.mm.error( "Ooops", True )

	def onPlayerConnect( self, player ):
		"""Init the player for monitoring."""
		if 1 != self.__state:
			return 0

		self.mm.debug( 2, "K: connect %s" % player.getName() )
		player.mmKickerInfo = KickerInfo()

	def playerKickerInfo( self, player ):
		"""Return the passed player kicker info initialising if needed."""
		if not player.__dict__.has_key( 'mmKickerInfo' ):
			player.mmKickerInfo = KickerInfo()

		return player.mmKickerInfo

	def onChatMessage( self, playerid, text, channel, flags ):
		"""Check for ban / kick words."""
		if 1 != self.__state:
			return 0

		try:
			if playerid >= 0:
				player = bf2.playerManager.getPlayerByIndex( playerid )
				if player:
					# Chat spam checks are done regardless of enableChatChecks flag
					kicker_info = self.playerKickerInfo( player )
					now = host.timer_getWallTime()
					kicker_info.chatSpamCheck.append( now )
					expire = now - self.__config['chatSpamPeriod']
					kicker_info.chatSpamCheck = filter( lambda time: time > expire, kicker_info.chatSpamCheck )
					if self.__config['chatSpamLimit'] <= len( kicker_info.chatSpamCheck ):
						# Player is chat spamming
						return self.mm.banManager().banPlayer( player, self.__config['chatSpamBanReason'], self.__config['chatSpamBanPeriod'], self.__config['kickType'], self.__config['banType'], 'ModManager Kicker', self.__config['kickDelay'] )

					if self.__config['enableChatChecks']:
						self.mm.debug( 5, "K-CC: %s" % player.getName() )
						# we have a real player i.e. not an admin
						isban = self.__banWords.has_key
						iskick = self.__kickWords.has_key
						words = mm_utils.MsgChannels.named[channel].stripPrefix( text ).lower().split()
						# first use a hash lookup for speed
						for word in words:
							if isban( word ):
								# Player used a ban word tell them and then ban them
								return self.__wordWarnBanPlayer( player, word )

							elif iskick( word ):
								# Player used a kick word warn them if required
								# if warn limit has been reached kick them
								return self.__wordWarnKickPlayer( player, word )

						# no literal words used, check patterns
						for ban in self.__banPatterns:
							( regexp, idx ) = self.__banPatterns[ban]
							for word in words:
								if regexp.match( word ):
									# Player used a ban word tell them and then ban them
									# N.B. Add to the hash search to speed up future matches
									self.__banWords[word] = len( self.__banWords )
									return self.__wordWarnBanPlayer( player, word )

						for kick in self.__kickPatterns:
							( regexp, idx ) = self.__kickPatterns[kick]
							for word in words:
								if regexp.match( word ):
									# Player used a ban word tell them and then ban them
									# N.B. Add to the hash search to speed up future matches
									self.__kickWords[word] = len( self.__kickWords )
									return self.__wordWarnKickPlayer( player, word )
		except:
			self.mm.error( "Ooops", True )

	def __wordWarnBanPlayer( self, player, word ):
		"""Warn a player for using a kick word and kick / ban if needed."""
		kicker_info = self.playerKickerInfo( player )
		kicker_info.banWordWarnings += 1
		if kicker_info.banWordWarnings > self.__config['banLimit']:
			return self.mm.banManager().banPlayer( player, self.__config['banWordReason'], self.__config['banPeriod'], self.__config['kickType'], self.__config['banType'], 'ModManager Kicker', self.__config['kickDelay'] )
		else:
			return mm_utils.msg_player( player.index, self.__config['warnWordMessage'] % player.getName() )

	def __wordWarnKickPlayer( self, player, word ):
		"""Warn a player for using a kick word and kick / ban if needed."""
		kicker_info = self.playerKickerInfo( player )
		kicker_info.kickWordWarnings += 1
		if kicker_info.kickWordWarnings > self.__config['kickLimit']:
			return self.mm.banManager().kickPlayer( player, self.__config['kickWordReason'] )
		else:
			return mm_utils.msg_player( player.index, self.__config['warnWordMessage'] % player.getName() )

	def onGameStatusChanged( self, status ):
		"""When we start a new round / map reset our counters."""

		# Note: This is valid as the handlers appear to be executed in
		# registration order so modmanger always has the new state
		# when we are called.
		if status == bf2.GameStatus.Playing and self.mm.roundStarted:
			# Moved to real play
			for player in bf2.playerManager.getPlayers():
				self.playerKickerInfo( player ).roundReset()

	def init( self ):
		"""Provides default initialisation."""

		# Load the configuration
		self.__config = self.mm.getModuleConfig( configDefaults )
		self.__playing = 0
		self.__banWords = {}
		self.__banPatterns = {}
		self.__kickPatterns = {}
		self.__kickWords = {}

		# Register our base handlers
		if 0 == self.__state:
			self.mm.debug( 2, "Setting Connect and Chat handlers" )
			host.registerHandler( 'PlayerConnect', self.onPlayerConnect, 1 )
			host.registerHandler( 'ChatMessage', self.onChatMessage, 1 )
			self.mm.debug( 2, "Handlers set" )
		else:
			self.mm.debug( 2, "Handlers NOT set" )

		host.registerGameStatusHandler( self.onGameStatusChanged )

		# Register our rcon command handlers
		self.mm.registerRconCmdHandler( 'kicker', { 'method': self.cmdExec, 'subcmds': self.__cmds, 'level': 1 } )

		# Apply ranked server restrictions
		if host.ss_getParam('ranked'):
			if 0 != self.__config['minPing']:
				self.__config['minPing'] = 0
				self.mm.warn( "Min ping is restricted on ranked servers setting to %d" % self.__config['minPing'] )

			if self.__config['maxPing'] and self.__config['maxPing'] < 160:
				self.__config['maxPing'] = 160
				self.mm.warn( "Max ping is restricted on ranked servers setting to %d" % self.__config['maxPing'] )

		# set up our times
		self.__checkTimer = bf2.Timer( self.checkPlayers, self.__config['initDelay'], 1 )
		self.__checkTimer.setRecurring( self.__config['sampleRate'] )

		# ban words
		idx = 0
		for word in self.__config['banWords']:
			self.__banWords[word] = idx
			idx += 1

		# ban patterns
		idx = 0
		for pattern in self.__config['banPatterns']:
			try:
				self.__banPatterns[pattern] = [ re.compile( pattern ), idx ]
				idx += 1
			except:
				self.mm.error( "Invalid bad pattern '%s'" % pattern )

		# kick words
		idx = 0
		for word in self.__config['kickWords']:
			self.__kickWords[word] = idx
			idx += 1

		# kick patterns
		idx = 0
		for pattern in self.__config['kickPatterns']:
			try:
				self.__kickPatterns[pattern] = [ re.compile( pattern ), idx ]
				idx += 1
			except:
				self.mm.error( "Invalid kick pattern '%s'" % pattern )

		# add already connected players
		for player in bf2.playerManager.getPlayers():
			player.mmKickerInfo = KickerInfo()

		self.__state = 1

	def shutdown( self ):
		"""Shutdown and stop processing."""

		# destroy our timers
		self.__checkTimer.destroy()
		self.__checkTimer = None

		# Clear players
		for player in bf2.playerManager.getPlayers():
			del player.mmKickerInfo

		# Unregister our handlers
		host.unregisterGameStatusHandler( self.onGameStatusChanged )
		self.mm.unregisterRconCmdHandler( 'kicker' )

		# Unregister our game handlers
		# Flag as shutdown as there is currently way to do this
		self.__state = 2

def mm_load( modManager ):
	"""Creates your object."""
	return Kicker( modManager )
