# vim: ts=4 sw=4 noexpandtab
""" Team autobalance system.

This is a autobalance system ModManager module

===== Config =====

 # Allow Commander if 0 then we never autobalance the commander
 mm_autobalance.allowCommander 0
 
 # Allow Squad Leader if 0 then we only autobalance squad leaders
 # if they are the only member of that squad
 mm_autobalance.allowSquadLeader 0
 
 # Allow Squad Member if 0 then we only autobalance squad members
 # if there are no none squad members / commander on the team
 mm_autobalance.allowSquadMember 0
 
 # Allows plays to be switched teams at the end of a round
 # 0 => No swap
 # 1 => Swap teams
 # 2 => Randomise teams
 mm_autobalance.roundSwitch

===== History =====
 v2.5 - 12/10/2011:
 Fixed being able to load on Heroes

 v2.4 - 12/10/2011:
 Added BFP4F Support

 v2.3 - 14/07/2009:
 Disabled this module for Heroes as its never valid due to the fixed player classes
 
 v2.2 - 07/10/2006:
 Fixed off by one issue on player connect

 v2.1 - 03/10/2006:
 Merged with ClanMatch and enhanced to have multiple on round change methods
 
 v2.0 - 13/09/2006:
 Enhancements / fixes merged from BF2142 Closed BETA 2
 
 v1.9 - 30/08/2006:
 Added supported games
 Included changes from BF2142 Tuning BETA 2

 v1.8 - 13/07/2006
 Added gpm_coop checks from v1.4 patch

 v1.7 - 20/05/2006:
 Added gpm_coop check from v1.3 patch
 
 v1.6 - 08/08/2005:
 Fix for player joining during pre / post game not being balanced
 correctly.

 v1.5 - 03/08/2005:
 Optimised onPlayerConnect team check
 
 v1.4 - 21/07/2005:
 Flagged as reload safe
 
 v1.3 - 13/07/2005:
 Enhanced squad based autobalance descision making to take
 into account team composition.
 
 v1.2 - 09/07/2005:
 Added commander, and squad balance options
 
 v1.1 - 30/06/2005:
 Updated to ModManager format by Steven 'Killing' Hartland
 
 v1.0:
 Created by: DICE
"""

import bf2
import host
import random
import mm_utils

__version__ = 2.5

__required_modules__ = {
	'modmanager': 1.6
}

__supports_reload__ = True

__supported_games__ = {
	'bf2': True,
	'bf2142': True,
	'bfheroes': False,
	'bfp4f': True
}

__description__ = "ModManager Team autobalance v%s" % __version__

configDefaults = {
	'allowCommander': 0,
	'allowSquadLeader': 0,
	'allowSquadMember': 0,
	'roundSwitch': 0,
}

class AutoBalance( object ):

	def __init__( self, modManager ):
		self.mm = modManager
		self.__state = 0

	def onPlayerConnect( self, p ):
		"""Autobalance the new player if required."""
		if 1 != self.__state:
			return

		if self.mm.isBattleField2142() and not p.isValid():
			return

		# dont team switch alive players, or they will have the wrong teams kit
		if p.isAlive():
			return

		# place player on the team with least players
		team1 = 0
		team2 = 0
		for tp in bf2.playerManager.getPlayers():
			if 1 == tp.getTeam():
				team1 += 1
			else:
				team2 += 1

		# Ignore the new player's team entry
		# N.B. Doing it this way avoids a loop level check
		if 1 == p.getTeam():
			team1 -= 1
		else:
			team2 -= 1

		if ( team2 * bf2.serverSettings.getTeamRatioPercent() / 100.0 ) > team1:
			p.setTeam(1)
		else:
			p.setTeam(2)

	def onPlayerDeath( self, p, vehicle ):
		"""Autobalance a player that has died if required and allowed by the balance rules."""
		if 1 != self.__state:
			return

		if p == None:
			return

		if self.mm.isBattleField2142():
			# bf2142 specific
			if not p.isValid() or p.isAutoController():
				return
		else:
			# bf2 specific
			if ( host.ss_getParam('gameMode') == "gpm_coop") and p.isAIPlayer():
				return

		if not bf2.serverSettings.getAutoBalanceTeam():
			return

		# dont use autobalance when its suicide/changes team
		if p.getSuicide():
			p.setSuicide(0)
			return

		if ( not self.__config['allowCommander'] ) and p.isCommander():
			# dont autobalance the commander
			return

		squadid = p.getSquadId()
		teamid = p.getTeam()
		players = bf2.playerManager.getPlayers()

		if ( not self.__config['allowSquadLeader'] ) and p.isSquadLeader():
			# only autobalance the squad leader if they are the only
			# member of that squad
			squad_members = 0
			for tp in players:
				if squadid == tp.getSquadId() and tp.index != p.index:
					# we have other members in this squad dont autobalance
					#self.mm.debug( 2, "AB: no ( squad leader with members )" )
					return

		if ( not self.__config['allowSquadMember'] ) and ( squadid > 0 ):
			# only autobalance squad members if there are no none
			# squad members / commander on this team
			basic_players = 0
			for tp in players:
				if ( 0 == tp.getSquadId() ) and ( teamid == tp.getTeam() ) and ( not p.isCommander() ):
					# none squad member / commander of this team
					basic_players += 1

			if 0 != basic_players:
				# we have basic players in this team we
				# will balance them instead
				#self.mm.debug( 2, "AB: no ( basic players avail )" )
				return

		aiPlayerBalance = 0
		team1 = 0
		team2 = 0
		for tp in players:
			if tp.getTeam() == 1:
				team1 += 1
			else:
				team2 += 1

			if tp.isAIPlayer():
				aiPlayerBalance += 1
			else:
				aiPlayerBalance -= 1

		if host.sgl_getIsAIGame():
			if self.mm.isBattleField2142() or not (host.ss_getParam('gameMode') == "gpm_coop"):
				if not (aiPlayerBalance < 0):
					if not p.isAIPlayer():
						return

		team2 = team2 * bf2.serverSettings.getTeamRatioPercent() / 100.0
		if ( teamid == 1 ):
			if ( team2 + 1 ) < team1:
				#self.mm.debug( 2, "AB: player '%s' -> team %d" % ( p.getName(), 2 ) )
				p.setTeam( 2 )
		elif ( teamid == 2 ):
			if ( team1 + 1 ) < team2:
				#self.mm.debug( 2, "AB: player '%s' -> team %d" % ( p.getName(), 1 ) )
				p.setTeam( 1 )

	def onPlayerChangeTeams( self, p, humanHasSpawned ):
		"""Ensure the player isnt unbalancing the teams."""
		if 1 != self.__state:
			return

		self.mm.debug( 2, "AB: change" )

		if not bf2.serverSettings.getAutoBalanceTeam():
			return

		# dont teamswitch alive players, or they will have the wrong teams kit
		if p.isAlive():
			return

		if host.sgl_getIsAIGame() and ( self.mm.isBattleField2142() or not ( host.ss_getParam('gameMode') == "gpm_coop" ) ):
			if humanHasSpawned or p.isAIPlayer():
				return

			# handling aiplayer team change autobalance when round not started
			team = p.getTeam()
			aiplayer = 0

			for tp in bf2.playerManager.getPlayers():
				if aiplayer == 0 and tp.getTeam() == team and tp.isAIPlayer():
					aiplayer = tp
					break

			if aiplayer:
				if p.getTeam() == 1:
					aiplayer.setTeam(2)
				else:
					aiplayer.setTeam(1)

		else:
			# checking to see if player is allowed to change teams

			team1 = 0
			team2 = 0
			for tp in bf2.playerManager.getPlayers():
				if tp.getTeam() == 1:
					team1 += 1
				else:
					team2 += 1

			if abs(team1 - team2) > 1:
				if p.getTeam() == 1:
					p.setTeam(2)
				else:
					p.setTeam(1)

	def onGameStatusChanged( self, status ):
		"""Make a note of the game status"""
		"""Switch players to the other team if end of round"""
		if 0 != self.__config['roundSwitch'] and bf2.GameStatus.PreGame == status and bf2.GameStatus.EndGame == self.mm.lastGameStatus:
			# End of round so swap players
			if 1 == self.__config['roundSwitch']:
				# Straight swap
				for player in bf2.playerManager.getPlayers():
					# avoid autobalance changing us back
					player.setSuicide( 1 )
					# Change their team
					if 1 == player.getTeam():
						player.setTeam( 2 )
					else:
						player.setTeam( 1 )

			elif 2 == self.__config['roundSwitch']:
				# Randomise
				random.seed();
				players = bf2.playerManager.getPlayers()
				random.shuffle( players )
				i = 1
				half = int( len( players ) / 2 );
				for player in players:
					# avoid autobalance changing us back
					player.setSuicide( 1 )
					# Change their team
					if i <= half:
						player.setTeam( 1 )
					else:
						player.setTeam( 2 )
					i += 1

	def init( self ):
		"""Provides default initialisation."""
		self.__config = self.mm.getModuleConfig( configDefaults )

		# Register our game handlers
		if 0 == self.__state:
			host.registerHandler( 'PlayerConnect', self.onPlayerConnect, 1 )
			host.registerHandler( 'PlayerDeath', self.onPlayerDeath, 1 )
			host.registerHandler( 'PlayerChangeTeams', self.onPlayerChangeTeams, 1 )

		# Register your game handlers and provide any
		# other dynamic initialisation here
		host.registerGameStatusHandler( self.onGameStatusChanged )

		self.__state = 1

	def shutdown( self ):
		"""Shutdown and stop processing."""

		# Unregister game handlers and do any other
		# other actions to ensure your module no longer affects
		# the game in anyway
		host.unregisterGameStatusHandler( self.onGameStatusChanged )

		# Flag as shutdown as there is currently way to do this
		self.__state = 2

def mm_load( modManager ):
	"""Creates the auto balance object."""
	return AutoBalance( modManager )
