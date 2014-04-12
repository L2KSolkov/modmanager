# vim: ts=4 sw=4 noexpandtab
"""Util methods from other modules

We have some slightly altered versions due to the lack of functionality
in os and sys breaking the core ones

===== History =====
 v3.4 - 27/01/2010:
 Fixed get_cd_key_hash for BFHeroes and BFP4F

 v3.3 - 13/01/2009:
 Added to_unicode method and removed escaping from xml_escape as all calls now pass in unicode
 
 v3.2 - 29/11/2008:
 xml_escape now uses encode ignore instead of encode of replace

 v3.1 - 28/11/2008:
 largs now supports wanted = 0 which returns as many arguments as there are
 
 v3.0 - 20/10/2008:
 Escaped player names in wild card search so that pattern characters in the player name e.g. * dont break the search
 
 v2.9 - 28/06/2007:
 find_player now supports wild card matching on player name if requested
 
 v2.8 - 18/02/2007:
 Reverted to use server message as player message only works for player slot 0
 
 v2.7 - 01/12/2006:
 Fixed typo's in find_player and enhanced so that quotes and spaces are striped from names

 v2.6 - 03/11/2006:
 Added find_player which finds a player given either a player name or playerid
 
 v2.5 - 18/10/2006:
 Fix for largs returing invalid details if the first character was a quote

 v2.4 - 24/07/2006:
 Activated single player message method which should be available in patch v1.4

 v2.3 - 06/05/2006:
 Removed player message method as v1.3 fix doesnt work

 v2.2 - 05/05/2006:
 Updated to use new player message method available in patch v1.3

 v2.1 - 29/03/2006:
 Added get_player_details which returns a list of players with mmDetails set. This contains cdkeyhash and port as fields.

 v2.0 - 24/03/2006:
 Updated largs to deal with Empty quoted args e.g. "" or ''

 v1.9 - 22/02/2006:
 kick_player and kick_player_now are now depricated see mm_banmanager kickPlayer and kickPlayerNow for replacements
 Added largs method for parsing arguments from a string
  
 v1.8 - 20/02/2006:
 Added xml.sax.saxutils replacement methods xml_escape and xml_unescape
 
 v1.7 - 16/02/2006:
 Removed debug from get_player_by_cd_key_hash
 Made get_int more resilient to bad input ( strips quotes and spaces )
 
 v1.6 - 15/02/2006:
 Now uses self.mm.banManager().<method>
 banReason's now default to None see: mm_banmanager.defaultBanReason
 banPeriod's now default to None see: mm_banmanager.defaultBanPeriod
 get_cd_key_hash now caches the players cdkey for faster access
 
 v1.5 - 01/02/2006:
 Added a default for mmKickReason to kick_player_now
 Added a default for mmBanReason to ban_player_now
 Now delegates bans to the Ban Manager
 Added get_player_by_cd_key_hash method
 Added get_cd_key_hash method
 
 v1.4 - 14/08/2005:
 Removed prefix param from MsgChannel constructor.
 MsgChannel.stripPrefix now removes all known prefixes for all channels
 Added status_name which will return a string of the passed in GameState
 
 v1.3 - 10/08/2005:
 Message methods now check and truncate long messages to avoid server crashes.
 
 v1.2 - 26/07/2005:
 Added msg_server and msg_player methods
 
 v1.1 - 11/07/2005:
 Added Message constant classes, MsgChannel and MsgType
 
 v1.0 - 26/06/2005:
 Initial version

Copyright (c)2008 Multiplay
Author: Steven 'Killing' Hartland
"""

import re
import sys
import types
import host
import bf2

__version__ = 3.4

__all__ = [
	# custom methods
	"method_name",
	"lsplit",
	"exec_subcmd",
	"caller_module",
	"msg_server",
	"msg_player",
	"kick_player",
	"ban_player",
	"kick_player_now",
	"ban_player_now",
	"get_int",
	"status_name",
	"get_cd_key_hash",
	"get_player_by_cd_key_hash",

	# trace back methods
	"format_exception",
	"format_exception_only",
	"format_tb",
	"format_list",
	"extract_tb",

	# linecache methods
	"getline",
	"clearcache",
	"checkcache"

	# xml.sax.saxutils methods
	"xml_escape", # escape
	"xml_unescape", # unescape
]

class MsgChannel( object ):
	def __init__( self, id, txt ):
		"""Create a channel object."""
		self.id = id
		self.txt = txt

	def stripPrefix( self, msg ):
		"""Return msg with this prefixes removed."""
		for prefix in ( '*\xa71DEAD\xa70*', 'HUD_TEXT_CHAT_TEAM', 'HUD_CHAT_DEADPREFIX', 'HUD_TEXT_CHAT_SQUAD' ):
			msg = msg.replace( prefix, '', 1 )

		return msg

class MsgChannels:
	Global = MsgChannel( 0, 'Global' )
	Team = MsgChannel( 1, 'Team' )
	Commander = MsgChannel( 2, 'Commander' )
	Squad = MsgChannel( 3, 'Squad' )
	SquadLeader = MsgChannel( 4, 'SquadLeader' )
	SquadId = MsgChannel( 5, 'SquadId' )
	LocalTeamMedic = MsgChannel( 6, 'LocalTeamMedic' )
	LocalGroundVehicle = MsgChannel( 7, 'LocalGroundVehicle' )
	LocalAirVehicle = MsgChannel( 8, 'LocalAirVehicle' )
	Local = MsgChannel( 9, 'Local' )
	LocalTeam = MsgChannel( 10, 'LocalTeam' )
	Vehicle = MsgChannel( 11, 'Vehicle' )
	ServerMessage = MsgChannel( 12, 'ServerMessage' )
	ServerTeamMessage = MsgChannel( 13, 'ServerTeamMessage' )
	Player = MsgChannel( 14, 'Player' )
	LocalRevive = MsgChannel( 15, 'LocalRevive' )
	AutoLocalRevive = MsgChannel( 16, 'AutoLocalRevive' )
	TeamAndLocalEnemies = MsgChannel( 17, 'TeamAndLocalEnemies' )
	SquadAndLocalEnemies = MsgChannel( 18, 'SquadAndLocalEnemies' )

	named = {
		'Global': Global,
		'Team': Team,
		'Commander': Commander,
		'Squad': Squad,
		'SquadLeader': SquadLeader,
		'SquadId': SquadId,
		'LocalTeamMedic': LocalTeamMedic,
		'LocalGroundVehicle': LocalGroundVehicle,
		'LocalAirVehicle': LocalAirVehicle,
		'Local': Local,
		'LocalTeam': LocalTeam,
		'Vehicle': Vehicle,
		'ServerMessage': ServerMessage,
		'Vehicle': Vehicle,
		'ServerMessage': ServerMessage,
		'ServerTeamMessage': ServerTeamMessage,
		'Player': Player,
		'LocalRevive': LocalRevive,
		'AutoLocalRevive': AutoLocalRevive,
		'TeamAndLocalEnemies': TeamAndLocalEnemies,
		'SquadAndLocalEnemies': SquadAndLocalEnemies,
	}

__status_names = {
	1: 'Playing',
	2: 'EndGame',
	3: 'PreGame',
	4: 'Paused',
	5: 'RestartServer',
	6: 'NotConnected'
}

class MsgType:
	Game = 0
	Server = 1
	TextChat = 2
	Radio = 3
	Unknown = 4

class KickBanType:
	rcon = 1
	punkBuster = 2 # Not supported yet

class BanMethod:
	key = 'Key'
	address = 'Address'

timers = {}
mm = None


def status_name( status ):
	"""Return the name of the status"""
	if __status_names.has_key( status ):
		return __status_names[status]
	else:
		return "Unknown"

def find_player( playerid, wild=False ):
	"""Return a player given a playerid or name
	Note: player name is match case insensitive.
	"""
	player = None
	try:
		num = int( playerid.strip( '"\' ' ) )
		if 0 > num:
			return None

		try:
			player = bf2.playerManager.getPlayerByIndex( num )
			return player
		except:
			return None

	except ValueError:
		# not an playerid check for name
		playerid = playerid.strip( '"\' ' ).lower()
		players = bf2.playerManager.getPlayers()
		for player in players:
			if player.getName().lower() == playerid:
				return player

		# still no match try a wild card search
		# The first match will be returned
		name_re = re.compile( '.*?' + re.escape( playerid ) + '.*' )
		for player in players:
			if name_re.search( player.getName().lower() ) is not None:
				return player


	return None

def get_int( ctx, string, desc='number' ):
	"""Return the number or None if invalid."""
	try:
		num = int( string.strip( '"\' ' ) )
	except ValueError:
		ctx.write( "Error: invalid %s '%s'\n" % ( desc, string ) )
		mm.error( "Invalid %s '%s'\n" % ( desc, string ) )
		num = None

	return num

def kick_player( player, kickReason=None, kickDelay=None, kickType=None ):
	"""Kick a player with a reason."""
	return mm.banManager().kickPlayer( player, kickReason, kickDelay, kickType )

def kick_player_now( player, kickType=None ):
	"""Kick a player."""
	return mm.banManager().kickPlayer( player, kickType )

def ban_player( player, banReason=None, banPeriod=None, msgDelay=5, banType=KickBanType.rcon, banMethod=BanMethod.key, bannedBy='Unknown' ):
	"""Ban a player for a given period with a reason."""
	return mm.banManager().banPlayer( player, banReason, banPeriod, banType, banMethod, bannedBy, msgDelay )

def ban_player_now( player, banType=KickBanType.rcon, banReason=None, banPeriod=None, banMethod=BanMethod.key, bannedBy='Unknown' ):
	"""Ban a player."""
	return mm.banManager().banPlayerNow( player, banReason, banPeriod, banType, banMethod, bannedBy )

def msg_player( playerid, msg ):
	"""Sends a message to a player on the server."""
	# TODO: update to send the message to the player once this is fixed
	# in the server code
	if 243 < len( msg ):
		mm.warn( "Truncating long message '%s'" % msg )
		msg = msg[0:243]
	# BF2142 v1.10 only works sending messages to player 0 :(
	# so reverting to server send
	host.sgl_sendTextMessage( 0, MsgChannels.ServerMessage.id, MsgType.Server, msg, 0 )
	#mm.warn( "host.sgl_sendTextMessage( %s, %s, %s, %s, %s )" % ( playerid, MsgChannels.Player.id, MsgType.Server, msg, 0 ) )
	#host.sgl_sendTextMessage( playerid, MsgChannels.Player.id, MsgType.Server, msg, 0 )

def msg_server( msg ):
	"""Sends a message to all players on the server."""
	if 243 < len( msg ):
		mm.warn( "Truncating long message '%s'" % msg )
		msg = msg[0:243]
	host.sgl_sendTextMessage( 0, MsgChannels.ServerMessage.id, MsgType.Server, msg, 0 )

def exec_subcmd( mm, subcmds, ctx, cmd ):
	"""Execute a modules sub command."""
	module = caller_module()
	mm.debug( 2, "%s '%s' by %s" % ( module, cmd, ctx.getName() ) )

	( subcmd, args ) = lsplit( cmd.strip(), ' ', 2 )

	if subcmds.has_key( subcmd ):
		subcmd_details = subcmds[subcmd]
		if 0 == subcmd_details['level'] or ctx.authedAllowed( ctx, subcmd_details ):
			try:
				if subcmd_details['restricted'] and host.ss_getParam('ranked'):
					msg = "Restricted: Sorry command '%s' is not permitted on ranked servers" % subcmd
					self.mm.debug( 1, msg )
					ctx.write( msg )
				else:
					subcmds[subcmd]['method']( ctx, args )
			except Exception, e:
				# generate line number
				lineNum = ''
				execInfo = sys.exc_info()
				tb = execInfo[2]
				while tb is not None:
					if lineNum == '':
						lineNum = str( tb.tb_lineno )
					else:
						lineNum += ', ' + str( tb.tb_lineno )
					tb = tb.tb_next
				mm.error( "%s: Failed to run sub command '%s'" % ( module, ctx.currentCmd ), True )
				ctx.write('Exception in sub command \'%s\' %s %s (%s)\n' % ( ctx.currentCmd, str(execInfo[0]), str(e), lineNum))
		else:
			ctx.write( "error: you are not authorised to use the command '%s' it requires level %d you are only level %d" % ( subcmd, ctx.authedLevel, cmd_details['level'] ) )
			mm.warn( "Client %s tried to invoke '%s' without sufficient auth level" % ( ctx.getName(), subcmd ) )
	else:
		err = "%s: unknown sub command '%s'\n" % ( module, subcmd )
		mm.error( err )
		ctx.write( err )

def get_cd_key_hash( player ):
	"""Determine the players CDKey hash."""

	# Only BF2 doesnt getCDKeyHash
	if not mm.isBattleField2():
		return player.getCDKeyHash()

	# Players CDKey's dont change so check for it on the the player object
	if hasattr( player, 'mmCdKeyHash' ):
		return player.mmCdKeyHash

	id_re = re.compile( "Id:\s+%d\s+-" % player.index )
	found = False
	for line in host.rcon_invoke( "admin.listPlayers" ).split( '\n' ):
		line = line.strip()
		match = id_re.search( line )
		if match is not None:
			# This is the player we are interested in
			found = True
		elif found:
			# the next line is the cdkey hash
			# Store it on the player object for fast access next time
			player.mmCdKeyHash = line[len( "CD-key hash:" ):].strip()
			return player.mmCdKeyHash

	return None

def get_player_details():
	"""Returns the list of players with mmCDKeyHash set."""

	allset = True
	players_hash = {}
	for player in bf2.playerManager.getPlayers():
		if not hasattr( player, 'mmDetails' ):
			allset = False
			break
		players_hash[player.index] = player

	if allset:
		return players_hash.values()

	rawData = host.rcon_invoke( "admin.listplayers" )

	# Thanks Woody http://bf2.fun-o-matic.org/index.php/Cookbook:Accessing_CD_Key_Hash
	pattern = re.compile(r'''^Id:\ +(\d+)					# PlayerID
				\ -\ (.*?)									# Player Name
				\ is\ remote\ ip:\ (\d+\.\d+\.\d+\.\d+):	# IP Address
				(\d+)										# Port Number
				(?:.*?hash:\ (\w{32}))?						# CD Key Hash
				''', re.DOTALL | re.MULTILINE | re.VERBOSE )

	players = []
	for data in pattern.findall(rawData):
		player = players_hash[int(data[0])]
		player.mmDetails = {
			'cdkeyhash': data[4],
			'port': data[3]
		}
		# we do this just in case we have a miss match between
		# players_hash and the rawData
		players.append( player )

	return players

def get_player_by_cd_key_hash( cdkeyhash ):
	"""Find a player by cdkeyhash."""
	id_re = re.compile( "Id:\s+(\d+)\s+-" )
	playerid = None
	for line in host.rcon_invoke( "admin.listPlayers" ).split( '\n' ):
		line = line.strip()
		match =  id_re.search( line )
		if match is not None:
			# Valid playerid
			playerid = match.group( 1 )

		elif playerid is not None:
			# previous line was a playerid
			cdkey = line[len( "CD-key hash:" ):].strip()
			if cdkey == cdkeyhash:
				# found the player
				return bf2.playerManager.getPlayerByIndex( int( playerid ) )
			playerid = None

	return None

def caller_module( level=2 ):
	"""Return the name of the calling module."""
	try:
		raise Exception()
	except:
		frame = sys.exc_info()[2].tb_frame
		while level:
			frame = frame.f_back
			level -= 1

		return frame.f_globals.get('__name__')

def method_name( func ):
	"""Return the name for the given function."""
	full = str( func )
	if full.startswith( "<bound method" ):
		return full.split( " ", 3 )[2]
	else:
		return full[1:].split( " ", 1 )[0]

def lsplit( str, on, want, default='' ):
	"""Split the <str> using <on> returning a list with exactly <want> members."""
	if 0 == want:
		return str.split( on )
	else:
		parts = str.split( on, want - 1 )
	l = len( parts )
	if want == l:
		return parts
	else:
		for i in range( want - l ):
			parts.append( default )
		return parts

def largs( data, on, want, default='', quoted=False ):
	"""Split the <str> using based on whitespace taking into account quoted parts.

	Returns a list with exactly <want> members if none zero else returns all elements.
	If quotes are unmatched falls back to lsplit( str, None, want, default )
	"""
	# Note: This is not particularly pretty but does what is needed
	#mm.warn( "data: '%s'\nwant: %d\ndefault: %s\n" % ( data, want, default ) )
	left = data
	quote = None
	parts = []
	d = left.find( '"' )
	s = left.find( "'" )
	while -1 != d or -1 != s and ( want > len( parts ) or 0 == want ):
		while d >= 0 and '\\' == left[d-1]:
			last = d - 2
			slash_count = 1
			while last >= 0:
				if '\\' == left[last]:
					last -= 1
					slash_count += 1
				else:
					break

			#mm.warn( "SSS: %s\n%d => %d = %c %d = %d" % ( left, d, last, left[last], slash_count, slash_count % 2 ) )

			if slash_count % 2:
				# escaped double quote
				d = left.find( '"', d + 1 )
			else:
				break

		while s >= 0 and '\\' == left[s-1]:
			# escaped single quote
			last = s - 2
			slash_count = 1
			while last >= 0:
				if '\\' == left[last]:
					last -= 1
					slash_count += 1
				else:
					break

			#mm.warn( "SSS: %s\n%d => %d = %c %d = %d" % ( left, s, last, left[last], slash_count, slash_count % 2 ) )

			if slash_count % 2:
				# escaped single quote
				s = left.find( "'", s + 1 )
			else:
				break

		#mm.warn( "d:%d, s:%d, q:%s, left:%s" % ( d, s, quote, left.strip() ) )
	
		if -1 == d and -1 == s:
			# they where all escaped quotes
			break

		if quote is None:
			if d >= 0:
				# have a double quote
				if s < 0 or d < s:
					# next quote is a double quote
					quote = '"'
					if 0 != d:
						pre = left[:d-1].strip()
						if "" != pre:
							parts.append( { 'quote': None, 'string': unescape_arg( pre ) } )
					left = left[d+1:]
				else:
					# next quote is a single quote
					quote = "'"
					if 0 != s:
						pre = left[:s-1].strip()
						if "" != pre:
							parts.append( { 'quote': None, 'string': unescape_arg( pre ) } )
					left = left[s+1:]
			else:
				# have a single quote
				quote = "'"
				parts.append( { 'quote': None, 'string': unescape_arg( left[:s-1].strip() ) } )
				left = left[s+1:]

		elif "'" == quote:
			# processing a single quote
			if s >= 0:
				parts.append( { 'quote': quote, 'string': unescape_arg( left[:s] ) } )
				left = left[s+1:]
			else:
				mm.warn( "Unmatched single quote in '%s'!" % data );
				return lsplit( data, on, want, default )

			quote = None

		else:
			# processing a double quote
			if d >= 0:
				parts.append( { 'quote': quote, 'string': unescape_arg( left[:d] ) } )
				left = left[d+1:]
			else:
				mm.warn( "Unmatched double quote in '%s'!" % data );
				return lsplit( data, on, want, default )

			quote = None

		d = left.find( '"' )
		s = left.find( "'" )

	left = left.strip()
	if "" != left:
		parts.append( { 'quote': None, 'string': unescape_arg( left ) } )

	#mm.info( "LEN1: %d => %d" % ( len( parts ), want ) )
	# Now split all none quote elements into parts
	all_parts = []
	c = 0
	last = want - 1
	for p in parts:
		#mm.info( "P1:%d => %d" % ( c, len( all_parts ) ) )
		if p['quote'] is not None:
			# Quoted element
			if c < want or 0 == want:
				# Still want more element so add this one
				if quoted:
					all_parts.append( "%s%s%s" % ( p['quote'], p['string'], p['quote'] ) )
				else:
					all_parts.append( p['string'] )
				c += 1
			else:
				# we have already found enough elements append to the last one,
				# rebuilding the string as it was.
				all_parts[last] = "%s %s%s%s" % ( all_parts[last], p['quote'], p['string'], p['quote'] )
		else:
			# None quoted element
			if c < want:
				# We want more elements so split the string on white space
				for s in p['string'].split( None, want - c - 1 ):
					all_parts.append( s )
					c += 1
					#mm.info( "P2:%d => %d" % ( c, len( all_parts ) ) )
			elif 0 == want:
				# We want more elements so split the string on white space
				for s in p['string'].split( None ):
					all_parts.append( s )
					c += 1
					#mm.info( "P3:%d => %d" % ( c, len( all_parts ) ) )
			else:
				# we have already found enough elements append to the last one,
				# rebuilding the string as it was.
				all_parts[last] = "%s %s" % ( all_parts[last], p['string'] )

	l = len( all_parts )
	#mm.info( "LEN2: %d => %d" % ( l, want ) )
	if want == l or 0 == want:
		return all_parts
	else:
		for i in range( want - l ):
			all_parts.append( default )
		#mm.info( "LEN: %d => %d" % ( len( all_parts ), want ) )
		return all_parts

def unescape_arg( data ):
	"""Unescapes strings in data."""
	# Remove all escaped \'s
	c = 0
	while c < len( data ) - 1:
		if '\\' == data[c]:
			data = "%s%s" % ( data[:c], data[c+1:] )
		c += 1

	return data

def init( modmanager ):
	"""Sets our reference to the modmanager."""
	globals()['mm'] = modmanager


# Traceback methods due to line cache being broken
def format_exception(etype, value, tb, limit = None):
    """Format a stack trace and the exception information.

    The arguments have the same meaning as the corresponding arguments
    to print_exception().  The return value is a list of strings, each
    ending in a newline and some containing internal newlines.  When
    these lines are concatenated and printed, exactly the same text is
    printed as does print_exception().
    """
    if tb:
        list = ['Traceback (most recent call last):\n']
        list = list + format_tb(tb, limit)
    else:
        list = []
    list = list + format_exception_only(etype, value)
    return list

def format_exception_only(etype, value):
    """Format the exception part of a traceback.

    The arguments are the exception type and value such as given by
    sys.last_type and sys.last_value. The return value is a list of
    strings, each ending in a newline.  Normally, the list contains a
    single string; however, for SyntaxError exceptions, it contains
    several lines that (when printed) display detailed information
    about where the syntax error occurred.  The message indicating
    which exception occurred is the always last string in the list.
    """
    list = []
    if type(etype) == types.ClassType:
        stype = etype.__name__
    else:
        stype = etype
    if value is None:
        list.append(str(stype) + '\n')
    else:
        if etype is SyntaxError:
            try:
                msg, (filename, lineno, offset, line) = value
            except:
                pass
            else:
                if not filename: filename = "<string>"
                list.append('  File "%s", line %d\n' %
                            (filename, lineno))
                if line is not None:
                    i = 0
                    while i < len(line) and line[i].isspace():
                        i = i+1
                    list.append('    %s\n' % line.strip())
                    if offset is not None:
                        s = '    '
                        for c in line[i:offset-1]:
                            if c.isspace():
                                s = s + c
                            else:
                                s = s + ' '
                        list.append('%s^\n' % s)
                    value = msg
        s = _some_str(value)
        if s:
            list.append('%s: %s\n' % (str(stype), s))
        else:
            list.append('%s\n' % str(stype))
    return list

def format_tb(tb, limit = None):
    """A shorthand for 'format_list(extract_stack(f, limit))."""
    return format_list(extract_tb(tb, limit))


def format_list(extracted_list):
    """Format a list of traceback entry tuples for printing.

    Given a list of tuples as returned by extract_tb() or
    extract_stack(), return a list of strings ready for printing.
    Each string in the resulting list corresponds to the item with the
    same index in the argument list.  Each string ends in a newline;
    the strings may contain internal newlines as well, for those items
    whose source text line is not None.
    """
    list = []
    for filename, lineno, name, line in extracted_list:
        item = '  File "%s", line %d, in %s\n' % (filename,lineno,name)
        if line:
            item = item + '    %s\n' % line.strip()
        list.append(item)
    return list

def extract_tb(tb, limit = None):
    """Return list of up to limit pre-processed entries from traceback.

    This is useful for alternate formatting of stack traces.  If
    'limit' is omitted or None, all entries are extracted.  A
    pre-processed stack trace entry is a quadruple (filename, line
    number, function name, text) representing the information that is
    usually printed for a stack trace.  The text is a string with
    leading and trailing whitespace stripped; if the source is not
    available it is None.
    """
    if limit is None:
        if hasattr( sys, 'tracebacklimit' ):
            limit = sys.tracebacklimit
    list = []
    n = 0
    while tb is not None and (limit is None or n < limit):
        f = tb.tb_frame
        lineno = tb.tb_lineno
        co = f.f_code
        filename = co.co_filename
        name = co.co_name
        line = getline(filename, lineno)
        if line: line = line.strip()
        else: line = None
        list.append((filename, lineno, name, line))
        tb = tb.tb_next
        n = n+1
    return list

def _some_str(value):
    try:
        return str(value)
    except:
        return '<unprintable %s object>' % type(value).__name__


"""Cache lines from files.

This is intended to read lines from modules imported -- hence if a filename
is not found, it will look down the module search path for a file by
that name.
"""


def getline(filename, lineno):
    lines = getlines(filename)
    if 1 <= lineno <= len(lines):
        return lines[lineno-1]
    else:
        return ''

# The cache

cache = {} # The cache


def clearcache():
    """Clear the cache entirely."""

    global cache
    cache = {}

def getlines(filename):
    """Get the lines for a file from the cache.
    Update the cache if it doesn't contain an entry for this file already."""

    if filename in cache:
        return cache[filename][2]
    else:
        return updatecache(filename)

def fileexists(filename):
	"""Replacement method for os.stat."""
	try:
		f = open( filename, 'r' )
		f.close()
		return True
	except:
		pass
	return False

def updatecache(filename):
    """Update a cache entry and return its list of lines.
    If something's wrong, print a message, discard the cache entry,
    and return an empty list."""

    if filename in cache:
        del cache[filename]
    if not filename or filename[0] + filename[-1] == '<>':
        return []
    fullname = filename

    if not fileexists( fullname ):
        # Try looking through the module search path.
	basename = filename.split( "/" ).pop()
        for dirname in sys.path:
            # When using imputil, sys.path may contain things other than
            # strings; ignore them when it happens.
            try:
                fullname = "/".join(dirname, basename)
            except (TypeError, AttributeError):
                # Not sufficiently string-like to do anything useful with.
                pass
            else:
				if fileexist( fullname ):
					break
        else:
            # No luck
##          print '*** Cannot stat', filename, ':', msg
            return []
    try:
        fp = open(fullname, 'rU')
        lines = fp.readlines()
        fp.close()
    except IOError, msg:
##      print '*** Cannot open', fullname, ':', msg
        return []
#    size, mtime = stat.st_size, stat.st_mtime
    size, mtime = 0, 0
    cache[filename] = size, mtime, lines, fullname
    return lines

def xml_escape(data, entities={}):
    """Escape &, <, and > in a string of data.

    You can escape other strings of data by passing a dictionary as
    the optional entities parameter.  The keys and values must all be
    strings; each key will be replaced with its corresponding value.
    """

    # must do ampersand first
    data = data.replace("&", "&amp;")
    data = data.replace(">", "&gt;")
    data = data.replace("<", "&lt;")
    if entities:
        data = __xml_dict_replace(data, entities)

    return data #data.decode( 'utf-8', 'replace' ).encode( 'utf-8', 'xmlcharrefreplace' )

def xml_unescape(data, entities={}):
    """Unescape &amp;, &lt;, and &gt; in a string of data.

    You can unescape other strings of data by passing a dictionary as
    the optional entities parameter.  The keys and values must all be
    strings; each key will be replaced with its corresponding value.
    """
    data = data.replace("&lt;", "<")
    data = data.replace("&gt;", ">")
    if entities:
        data = __xml_dict_replace(data, entities)
    # must do ampersand last
    return data.replace("&amp;", "&") #.encode( 'utf-8', 'xmlcharrefreplace' )

def __xml_dict_replace(s, d):
    """Replace substrings of a string using a dictionary."""
    for key, value in d.items():
        s = s.replace(key, value)
    return s

def to_unicode( obj, encoding='utf-8' ):
	if isinstance( obj, basestring ):
		if not isinstance( obj, unicode ):
			obj = unicode( obj, encoding )
	return obj
