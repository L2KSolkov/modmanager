# vim: ts=4 sw=4 noexpandtab
"""ClanMatch module.

This is  Clan Match ModManager module *** DEPRECATED ***
 
===== History =====
 v1.4 - 12/10/2011:
 Added BFP4F Support

 v1.3 - 04/10/2006:
 This module is now deprecated please use mm_autobalance.roundSwitch instead!
 
 v1.2 - 30/08/2006:
 Added supported games
 
 v1.1 - 25/11/2005:
 Enabled roundSwitch config option

 v1.0 - 30/10/2005:
 Initial version

Copyright (c)2008 Multiplay
Author: Steven 'Killing' Hartland
"""

import bf2
import host
import mm_utils

# Set the version of your module here
__version__ = 1.4

# Set the required module versions here
__required_modules__ = {
	'modmanager': 1.6
}

# Does this module support reload ( are all its reference closed on shutdown? )
__supports_reload__ = True

__supported_games__ = {
	'bf2': True,
	'bf2142': True
	'bfheroes': False,
	'bfp4f': False
}

# Set the description of your module here
__description__ = "ClanMatch v%s" % __version__

# Add all your configuration options here
configDefaults = {
}

class ClanMatch( object ):

	def __init__( self, modManager ):
		# ModManager reference
		self.mm = modManager

		# Internal shutdown state
		self.__state = 0

		self.mm.warn( "This module is deprecated, please use mm_autobalance.roundSwitch instead!" );

	def cmdExec( self, ctx, cmd ):
		"""Execute a ClanMatch sub command."""

		# Note: The Python doc above is used for help / description
		# messages in rcon if not overriden
		return mm_utils.exec_subcmd( self.mm, self.__cmds, ctx, cmd )

	def init( self ):
		"""Provides default initialisation."""

		# Load the configuration
		self.__config = self.mm.getModuleConfig( configDefaults )

		# Update to the running state
		self.__state = 1

	def shutdown( self ):
		"""Shutdown and stop processing."""

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
	return ClanMatch( modManager )
