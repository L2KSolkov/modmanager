# vim: ts=4 sw=4 noexpandtab
"""Auto announcer system.

This is an Auto Announcer ModManager module

===== Config =====
 # Add a join message
 # Join messages can include the special string %player% which will be replaced with the joining players name
 mm_announcer.addJoinMessage "<message>"
 
 # Add a timed message
 mm_announcer.addTimedMessage "<start>:<repeat>:<message>"

===== Rcon commands =====
 # List the current announcements
 announcer list
 
 # Add a timed message
 announcer addTimed <start> <repeat> "<message>"
 
 # Remove a timed message
 announcer removeTimed <announceid>
 
 # Remove all timed messages
 announcer clearTimed
 
 # Add a join message
 announcer addJoin "<message>"
 
 # Remove a join message
 announcer removeJoin <announceid>
 
 # Remove all join messages
 announcer clearJoin

===== Notes =====
* Join messages currently go to everyone due to a python API bug
* The '|' character in messages to represents a new line.

===== History =====
 v1.8 - 12/10/2011:
 Added BFP4F Support

 v1.7 - 13/01/2009:
 New line '|' splits ignore patterns which are immediately preceded by the pattern: '§\d+'

 v1.6 - 22/09/2006:
 Added the ability to put the players name in join messages using the special string: %player%

 v1.5 - 30/08/2006:
 Added supported games

 v1.4 - 15/08/2005:
 Corrected Rcon commands docs
 Updated line split '|' to work consistently across join and timed messages

 v1.3 - 12/08/2005:
 Fixed module shutdown error
 
 v1.2 - 01/08/2005:
 Corrected list output
 Added default timed message
  
 v1.1 - 27/07/2005:
 Added new line support and updated documentation
 
 v1.0 - 30/06/2005:
 Initial version

Copyright (c)2008 Multiplay
Author: Steven 'Killing' Hartland
"""

import re
import bf2
import host
import mm_utils

__version__ = 1.8

__required_modules__ = {
	'modmanager': 1.6
}

__supported_games__ = {
	'bf2': True,
	'bf2142': True,
	'bfheroes': True,
	'bfp4f': True
}

__supports_reload__ = True

__description__ = "ModManager Announcer v%s" % __version__

configDefaults = {
	'joinMessages': [ 'Welcome to a ModManager enabled server!' ],
	'timedMessages': []
}

class Announcer( object ):
	def __init__( self, modManager ):
		self.mm = modManager
		self.__state = 0

		# Our internal commands
		self.__cmds = {
			# Global methods
			'list': { 'method': self.cmdList, 'level': 10 },

			# Timed methods
			'addTimed': { 'method': self.cmdAddTimed, 'args': '<start> <repeat> "<message>"', 'level': 30 },
			'removeTimed': { 'method': self.cmdRemoveTimed, 'args': '<announceid>', 'level': 30 },
			'clearTimed': { 'method': self.cmdClearTimed, 'level': 30 },

			# Join methods
			'addJoin': { 'method': self.cmdAddJoin, 'args': '"<message>"', 'level': 30 },
			'removeJoin': { 'method': self.cmdRemoveJoin, 'args': '<announceid>', 'level': 30 },
			'clearJoin': { 'method': self.cmdClearJoin, 'level': 30 }
		}

	def escape_codes( self, txt ):
		"""Escape codes."""
		return re.sub( '§(?P<num>\d+)\|', '§\g<num>#=#=', txt )

	def unescape_codes( self, txt ):
		"""Escape codes."""
		return re.sub( '§(?P<num>\d+)#=#=', '§\g<num>|', txt )

	def announce( self, details ):
		"""Announce the message to the server."""
		self.mm.debug( 2, "Announcer: '%s'" % details['text'] )

		#  Escape color / size codes
		try:
			for line in self.escape_codes( details['text'] ).split( '|' ):
				mm_utils.msg_server( self.unescape_codes( line ) )
		except:
			self.mm.error( "Aaaaa '%s'" % details['text'], True )

		return 1

	def cmdExec( self, ctx, cmd ):
		"""Execute a Announcer sub command."""
		return mm_utils.exec_subcmd( self.mm, self.__cmds, ctx, cmd )

	def cmdList( self, ctx, cmd ):
		"""List the current announcements."""

		idx = 0
		if self.__joinMessages:
			ctx.write( 'Join messages:\n' )
			for msg in self.__joinMessages:
				ctx.write( "#%d: %s\n" % ( idx, msg ) )
				idx += 1
			ctx.write( '\n' )
		else:
			ctx.write( 'No join messages\n' )

		if self.__timedMessages:
			ctx.write( 'Timed messages:\n' )
			idx = 0
			for details in self.__timedMessages:
				ctx.write( "#%d: Start:%d, Repeat:%d, Text: %s\n" % ( idx, details['start'], details['repeat'], details['text'] ) )
				idx += 1
		else:
			ctx.write( 'No timed messages\n' )

		return 1

	#
	# Timed message methods
	#

	def cmdAddTimed( self, ctx, cmd ):
		"""Add a timed message."""
		try:
			( start, repeat, text ) = cmd.split( None, 2 )
			text = text.strip( '"' )
			self.__addTimedMsg( int( start ), int( repeat ), text )
		except:
			self.mm.error( "Invalid timed message '%s'" % cmd, True )
			ctx.write( "Invalid timed message '%s'\n" % cmd )
			return 0

		self.mm.addParam( 'timedMessages', "%s:%s:%s" % ( start, repeat, text ) )

		ctx.write( "Timed message added\n" )

		return 1

	def __addTimedMsg( self, start, repeat, text ):
		"""Create a timed message."""
		details = {
			'start': start,
			'repeat': repeat,
			'text': text
		}
		timer = bf2.Timer( self.announce, start, 1, details )
		if repeat:
			timer.setRecurring( repeat )
		details['timer'] = timer

		self.__timedMessages.append( details )
		return details

	def cmdRemoveTimed( self, ctx, cmd ):
		"""Remove a timed message."""
		try:
			messageid = int( cmd )
		except TypeError:
			self.mm.error( "Invalid timed message '%s' (bad messageid)" % cmd, True )
			ctx.write( "Invalid timed message '%s' (bad messageid)" % cmd )
			return 0

		if len( self.__timedMessages ) <= messageid:
			self.mm.error("Invalid timed message '%s' (invalid messageid)" % cmd, True )
			ctx.write( "Invalid timed message '%s' (invalid messageid)" % cmd )
			return 0

		details = self.__timedMessages[messageid]
		details['timer'].destroy()
		details['timer'] = None
		del self.__timedMessages[messageid]

		self.mm.removeParam( 'timedMessages', messageid )

		ctx.write( "Timed message removed\n" )

		return 1

	def cmdClearTimed( self, ctx, cmd ):
		"""Removes all timed messages."""
		for details in self.__timedMessages:
			details['timer'].destroy()
			details['timer'] = None

		self.__timedMessages = []

		self.mm.setParam( 'timedMessages', [] )

		ctx.write( "All timed messages removed\n" )

		return 1

	#
	# Join message methods
	#

	def cmdAddJoin( self, ctx, cmd ):
		"""Add a timed message."""
		msg = cmd.strip( '"' )
		self.__joinMessages.append( msg )
		ctx.write( "Join message added\n" )
		self.mm.addParam( 'joinMessages', msg )

		# tell the existing players
		for player in bf2.playerManager.getPlayers():
			self.onPlayerConnect( player )

		return 1

	def cmdRemoveJoin( self, ctx, cmd ):
		"""Add a timed message."""
		try:
			messageid = int( cmd )
		except TypeError:
			self.mm.error( 2, "Invalid join message '%s' (bad messageid)" % cmd, True )
			ctx.write( "Invalid join message '%s' (bad messageid)\n" % cmd )
			return 0

		if len( self.__joinMessages ) <= messageid:
			self.mm.error( 2, "Invalid join message '%s' (invalid messageid)" % cmd, True )
			ctx.write( "Invalid join message '%s' (invalid messageid)\n" % cmd )
			return 0

		del self.__joinMessages[messageid]
		self.mm.removeParam( 'joinMessages', messageid )
		ctx.write( "Join message removed\n" )

		return 1

	def cmdClearJoin( self, ctx, cmd ):
		"""Removes all timed messages."""
		self.__joinMessages = []
		self.mm.setParam( 'joinMessages', [] )

		ctx.write( "All join messages removed\n" )

		return 1

	#
	# Event handlers
	#
	def onPlayerConnect( self, player ):
		"""Make a note of the connected player."""
		if 1 != self.__state:
			return 0

		self.__newPlayers[player.index] = player

	def onPlayerDisconnect( self, player ):
		"""Remove our reference to the connected player."""
		if 1 != self.__state:
			return 0

		if self.__newPlayers.has_key( player.index ):
			del self.__newPlayers[player.index]

	def onPlayerSpawn( self, player, soldier ):
		"""Announce to new spawning players."""
		if 1 != self.__state:
			return 0

		if self.__newPlayers.has_key( player.index ):
			# First spawn for this player, send message
			for msg in self.__joinMessages:
				for line in self.escape_codes( msg ).split( '|' ):
					line = self.unescape_codes( line.replace( '%player%', player.getName() ) );
					mm_utils.msg_player( player.index, line )
			del self.__newPlayers[player.index]

	def init( self ):
		"""Provides default initialisation."""
		self.__config = self.mm.getModuleConfig( configDefaults )
		self.__joinMessages = []
		self.__timedMessages = []
		self.__newPlayers = {}

		# Register our base handlers
		if 0 == self.__state:
			host.registerHandler( 'PlayerConnect', self.onPlayerConnect, 1 )
			host.registerHandler( 'PlayerSpawn', self.onPlayerSpawn, 1 )
			host.registerHandler( 'PlayerDisconnect', self.onPlayerDisconnect, 1 )

		# Load the join messages
		for msg in self.__config['joinMessages']:
			self.__joinMessages.append( msg )

		# Load in the timed messages
		for msg in self.__config['timedMessages']:
			try:
				( start, repeat, text ) = msg.split( ':', 2 )
				self.__addTimedMsg( int( start ), int( repeat ), text )
			except:
				self.mm.error( "Announcer: Invalid timed messaged '%s'" % msg )

		# Register our rcon command handlers
		self.mm.registerRconCmdHandler( 'announcer', { 'method': self.cmdExec, 'subcmds': self.__cmds, 'level': 1 } )

		self.__state = 1

	def shutdown( self ):
		"""Shutdown and stop processing."""

		# remove all our timers
		for details in self.__timedMessages:
			details['timer'].destroy()
			details['timer'] = None

		self.__timedMessages = []

		# Unregister our rcon command handlers
		self.mm.unregisterRconCmdHandler( 'announcer' )

		# Unregister our game handlers
		# Flag as shutdown as there is currently way to do this
		self.__state = 2

def mm_load( modManager ):
	"""Creates the auto balance object."""
	return Announcer( modManager )
