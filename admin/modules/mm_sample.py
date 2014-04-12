# vim: ts=4 sw=4 noexpandtab
"""Sample module.

This is a Sample ModManager module

===== Config =====
 # Sets option 1
 mm_sample.myOption1 1
 
 # Sets option 2
 mm_sample.myOption2 "hello there"

===== History =====
 v1.4 - 12/10/2011:
 Added BFP4F Support

 v1.3 - 30/08/2006:
 Added supported games

 v1.2 - 13/08/2005:
 Added missing mm.unregisterRconCmdHandler to shutdown
 
 v1.1 - 29/07/2005:
 Updated API definition
 
 v1.0 - 01/07/2005:
 Initial version

Copyright (c)2005 Multiplay
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

# Sets which games this module supports
__supported_games__ = {
	'bf2': True,
	'bf2142': True,
	'bfheroes': True,
	'bfp4f': True
}

# Set the description of your module here
__description__ = "MyModule v%s" % __version__

# Add all your configuration options here
configDefaults = {
	'myOption1': 1,
	'myOption2': 'Hello there'
}

class MyModule( object ):

	def __init__( self, modManager ):
		# ModManager reference
		self.mm = modManager

		# Internal shutdown state
		self.__state = 0

		# Add any static initialisation here.
		# Note: Handler registration should not be done here
		# but instead in the init() method

		# Your rcon commands go here:
		self.__cmds = {
			'sample': { 'method': self.cmdSample, 'level': 10 }
		}

	def cmdExec( self, ctx, cmd ):
		"""Execute a MyModule sub command."""

		# Note: The Python doc above is used for help / description
		# messages in rcon if not overriden
		return mm_utils.exec_subcmd( self.mm, self.__cmds, ctx, cmd )

	def cmdSample( self, ctx, cmd ):
		"""Does XYZ.
		Details about this function
		"""
		# Note: The Python doc above is used for help / description
		# messages in rcon if not overriden
		self.mm.debug( 2, "Running cmdSample '%s'" % cmd )
		ctx.write( "Your arguments where '%s'" % cmd )
		return 1

	def onPlayerSpawn( self, player, soldier ):
		"""Do something when a player spawns."""
		if 1 != self.__state:
			return 0

		# Put your actions here

	def init( self ):
		"""Provides default initialisation."""

		# Load the configuration
		self.__config = self.mm.getModuleConfig( configDefaults )

		# Register your game handlers and provide any
		# other dynamic initialisation here

		if 0 == self.__state:
			# Register your host handlers here
			host.registerHandler( 'PlayerSpawn', self.onPlayerSpawn, 1 )

		# Register our rcon command handlers
		self.mm.registerRconCmdHandler( 'sample', { 'method': self.cmdExec, 'subcmds': self.__cmds, 'level': 1 } )

		# Update to the running state
		self.__state = 1

	def shutdown( self ):
		"""Shutdown and stop processing."""

		# Unregister game handlers and do any other
		# other actions to ensure your module no longer affects
		# the game in anyway
		self.mm.unregisterRconCmdHandler( 'sample' )

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
	return MyModule( modManager )
