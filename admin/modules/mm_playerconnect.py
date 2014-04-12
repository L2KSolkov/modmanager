# vim: ts=4 sw=4 noexpandtab
""" Rank limiting system.

This is a rank limiting system ModManager module

===== Config =====

 # See serversettings.con: sv.maxRank

===== History =====
 v1.5 - 12/10/2011:
 Added BFP4F Support

 v1.4 - 01/05/2008:
 Added Player validation support for BF2 v1.50

 v1.3 - 01/05/2008:
 Added Player validation method from BF2142 v1.50
 
 v1.2 - 20/06/2006:
 Corrected missing params to onPlayerChallenge and onPrePlayerConnect
 
 v1.1 - 30/06/2006:
 Updated to ModManager format by Steven 'Killing' Hartland
 
 v1.0:
 Created by: DICE
 Battlefield 2142 -- example player connect checking system module.
 Default module for handling how players can be denied access
 to a server.

 Copyright (c)2006 Digital Illusions CE AB
 Author: Kristoffer Benjaminsson
"""

import bf2
import host
import bf2.stats.constants
import mm_utils

__version__ = 1.5

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

__description__ = "ModManager Player Connect v%s" % __version__

configDefaults = {
	'nameHackBanReason': "Using name kacks",
	'pidHackBanReason': "Using PID kacks",
	'nameHackBanAnnouncement': "Player: '%s' real name: '%s' was kicked and banned for using Name Hacks",
	'pidHackBanAnnouncement': "Player: '%s' tried to use PlayerID: %s when their real PlayerID is %s and was kicked and banned for using PID Hacks",
	'kickBanType': mm_utils.KickBanType.rcon,
	'kickDelay': 5,
	'banType': mm_utils.BanMethod.key,
	'banPeriod': 'Perm',
}


class RankLimiter( object ):
	def __init__( self, modManager ):
		"""Create a new instance."""
		self.mm = modManager
		self.__state = 0

	def init( self ):
		"""Provides default initialisation."""
		self.__config = self.mm.getModuleConfig( configDefaults )

		if 0 == self.__state:
			if ( not self.mm.isBattleField2 ):
				host.registerHandler( 'PlayerChallenge', self.onPlayerChallenge, 1 )
				host.registerHandler( 'PrePlayerConnect', self.onPrePlayerConnect, 1 )

			# Added by Niklas Henriks to validate player Name and ID for update 1.50.
			try:
				host.registerHandler( 'ValidatePlayerNameResponse', self.onPlayerNameValidated, 1 )
			except:
				# Ignore error for backwards compatibility
				pass

		self.__state = 1

	def shutdown( self ):
		"""Shutdown and stop processing."""

		# Flag as shutdown as there is currently way to do this
		self.__state = 2

	# onPlayerChallenge is called by the engine as part of the
	# challenge-response handshaking. At this time only client ID and rank
	# is available. Servers can use this information to deny access
	# based on the players rank.
	# Only called for ranked servers
	def onPlayerChallenge( self, clientId, rank ):
		self.mm.debug( 3, "onPlayerChallenge: " + ":" + str(clientId) + ":" + str(rank) )

		# this can happen if it's the first time a player runs
		# the game on a computer and no stats were retrieved
		if rank == -1:
			return

		if bf2.serverSettings.getMaxRank() > 0 and rank > bf2.serverSettings.getMaxRank():
			bf2.gameServer.abortCurrentConnectionAttempt(clientId)

	# onPlayerNameValidated is called by the engine when a reply from GameSpy arives, this is done directly when the player connects to the game server.
	# Only used on dedicated servers.
	def onPlayerNameValidated( self, realNick, oldNick, realPID, oldPID, player ):
		self.mm.debug( 3, "Player Name Validated realNick: '%s', oldNick: '%s', realPID: %s, oldPID: %s, player: %d" % ( realNick, oldNick, realPID, oldPID, player.index ) )

		if realNick != oldNick:
			# Nick Hacker ban
			self.mm.banManager().banPlayer( player, self.__config['nameHackBanReason'], self.__config['banPeriod'], self.__config['kickBanType'], self.__config['banType'], 'ModManager PlayerConnect', self.__config['kickDelay'] )
			if self.__config['nameHackBanAnnouncement']:
				msg = self.__config['nameHackBanAnnouncement'] % ( oldNick, realNick )
				mm_utils.msg_server( msg )
				self.mm.info( msg )
			return

		if realPID != oldPID:
			# PID Hacker ban
			self.mm.banManager().banPlayer( player, self.__config['pidHackBanReason'], self.__config['banPeriod'], self.__config['kickBanType'], self.__config['banType'], 'ModManager PlayerConnect', self.__config['kickDelay'] )
			# Announcement
			if self.__config['pidHackBanAnnouncement']:
				msg = self.__config['pidHackBanAnnouncement'] % ( oldNick, oldPID, realPID )
				mm_utils.msg_server( msg )
				self.mm.info( msg )

	# onPrePlayerConnect is called by the engine after the challenge-response
	# handshake is done, but prior to the player actually beeing created.
	# The clientId passed is the same as passed to the onPlayerChallenge event.
	def onPrePlayerConnect( self, clientId, playerNick ):
		self.mm.debug( 3, "onPrePlayerConnect: " + str( playerNick ) + ":" + str( clientId ) )
		#if playerNick == "some_nick_to_deny":
		#	bf2.gameServer.abortCurrentConnectionAttempt(clientId)			

def mm_load( modManager ):
	"""Creates the rank limiter object."""
	return RankLimiter( modManager )

