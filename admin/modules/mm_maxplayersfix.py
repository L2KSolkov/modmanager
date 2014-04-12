# vim: ts=4 sw=4 noexpandtab
"""Max Players Fix module.

This is the Max Players Fix module

===== Config =====
 # The reason specified when the new player is kicked
 mm_maxplayersfix.kickMessage "Too many players bug"

===== History =====
 v1.1 - 12/10/2011:
 Added BFP4F Support

 v1.0 - 19/01/2007:
 Initial version

Copyright (c)2008 Multiplay
Author: Steven 'Killing' Hartland
"""

import bf2
import host
import mm_utils

# Set the version of your module here
__version__ = 1.1

# Set the required module versions here
__required_modules__ = {
	'modmanager': 1.6,
	'mm_kicker': 2.2
}

# Does this module support reload ( are all its reference closed on shutdown? )
__supports_reload__ = True

# Sets which games this module supports
__supported_games__ = {
	'bf2': True,
	'bf2142': True,
	'bfheroes': False,
	'bfp4f': False
}

# Set the description of your module here
__description__ = "Max Players Fix v%s" % __version__

# Add all your configuration options here
configDefaults = {
	'kickMessage': 'Too many players bug'
}

class MaxPlayersFix( object ):

	def __init__( self, modManager ):
		# ModManager reference
		self.mm = modManager

		# Internal shutdown state
		self.__state = 0

		# Add any static initialisation here.
		# Note: Handler registration should not be done here
		# but instead in the init() method

	def sortByConnected( self, p1, p2 ):
		"""Sorts a players by their connected time"""
		if self.__reservedSlots.has_key( p1.getName() ):
			p1_reserved = True
		else:
			p1_reserved = False

		if self.__reservedSlots.has_key( p2.getName() ):
			p2_reserved = True
		else:
			p2_reserved = False

		if p1_reserved and not p2_reserved:
			return 1
		elif p2_reserved and not p1_reserved:
			return -1

		return int( p2.mmKickerInfo.connectedAt - p1.mmKickerInfo.connectedAt )

	def onPlayerSpawn( self, player, soldier ):
		"""Do something when a player spawns."""
		if 1 != self.__state:
			return 0

		try:
			players = bf2.playerManager.getPlayers()
			num_players = len( players )
			max_players = bf2.serverSettings.getMaxPlayers()
			if num_players > max_players:
				self.mm.warn( "Too may players %d > %d (fixing)" % ( num_players, max_players ) )
				players_to_kick = num_players - max_players
				reason = self.__config['kickMessage']

				# Need to check the reserved slots for sorting
				self.__reservedSlots = {}
				for nick in host.rcon_invoke( 'reservedSlots.list' ).split( '\n' ):
					self.__reservedSlots[nick] = True
					
				# Sort so we kick the last player to join
				players.sort( self.sortByConnected )
				for p in players:
					self.mm.banManager().kickPlayer( p, reason )
					players_to_kick -= 1
					if 0 == players_to_kick:
						return 1
		except Exception, detail:
			self.mm.error( "Error (%s)" % ( detail ), True )
			return False

		return 0
				

	def init( self ):
		"""Provides default initialisation."""

		# Load the configuration
		self.__config = self.mm.getModuleConfig( configDefaults )

		# Register your game handlers and provide any
		# other dynamic initialisation here

		if 0 == self.__state:
			# Register your host handlers here
			host.registerHandler( 'PlayerSpawn', self.onPlayerSpawn, 1 )

		# Update to the running state
		self.__state = 1

	def shutdown( self ):
		"""Shutdown and stop processing."""

		# Unregister game handlers and do any other
		# other actions to ensure your module no longer affects
		# the game in anyway

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
	return MaxPlayersFix( modManager )
