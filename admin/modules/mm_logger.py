# vim: ts=4 sw=4 noexpandtab
"""File based Logger.

This is a basic logger which writes to a file.

===== Config =====
 # The file name to log to
 mm_logger.logFilename "modmanager.log"
 
 # Auto flush, writes info to disk instantly instead of buffering if 1
 mm_logger.logAutoFlush 1

 # Append to the log if it already exists if set to 1
 mm_logger.logAppend 1

===== History =====
 v1.5 - 12/10/2011:
 Added BFP4F Support

 v1.4 - 29/09/2006:
 Fixed shutdown issue printing to closed file
 
 v1.3 - 30/08/2006:
 Added supported games

 v1.2 - 02/08/2005:
 Added logAppend default 0 to try to keep log sizes under control
 
 v1.1 - 27/07/2005:
 Updated documentation
 
 v1.0 - 30/06/2005:
 Initial version

Copyright (c)2008 Multiplay
Author: Steven 'Killing' Hartland
"""

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

__description__ = "ModManager Logger v%s" % __version__

__all__ = [
	"write",
]

configDefaults = {
	# The log file to use
	'logFilename': 'modmanager.log',
	'logAutoFlush': 1,
	'logAppend': 0,
}

class defaultLogger:
	def __init__( self, modManager ):
		self.mm = modManager
		self.__file = None

	def init( self ):
		"""Get config and setup log file."""
		self.__config = self.mm.getModuleConfig( configDefaults )
		self.__autoFlush = self.__config['logAutoFlush']

		try:
			if self.__config['logAppend']:
				self.__file = open( self.__config['logFilename'], 'a+' )				
			else:
				self.__file = open( self.__config['logFilename'], 'w+' )

		except RuntimeError, detail:
			msg = "Failed to open '%s' (%s)" % ( self.__config['logFilename'], detail )
			raise IOError, msg

	def write( self, str ):
		"""Write the message to the log file, flushing if needed."""
		if self.__file:
			self.__file.write( str )
			if self.__autoFlush:
				self.__file.flush()

	def close( self ):
		"""Close the log file."""
		if self.__file:
			ret = self.__file.close()
			self.__file = None
			return ret
		return 1

	def shutdown( self ):
		"""Shutdown."""
		return self.close()

def mm_load( modManager ):
	return defaultLogger( modManager )
