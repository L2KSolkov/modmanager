# vim: ts=4 sw=4 noexpandtab
"""Team kill punish system

This is a team kill ModManager module

===== Config =====
 # Sets the time allowed for punishment
 mm_tk_punish.punishTime 20
 
 # Sets if punish / forgives should be announced
 # 0 = no announcements
 # 1 = announce punishes only
 # 2 = announce punishes and forgives
 mm_tk_punish.announcePunishments 1
 
 # Sets the punish message ( must included the default replacement parameters )
 mm_tk_punish.punishMessage "TKPUNISH: %s punishes %s for a teamkill (%s has %d punishes and %d forgives)"
 
 # Sets the forgive message ( must included the default replacement parameters )
 mm_tk_punish.forgiveMessage "TKPUNISH: %s forgives %s for a teamkill (%s has %d punishes and %d forgives)"
 
 # Ban reason
 mm_tk_punish.banReason "Team killing"
 
 # Ban period
 mm_tk_punish.banPeriod "Round"
 
 # Ban Message delay
 mm_tk_punish.banMessageDelay 5
 
 # Banned by
 mm_tk_punish.bannedBy "ModManager Team Kill Punisher"

===== History =====
 v2.3 - 12/10/2011:
 Added BFP4F Support

 v2.2 - 25/08/2009:
 Updated Aviator test from BF2 1.50 patch

 v2.1 - 21/04/2009:
 Added road kill tk change from BF2 v1.50 patch
 
 v2.0 - 15/04/2008:
 Added a validation for attacher removal of pending tk's

 v1.9 - 30/08/2006:
 Added supported games
 
 v1.8 - 29/03/2006:
 Now resets player tkData before each round

 v1.7 - 22/02/2006:
 Additional error checking for punish announcements + logging of punishes
 Fixed TK announcements use of invalid victim object

 v1.6 - 20/02/2006:
 Announcements are now logged
 Announcement errors are now delt with
 
 v1.5 - 18/02/2006:
 Added missing configuration defaults
 
 v1.4 - 15/02/2006:
 Now uses self.mm.banManager().<method>
 Config option banMessage replaced by banReason for ban manager compatibility
 
 v1.3 - 01/02/2006:
 Added Punish / Forgive announcements ( original idea from Battlefield.no )
 Now uses the ban manager to execute bans
 Now requires ModManager version 1.1
 
 v1.2 - 04/10/2005:
 Incorporated BF2 1.03 patch changes ( ban now uses key and artillery kills are no longer counted )
 
 v1.1 - 30/06/2005:
 Updated to ModManager format by Steven 'Killing' Hartland
 
 v1.0:
 Created by DICE
"""

import bf2
import host
import mm_utils
import bf2.stats.constants

__version__ = 2.3

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

__description__ = "ModManager Team kill punisher v%s" % __version__

configDefaults = {
	'punishTime': 20,
	'announcePunishments': 1,
	'punishMessage': "TKPUNISH: %s punishes %s for a teamkill (%s has %d punishes and %d forgives)",
	'forgiveMessage': "TKPUNISH: %s forgives %s for a teamkill (%s has %d punishes and %d forgives)",
	'banReason': "Team killing",
	'banMessageDelay': 5,
	'banPeriod': 'Round',
	'bannedBy': "ModManager Team Kill Punisher"
}

TK_PUNISH_COMMANDID = 100
TK_FORGIVE_COMMANDID = 101

class TkData:
	def __init__(self):
		self.punished = 0
		self.timesPunished = 0
		self.timesForgiven = 0
		self.pending = []
		self.lastTKedBy = None

class Punisher( object ):

	def __init__( self, modManager ):
		"""Create a new instance."""
		self.mm = modManager
		self.__state = 0

	def checkEnable( self ):
		"""Check to see if team kill punish is enabled."""
		if not bf2.serverSettings.getTKPunishEnabled():
			if self.updateTimer:
				self.updateTimer.destroy()
				self.updateTimer = None
			return False
		else:
			if not self.updateTimer:
				self.updateTimer = bf2.Timer( self.onUpdate, 10, 1 )
				self.updateTimer.setRecurring( 10 )

			return True

	def onUpdate( self, data ):
		"""Process updates."""
		if not self.checkEnable():
			return

		currentTime = host.timer_getWallTime()

		newPending = {}
		for attacker in self.hasPendingTks.iterkeys():
			newList = []

			for tk in attacker.tkData.pending:
				tkDate = tk[0]
				tkVictim = tk[1]

				# check if there is a pending TK with time expired
				if tkDate + self.__config['punishTime'] < currentTime:
					if bf2.serverSettings.getTKPunishByDefault():
						attacker.tkData.punished += 1
						self.checkPunishLimit(attacker)

						tkVictim.tkData.timesPunished += 1
						if self.__config['announcePunishments']:
							try:
								msg = self.__config['punishMessage'] % ( tkVictim.getName(), attacker.getName(), tkVictim.getName(), tkVictim.tkData.timesPunished, tkVictim.tkData.timesForgiven )
								mm_utils.msg_server( msg )
								self.mm.info( msg )
							except Exception, details:
								self.mm.error( "Error announcing Punish (%s)" % details )
					else:
						tkVictim.tkData.timesForgiven += 1
						if 2 == self.__config['announcePunishments']:
							try:
								msg = self.__config['forgiveMessage'] % ( tkVictim.getName(), attacker.getName(), tkVictim.getName(), tkVictim.tkData.timesPunished, tkVictim.tkData.timesForgiven )
								mm_utils.msg_server( msg )
								self.mm.info( msg )
							except Exception, details:
								self.mm.error( "Error announcing forgive (%s)" % details )

					# remove player from global list, if it was the last tk
					if len(attacker.tkData.pending) == 1:
						pass
					else:
						newPending[attacker] = 1

				else:
					newList += [tk]
					newPending[attacker] = 1

			attacker.tkData.pending = newList

		self.hasPendingTks = newPending


	def checkPunishLimit(self, player):
		"""Check to see if the player has triggered a punishment."""
		if player.tkData.punished >= bf2.serverSettings.getTKNumPunishToKick():
			self.mm.banManager().banPlayer( player, self.__config['banReason'], self.__config['banPeriod'], mm_utils.KickBanType.rcon, None, self.__config['bannedBy'], self.__config['banMessageDelay'] )


	# event actions

	def onPlayerConnect( self, player ):
		"""Add team kill data to the player."""
		if 1 != self.__state:
			return 0

		player.tkData = TkData()


	def onClientCommand( self, command, issuer, args ):
		"""Envoke punishment if required."""
		if 1 != self.__state:
			return 0

		if not self.checkEnable():
			return

		if command == TK_PUNISH_COMMANDID:
			self.executePunishAction(issuer, True)
		elif command == TK_FORGIVE_COMMANDID:
			self.executePunishAction(issuer, False)


	def onPlayerKilled( self, victim, attacker, weapon, assists, object ):
		"""Check to team kills."""
		if 1 != self.__state:
			return 0
		if not self.checkEnable():
			return

		if not victim or not attacker or victim == attacker or victim.getTeam() != attacker.getTeam():
			return

		# verify that TK was really given

		# no teamkills from wrecks
		if object != None and object.getIsWreck():
			return

		# no teamkills from artillery
		if weapon:
			attackerVehicle = bf2.objectManager.getRootParent(weapon)
			if attackerVehicle.isPlayerControlObject and attackerVehicle.getIsRemoteControlled():
				return

		if weapon == None and object != None:
			victimVehicle = victim.getVehicle()
			victimRootVehicle = bf2.objectManager.getRootParent(victimVehicle)
			victimVehicleType = bf2.stats.constants.getVehicleType(victimRootVehicle.templateName)
			attackerVehicle = attacker.getVehicle()
			attackerRootVehicle = bf2.objectManager.getRootParent(attackerVehicle)
			attackerVehicleType = bf2.stats.constants.getVehicleType(attackerRootVehicle.templateName)
			#No tk on roadkill from airplane and helo
			if attackerVehicleType == VEHICLE_TYPE_AVIATOR and victimVehicleType == VEHICLE_TYPE_SOLDIER:
				return

		# ok, we have a teamkill
		currentTime = host.timer_getWallTime()
		attacker.tkData.pending += [(currentTime, victim)]
		self.hasPendingTks[attacker] = 1

		victim.tkData.lastTKedBy = attacker # can only punish / forgive the last TK'er

		bf2.gameLogic.sendClientCommand(victim.index, TK_PUNISH_COMMANDID, (2, victim.index, attacker.index, self.__config['punishTime']))


	def executePunishAction( self, victim, punish ):
		"""Punish or forgive a player."""
		if not self.checkEnable() or not victim or not victim.isValid():
			return

		attacker = victim.tkData.lastTKedBy
		if attacker == None or not attacker.isValid():
			return

		currentTime = host.timer_getWallTime()

		newList = []
		for tk in attacker.tkData.pending:
			tkDate = tk[0]
			tkVictim = tk[1]

			# if the attacker had a pending tk, and time has not run out
			if tkVictim == victim and tkDate + self.__config['punishTime'] > currentTime:
				if punish:
					attacker.tkData.punished += 1
					bf2.gameLogic.sendClientCommand(-1, TK_PUNISH_COMMANDID, (0, victim.index, attacker.index)) # 100 = tkpunish event, 0 = punish
					tkVictim.tkData.timesPunished += 1
					if self.__config['announcePunishments']:
						try:
							msg = self.__config['punishMessage'] % ( tkVictim.getName(), attacker.getName(), tkVictim.getName(), tkVictim.tkData.timesPunished, tkVictim.tkData.timesForgiven )
							mm_utils.msg_server( msg )
							self.mm.info( msg )
						except Exception, details:
							self.mm.error( "Error announcing forgive (%s)" % details )
				else:
					bf2.gameLogic.sendClientCommand(-1, TK_PUNISH_COMMANDID, (1, victim.index, attacker.index)) # 100 = tkpunish event, 1 = forgive
					tkVictim.tkData.timesForgiven += 1
					if 2 == self.__config['announcePunishments']:
						try:
							msg = self.__config['forgiveMessage'] % ( tkVictim.getName(), attacker.getName(), tkVictim.getName(), tkVictim.tkData.timesPunished, tkVictim.tkData.timesForgiven )
							mm_utils.msg_server( msg )
							self.mm.info( msg )
						except Exception, details:
							self.mm.error( "Error announcing forgive (%s)" % details )
			else:
				newList += [tk]

		attacker.tkData.pending = newList

		if 0 == len(attacker.tkData.pending) and self.hasPendingTks.has_key( attacker ):
			del self.hasPendingTks[attacker]

		self.checkPunishLimit(attacker)

	def onGameStatusChanged( self, status ):
		"""Resets player tkData."""
		try:
			if bf2.GameStatus.PreGame == status:
				# Starting a new round reset all details
				for player in bf2.playerManager.getPlayers():
					self.onPlayerConnect( player )

		except Exception, details:
			self.mm.error( "Oooops: %s" % details, True )

	def init( self ):
		"""Provides default initialisation."""
		self.__config = self.mm.getModuleConfig( configDefaults )
		self.hasPendingTks = {}
		self.updateTimer = None

		# Register our base handlers
		host.registerGameStatusHandler( self.onGameStatusChanged )

		if 0 == self.__state:
			host.registerHandler( 'PlayerConnect', self.onPlayerConnect, 1 )
			host.registerHandler( 'PlayerKilled', self.onPlayerKilled )
			host.registerHandler( 'ClientCommand', self.onClientCommand )

		# Connect already connected players if reinitializing
		for p in bf2.playerManager.getPlayers():
			self.onPlayerConnect( p )

		self.checkEnable()
		self.__state = 1

	def shutdown( self ):
		"""Shutdown and stop processing."""

		# Unregister our game handlers
		host.unregisterGameStatusHandler( self.onGameStatusChanged )

		if self.updateTimer:
			self.updateTimer.destroy()
			self.updateTimer = None

		# Flag as shutdown as there is currently way to do this
		self.__state = 2

def mm_load( modManager ):
	"""Creates the team kill punisher object."""
	return Punisher( modManager )
