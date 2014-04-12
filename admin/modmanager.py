# vim: ts=4 sw=4 noexpandtab

"""Battlefield -- ModManager.

This is a Module Manager for BattleField
It enables users to add and remove modules dynamicly using
a centralised configuration which is multi server friendly.

The location of the config file modmanager.con is determined by the directory identified
by +config command line option for BF2 and by the directory identified by the +overlayPath
command line option on BF2142. If neither are set it will look in the <mod>/settings directory.

It provides a fully expandable and configurable Module
framework and Rcon implementation.

===== Config =====
 # The sub path where modules are to be found
 modmanager.moduleBase "modules"
 
 # Auto save config when shutting down
 modmanager.autoSave 1
 
 # The path to look in when @HOME@ is seen in the path
 # of the servers main config file
 modmanager.homeGuess "C:/Documents and Settings/Administrator/My Documents/Battlefield 2/"
 
 # The name of the core rcon module
 modmanager.rconModule "mm_rcon"
 
 # The name of the core ban manager module
 modmanager.banManagerModule "mm_banmanager"
 
 # The name of the core logger module
 modmanager.logModule "mm_logger"
 
 # Enable / disable debug logging
 modmanager.debugEnable 0
 
 # The file to send debug logging to
 modmanager.debugFile "modmanager_debug.log"
 
 # The log verbosity:
 # 0 = errors
 # 1 = + warnings
 # 2 = + info ( default )
 # 3 = + debug
 # ...
 modmanager.logLevel 2,
 
 # If the log file is auto flushed after every write
 modmanager.logAutoFlush 1
 
 # The format for the log date
 modmanager.logDateFormat "[%Y-%m-%d %H:%M:%S] "

===== Rcon methods =====
 # Print the running config
 mm printRunningConfig
 
 # Save the running config
 mm saveConfig
 
 # Load the specified module
 mm loadModule <module_name>
 
 # List the known modules an their states
 mm listModules
 
 # Shutdown the specified module
 mm shutdownModule <module_name>
 
 # Start the specified module
 mm startModule <module_name>
 
 # Reload the specified module
 mm reloadModule <module_name>
 
 # Set the parameter of a module
 mm setParam <module_name> <param> <value>

===== Notes =====
* Its not currently garanteed that shutdown methods are called when the server exits. Due to this autoSave may be unreliable
* Setting the parameter of a module may not take effect until that module is reloaded or the server restarted ( requires saveConfig )

===== History =====
 v2.2c - 14/05/2013
 Added dependant_day_night to Heroes
 
 v2.2b - 29/01/2013
 Added compatibility for long values

 v2.2a - 11/12/2012
 Added ruin_snow to Heroes
 
 v2.2 - 10/12/2012
 Added new map to Play4Free

 v2.1v - 22/10/2012
 Added new gametype to Play4Free

 v2.1u - 19/09/2012
 Added dependent_day to Heroes

 v2.1t - 17/07/2012
 Added Ruin_Day to Heroes

 v2.1s - 21/06/2012
 Added river to Heroes
 
 v2.1r - 24/05/2012
 Added Trail to Play 4 Free
 
 v2.1q - 17/04/2012
 Added Lunar Landing to Battlefield Heroes

 v2.1p - 23/02/2012
 Added Mashtuur City to Play 4 Free
 
 v2.1o - 24/01/2012
 Added royal_rumble_day to Battlefield Heroes
 
 v2.1n - 13/12/2011
 Added new Battlefield Heroes map: royal_rumble_snow
 
 v2.1m - 08/12/2011
 Added new map for Battlefield Play for Free
 Missing version info:
 v2.1l - Added CTF Gametype to Battlefield Heroes
 v2.1k - Added royal_rumble for Battlefield Heroes
 v2.1j Added Dragon Valley for Battlefield Play 4 Free
 
 v2.1h - 27/06/2011
 Corrected isXXX description
 
 v2.1 - 12/01/2011
 Added Support for Battlefield Play for Free

 v2.0c - 10/11/2009:
 Added support for Windows paths in automatic fallback on BF2 for config location
 
 v2.0 - 07/05/2009:
 Added isBattleFieldHeroes

 v1.9 - 21/04/2009:
 Version bump for BF2 v1.50 patch support

 v1.8 - 10/05/2008:
 Version bump for BF2142 v1.50 patch support

 v1.7 - 21/02/2007:
 setParam is now prevented from altering mm_rcon.restrictedGametypes and mm_rcon.lockedSettings
 Added a method to retrieve the rcon handle
 
 v1.6 - 08/02/2007:
 Version bump
 Increased error checking for config parsing
 setParam is now prevented from altering restricted parameters

 v1.5 - 03/11/2006:
 Added new rcon methods runRconCommand and getRconContext
 
 v1.5-rc2 - 18/10/2006:
 Corrected loading of legacy modules

 v1.5-rc1 - 16/08/2006:
 Now uses .search instead of .match in regexp
 Removed invalid supported games output
 Added 2142 compatibility
 Added isBattleField2142, isBattleField2 and getGame methods to enable game checks
 Version bump

 v1.4 - 30/05/2006:
 Version bump

 v1.3 - 30/05/2006:
 Version bump

 v1.2a - 22/03/2006:
 Swapped rcon and banManager initialisation order so that banManager can register rcon commands

 v1.2 - 22/02/2006:
 Bumped version number for ban manager release
 Now also searches admin/ + moduleBase + /libs for python modules

 v1.1a - 15/02/2006:
 Removed proxy methods for ban manager methods to reduce the design coupling of mm and banmanager
 All Ban Manager methods should now be accessed via mm.banManager().<method>
 
 v1.1 - 13/02/2005:
 Fixed random module dependency load problem
 Added Ban Manager proxy methods
 
 v1.0 - 04/10/2005:
 Corrected autoSave ( still unreliable as the servers doesnt call shutdown most the time )
 
 v1.0 - rc-5 23/08/2005:
 Added configPath() method
 Updated time logic to take into account none started matches and correct roundTimeLeft()
 
 v1.0 - rc-4 16/08/2005:
 shutdown() and init() are now mandatory methods for modules
 Added startTimeWall and startTimeUTC properties which identifies then the round started excluding start delay
 Added roundTime() and roundTimeLeft() methods which return the number of seconds the round has been playing for and has left respectively. Pauses and start delay are taken into account
 
 v1.0 - beta1 - 02/08/2005:
 Initial version

Copyright (c)2008 Multiplay
Author: Steven 'Killing' Hartland
"""

import sys
import mm_utils
import datetime
import time
import re
import host
import bf2
import bf2.stats.constants

__version__ = 2.2

__description__ = "Multiplay, ModManager v%s" % __version__

__all__ = [
	"rconModule",
	"banManagerModule",
	"logModule",
	"logLevel",
	"logFilename"
	"logDateFormat"
	"banFilename",
	"debugEnable",
	"debugFile",
	"isWin32",
]

configDefaults = {
	#
	# Module settings
	'moduleBase': 'modules',
	'autoSave': 1,
	'homeGuess': 'C:/Documents and Settings/Administrator/My Documents/Battlefield 2/',

	#
	# Core modules
	#
	'rconModule': 'mm_rcon',
	'banManagerModule': 'mm_banmanager',
	'logModule' : 'mm_logger',

	#
	# Debug settings
	#
	'debugEnable': 0,
	'debugFile': 'modmanager_debug.log',

	#
	# Logging settings
	#
	# The log verbosity:
	# 0 = errors
	# 1 = + warnings
	# 2 = + info ( default )
	# 3 = + debug
	# ...
	'logLevel': 2,

	# If the log file is auto flushed after every write
	'logAutoFlush' : 1,

	# Append to the log
	'logAppend': 0,

	# The format for the log date
	'logDateFormat': "[%Y-%m-%d %H:%M:%S] ",
}

class ModuleStatus:
	unloaded = 0
	loaded = 1
	running = 2

class DebugLogger:
	"""The logger used for debugging ModManager."""
	def __init__( self, filename, logAppend, autoFlush ):
		"""Opens the given filename for appending."""
		self.autoFlush = autoFlush
		try:
			if logAppend:
				self.__file = open( filename, 'a+' )
			else:
				self.__file = open( filename, 'w+' )

		except StandardError, detail:
			msg = "Failed to open '%s' (%s)" % ( filename, detail )
			raise IOError, msg

	def write( self, str ):
		"""Writes to the debug log flushing if required."""
		self.__file.write( str )
		if self.autoFlush:
			self.__file.flush()

	def close( self ):
		"""Close the debug log."""
		if self.__file:
			self.__file.close()

class ModManager( object ):
	"""The core manager which looks after the modules and configuration."""
	def __init__( self, debuglog ):
		"""Create a module manager, loading the configuration and any requested modules."""
		# default init

		self.__bf2String = 'Battlefield 2'
		self.__bf2142String = 'Battlefield 2142'
		self.__bfheroesString = 'Battlefield Heroes'
		self.__bfp4fString = 'Battlefield Play 4 Free'
		self.__bf2Id = 'bf2'
		self.__bf2142Id = 'bf2142'
		self.__bfheroesId = 'bfheroes'
		self.__bfp4fId = 'bfp4f'
		self.__gameId = self.__bf2Id
		self.__gameString = self.__bf2String
		self.__gameName = self.__bf2Id
		self.__state = 0
		self.__logger = None
		self.__modules = {}
		self.__updateRequestors = []
		self.__configFull = { __name__: {} }
		self.__playCount = 0
		self.__pauseStart = 0
		self.__matchTimeLost = 0
		self.__timeLimit = 0
		self.lastGameStatus = bf2.GameStatus.PreGame
		self.currentGameStatus = bf2.GameStatus.PreGame
		self.gamePlaying = False
		self.roundStarted = False
		self.startTimeUTC = int( time.time() )
		self.startTimeWall = int( host.timer_getWallTime() )

		# Load our config default and set to local vars
		for var in configDefaults:
			val = configDefaults[var]
			self.__configFull[__name__][var] = val
			self.__setattr__( var, val )

		mm_utils.init( self )

		# Determine where to load the config from
		self.__setConfigFile();

		# parse the configuration file
		self.__parseConfig()

		# Enable debug if required
		if self.debugEnable:
			# close the startup log
			# Note: we dont always close this as that would cause issues
			if debuglog:
				debuglog.close()
			# open the new one ( settings may have changed
			sys.stdout = sys.stderr = DebugLogger( self.debugFile, self.logAppend, self.logAutoFlush )

		# add the module base to the path
		sys.path.append( 'admin/' + self.moduleBase )
		sys.path.append( 'admin/' + self.moduleBase + '/libs' )

		# create the logger
		self.__initLogger()

		self.info( 'Creating Multiplay, ModManager v%s for %s (www.multiplay.co.uk)' % ( __version__, self.__gameString ) )

		# We listen to state changes so we can tell others what
		# the current state is if they are dynamically loaded
		host.registerGameStatusHandler( self.onGameStatusChanged )

		# create the rcon
		self.__initRcon()

		# Initialise the ban system
		self.__initBanManager()

		# Register our rcon command handlers
		# Our internal commands
		self.__cmds = {
			'printRunningConfig': { 'method': self.cmdPrintRunningConfig, 'aliases': [ 'print' ], 'level': 80 },
			'saveConfig': { 'method': self.cmdSaveConfig, 'aliases': [ 'save' ], 'level': 90 },
			'loadModule': { 'method': self.cmdLoadModule, 'args': '<module_name>', 'aliases': [ 'load' ], 'level': 90 },
			'listModules': { 'method': self.cmdListModules, 'aliases': [ 'list' ], 'level': 70 },
			'shutdownModule': { 'method': self.cmdShutdownModule, 'args': '<module_name>', 'aliases': [ 'shutdown' ], 'level': 90 },
			'startModule': { 'method': self.cmdStartModule, 'args': '<module_name>', 'aliases': [ 'start' ], 'level': 90 },
			'reloadModule': { 'method': self.cmdReloadModule, 'args': '<module_name>', 'aliases': [ 'reload' ], 'level': 90 },
			'setParam': { 'method': self.cmdSetParam, 'args': '<module_name> <param> <value>', 'aliases': [ 'set' ], 'level': 90 },
		}

		# load the modules
		self.__loadModules();

	def isBattleField2142( self ):
		"""Is the game BattleField 2142"""
		return self.__gameId == self.__bf2142Id

	def isBattleField2( self ):
		"""Is the game BattleField 2"""
		return self.__gameId == self.__bf2Id

	def isBattleFieldHeroes( self ):
		"""Is the game BattleField Heroes"""
		return self.__gameId == self.__bfheroesId

	def isBattleFieldPlay4Free( self ):
		"""Is the game BattleField Play 4 Free"""
		return self.__gameId == self.__bfp4fId

	def getGameString( self ):
		"""Return the game string"""
		return self.__gameString

	def getGameId( self ):
		"""Return the game id"""
		return self.__gameId

	def pause( self ):
		"""Pause the game."""
		if bf2.GameStatus.Playing == self.currentGameStatus:
			msg = host.rcon_invoke( 'gameLogic.togglePause' )
			# TODO: remove when fixed
			self.onGameStatusChanged( bf2.GameStatus.Paused )
		else:
			msg = ''

		return msg

	def unpause( self ):
		"""Unpause the game."""
		if bf2.GameStatus.Paused == self.currentGameStatus:
			msg = host.rcon_invoke( 'gameLogic.togglePause' )
			# TODO: remove when fixed
			self.onGameStatusChanged( bf2.GameStatus.Playing )
		else:
			msg = ''

		return msg

	def onGameStatusChanged( self, status ):
		"""Make a note of the game status"""
		self.debug( 1, "STATUS: %d = %s" % ( status, mm_utils.status_name( status ) ) )
		if bf2.GameStatus.EndGame == status:
			self.__playCount = 0
			self.__pauseStart = 0
			self.__timeLimit = 0
			self.gamePlaying = False
			self.roundStarted = False

		elif bf2.GameStatus.Playing == status:
			self.gamePlaying = True
			now = int( host.timer_getWallTime() )

			if bf2.GameStatus.PreGame == self.currentGameStatus:
				# normal transition i.e. not pause
				start_delay = int( host.rcon_invoke( 'sv.startDelay' ) )
				self.__playCount += 1
				self.__timeLimit = host.ss_getParam( 'timeLimit' )
				self.__matchTimeLost = 0
				self.startTimeUTC = int( time.time() ) + start_delay
				self.startTimeWall = now + start_delay
				if 2 == self.__playCount:
					# We see state change from PreGame -> Playing twice before the round really starts
					self.roundStarted = True

			elif bf2.GameStatus.Paused == self.currentGameStatus:
				self.__matchTimeLost += ( now - self.__pauseStart )
				self.__pauseStart = 0

		elif bf2.GameStatus.Paused == status:
			self.__pauseStart = int( host.timer_getWallTime() )

		else:
			self.__pauseStart = 0

		self.lastGameStatus = self.currentGameStatus
		self.currentGameStatus = status
		#self.debug( 3, "STATUS NOW: last = %s, current = %s, playing = %s, started = %s" % ( mm_utils.status_name( self.lastGameStatus ), mm_utils.status_name( self.currentGameStatus ), self.gamePlaying, self.roundStarted ) )

	def roundTime( self ):
		"""Return how long a round has been running for.

		Takes into account start delay and any pauses.
		"""
		now = int( host.timer_getWallTime() )

		if bf2.GameStatus.Paused == self.currentGameStatus:
			cur_pause = now - self.__pauseStart
			round_time = now - self.startTimeWall - self.__matchTimeLost - cur_pause
		else:
			round_time = now - self.startTimeWall - self.__matchTimeLost

		if 0 > round_time:
			return 0
		else:
			return round_time

	def roundTimeLeft( self ):
		"""Return how long a round has left to play.

		Returns 0 if there is no time limit or the round hasn't started
		"""

		if self.__timeLimit:
			self.debug( 2, "TIME: %d, %d" % ( self.__timeLimit, self.roundTime() ) )
			time_left = self.__timeLimit - self.roundTime()
			if 0 > time_left:
				# game which hasnt really started so timelimit is not in effect
				return 0
			else:
				return time_left
		else:
			self.debug( 2, "TIME1: 0" )
			return 0

	def configPath( self ):
		"""Returns the config directory."""
		return self.__configPath

	#
	# Private Methods
	#

	def __setConfigFile( self ):
		"""Determines where our config file is."""
		try:
			# Try 2142 way
			self.__configPath = host.sgl_getOverlayDirectory()
			try:
				test = bf2.stats.constants.TYPE_BFHEROES
				self.__gameString = self.__bfheroesString
				self.__gameId = self.__bfheroesId
			except:
				try:
					test = bf2.stats.constants.ARMY_US
					self.__gameString = self.__bfp4fString
					self.__gameId = self.__bfp4fId
				except:
					self.__gameString = self.__bf2142String
					self.__gameId = self.__bf2142Id
		except:
			# Failed 2142 so fall back to determining from the config
			self.__gameString = self.__bf2String
			self.__gameId = self.__bf2Id
			configFileParts = host.rcon_invoke( 'sv.configFile' ).replace( '\\', '/' ).split( '/' );
			del configFileParts[len( configFileParts ) - 1]

			self.__configPath = "/".join( configFileParts )

		if self.__configPath.startswith( '@HOME@' ):
			# since we have no access to the environment and cant
			# do any directory listings atm we have to just guess
			self.warn( "Guessing '@HOME@' = '%s'" % self.homeGuess )
			self.__configPath = "%s%s" % ( self.homeGuess, self.__configPath[5:] )

		filename = "%s/%s.con" % ( self.__configPath, __name__ )

		# lets check
		try:
			check = open( filename, 'r' )
		except:
			# nope no good so lets check in the standard place
			self.__configPath = "%s/settings" % host.sgl_getModDirectory().replace( '\\', '/' )
			filename = "%s/%s.con" % ( self.__configPath, __name__ )

			try:
				check = open( filename, 'r' )
			except:
				self.error( "Failed to determine location of '%s.con'" % __name__ )
			else:
				self.__configFile = filename
				self.warn( "Using config file '%s'" % filename )
				check.close()
		else:
			check.close()
			self.__configFile = filename

	def __getattr__( self, name ):
		"""Return the attributes value."""
		try:
			return self.__dict__[name]
		except AttributeError:
			raise AttributeError, name

	def __setattr__( self, name, value ):
		"""Set the attributes value."""
		self.__dict__[name] = value

	def __delattr__( self, name ):
		"""Delete the attribute."""
		del self.__dict__[name]

	def __initLogger( self ):
		"""Initialise the logger."""
		self.__addModule( self.logModule )
		self.__logger = self.__loadModule( self.logModule )
		if not self.__logger:
			return 0

		return self.__initModule( self.logModule )

	def __initRcon( self ):
		"""Initialise rcon."""
		self.__addModule( self.rconModule )
		self.__rcon = self.__loadModule( self.rconModule )
		if not self.__rcon:
			return 0

		return self.__initModule( self.rconModule )

	def __initBanManager( self ):
		"""Initialise ban Manager."""
		self.__addModule( self.banManagerModule )
		self.__banManager = self.__loadModule( self.banManagerModule )
		if not self.__banManager:
			return 0

		return self.__initModule( self.banManagerModule )

	def __addModule( self, module_name ):
		"""Add a module to our list of modules."""
		self.debug( 2, "addModule '%s'" % module_name )
		self.__modules[module_name] = { 'status': ModuleStatus.unloaded }

	def __loadModules( self ):
		"""Load all modules"""


		# Note: We have to use .keys() as __loadModule may change the size
		# of .__modules
		module_names = self.__modules.keys()
		loaded = 0
		for module_name in module_names:
			if ModuleStatus.unloaded == self.__modules[module_name]['status']:
				# modules not currently loaded so load
				if self.__loadModule( module_name ):
					loaded += 1
		self.info( "Loaded %d additional modules" % loaded )

	def __loadModule( self, module_name, ctx=None ):
		"""Load a specific module."""
		try:
			self.debug( 2, "Loading module '%s'" % module_name )
			module = __import__( module_name )

		except StandardError, detail:
			msg = "Failed to load module '%s' ( %s )\n" % ( module_name, detail )
			self.error( msg, True )
			if ctx is not None:
				ctx.write( msg )
			return 0

		# check we are a high enough version
		if module.__required_modules__[__name__] > __version__:
			msg = "Module '%s' v%s requires ModManager v%s or higher\n" % ( module_name, module.__version__, module.__required_modules__[__name__] )
			self.error( msg )
			if ctx is not None:
				ctx.write( msg )
			return 0

		# Check we are a supported game
		if hasattr( module, '__supported_games__' ):
			if not module.__supported_games__[self.__gameId]:
				msg = "Module '%s' v%s does not support '%s'\n" % ( module_name, module.__version__, self.__gameId )
				self.error( msg )
				if ctx is not None:
					ctx.write( msg )
				return 0
		else:
			if self.isBattleField2():
				msg = "Legacy module '%s' v%s detected assuming '%s' support" % ( module_name, module.__version__, self.__bf2String )
				self.warn( msg )
				if ctx is not None:
					ctx.write( msg )

			else:
				msg = "Legacy module '%s' v%s detected assuming NO '%s' support" % ( module_name, module.__version__, self.__bf2142String )
				self.error( msg )
				if ctx is not None:
					ctx.write( msg )
				return 0

		# ensure we have all dependent modules
		# NOTE: we dont check for infinte loops here
		for req_module_name in module.__required_modules__:
			if __name__ == req_module_name:
				continue
			self.debug( 2, "%s requires %s (autoloading)" % ( module_name, req_module_name ) )
			if not self.__modules.has_key( req_module_name ):
				# module we dont know about yet
				self.__addModule( req_module_name )
				if not self.__loadModule( req_module_name ):
					return 0

			if ModuleStatus.loaded > self.__modules[req_module_name]['status']:
				# we know the module but its not loaded yet
				if not self.__loadModule( req_module_name ):
					return 0
			
			if module.__required_modules__[req_module_name] > self.__modules[req_module_name]['module'].__version__:
				# module version is too low
				msg = "Module '%s' v%s requires '%s' v%s or higher (found %s)\n" % ( module_name, module.__version__, req_module_name, module.__required_modules__[req_module_name], self.__modules[req_module_name]['module'].__version__ )
				self.error( msg )
				if ctx is not None:
					ctx.write( msg )
				return 0				

		try:
			obj = module.mm_load( self )
			self.__modules[module_name]['object'] = obj
		except:
			msg = "Failed to mm_load '%s'\n" % module_name
			self.error( msg, True )
			if ctx is not None:
				ctx.write( msg )
			return 0

		# all good
		self.__modules[module_name]['module'] = module
		self.__modules[module_name]['status'] = ModuleStatus.loaded
		msg = "Module '%s' v%s loaded\n" % ( module_name, module.__version__ )
		self.info( msg )
		if ctx is not None:
			ctx.write( msg )

		return obj

	def __unloadModule( self, module_name ):
		"""Unload a specific module."""
		try:
			module = self.__modules[module_name]['module']
			try:
				self.__modules[module_name]['status'] = ModuleStatus.unloaded
				self.__modules[module_name]['module'] = None
				del module
				self.error( "Module '%s' was unloaded loaded" % module_name )

			except StandardError, detail:
				self.error( "Module '%s' failed to unload (%s)" % ( module_name, detail ) )

		except KeyError:
			self.error( "Module '%s' was not loaded" % module_name )

	def __initModule( self, module_name, ctx=None ):
		"""Initialise a module."""
		if self.__modules[module_name]['status'] == ModuleStatus.loaded:
			try:
				self.__modules[module_name]['object'].init()
				self.__modules[module_name]['status'] = ModuleStatus.running
				msg = "Module '%s' initialised\n" % module_name
				self.info( msg )
				if ctx is not None:
					ctx.write( msg )
				return 1

			except Exception, detail:
				# Ignore this module doesnt support init
				msg = "Failed to initialise module '%s' (%s)" % ( module_name, detail )
				self.error( msg, True )
				if ctx is not None:
					ctx.write( msg )

		return 0

	def __shutdownModule( self, module_name, ctx=None ):
		"""Shutdown a module."""
		if self.__modules[module_name]['status'] == ModuleStatus.running:
			try:
				self.__modules[module_name]['object'].shutdown()
				self.__modules[module_name]['status'] = ModuleStatus.loaded
				msg = "Module '%s' shutdown\n" % module_name
				self.info( msg )
				if ctx is not None:
					ctx.write( msg )
				return 1

			except Exception, detail:
				msg = "Failed to shutdown module '%s' (%s)\n" % ( module_name, detail )
				self.error( msg, True )
				if ctx is not None:
					ctx.write( msg )

		elif self.__modules[module_name]['status'] == ModuleStatus.loaded:
			msg = "Module '%s' already shutdown\n" % ( module_name )
			self.debug( 2, msg )
			if ctx is not None:
				ctx.write( msg )
			return 1;

		return 0

	def __decodeConfigValue( self, key, value ):
		"""Converts a config value from string to int if required."""
		if value is None:
			return None

		# remove white space
		if value.startswith( '"' ):
			# String value
			# remove outer quotes
			value = value.strip( '"' )
			self.debug( 1, "Setting '%s' = '%s'" % ( key, value ) )
		else:
			# Int value
			try:
				value = int( value )
				self.debug( 1, "Setting '%s' = %d" % ( key, value ) )
			except:
				self.warn( "Invalid config for '%s' ( Unquoted string? )" )

		return value

	def __parseConfig( self ):
		"""Parse the configuration file."""
		self.info( "Loading config '%s'" % ( self.__configFile ) )

		add_re = re.compile( '^add([A-Z].*)$' )
		set_re = re.compile( '^set([A-Z].*)$' )

		try:
			config = open( self.__configFile, 'r' )
			lineNo = 0
			for line in config:
				lineNo += 1
				line = line.strip()
				if 0 != len( line ) and not line.startswith( "#" ):
					try:
						( key, val1, val2 ) = mm_utils.largs( line, ' ', 3, None, True )
						val1 = self.__decodeConfigValue( key, val1 )
						val2 = self.__decodeConfigValue( key, val2 )

						try:
							oldVal = self.__getattr__( key )
							self.warn( "Overriding %s = '%s' with '%s'" % ( key, oldVal, val1 ) )
						except KeyError:
							# ignore
							pass

						# load to the relavent place
						( module, module_key ) = mm_utils.lsplit( key, '.', 2 )
						#self.debug( 2, "%s . %s = %s" % ( module, module_key, value ) )
						if __name__ == module:
							if "loadModule" == module_key:
								# loadable module
								self.__addModule( val1 )

							else:
								# core config file
								self.__setattr__( module_key, val1 )
								self.__setParam( module, module_key, val1 )
						else:
							match = add_re.search( module_key )
							if match is not None:
								# user multi setting
								# matches things like:
								# <module>.addProfileId 1
								# <module>.addProfileId 2
								# and sets:
								# <module>.profileIds = [ 1, 2 ]
								# or:
								# <module>.addCmdAlias "k" "kick"
								# <module>.addCmdAlias "b" "ban"
								# and sets:
								# <module>.cmdAliass = { 'k': 'kick', 'b': 'ban' }
								self.__addParam( module, "%c%ss" % ( module_key[3:4].lower(), module_key[4:] ), val1, val2 )

							else:
								# user single setting
								self.__setParam( module, module_key, val1 )

					except Exception, detail:
						self.error( 'Syntax error in "%s" on line %d (%s)' % ( self.__configFile, lineNo, detail ), True )
			config.close()
		except IOError, detail:
			self.error( "Couldn't read '%s' (%s)" % ( self.__configFile, detail ) )

	def __log( self, level, msg ):
		"""Log the message if its level is less than or equal to the current log level."""
		if self.logLevel >= level:
			currentDate = datetime.datetime.today()
			dateString = time.strftime( self.logDateFormat, currentDate.timetuple() )
			output = ''
			cr = '\n'
			if msg.endswith( '\n' ):
				cr = ''
			if 0 == level:
				output = "%sError: %s%s" % ( dateString, msg, cr )
				sys.stderr.write( output )

			elif 1 == level:
				output = "%sWarn: %s%s" % ( dateString, msg, cr )
				sys.stderr.write( output )

			elif 2 == level:
				output = "%sInfo: %s%s" % ( dateString, msg, cr )
				sys.stdout.write( output )

			else:
				output = "%sDebug[%s]: %s%s" % ( dateString, level, msg, cr )
				sys.stdout.write( output )

			if self.__logger:
				self.__logger.write( output )

	def __setParam( self, module, var, val ):
		"""Set the modules configuration parameter."""
		if self.__configFull.has_key( module ):
			self.__configFull[module][var] = val
		else:
			self.__configFull[module] = { var: val }

		if __name__ == module:
			self.__setattr__( var, val )

	def __removeParam( self, module, key, idx ):
		"""Remove the modules configuration parameter."""
		if not self.__configFull.has_key( module ):
			self.warn( "Failed to remove parameter %s.%s[%d] ( unknown module )" % ( module, key, idx ) )
			return 0

		if not self.__configFull[module].has_key( key ):
			self.warn( "Failed to remove parameter %s.%s[%d] ( unknown key )" % ( module, key, idx ) )
			return 0

		l = len( self.__configFull[module][key] )
		if l <= idx:
			self.warn( "Failed to remove parameter %s.%s[%d] > %d ( invalid index )" % ( module, key, idx, l ) )
			return 0

		del self.__configFull[module][key][idx]
		return 1

	def __addParam( self, module, key, val1, val2=None ):
		"""Add the modules configuration parameter."""
		#self.debug( 2, "ADD2: %s.%s = %s, %s" % ( module, key, val1, val2 ) )

		if val2 is None:
			#self.debug( 2, "LIST2: %s.%s = %s" % ( module, key, val1 ) )
			# Straight value
			if self.__configFull.has_key( module ):
				if self.__configFull[module].has_key( key ):
					self.__configFull[module][key].append( val1 )
				else:
					self.__configFull[module][key] = [ val1 ]
			else:
				module_keys = { key: [ val1 ] }
				self.__configFull[module] = module_keys
		else:
			#self.debug( 2, "DICT2: %s.%s = %s, %s" % ( module, key, val1, val2 ) )
			# value pair
			try:
				val2 = int( val2 )
				#self.debug( 2, "INT: %d" % ( val2 ) )
			except:
				pass
			#self.debug( 2, "HASH2: %s %s" % ( val1, val2 ) )
			if self.__configFull.has_key( module ):
				if self.__configFull[module].has_key( key ):
					self.__configFull[module][key][val1] = val2
				else:
					self.__configFull[module][key] = { val1: val2 }
			else:
				self.__configFull[module] = { key: { val1: val2 } }

	def __getParam( self, module, key ):
		"""Return the modules configuration parameter."""
		try:
			return self.__configFull[module][key];
		except KeyError:
			self.warn( "Request for invalid param '%s.%s'" % ( module, key ) )

	def __getModuleConfig( self, module ):
		"""Return the modules configuration."""
		if self.__configFull.has_key( module ):
			return self.__configFull[module]
		else:
			return {}

	def __saveConfig( self, ctx=None ):
		"""Save the entire config.

		Note: return value 0 indicates success
		"""
		try:
			fh = open( self.__configFile, 'w' )
		except IOError, detail:
			msg = "Failed to open config '%s' for write (%s)\n" % ( self.__configFile, detail )
			self.error( msg )
			if ctx is not None:
				ctx.write( msg )
			return 0

		if not self.__writeConfig( fh ):
			msg = "Failed to save config\n"
		else:
			msg = "Config saved\n"

		self.info( msg )
		if ctx is not None:
			ctx.write( msg )

		fh.close()

		return 0

	def __writeConfig( self, fh ):
		"""Write the module config to the file handle."""
		try:
			# Global first
			self.__writeModuleConfig( fh, __name__ )

			# Addon modules
			fh.write( "\n# Modules\n" )
			for module_name in self.__modules:
				if module_name != self.logModule and module_name != self.rconModule and module_name != self.banManagerModule:
					fh.write( '%s.loadModule "%s"\n' % ( __name__, module_name ) )
			fh.write( "\n" )

			# Now all the known modules configs
			modules = self.__configFull.keys()
			modules.sort()
			for module in modules:
				if __name__ != module:
					self.__writeModuleConfig( fh, module )

		except IOError, detail:
			msg = "Failed to save config '%s' (%s)\n" % ( self.__configFile, detail )
			self.error( msg )
			if ctx is not None:
				ctx.write( msg )
			return 0

		return 1

	def __writeModuleConfig( self, fh, module_name ):
		"""Write out the named modules header and config to the passed file handle."""

		# Write the descriptive header
		if self.__modules.has_key( module_name ):
			# module is loaded
			if self.__modules[module_name]['status'] > ModuleStatus.unloaded:
				# modules loaded use the description
				try:
					fh.write( "#\n# %s\n#\n" % self.__modules[module_name]['module'].__description__ )
				except:
					fh.write( "#\n# %s\n#\n" % module_name )
			else:
				fh.write( "#\n# %s\n#\n" % module_name )
		elif __name__ == module_name:
			# Us
			fh.write( "#\n# %s\n#\n" % __description__ )
		else:
			# Unloaded module
			fh.write( "#\n# %s\n#\n" % module_name )

		# Now the parameters for this module
		params = self.__configFull[module_name]
		var_names = params.keys()
		var_names.sort()
		for param in var_names:
			value = params[param]
			if isinstance( value, ( int, long ) ):
				# just an int
				fh.write( '%s.%s %s\n' % ( module_name, param, value ) )

			elif isinstance( value, dict ):
				# multi value list
				if param.endswith( 's' ):
					# strip the s
					multi_param = "add%s%s" % ( param[0:1].upper(), param[1:len( param ) - 1] )
				else:
					multi_param = "add%s%s" % ( param[0:1].upper(), param[1:] )

				for k in value:
					val = value[k]
					if isinstance( k, ( int, long ) ):
						if isinstance( val, ( int, long ) ):
							fh.write( '%s.%s %d %d\n' % ( module_name, multi_param, k, val ) )
						else:
							fh.write( '%s.%s %d "%s"\n' % ( module_name, multi_param, k, val ) )
					else:
						# string, double quote it
						if isinstance( val, ( int, long ) ):
							fh.write( '%s.%s "%s" %d\n' % ( module_name, multi_param, k, val ) )
						else:
							fh.write( '%s.%s "%s" "%s"\n' % ( module_name, multi_param, k, val ) )

			elif isinstance( value, list ):
				# multi value list
				if param.endswith( 's' ):
					# strip the s
					multi_param = "add%s%s" % ( param[0:1].upper(), param[1:len( param ) - 1] )
				else:
					multi_param = "add%s%s" % ( param[0:1].upper(), param[1:] )

				for multi in value:
					if isinstance( multi, ( int, long ) ):
						# just an int
						fh.write( '%s.%s %s\n' % ( module_name, multi_param, multi ) )
					else:
						# string, double quote it
						fh.write( '%s.%s "%s"\n' % ( module_name, multi_param, multi ) )
			else:
				# string, double quote it
				fh.write( '%s.%s "%s"\n' % ( module_name, param, value ) )

		fh.write( "\n" )

	#
	# Rcon methods
	#
	def cmdExec( self, ctx, cmd ):
		"""Execute a ModManager sub command."""
		return mm_utils.exec_subcmd( self, self.__cmds, ctx, cmd )

	def cmdReloadModule( self, ctx, module_name ):
		"""Reload and existing module."""
		if self.rconModule == module_name or self.logModule == module_name or self.banManagerModule == module_name:
			msg = "Failed to shutdown module '%s' ( not permitted )\n" % module_name
			self.warn( msg )
			ctx.write( msg )
			return 0

		if not self.__modules.has_key( module_name ):
			msg = "Failed to reload module '%s' ( module not loaded )\n" % module_name
			self.warn( msg )
			ctx.write( msg )
			return 0

		details = self.__modules[module_name]

		# check if the initial load failed
		if details['status'] == ModuleStatus.unloaded:
			# Initial load failed just try to load
			if not self.__loadModule( module_name, ctx ):
				return 0
			return 1

		module = details['module']
		if not module.__dict__.has_key( '__supports_reload__' ) or not module.__supports_reload__:
			msg = "Failed to reload module '%s' ( reload not supported )\n" % module_name
			self.warn( msg )
			ctx.write( msg )
			return 0

		# module supports reload

		# call shutdown on the existing copy
		if not self.__shutdownModule( module_name, ctx ):
			return 0

		try:
			module = reload( module )
			self.__modules[module_name]['module'] = module
			self.__modules[module_name]['status'] = ModuleStatus.loaded
		except Exception, detail:
			msg = "Failed to reload module '%s' (%s)\n" % ( module_name, detail )
			self.error( msg, True)
			ctx.write( msg )
			return 0

		try:
			self.__modules[module_name]['object'] = module.mm_load( self )
		except:
			msg = "Failed to mm_load '%s'\n" % module_name
			self.error( msg, True )
			if ctx is not None:
				ctx.write( msg )
			return 0

		msg = "Module '%s' reloaded\n" % module_name
		self.info( msg )
		ctx.write( msg )

		# Version compatibility check
		if module.__required_modules__['modmanager'] > __version__:
			msg = "Module '%s' v%s requires ModManager v%s or higher\n" % ( module_name, module.__version__, module.__required_modules__['modmanager'] )
			self.error( msg )
			ctx.write( msg )
			return 0

		# Initialise the module
		if not self.__initModule( module_name, ctx ):
			return 0

		return 1;

	def cmdSetParam( self, ctx, cmd ):
		"""Sets a module parameter."""
		parts = cmd.split( None, 2 )
		if 3 != len( parts ):
			msg = "Invalid set arguments '%s'" % cmd
			self.warn( msg )
			ctx.write( msg )

		( module_name, var, val ) = parts

		if not self.__configFull.has_key( module_name ):
			msg = "Failed to set param '%s' ( invalid module )\n" % cmd
			self.warn( msg )
			ctx.write( msg )
			return 0

		if not self.__configFull[module_name].has_key( var ):
			msg = "Failed to set param '%s' ( invalid param )\n" % cmd
			self.warn( msg )
			ctx.write( msg )
			return 0

		if self.rconModule == module_name:
			if "restrictedGametypes" == var or "lockedSettings" == var:
				msg = "Failed to set param '%s' ( restricted / locked param )\n" % cmd
				self.warn( msg )
				ctx.write( msg )
				return 0
			
		if not val.startswith( '"' ):
			try:
				int_val = int( val )
			except TypeError:
				msg = "Failed to set param '%s' ( invalid var, expected quote string or integer value )\n" % cmd
				self.warn( msg )
				ctx.write( msg )
				return 0
			self.__configFull[module_name][var] = int_val
		else:
			self.__configFull[module_name][var] = val.strip( '"' )

		msg = "Param %s.%s set to %s\n" % ( module_name, var, val )
		self.info( msg )
		ctx.write( msg )
		return 1

	def cmdLoadModule( self, ctx, module_name ):
		"""Load a new module."""
		if self.__modules.has_key( module_name ):
			msg = "Failed to load module '%s' ( already loaded )\n" % module_name
			self.warn( msg )
			ctx.write( msg )
			return 0

		self.__addModule( module_name )

		if not self.__loadModule( module_name, ctx ):
			# Remove all reference
			del self.__modules[module_name]
			return 0

		if not self.__initModule( module_name, ctx ):
			return 0

		return 1;

	def cmdStartModule( self, ctx, module_name ):
		"""Start and existing module."""
		if not self.__modules.has_key( module_name ):
			msg = "Failed to shutdown module '%s' ( not loaded )\n" % module_name
			self.warn( msg )
			ctx.write( msg )
			return 0

		return self.__initModule( module_name, ctx )

	def cmdShutdownModule( self, ctx, module_name ):
		"""Shutdown and existing module."""
		if self.rconModule == module_name or self.logModule == module_name or self.banManagerModule == module_name:
			msg = "Failed to shutdown module '%s' ( not permitted )\n" % module_name
			self.warn( msg )
			ctx.write( msg )
			return 0

		if not self.__modules.has_key( module_name ):
			msg = "Failed to shutdown module '%s' ( not loaded )\n" % module_name
			self.warn( msg )
			ctx.write( msg )
			return 0

		return self.__shutdownModule( module_name, ctx )

	def cmdListModules( self, ctx, cmd ):
		"""List the loaded modules."""
		# would be nice to be able to list the available modules
		# but the python core is crippled
		ctx.write( 'Loaded modules:\n' )
		for module_name in self.__modules:
			details = self.__modules[module_name]
			status = details['status']
			if ModuleStatus.unloaded == status:
				ctx.write( ' %s ( unloaded )\n' % module_name )
			elif ModuleStatus.loaded == status:
				ctx.write( ' %s v%s ( loaded )\n' % ( module_name, details['module'].__version__ ) )
			elif ModuleStatus.running == status:
				ctx.write( ' %s v%s ( running )\n' % ( module_name, details['module'].__version__ ) )

		return 1

	def cmdSaveConfig( self, ctx, cmd ):
		"""Start and existing module."""
		return self.__saveConfig( ctx )

	def cmdPrintRunningConfig( self, ctx, cmd ):
		"""Write the config to ctx."""
		return self.__writeConfig( ctx )
	#
	# Config methods
	#

	def configFile( self ):
		"""Return the config filename."""
		return self.__configFile

	def getModuleConfig( self, moduleDefaults={} ):
		"""Return the modules configuration, adding any missing default values."""
		module = mm_utils.caller_module()
		moduleConfig = self.__getModuleConfig( module )
		for key in moduleDefaults:
			if not moduleConfig.has_key( key ):
				# missing default add it to the config
				self.debug( 1, "missing %s" % key )
				if isinstance( moduleDefaults[key], dict ):
					self.debug( 1, "DICT1: %s => %s" % ( module, key ) )
					if moduleDefaults[key]:
						vals = moduleDefaults[key]
						for k in vals.keys():
							self.__addParam( module, key, k, vals[k] )
					else:
						# fake the empty dict
						self.__setParam( module, key, {} )

				elif isinstance( moduleDefaults[key], list ):
					self.debug( 1, "LIST1: %s => %s" % ( module, key ) )
					# multi val
					if moduleDefaults[key]:
						for val in moduleDefaults[key]:
							self.__addParam( module, key, val )
					else:
						# fake the empty list
						self.__setParam( module, key, [] )
				else:
					# single val
					self.__setParam( module, key, moduleDefaults[key] )

		# reget to ensure we have all the defaults
		return self.__getModuleConfig( module )

	def setParam( self, key, value ):
		"""Set the calling modules parameter."""
		return self.__setParam( mm_utils.caller_module(), key, value )

	def addParam( self, key, val1, val2=None ):
		"""Add a value to the the calling modules parameters."""
		return self.__addParam( mm_utils.caller_module(), key, val1, val2 )

	def removeParam( self, key, idx ):
		"""Remove one of the calling modules parameter values."""
		return self.__removeParam( mm_utils.caller_module(), key, idx )

	def getParam( self, key ):
		"""Return the calling modules parameter."""
		return self.__getParam( mm_utils.caller_module(), key )

	def setRconParam( self, key, value ):
		"""Set the rcon modules parameter."""
		return self.__getParam( self.rconModule, value )

	def getRconParam( self, key ):
		"""Return the rcon modules parameter."""
		return self.__getParam( self.rconModule )

	def saveConfig( self ):
		"""Save the current ModManager configuration."""
		return self.__saveConfig()

	#
	# Logging methods
	#

	def debug( self, level, msg ):
		"""Log the message at the given debug level."""
		self.__log( 2 + level, msg )

	def info( self, msg ):
		"""Log the message at the info level."""
		self.__log( 2, msg )

	def warn( self, msg ):
		"""Log the message at the warn level."""
		self.__log( 1, msg )

	def error( self, msg, traceback=False ):
		"""Log the message at the error level."""
		self.__log( 0, msg )
		if traceback:
			self.__log( 0, self.exceptionString() )

	def exceptionString( self ):
		"""Returns a formatted string of the exception."""
		return "".join( mm_utils.format_exception( *sys.exc_info() ) )

	#
	# Rcon methods
	#

	def runRconCommand( self, client, cmd ):
		"""Run an rcon command."""
		return self.__rcon.onRemoteCommand( client, cmd )

	def getRconContext( self, clientid ):
		"""Run an rcon command."""
		return self.__rcon.getContext( clientid )

	def registerRconCmdHandler( self, name, details ):
		"""Register a new rcon function hander."""
		return self.__rcon.registerCmdHandler( name, details )

	def unregisterRconCmdHandler( self, name ):
		"""Unregister an existing rcon function handler."""
		return self.__rcon.unregisterCmdHandler( name )

	def registerRconConnectHandler( self, func ):
		"""Register a new rcon connect hander."""
		return self.__rcon.registerConnectHandler( func )

	def unregisterRconConnectHandler( self, func ):
		"""Unregister an existing rcon connect handler."""
		return self.__rcon.unregisterConnectHandler( func )

	def registerRconDisconnectHandler( self, func ):
		"""Register a new rcon disconnect hander."""
		return self.__rcon.registerDisconnectHandler( func )

	def unregisterRconDisconnectHandler( self, func ):
		"""Unregister an existing rcon disconnect handler."""
		return self.__rcon.unregisterDisconnectHandler( func )

	def registerRconAuthHandler( self, auth_func, check_func ):
		"""Register a new rcon auth hander."""
		return self.__rcon.registerAuthHandler( auth_func, check_func )

	def unregisterRconAuthHandler( self, func ):
		"""Unregister an existing rcon auth handler."""
		return self.__rcon.unregisterAuthHandler( func )

	def registerRconAuthedHandler( self, func ):
		"""Register a new rcon authed hander."""
		return self.__rcon.registerAuthedHandler( func )

	def unregisterRconAuthedHandler( self, func ):
		"""Unregister an existing rcon auth handler."""
		return self.__rcon.unregisterAuthedHandler( func )

	def rcon( self ):
		"""Return the rcon handle."""
		return self.__rcon

	#
	# Ban Manager methods
	#

	def banManager( self ):
		"""Return the ban manager handle."""
		return self.__banManager

	#
	# Update methods
	#

	def registerUpdates( self, method ):
		"""Requests updates."""
		self.__updateRequestors.append( method )

	def unregisterUpdates( self, method ):
		"""Cancel request for updates."""
		self.__updateRequestors.remove( method )

	#
	# Core game methods
	#

	def init( self ):
		"""Initialise the module manager and all loaded modules."""
		self.__state = 1

		# Register our handers
		self.registerRconCmdHandler( 'mm', { 'method': self.cmdExec, 'subcmds': self.__cmds } )

		initialised = 0
		for module_name in self.__modules:
			initialised += self.__initModule( module_name )
		self.info( "Initialised %d modules" % initialised )

	def shutdown( self ):
		"""Shutdown the Module manager and all modules."""
		self.info( 'ModManager shutting down' )

		# Save the config if required
		if self.autoSave:
			self.__saveConfig()

		shutdown = 0
		for module_name in self.__modules:
			shutdown += self.__shutdownModule( module_name )
		self.info( "%d modules shutdown" % shutdown )

		host.unregisterGameStatusHandler( self.onGameStatusChanged )

	def update( self ):
		"""Update all the modules that have registered for updates.

		Note / Warning:
		We could use the same method as for shutdown and init but
		due to the frequency of update calls we use this optimised
		methodology.
		"""
		for method in self.__updateRequestors:
			try:
				method()
			except StandardError, detail:
				self.error( "Failed to update '%s' (%s)" % ( mm_utils.method_name( method ), detail ), True )

# Create the singleton manger
# TODO: enforce singleton status
debuglog = None
if configDefaults['debugEnable']:
	debuglog = sys.stdout = sys.stderr = DebugLogger( configDefaults['debugFile'], configDefaults['logAppend'], configDefaults['logAutoFlush'] )
	
modManager = ModManager( debuglog );

def getInstance():
	"""Return the module manager instance."""
	return modManager

# These functions are called from the engine -- we implement them in terms of a
# class instance:

def init():
	"""Call initialise on the module manager."""
	modManager.init();

def shutdown():
	"""Call shutdown on the module manager."""
	modManager.shutdown()

def update():
	"""Call update on the module manager."""
	modManager.update()
