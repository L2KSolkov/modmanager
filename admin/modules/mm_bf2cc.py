# -*- coding: latin-1 -*-
# vim: ts=4 sw=4 noexpandtab
"""Battlefield 2 -- bf2cc for ModManager.

This is a BF2CC module for ModManager.

===== Config =====
 # The number of lines of chat to buffer
 mm_bf2cc.chatBufferSize 50

 # The format for server chat messages ( must include the two %s's which are expanded to: <admin name> and <msg> respectively )
 mm_bf2cc.serverChatFormat "[Admin: %s] %s"

See www.bf2cc.com for more details

ModManager conversion and additional development by:
Steven 'Killing' Hartland

===== History =====
 v7.2 - 23/06/2011:
 Updated BFP4F Support to add ReservedSlot info
  
 v7.1 - 12/10/2011:
 Added BFP4F Support

 v7.0 - 12/01/2020:
 Removed call for host.rcon_invoke( 'sv.numreservedslots' ) from Heroes as thats been removed
 
 v6.9 - 28/11/2009:
 Prevent teamswitching, fling and killplayer on heroes servers
 
 v6.8 - 03/06/2009:
 Fixed broken player list

 v6.7 - 07/05/2009:
 Added Heroes compatibility:-
 Each player in pl for heroes adds:
 	Int32 Is VIP player (0 - no, otherwise yes)
 	Int64 Nucleus id
 si in heroes adds:
 	Int32 Rounds per map
 	Int32 Round number

 v6.6 - 31/05/2007:
 Now uses mm_utils.get_cd_key_hash( player ) to obtain cdkeyhash's this avoids an issue in BF2142 at least where some player names break admin.listPlayers
 Added a workaround for broken BF2cc version check

 v6.5 - 03/11/2006:
 switchplayer and sendplayerchat now support player names as well as playerid's
 Added some additional comments
 Added missing \n in output
 
 v6.4 - 19/10/2006:
 Fixed onPlayerDeath not dealing with None victim
 
 v6.3 - 29/09/2006:
 Added encoding type to prevent warning when loading
 
 v6.2 - 30/08/2006:
 Added supported games
 Updated cmdSendPlayerChat to use largs
 
 v6.1 - 30/05/2006:
 Fixed player details for bots

 v6.0 - 20/04/2006:
 Version increment

 v5.2 - 22/03/2006:
 Extra validation done in cmdGetPlayerHash
 
 v5.1 - 08/03/2006:
 Added punished info to the player info
 
 v5.0 - 28/02/2006:
 Now requires mm_tk_punish for so we can display punish information
 Added team kill forgive / punish information to cmdGetPlayerList

 v4.9 - 21/02/2006:
 Added serverChatFormat config option which now doesnt use large fonts by default. Prefix with ' §3 ' for large messages.

 v4.8 - 07/02/2006:
 sendserverchat now uses large text
 
 v4.7 - 22/11/2005:
 Fix for maplist causing the server to crash
 Fix for player hash pattern match and LAN servers
 Fixed formatting issues
 Now only compatible with 4.6 or later
 
 v4.6 - 17/11/2005:
 Added methods to report player hashes
 Removed reporting of ticketChangePerSecond to prevent overflow errors
 
 v4.5 - 05/10/2005:
 Fix for getRootParent being removed from constants.py in BF2 1.03, this fixes vehicle reporting
 Added a compatibility version which will enable older BF2CC clients and daemons to connect if no protocol changes have occured
 
 v4.4 - 04/09/2005:
 Now requires version 1.9 of the mm_kicker
 
 v4.3 - 20/08/2005:
 Removed \n from server name in si response
 Updated to use mm methods for round times 
 
 v4.2 - 11/08/2005:
 Now uses mm_utils.get_int instead of local self.__getInt
 
 v4.1 - 02/08/2005:
 Player switch now uses auto as its default mode which will use NextDeath if 
 the player is alive NowNoMove otherwise
 
 v4.0 - 02/08/2005:
 Player position information is now delayed to prevent cheating
 
 v3.9 - 29/07/2005:
 Disabled player switch modes other than NextDeath
 Updated modmanager API calls
 Optimised snapshot
 
 v3.8 - 27/07/2005:
 More fields added to player listing and server snapshot for daemon processing.
 
 v3.7 - 21/07/2005:
 Added more info to snapshots
 
 v3.6 - 14/07/2005:
 Added monitoring
 Switch player now has multiple modes, new default is switch on death
 
 Original code by:
 The bf2cc team ( www.bf2cc.com )
"""

import host
import bf2
import mm_utils
import sys
import time
import re
from bf2.stats.constants import *

__version__ = 7.2
__compat_version__ = 6.1

__required_modules__ = {
	'modmanager': 2.0,
	'mm_kicker': 1.9,
	'mm_tk_punish': 1.7
}

__supports_reload__ = True

__supported_games__ = {
	'bf2': True,
	'bf2142': True,
	'bfheroes': True,
	'bfp4f': True
}

__description__ = "BF2CC v%s for ModManager" % __version__

__all__ = [
]

configDefaults = {
	'chatBufferSize': 50, # How many lines of buffer to use
	'serverChatFormat': "[Admin: %s] %s"
}

class SwitchMode:
	Auto = 0
	NextDeath = 1
	NowAndMove = 2
	NowNoMove = 3

class RingBuffer(list):
	"""Ring buffer implementation.

	Note: couldnt use dequeue because it's not supported in the bf2 engine.
	"""
	def __init__( self, capacity ):
		list.__init__( self )
		assert capacity > 0
		self.capacity = capacity

	def append(self, x):
		if self.__len__() >= self.capacity:
			self.pop( 0 )

		list.append( self, x )

class BF2CC:
	"""BF2CC module manager class.

	Extends ModuleManagers basic Rcon to support bf2cc
	See: http://www.bf2cc.com for details
	"""

	def __init__( self, modManager ):
		"""Extend the basic rcon to support BF2CC.

		Here we provide bf2cc extensions to rcon.
		All commands are prefixed 'bf2cc'
		"""

		# modManger details
		self.mm = modManager
		self.__state = 0

		# Our internal commands
		self.__cmds = {
			# Local commands
			'pause': { 'method': self.cmdPause, 'level': 10 },
			'unpause': { 'method': self.cmdUnpause, 'level': 10 },
			'togglepause': { 'method': self.cmdUnpause, 'level': 10 },
			'check': { 'method': self.cmdCheck, 'level': 10 },

			# Queries
			'si': { 'method': self.cmdGetSnapshot, 'desc': 'Prints server information', 'level': 20 },
			'pl': { 'method': self.cmdGetPlayerList, 'desc': 'Prints player information', 'level': 20 },
			'serverchatbuffer': { 'method': self.cmdGetServerChatBuffer, 'level': 20 },
			'clientchatbuffer': { 'method': self.cmdGetClientChatBuffer, 'level': 20 },
			'getplayerhash': { 'method': self.cmdGetPlayerHash, 'level': 20 },

			# Admin commands
			'setadminname': { 'method': self.cmdSetAdminName, 'args': '<admin_name>', 'level': 1 },
			'getadminlist': { 'method': self.cmdGetAdminList, 'level': 5 },
			'sendadminchat': { 'method': self.cmdSendAdminChat, 'args': '<admin_name> <message>', 'level': 20 },
			'sendplayerchat': { 'method': self.cmdSendPlayerChat, 'args': '<playerid> <message>', 'level': 20 },
			'sendserverchat': { 'method': self.cmdSendServerChat, 'args': '<message>', 'level': 20 },
			'monitor': { 'method': self.cmdMonitor, 'args': '[0|1]', 'level': 10 }
		}

		if not modManager.isBattleFieldHeroes() and not modManager.isBattleFieldPlay4Free():
			self.__cmds['killplayer'] = { 'method': self.cmdKillPlayer, 'args': '<playerid>', 'restricted': 1, 'level': 30 }
			self.__cmds['switchplayer'] = { 'method': self.cmdSwitchPlayer, 'args': '<playerid> [1|2|3]', 'level': 20 }
			self.__cmds['fling'] = { 'method': self.cmdFling, 'args': '<playerid> <height>', 'restricted': 1, 'level': 30 }


	# Not used ATM
	def clientConnect( self, ctx ):
		"""Process the client connect."""
		self.mm.debug( 2, "BF2CC.clientConnect '%s'" % ctx.getName() )

	def clientAuthed( self, ctx ):
		"""Change this clients as authed / registered status."""
		key = ctx.key()
		if ctx.authedLevel:
			ctx.bf2ccClient = Client( self.mm, self )
			self.__authedClients[key] = ctx
		elif self.__authedClients.has_key( key ):
			del self.__authedClients[key]

	def clientDisconnect( self, ctx ):
		"""Remove this client from our list."""
		key = ctx.key()
		#self.mm.debug( 2, "BF2CC.clientDisconnect '%s'" % ctx.getName() )
		if self.__authedClients.has_key( key ):
			del self.__authedClients[key]

	def cmdExec( self, ctx, cmd ):
		"""Execute a bf2cc sub command."""
		key = ctx.key()
		#self.mm.debug( 2, "BF2CC.cmdExec '%s' by %s" % ( cmd, ctx.getName() ) )
		if not self.__authedClients.has_key( key ):
			self.mm.error( "BF2CC: Exec recieved for unknown client %s" % ctx.getName() )
			return 0

		return mm_utils.exec_subcmd( self.mm, self.__cmds, ctx, cmd )

	def onPlayerKilled( self, victim, attacker, weapon, assists, object ):
		"""Log that a player has been killed."""
		if 1 != self.__state:
			return 0
		#self.mm.debug( 3, 'BF2CC: player killed!' )

	def onPlayerDeath( self, victim, vehicle ):
		"""Log that a player has died."""
		if 1 != self.__state or victim is None:
			return 0

		if not self.mm.gamePlaying:
			# Seems to cause issues with players connections
			return 0
		
		if self.__playersToSwitch.has_key( victim.index ):
			old_teamid = self.__playersToSwitch[victim.index]
			cur_teamid = victim.getTeam()
			if old_teamid == cur_teamid:
				# player hasnt already switched so switch them
				if ( 1 == cur_teamid ):
					victim.setTeam( 2 )
				else:
					victim.setTeam( 1 )
			# All done
			del self.__playersToSwitch[victim.index]

		return 1

	def onChatMessage( self, playerid, text, channel, flags ):
		"""Enqueue the chat message in relavent buffers."""
		if 1 != self.__state:
			return 0

		playerName = 'Admin'
		team = 'None'

		if playerid >= 0:
			p = bf2.playerManager.getPlayerByIndex( playerid )
			if p is not None:
				playerName = p.getName()
				team = p.getTeam()

		msg = '%d\t%s\t%s\t%s\t[%s]\t%s\r' % ( playerid, playerName, team, channel, time.strftime( "%H:%M:%S", time.localtime()), text )
		self.serverChatBuffer.append( msg )
		for key in self.__authedClients:
			self.__authedClients[key].bf2ccClient.clientChatBuffer.append( msg )

	def onGameStatusChanged( self, status ):
		"""Update our internal version of the game status."""

		# enqueue the status change for clients that are in monitoring mode.
		for key in self.__authedClients:
			ctx = self.__authedClients[key]
			if ctx.bf2ccClient.isMonitoring:
				ctx.conn.outbuf.enqueue( str( status ) + '\x04' )

	def cmdPause( self, ctx, cmd ):
		"""Pause the server if its running."""
		if bf2.GameStatus.Playing == self.mm.currentGameStatus:
			ctx.write( self.mm.pause() )

	def cmdUnpause(self, ctx, cmd ):
		"""Unpause the server if its paused."""
		if bf2.GameStatus.Paused == self.mm.currentGameStatus:
			ctx.write( self.mm.unpause() )

	def cmdTogglePause( self, ctx, cmd ):
		"""Pause the server if its running."""
		if bf2.GameStatus.Playing == self.mm.currentGameStatus:
			ctx.write( self.mm.pause() )
		else:
			ctx.write( self.mm.unpause() )

	def cmdCheck( self, ctx, cmd ):
		"""Send some check details to the client."""
		if self.mm.isBattleField2():
			# Due to a bug in BF2cc's version code ( doesnt use the compat_version ) we have to
			# revert the main version to that of the compat version to ensure it works
			ctx.write( '%s\t%s\t%s\n' % ( __compat_version__, self.serverType, __compat_version__ ) )
		else:
			ctx.write( '%s\t%s\t%s\n' % ( __compat_version__, self.serverType, __version__ ) )

	def cmdGetClientChatBuffer( self, ctx, cmd ):
		"""Send the clients buffered chat."""
		if ctx.bf2ccClient.clientChatBuffer:
			ctx.write( '\r'.join( ctx.bf2ccClient.clientChatBuffer ) + '\r\n' )
		else:
			ctx.write( '\n' )

		ctx.bf2ccClient.clientChatBuffer = RingBuffer( self.chatBufferSize ) # clears the chat buffer

	def cmdGetServerChatBuffer( self, ctx, cmd ):
		"""Send the servers buffered chat."""
		if self.serverChatBuffer:
			ctx.write( '\r'.join( self.serverChatBuffer ) + '\r\n' )
		else:
			ctx.write( '\n' )
	
	def cmdGetPlayerHash(self, ctx, cmd):
		parts = cmd.split()
		l = len( parts )
		if 0 == l:
			ctx.write( 'Error: no playerid specified\n' )
			return 0

		try:
			player = bf2.playerManager.getPlayerByIndex( int( parts[0] ) )
			if player is None:
				ctx.write( "Error: Invalid playerid '%s'\n" % parts[0] )
				return 0		
			cdkeyhash = mm_utils.get_cd_key_hash( player )
			if cdkeyhash is None:
				ctx.write( "Error: No cd key hash found for playerid '%s'" % parts[0] )
			else:
				ctx.write( "%s\n" % cdkeyhash )
		except:
			ctx.write( "Error: Invalid playerid '%s'\n" % parts[0] )
			return 0		
	
	def cmdGetPlayerList( self, ctx, cmd ):
		r"""Return a string representation of the current state of the players on the server.

		Each player is seperated by \r ( <cr> )
		Each player field is seperated by \t ( <tab> )
		"""
		
		parts = []
		bHasVips = self.mm.isBattleFieldHeroes() or self.mm.isBattleFieldPlay4Free()
		for p in bf2.playerManager.getPlayers():
			pparts = []

			try:
				# Basic info
				pparts.append( p.index )						#0
				pparts.append( p.getName() )
				pparts.append( p.getTeam() )					#2
				pparts.append( p.getPing() )
				pparts.append( p.isConnected() )				#4
				pparts.append( p.isValid() )
				pparts.append( p.isRemote() )					#6
				pparts.append( p.isAIPlayer() )
				pparts.append( p.isAlive() )					#8
				pparts.append( p.isManDown() )
				pparts.append( p.getProfileId() )				#10
				pparts.append( p.isFlagHolder() )
				pparts.append( p.getSuicide() )					#12
				pparts.append( p.getTimeToSpawn() )
				pparts.append( p.getSquadId() )					#14
				pparts.append( p.isSquadLeader() )
				pparts.append( p.isCommander() )				#16
				pparts.append( p.getSpawnGroup() )
				pparts.append( p.getAddress() )					#18

				# Score info
				score = p.score
				pparts.append( score.damageAssists )
				pparts.append( score.passengerAssists )			#20
				pparts.append( score.targetAssists )
				# I think these are renamed to RoadKills or Runovers
				## #self.driverSpecials = player.score.driverSpecials
				pparts.append( score.revives )					#22
				pparts.append( score.teamDamages )
				pparts.append( score.teamVehicleDamages )		#24
				pparts.append( score.cpCaptures )
				pparts.append( score.cpDefends )				#26
				pparts.append( score.cpAssists )
				pparts.append( score.cpNeutralizes )			#28
				pparts.append( score.cpNeutralizeAssists )
				pparts.append( score.suicides )					#30
				pparts.append( score.kills )
				pparts.append( score.TKs )						#32


				# Get the Vehicle
				try:
					# The pointer we saw was to the Struct of the vehicle
					vehicle = p.getVehicle()
					if vehicle:
						# Need the Constants.py for this function and Vehicle Types/Enums
						rootVehicle = bf2.objectManager.getRootParent( vehicle )
						VehicleType = getVehicleType( rootVehicle.templateName )
						VehicleName = rootVehicle.templateName
					else:
						VehicleType = '-1'
						VehicleName = 'unknown'
				except:
					VehicleType = '-1'
					VehicleName = 'unknown'

				pparts.append( VehicleType )
				# Get the Kit
				try:
					if p.isAlive():
						kit = p.getKit()
						pparts.append( kit.templateName )		#34 = Kit if player is Dead then return "none"
					else:
						pparts.append( 'none' )
				except:
					pparts.append( 'none' )

				# Get Player connect time
				if p.__dict__.has_key( 'mmKickerInfo' ):
					ki = p.mmKickerInfo
					pparts.append( ki.connectedAt )				#35
				else:
					pparts.append( host.timer_getWallTime() )	#35

				# Forgot to Add Deaths and Score...
				pparts.append( p.score.deaths )					#36
				pparts.append( p.score.score )
				pparts.append( VehicleName )					#38
				pparts.append( p.score.rank )

				# Position
				try:
					( x, y, z ) = ki.safePos()
					pparts.append( '%f,%f,%f' % ( x, y, z ) )	#40
				except:
					pparts.append( '0.0,0.0,0.0' )

				# Additional info
				pparts.append( "%d" % ki.idleTime )				#41
				
				if p.isAIPlayer():
					pparts.append( 'Bot - No Hash' )			#42
				else:
					cdkeyhash = mm_utils.get_cd_key_hash( p )
					if cdkeyhash is None:
						pparts.append( 'LAN - No Hash' )		#42	
					else:
						pparts.append( cdkeyhash )				#42

				# Team kill info
				if p.__dict__.has_key( 'tkData' ):
					pparts.append( p.tkData.punished )			#43
					pparts.append( p.tkData.timesPunished )		#44
					pparts.append( p.tkData.timesForgiven )		#45
				else:
					# Still connecting
					pparts.append( 0 )							#43
					pparts.append( 0 )							#44
					pparts.append( 0 )							#45

				if bHasVips:
					pparts.append( p.getVip() )					#46
					pparts.append( p.getNucleusId() )			#47

				parts.append( '\t'.join( map( str, pparts ) ) )

			except:
				self.mm.error( "Player info error", True )

		# ensure we have a terminating \r
		parts.append( '' )
		ctx.write( '\r'.join( parts ) )

	def cmdGetSnapshot( self, ctx, cmd ):
		r"""Return a string representation of the current state of the server.

		The string includes the following information:
		1. Current map
		2. Next map
		3. Player numbers ( connected, joining, max )
		4. Server name
		5. Team details
		6. Time details
		7. Game mode
		8. Game mod
		9. World size
		10. Time limit

		Each field is seperated by a \t ( <tab )
		"""

		allMaps = str( host.rcon_invoke( 'mapList.list' ) ).split('\n')
		mapcount = len( allMaps )
		if mapcount > 2:
			nextMapIndex = host.rcon_invoke( 'admin.nextLevel' )
			nextMapName = allMaps[int(nextMapIndex)].split('"')[1]
		else:
			nextMapName = ''

		parts = []
		# Version
		parts.append( __version__ )												#0

		# TODO: server status
		parts.append( self.mm.currentGameStatus )

		# Max players
		parts.append( host.ss_getParam( 'maxPlayers' ) )						#2

		connectedPlayers = 0
		joiningPlayers = 0
		team1 = 0
		team2 = 0
		for p in bf2.playerManager.getPlayers():
			try:
				if p.isConnected() == 0:
					joiningPlayers += 1
				else:
					connectedPlayers += 1
			except:
				joiningPlayers += 1

			if p.getTeam() == 1:
				team1 += 1
			else:
				team2 += 1

		# Connected players
		parts.append( connectedPlayers )

		# Joining players
		parts.append( joiningPlayers )											#4

		# Current map name
		parts.append( host.sgl_getMapName() )

		# Next map
		parts.append( nextMapName )												#6

		# Server name
		parts.append( host.rcon_invoke( 'sv.serverName' ).strip() )

		# Team 1 details
		parts.append( host.sgl_getParam( 'teamName', 1, 0 ) )					#8
		parts.append( host.sgl_getParam( 'ticketState', 1, 0 ) )
		parts.append( host.sgl_getParam( 'startTickets', 1, 0 ) )				#10
		parts.append( host.sgl_getParam( 'tickets', 1, 1 ) )
		parts.append( '0' )														#12

		# Team 2 details
		parts.append( host.sgl_getParam( 'teamName', 2, 0 ) )
		parts.append( host.sgl_getParam( 'ticketState', 2, 0 ) )				#14
		parts.append( host.sgl_getParam( 'startTickets', 2, 0 ) )
		parts.append( host.sgl_getParam( 'tickets', 2, 1 ) )					#16
		parts.append( '0' )

		timeLimit = host.ss_getParam('timeLimit')
		if timeLimit:
			timeLeft = self.mm.roundTimeLeft()
		else:
			timeLeft = -1

		# Elapsed Time in seconds
		parts.append( self.mm.roundTime() )										#18

		# Remaining time in seconds
		parts.append( timeLeft )

		# Gamemode
		parts.append( host.ss_getParam( 'gameMode' ) )							#20

		# Mod running
		modDirs = str( host.sgl_getModDirectory() ).replace( '\\', '/' ).split( '/' )
		modDir = modDirs[modDirs.__len__() - 1]
		parts.append( modDir )

		# World size - 22
		parts.append( host.sgl_getWorldSize() )

		# TimeLimit - 23
		parts.append( timeLimit )

		# Autobalance Team - 24
		parts.append( bf2.serverSettings.getAutoBalanceTeam() )

		# Ranked status - 25
		parts.append( str( host.ss_getParam( 'ranked' ) ) )

		# Team 1 count - 26
		parts.append( str( team1 ) )

		# Team 2 count - 27
		parts.append( str( team2 ) )

		# query at... For compare to player connected - 28
		parts.append( str( host.timer_getWallTime() ) ) 
		
		if self.mm.isBattleFieldHeroes() or self.mm.isBattleFieldPlay4Free():
			# query ReservedSlot Count - 29
			parts.append( 0 )

			# Rounds per map
			parts.append( bf2.serverSettings.getRoundsPerMap() )				#30

			# Current round number
			parts.append( bf2.gameLogic.getRoundNr() )							#31
		else:
			# query ReservedSlot Count - 29
			parts.append( host.rcon_invoke( 'sv.numreservedslots' ) )
		
		ctx.write( "%s\n" % '\t'.join( map( str, parts ) ) )

	def cmdFling( self, ctx, cmd ):
		"""fling a player high.

		cmd = playerid height
		"""

		parts = cmd.split()
		l = len( parts )
		if 0 == l:
			ctx.write( 'Error: no playerid specified\n' )
			return 0
		elif 1 == l:
			ctx.write( 'Error: no height specified\n' )
			return 0

		playerid = mm_utils.get_int( ctx, parts[0], 'playerid' )
		if playerid is None:
			return 0

		height = mm_utils.get_int( ctx, parts[1], 'height' )
		if height is None:
			return 0

		player = bf2.playerManager.getPlayerByIndex( playerid )

		if not player or not player.isAlive() or player.isManDown():
			ctx.write('Error: Player is currently dead or down')
			return 0

		try:
			veh = player.getVehicle()
			pos = veh.getPosition()
			veh.setPosition(tuple([float(pos[0]), float( pos[1] + height ), float(pos[2])]))
		except Exception, e:
			self.mm.error( 'Failed to fling player', True )
			ctx.write('Error: Error flinging player.')

	def cmdMonitor( self, ctx, cmd ):
		"""Register interests in all game state changes.

		0 = Turn off monitoring
		1 = Turn on monitoring
		"""
		if '' == cmd or '1' == cmd:
			self.mm.debug( 2, "Client '%s' monitoring enabled" % ctx.getName() )
			ctx.bf2ccClient.isMonitoring = True
		else:
			self.mm.debug( 2, "Client '%s' monitoring disabled" % ctx.getName() )
			ctx.bf2ccClient.isMonitoring = False

	def cmdSwitchPlayer( self, ctx, cmd ):
		"""Switch a player from one side to another.
		The switch mode flag options are:
		0 = Auto ( uses NextDeath if player is alive NowNoMove otherwise )
		1 = NextDeath
		2 = NowAndMove
		3 = NowNoMove
		"""

		parts = cmd.split()
		l = len( parts )

		if 0 == l:
			ctx.write( 'Error: no playerid specified\n' )
			return 0

		elif 1 == l:
			# Safe default
			switch_mode = SwitchMode.Auto

		else:
			switch_mode = mm_utils.get_int( ctx, parts[1], 'switch_mode' )
			if switch_mode is None:
				ctx.write( "Error: Invalid switch mode '%s'\n" % parts[1] )
				return 0

		player = mm_utils.find_player( parts[0] )

		if player is None:
			ctx.write( 'Error: Player %s not found.\n' % parts[0] )
			self.mm.warn( 'Switch player failed (player %s not found)' % parts[0] )
			return 0

		curTeam = player.getTeam()

		if curTeam == 1:
			new_team = 2
		else:
			new_team = 1

		if switch_mode == SwitchMode.Auto:
			if player.isAlive():
				# Auto and player is alive so use next death
				switch_mode = SwitchMode.NextDeath
			else:
				# Auto and player is alive so use next death
				switch_mode = SwitchMode.NowNoMove
		
		if switch_mode == SwitchMode.NextDeath:
			ctx.write( "Player '%s' scheduled to switch next death.\n" % player.getName() )
			self.__playersToSwitch[player.index] = player.getTeam()
			return 1

		if not self.mm.gamePlaying:
			ctx.write( 'Player not switched ( game not playing )\n' )
			return 0

		# avoid autobalance changing us back
		player.setSuicide( 1 )
		# Change their team
		player.setTeam( new_team )

		if player.isAlive() and switch_mode == SwitchMode.NowAndMove:
			# Players didnt die on change so move them to the nearest control point held by their new team
			# if move was indicated by the switch mode
			soldier = player.getVehicle()
			( px, py, pz ) = soldier.getPosition()
			closest_point = None
			controlPoints = bf2.objectManager.getObjectsOfType( 'dice.hfe.world.ObjectTemplate.ControlPoint' )
			for cp in controlPoints:
				if new_team == cp.cp_getParam( "team" ):
					( x, y, z ) = cp.getPosition()
					xdiff = ( x - px )
					zdiff = ( z - pz )
					distance = ( xdiff * xdiff ) + ( zdiff * zdiff )
					if closest_point is None or distance < closest_point.__distance:
						closest_point = cp
						closest_point.__distance = distance

			if closest_point is not None:
				soldier.setPosition( closest_point.getPosition() )


		ctx.write('Player switched\n')

	def cmdKillPlayer( self, ctx, cmd ):
		"""Kill a specific player."""
		# currently not supported.
		#self.mm.warn( 'bf2cc: kill player not currently supported' )
		#ctx.write( 'bf2cc: kill player not currently supported' )
		#return
		return 0

		playerid = mm_utils.get_int( ctx, cmd, 'playerid' )

		if 0 > playerid:
			return 0

		player = bf2.playerManager.getPlayerByIndex( playerid )
		ctx.write(str(player.getDefaultVehicle().getDamage()))
		if not player or not player.isAlive():
			ctx.write('Error: Player not found or not alive.')
			return

		veh = player.getDefaultVehicle()
		veh.setDamage(0)

	def cmdSetAdminName( self, ctx, cmd ):
		"""Set the name of the current admin"""
		if cmd == '':
			ctx.write('Error: no name specified\n')
		else:
			ctx.bf2ccClient.adminName = cmd
			ctx.write('Admin name set to %s\n' % cmd)

	def cmdSendServerChat( self, ctx, cmd ):
		"""Say a message to the players as the admin."""
		msg = self.__config['serverChatFormat'] % ( ctx.bf2ccClient.adminName, cmd )
		host.rcon_invoke( 'game.sayall \"%s\"' % ( msg ) )
		ctx.write('Chat sent to server\n')

	def cmdSendAdminChat( self, ctx, cmd ):
		"""Say a message to another admin."""
		( sendToAdmin, chatText ) = mm_utils.lsplit( cmd, None, 2, '' )

		sendCount = 0
		for key in self.__authedClients:
			client = self.__authedClients[key].bf2ccClient
			if client.adminName == sendToAdmin:
				sendCount += 1
				client.clientChatBuffer.append('%d\t%s\t%s\t%s\t[%s] %s\r' % (-1, ctx.bf2ccClient.adminName, 'Admin', 'Admin', time.strftime("%m-%d %H:%M", time.localtime()), chatText))

		if sendCount > 0:
			ctx.write('Chat sent to admin(s) %s\n' % sendToAdmin)
		else:
			ctx.write('Error: no admin(s) with the name %s\n' % sendToAdmin)

	def cmdGetAdminList( self, ctx, cmd ):
		"""Returns a list of admins (excluding the requesting admin)."""
		ret = ''
		for key in self.__authedClients:
			c = self.__authedClients[key]
			# ATM only list tcp connections
			if ctx != c and c.isSocket():
				ret += "%s:%d\t%s\r" % ( c.conn.addr[0], c.conn.addr[1], c.bf2ccClient.adminName )

		ctx.write("%s\n" % ret)

	def cmdSendPlayerChat( self, ctx, cmd ):
		"""Send a message to a specific player."""
		( playerid, msg ) = mm_utils.largs( cmd, None, 2, '' )

		player = mm_utils.find_player( playerid )

		if player is None:
			ctx.write( 'Error: player %s not found\n' % playerid )
			self.mm.error( "Failed to find player %s" % playerid )
		else:
			chatText = '[%s] %s' % ( ctx.bf2ccClient.adminName, msg )
			mm_utils.msg_player( player.index, chatText )
			ctx.write( 'Chat sent to player %s\n' % playerid )

	def init( self ):
		"""Provides default initialisation."""
		# local state
		self.__config = self.mm.getModuleConfig( configDefaults )
		self.chatBufferSize = self.__config['chatBufferSize']
		self.serverChatBuffer = RingBuffer( self.chatBufferSize )

		# Check the ranked status and set our type accordingly
		if host.ss_getParam('ranked'):
			# Ranked used to limit functionality in the front end
			self.serverType = 'r'
		else:
			self.serverType = 's'

		# Our copy of the authed clients
		# Note: we could optimise this all out
		self.__authedClients = {}

		# Players to swich when they next die
		self.__playersToSwitch = {}

		# Register our base handlers
		host.registerGameStatusHandler( self.onGameStatusChanged )

		if 0 == self.__state:
			host.registerHandler( 'ChatMessage', self.onChatMessage, 1 )
			host.registerHandler( 'PlayerDeath', self.onPlayerDeath )
			# Not currently used
			#host.registerHandler( 'PlayerKilled', self.onPlayerKilled )

		# Register our rcon command handler
		self.mm.registerRconCmdHandler( 'bf2cc', { 'method': self.cmdExec, 'subcmds': self.__cmds, 'level': 1 } )

		# Register our connection handlers
		#self.mm.registerRconConnectHandler( self.clientConnect )
		self.mm.registerRconDisconnectHandler( self.clientDisconnect )

		# Register our authed handler
		self.mm.registerRconAuthedHandler( self.clientAuthed )

		self.__state = 1

	def shutdown( self ):
		"""Shutdown and stop processing."""

		# Unregister our rcon command handlers
		self.mm.unregisterRconCmdHandler( 'bf2cc' )

		# Unregister our connection handlers
		#self.mm.registerRconConnectHandler( self.clientConnect )
		self.mm.unregisterRconDisconnectHandler( self.clientDisconnect )

		# Unregister our authed handler
		self.mm.unregisterRconAuthedHandler( self.clientAuthed )

		# Unregister our game handlers
		host.unregisterGameStatusHandler( self.onGameStatusChanged )

		# Flag as shutdown as there is currently way to do this
		self.__state = 2

class Client(object):
	"""Keeps tack of client state."""
	def __init__( self, modManager, bf2ccServer ):
		self.mm = modManager
		self.bf2ccServer = bf2ccServer

		# list of chats for this client.
		self.clientChatBuffer = RingBuffer( bf2ccServer.chatBufferSize )

		# The default admin name
		self.adminName = 'Admin'

		# Monitoring
		self.isMonitoring = False;


def mm_load( modManager ):
	"""Creates the bf2cc core object which extends rcon."""
	return BF2CC( modManager )
