# vim: ts=4 sw=4 noexpandtab
"""Ban Manager module.

This is a Ban Manager ModManager module

===== Config =====
 # The filename to use for bans
 mm_banmanager.banFilename "mm_bans.xml"
 
 # The message format announced to players being banned
 # This must include the template %s <player> and %s <reason>
 mm_banmanager.banMessage "%s you are being banned (reason:%s)
 
 # The default ban reason
 mm_banmanager.defaultBanReason "Unknown"
 
 # The default ban period
 mm_banmanager.defaultBanPeriod "Perm"
 
 # The default ban method must be either "Key" or "Address"
 mm_banmanager.defaultBanMethod "Key"
 
 # The default ban message delay
 mm_banmanager.defaultBanDelay 5
 
 # The default unban reason
 mm_banmanager.defaultUnBanReason "Unknown"
 
 # The default ban nick 
 mm_banmanager.defaultBanNick "N/A"
 
 # The default ban address 
 mm_banmanager.defaultBanAddress "N/A"
 
  # The default ban cd key hash 
 mm_banmanager.defaultBanCdKeyHash "N/A"
 
 # The default kick reason
 mm_banmanager.defaultKickReason "Unknown"
 
 # The date time format used for bans parsed in and output in the xml
 mm_banmanager.dateTimeFormat "%d/%m/%Y %H:%M:%S %Z"
 
 # The backup date time format used to parse in bans from the xml file
 mm_banmanager.oldDateTimeFormat "%a %b %d %H:%M:%S %Y"

===== Notes =====
Don't use admin commands directly on the servers console to manipulate bans or inconsistencies will occur.
All rcon commands are safe to use.
It is strongly recommended you do NOT change defaultBanAddress, defaultBanCdKeyHash or defaultBanProfileId

===== History =====
 v3.8 - 29/01/2013:
 Fixed compatibility issue with BFHeores using long not int profileid's

 v3.7 - 13/09/2012:
 Added checks and auto upgrades for Heroes which no longer supports Address bans

 v3.6 - 12/10/2011:
 Added BFP4F Support

 v3.5 - 10/10/2006:
 Now uses .search instead of .match on regexps
 
 v3.4 - 30/08/2006:
 Added supported games 
 
 v3.3 - 17/04/2006:
 Added dateTime and skipSave params to banPlayerKey and banPlayerAddress methods
 
 v3.2 - 05/04/2006:
 API cleanup implementing internal __addBan __removeBan methods which are now exclusively used for manipulating the internal ban list
 Added local rcon method listBans

 v3.1 - 04/04/2006:
 Added local addBan method
 Corrected cmdAddBan now correctly adds server side ban
 Corrected cmdUpdateBan now correctly removes any old ban and adds the new one

 v3.0 - 29/03/2006:
 Added datetime param to updateBan and addBan rcon commands

 v2.9 - 24/03/2006:
 Added local ban manipulation rcon commands

 v2.8 - 22/03/2006:
 Corrected usage of ban['datetime'] and time.now() typo in periodic ban reads
 
 v2.7 - 11/03/2006:
 Corrected shutdown of onGameStatusChanged
 
 v2.6 - 10/03/2006:
 Added dateTimeFormat and oldDateTimeFormat parameter to allow for custom formats. Note all dates are stored and output in GMT.
 
 v2.5 - 08/03/2006:
 A banDelay of 0 passed to banPlayer now prevents any ban message being displayed.
 
 v2.4 - 02/03/2006:
 Now clears all legacy bans on load if a Banmanager banfile is detected and on map change. This prevents old bans creeping in unnoticed.
 Corrected availability of now variable for timed bans
 
 v2.3 - 02/03/2006:
 Optimised logic ( common case first ).
 Corrected typo in clearBans for time based bans.

 v2.2 - 28/02/2006:
 Now only reads in server based "legacy" bans if configured banFilename doesnt exist. This prevents problems on multi server installs.

 v2.1 - 26/02/2006:
 clearBanList now correctly clears __roundBans and __unbanTimers preventing incorrect warnings when the cleared bans expire.
 
 v2.0 - 22/02/2006:
 Added defaultBanCdKeyHash, defaultBanAddress and defaultBanProfileId config options
 Now checks to ensure that banMethod is valid and will attempt to correct based on the ban info available
 Now deals with duplicate bans within the ban message notification period
 Added kickPlayer and kickPlayerNow methods which replace those from mm_utils
 Now checks to ensure Round bans arent read back in from disk on initialisation
 
 v1.9 - 22/02/2006:
 Corrected documented defaults for defaultBanPeriod => "Perm" and defaultBanMethod => "Key"
 
 v1.8 - 21/02/2006:
 Added getBanList method which returns a copy of the servers current banlist hash
 Corrected banlist read in for player nick
 Renamed validateBanKey to validateBanAddressOrKey ( more approproate name )
 Now calls validatePlayerName to determine the Player Nick in legacy methods
 Removed spurious ',' which broke banPlayerNow
 
 v1.7 - 20/02/2006:
 Now escapes XML entities
 Added defaultBanNick
 Now validates banfile on read in fixing data if possible
 
 v1.6 - 19/02/2006:
 Enhanced input validation to unban method
 
 v1.5 - 19/02/2006:
 Added check for invalid unban ( empty ban key / address )
 Added early determination of player: name, profileid, address and cdkey
 Enhanced error detection and recovery for delayed bans
 Added unBanReason validation
 
 v1.4 - 18/02/2006:
 Fixed cut and paste error in validateBanKey
 
 v1.3 - 16/02/2006:
 Added validation for ban cdkey hashes and addresses
 Fixed log entry for banPlayerAddress and banPlayerKey
 
 v1.2 - 15/02/2006:
 Now uses admin.addAddressToBanList and admin.addKeyToBanList as a backup to admin.banPlayer and admin.banPlayerKey
 Corrected inverted use of admin.banPlayer and admin.banPlayerKey
 Added banPlayerAddress and banPlayerKey methods for adding manual bans
 Ban file is now valid XML i.e. contains a header and a root <banlist> node
 unbanPlayer now logs at level info
 clearBanList now logs at level info
 Added banMessage, defaultBanReason, defaultBanDelay and defaultBanPeriod config parameters
 Added validation of banPeriod, banReason, banDelay, banType and bannedBy
 Now also issues a kick to a player when they are banned to workaround bans issued in the early stages of a player connecting failing to activate
 Now deals with from now and epoc bans
 Added expireBan
 unbanPlayer now takes an optional reason
 
 v1.1 - 13/02/2006:
 Error case trap for player.getName() failing added
 
 v1.0 - 01/02/2006:
 Initial version

Copyright (c)2008 Multiplay
Author: Steven 'Killing' Hartland
"""

import re
import time
import bf2
import host
import mm_utils
import codecs

# Set the version of your module here
__version__ = 3.8

# Set the required module versions here
__required_modules__ = {
	'modmanager': 1.6
}

# Does this module support reload ( are all its reference closed on shutdown? )
__supports_reload__ = True

__supported_games__ = {
	'bf2': True,
	'bf2142': True,
	'bfheroes': True,
	'bfp4f': True
}

# Set the description of your module here
__description__ = "BanManager v%s" % __version__

# Add all your configuration options here
configDefaults = {
	# The filename to use for bans
	'banFilename': 'mm_bans.xml',
	'banMessage': '%s you are being banned (reason: %s)',
	'kickMessage': '%s you are being kicked (reason: %s)',
	'defaultBanDelay': 5,
	'defaultBanReason': 'Unknown',
	'defaultBanPeriod': 'Perm',
	'defaultBanMethod': 'Key',
	'defaultBannedBy': 'Unknown',
	'defaultUnBanReason': 'Unknown',
	'defaultBanNick': 'N/A',
	'defaultBanAddress': 'N/A',
	'defaultBanCdKeyHash': 'N/A',
	'defaultBanProfileId': 'N/A',
	'defaultKickDelay': 5,
	'defaultKickReason': 'Unknown',
	'dateTimeFormat': "%d/%m/%Y %H:%M:%S %Z",
	'oldDateTimeFormat': "%a %b %d %H:%M:%S %Y",
}

class BanManager( object ):

	def __init__( self, modManager ):
		# ModManager reference
		self.mm = modManager

		# Internal shutdown state
		self.__state = 0
		self.__bans = {}
		self.__banTimers = {}
		self.__unBanTimers = {}
		self.__kickTimers = {}
		self.__roundBans = {}
		self.__fromNowRe = re.compile( r'^\d+$' )
		self.__epocRe = re.compile( r'^:\d+$' )
		self.__banPeriodRe = re.compile( r'^:?\d+$' )

		self.__cmds = {
			'updateBan': { 'method': self.cmdUpdateBan, 'args': '<cdkeyhash|ip> Key|Address "<nick>" "<period>" "<ip>" "<cdkeyhash>" "<profileid>" "<by>" "<reason>" "<datetime>"', 'level': 5 },
			'addBan': { 'method': self.cmdAddBan, 'args': 'Key|Address "<nick>" "<period>" "<ip>" "<cdkeyhash>" "<profileid>" "<by>" "<reason>"', 'level': 10 },
			'removeBan': { 'method': self.cmdRemoveBan, 'args': '<cdkeyhash|ip> <reason>', 'level': 5 },
			'banPlayer': { 'method': self.cmdBanPlayer,  'args': '<playerid> <period> "<reason>" <bannedby>', 'level': 10 },
			'reloadBans': { 'method': self.cmdReloadBans, 'level': 5 },
			'listBans': { 'method': self.cmdListBans, 'level': 5 },
			'clearBans': { 'method': self.cmdClearBans, 'level': 5 },
		}

	def cmdClearBans( self, ctx, cmd ):
		"""Clear all bans"""
		self.mm.debug( 2, "cmdClearBanList by %s" % ( ctx.getName() ) )
		if self.clearBanList():
			ctx.write( "Banlist cleared\n" )
		else:
			ctx.write( "Banlist failed to clear\n" )

	def cmdListBans( self, ctx, cmd ):
		"""Ban a player for a specified timer period from the server with a message."""
		self.mm.debug( 2, "cmdListBans by %s" % ( ctx.getName() ) )

		self.writeBanlist( ctx )

	def cmdUpdateBan( self, ctx, cmd ):
		"""Update a ban."""
		self.mm.debug( 2, "cmdUpdateBan %s" % cmd )
		( bankey, method, nick, period, address, cdkeyhash, profileid, by, reason, datetime ) = mm_utils.largs( cmd, None, 10, '' )
		if self.__bans.has_key( bankey ):
			ban = self.__bans[bankey]
			old_method = ban['method']

			# remove as the details may have changed
			del self.__bans[bankey]

			# Only update values which where specified
			if nick:
				ban['nick'] = self.validatePlayerName( nick )

			if period:
				ban['period'] = self.validateBanPeriod( period )

			if address:
				ban['address'] = self.validateBanAddress( address )

			if cdkeyhash:
				ban['cdkeyhash'] = self.validateBanCdKeyHash( cdkeyhash )

			if profileid:
				ban['profileid'] = self.validateBanProfileId( profileid )

			if by:
				ban['by'] = self.validateBannedBy( by )

			if reason:
				ban['reason'] = self.validateBanReason( reason )

			if method:
				ban['method'] = self.validateBanMethod( method, ban['cdkeyhash'], ban['address'] )

			if datetime:
				ban['datetime'] = datetime

			# Check and remove the old ban
			self.__removeBan( bankey, 'Ban update', True )

			# Add the new one
			if self.__addBan( ban['method'], ban['nick'], ban['period'], ban['address'], ban['cdkeyhash'], ban['profileid'], ban['by'], ban['reason'], ban['datetime'] ):
				ctx.write( 'Ban updated\n' )
			else:
				ctx.write( "Update failed ( save failed )\n" )

		else:
			ctx.write( "Update failed ( ban '%s' not found )\n" % bankey )

	def cmdAddBan( self, ctx, cmd ):
		"""Rcon command to add a ban."""
		self.mm.debug( 2, "cmdAddBan %s" % cmd )
		( method, nick, period, address, cdkeyhash, profileid, by, reason, datetime ) = mm_utils.largs( cmd, None, 9, '' )
		ban = self.__addBan( method, nick, period, address, cdkeyhash, profileid, by, reason, datetime )

		if ban:
			ctx.write( 'Ban added\n' )
		else:
			ctx.write( "Ban add failed ( save failed )\n" )

	def cmdReloadBans( self, ctx, cmd ):
		"""Reload bans."""
		self.mm.debug( 2, "cmdReloadBans" )
		if self.loadBans():
			ctx.write( 'Reload successful\n' )
		else:
			ctx.write( 'Reload failed\n' )

	def cmdRemoveBan( self, ctx, cmd ):
		"""Remove a ban."""
		self.mm.debug( 2, "cmdRemoveBan %s" % cmd )
		( ban, reason ) = mm_utils.largs( cmd, None, 2, '' )
		if self.__removeBan( ban, reason ):
			ctx.write( 'Unban successful\n' )
		else:
			ctx.write( 'Unban failed (ban not found)\n' )

	def cmdBanPlayer( self, ctx, cmd ):
		"""Ban a player for a specified time period from the server with a message."""
		self.mm.debug( 2, "cmdBanPlayerBy '%s' by %s" % ( cmd, ctx.getName() ) )

		( playerid, banPeriod, banReason, bannedBy ) = mm_utils.largs( cmd, None, 4, '' )

		playerid = mm_utils.get_int( ctx, playerid, 'playerid' )

		if 0 > playerid:
			ctx.write( 'Error: player Id not found\n')
			return 0

		try:
			player = bf2.playerManager.getPlayerByIndex( playerid )

			if player is None:
				ctx.write('Error: player Id %d not found\n' % playerid )
			else:
				if banReason is not None:
					banReason = banReason.strip( '" ' )
				if bannedBy is None:
					bannedBy = ctx.getName()
				self.banPlayer( player, banReason, banPeriod, None, None, bannedBy )
				ctx.write( "Player '%s' (%d) banned\n" % ( player.getName(), playerid ) )
		except:
			ctx.write('Error: player Id %d not found\n' % playerid )
			self.mm.error( "Failed to get player %d" % playerid, True )

	def cmdExec( self, ctx, cmd ):
		"""Execute a BanManager sub command."""

		return mm_utils.exec_subcmd( self.mm, self.__cmds, ctx, cmd )

	def validateBanCdKeyHash( self, cdKeyHash ):
		"""Validates a ban cdkey hash."""
		if cdKeyHash is None or "" == cdKeyHash:
			return self.__config['defaultBanCdKeyHash']

		cdKeyHash = cdKeyHash.strip( '"\' ' )

		# N.B. We could do some extra parsing here

		return cdKeyHash

	def validateBanProfileId( self, profileId ):
		"""Validates a unban reason."""
		if profileId is None:
			profileId = self.__config['defaultBanProfileId']
		elif isinstance( profileId , ( int, long ) ):
			profileId = str( profileId )
		else:
			profileId = profileId.strip( '"\' ' )
			if "" == profileId:
				profileId = self.__config['defaultBanProfileId']

		return profileId

	def validateUnBanReason( self, reason ):
		"""Validates a unban reason."""
		if reason is None:
			reason = self.__config['defaultUnBanReason']
		else:
			reason = reason.strip( '"\' ' )
			if "" == reason:
				reason = self.__config['defaultUnBanReason']

		return reason

	def validateKickReason( self, reason ):
		"""Validates a kick reason."""
		if reason is None:
			reason = self.__config['defaultKickReason']
		else:
			reason = reason.strip( '"\' ' )
			if "" == reason:
				reason = self.__config['defaultKickReason']

		return reason

	def validateBanAddress( self, address ):
		"""Validates a ban address."""
		if address is None or "" == address:
			return self.__config['defaultBanAddress']

		address = address.strip( '"\' ' )

		# N.B. We could do some extra parsing here
		# WARNING: If we do add extra checks here ensure they are compat with unban call to this function

		return address

	def validateBanAddressOrKey( self, key ):
		"""Validates a ban address / cdkey hash."""
		if key is None:
			return None

		key = key.strip( '"\' ' )

		if "" == key:
			return None

		return key

	def validateBanType( self, banType=None ):
		"""Validates a type for a ban."""
		if banType is not None and mm_utils.KickBanType.rcon != banType:
			self.mm.warn( "Unsupported ban type '%d' (using %d instead)" % ( banType, mm_utils.KickBanType.rcon ) )

		return mm_utils.KickBanType.rcon

	def validateBanPeriod( self, banPeriod=None ):
		"""Validates a ban period if anything is wrong returns the defaultBanPeriod."""
		if banPeriod is None or "" == banPeriod:
			# No ban period default to perm
			return self.__config['defaultBanPeriod']

		lowerBanPeriod = banPeriod.lower()
		
		if 'perm' == lowerBanPeriod:
			# Ban for permanently
			return 'Perm'

		elif 'round' == lowerBanPeriod:
			# Ban for this round
			return 'Round'

		if self.__banPeriodRe.search( banPeriod ) is not None:
			# From now or from epoc period
			return banPeriod

		self.mm.warn( "Invalid ban period '%s' detected defaulting to '%s'" % ( banPeriod, self.__config['defaultBanPeriod'] ) )

		return self.__config['defaultBanPeriod']

	def validateBanReason( self, banReason=None ):
		"""Returns a reason for a ban."""
		if banReason is None or "" == banReason:
			return self.__config['defaultBanReason']

		return banReason

	def validatePlayerName( self, playerName=None ):
		"""Returns a reason for a ban."""
		if playerName is None or "" == playerName:
			return self.__config['defaultBanNick']

		return playerName

	def validateBannedBy( self, bannedBy=None ):
		"""Returns a reason for a ban."""
		if bannedBy is None or "" == bannedBy:
			return self.__config['defaultBannedBy']

		return bannedBy

	def validateBanMethod( self, banMethod=None, banKey=None, banAddress=None ):
		"""Returns a method for a ban."""
		if banMethod is None or "" == banMethod:
			banMethod = self.__config['defaultBanMethod']

		if self.mm.isBattleFieldHeroes():
			# BF Heroes only supports key bans now
			if banMethod != mm_utils.BanMethod.key:
				self.mm.warn( "Invalid ban method '%s' detected ( Defaulting to '%s' )" % ( banMethod, mm_utils.BanMethod.key ) )
			return mm_utils.BanMethod.key
		elif banMethod != mm_utils.BanMethod.key and banMethod != mm_utils.BanMethod.address:
			self.mm.warn( "Invalid ban method '%s' detected ( Defaulting to '%s' )" % ( banMethod, mm_utils.BanMethod.key ) )
			banMethod = mm_utils.BanMethod.key

		# Validate the info against the data
		if banKey is None or banKey == self.__config['defaultBanCdKeyHash']:
			# We dont have a ban key
			if banAddress is not None and banAddress != self.__config['defaultBanAddress']:
				# We have a valid address but not key so must be an address ban
				return mm_utils.BanMethod.address

		elif banAddress is None or banAddress == self.__config['defaultBanAddress']:
			# We dont have a ban address
			if banKey is not None and banKey != self.__config['defaultBanCdKeyHash']:
				# We have a valid key but not address so must be an address ban
				return mm_utils.BanMethod.key

		return banMethod

	def validateBanDelay( self, banDelay=None ):
		"""Returns a delay for a ban."""
		if banDelay is None or "" == banDelay:
			return self.__config['defaultBanDelay']

		return banDelay

	def validateKickDelay( self, kickDelay=None ):
		"""Returns a delay for a kick."""
		if kickDelay is None or "" == kickDelay:
			return self.__config['defaultKickDelay']

		return kickDelay

	def saveBanlist( self ):
		"""Write the banlist out."""
		try:
			banFile = open( self.__banFileName, 'w+' )

		except RuntimeError, detail:
			self.mm.error( "Failed to open '%s' (%s)" % ( self.__banFileName, detail ), True )
			return False
		self.writeBanlist( banFile );

		banFile.close()
	
		return True

	def getBanList( self ):
		"""Returns a copy of the banlist."""
		self.__bans.copy()

	def writeBanlist( self, banFile ):
		"""Write the banlist out."""
		banFile.write( "<?xml version=\"1.0\" encoding=\"iso-8859-1\" ?>\n" )
		banFile.write( "<banlist>\n" )
		for key in self.__bans:
			ban = self.__bans[key]
			banFile.write( "	<ban>\n" )
			banFile.write( "		<datetime>%s</datetime>\n" % self.timeString( ban['datetime'] ) )
			banFile.write( "		<nick>%s</nick>\n" % mm_utils.xml_escape( ban['nick'] ) )
			banFile.write( "		<method>%s</method>\n" % ban['method'] )
			banFile.write( "		<period>%s</period>\n" % ban['period'] )
			banFile.write( "		<address>%s</address>\n" % ban['address'] )
			banFile.write( "		<cdkeyhash>%s</cdkeyhash>\n" % ban['cdkeyhash'] )
			banFile.write( "		<profileid>%s</profileid>\n" % ban['profileid'] )
			banFile.write( "		<by>%s</by>\n" % mm_utils.xml_escape( ban['by'] ) )
			banFile.write( "		<reason>%s</reason>\n" % mm_utils.xml_escape( ban['reason'] ) )
			banFile.write( "	</ban>\n" )
		banFile.write( "</banlist>\n" )

		return True

	def __addBan( self, method, nick, period, address, cdkeyhash, profileid, by, reason, datetime, skipSave=False ):
		"""Add a ban."""
		method = self.validateBanMethod( method, cdkeyhash, address )
		ban = {
			'datetime': self.parseDateTime( datetime ),
			'nick': self.validatePlayerName( nick ),
			'method': method,
			'period': self.validateBanPeriod( period ),
			'address': self.validateBanAddress( address ),
			'cdkeyhash': self.validateBanCdKeyHash( cdkeyhash ),
			'profileid': self.validateBanProfileId( profileid ),
			'by': self.validateBannedBy( by ),
			'reason': self.validateBanReason( reason )
		}


		if self.mm.isBattleFieldHeroes():
			# Heroes doesn't support address bans any more
			if mm_utils.BanMethod.address == method:
				# Check for old style cdkeyhash
				if cdkeyhash is None or 'NOT_USING_CD_KEYS_IN_WEST' == cdkeyhash:
					cdkeyhash = profileid
				method = mm_utils.BanMethod.key

		if mm_utils.BanMethod.key == method:
			key = ban['cdkeyhash']
			self.__bans[key] = ban
			host.rcon_invoke( "admin.addKeyToBanList %s %s" % ( ban['cdkeyhash'], ban['period'] ) )

		elif mm_utils.BanMethod.address == ban['method']:
			key = ban['address']
			self.__bans[key] = ban
			host.rcon_invoke( "admin.addAddressToBanList %s %s" % ( ban['address'], ban['period'] ) )

		else:
			self.mm.error( "Invalid banMethod '%s'" % ( banMethod ) )
			return None

		# Setup unban times for from now and epoc period bans
		# Note: we may loose presision here with the casts to int for bf2.Timer but not much we can do
		if 'Round' == ban['period']:
			# Round ban
			self.__roundBans[key] = ban

		elif self.__fromNowRe.search( ban['period'] ) is not None:
			# A from now ban period
			ban_start = ban['datetime']
			self.__unBanTimers[key] = bf2.Timer( self.expireBan, int( ban['period'] ), 1, key )

		elif self.__epocRe.search( ban['period'] ) is not None:
			# A from epoc ban period
			# Check it hasnt already expired
			expires_from_now = float( ban['period'] ) - now
			if expires_from_now < 0:
				# Expired already remove ban
				self.expireBan( key, True )
				return None
			else:
				# Still expires in the future
				self.__unBanTimers[key] = bf2.Timer( self.expireBan, int( expires_from_now ), 1, key )

		self.mm.info( "Banned '%s' (%s:%s) period '%s' by '%s' => '%s'" % ( ban['nick'], ban['profileid'], key, ban['period'], ban['by'], ban['reason'] ) )

		if skipSave or self.saveBanlist():
			return ban

		return None

	def __removeBan( self, ban, unBanReason=None, skipSave=False ):
		"""Unban a player."""
		ban = self.validateBanAddressOrKey( ban )

		if ban is None:
			self.mm.error( "Invalid unban request ( Ban key / address blank )")
			return False

		unBanReason = self.validateUnBanReason( unBanReason )
		self.mm.info( "Removing ban '%s' (%s)" % ( ban, unBanReason ) )

		# N.B. We do this blindly to to ensure that its done
		if not self.mm.isBattleFieldHeroes():
			host.rcon_invoke( "admin.removeAddressFromBanList %s" % ( ban ) )
		host.rcon_invoke( "admin.removeKeyFromBanList %s" % ( ban ) )

		# Remove any unban timer
		if self.__unBanTimers.has_key( ban ):
			self.__unBanTimers[ban].destroy()
			del self.__unBanTimers[ban]

		if self.__bans.has_key( ban ):
			del self.__bans[ban]

			if skipSave:
				return True
			# Persist the banlist
			return self.saveBanlist()
		else:
			self.mm.warn( "Ban '%s' not found" % ban )

		return False

	def banPlayerKey( self, cdKeyHash, banPeriod=None, banReason=None, bannedBy=None, banDateTime=None, skipSave=False ):
		"""Ban a player key for a given period with a reason."""
		cdKeyHash = self.validateBanAddressOrKey( cdKeyHash )

		if cdKeyHash is None:
			self.mm.error( "Invalid ban request ( Key was blank )")
			return False

		if not self.__addBan( mm_utils.BanMethod.key, None, banPeriod, None, cdKeyHash, None, bannedBy, banReason, banDateTime, skipSave ):
			return False

		return True

	def banPlayerAddress( self, address, banPeriod=None, banReason=None, bannedBy=None, banDateTime=None, skipSave=False ):
		"""Ban a player address for a given period with a reason."""
		address = self.validateBanAddressOrKey( address )

		if address is None:
			self.mm.error( "Invalid ban request ( Address was blank )")
			return False

		if not self.__addBan( mm_utils.BanMethod.address, None, banPeriod, address, None, None, bannedBy, banReason, banDateTime, skipSave ):
			return False

		return True

	def expireBan( self, ban, skipSave=False ):
		"""Remove an expired ban on a player."""
		self.__removeBan( ban, 'Expired', skipSave )

	def unbanPlayer( self, ban, unBanReason=None ):
		"""Unban a player."""
		return self.__removeBan( ban, unBanReason )

	def banList( self, ctx ):
		"""Writes the banlist to the passed client context."""
		self.writeBanlist( ctx )

	def clearBanList( self ):
		"""Clears all bans."""
		self.mm.info( "Clearing banlist")
		host.rcon_invoke( "admin.clearBanList" )
		self.__bans = {}
		self.__roundBans = {}
		for timer in self.__unBanTimers:
			self.__unBanTimers[timer].destroy()
		self.__unBanTimers = {}

		return self.saveBanlist()

	def timeString( self, when=None ):
		""" Returns a string representing the current GMT time."""
		if when is None:
			when = time.time()

		return time.strftime( self.__config['dateTimeFormat'], time.gmtime( when ) )

	def parseDateTime( self, when ):
		""" Returns a float representing UTC time in seconds since the epoch."""
		if when is None:
			return time.time()

		try:
			# Try the current configured dateTimeFormat
			return time.mktime( time.strptime( when, self.__config['dateTimeFormat'] ) )
		except:
			try:
				# Try the old dateTimeFormat
				return time.mktime( time.strptime( when, self.__config['oldDateTimeFormat'] ) )
			except:
				# All failed return the current time
				self.mm.error( "Failed to parse datetime '%s' (using current time)" % when )
				return time.time()

	def banPlayer( self, player, banReason=None, banPeriod=None, banType=None, banMethod=None, bannedBy=None, banDelay=None ):
		"""Ban a player for a given period with a reason."""
		if self.__banTimers.has_key( player.index ):
			# We already have a ban scheduled for this player
			self.mm.warn( "Ban failed ( Ban already in progress for player %d )" % ( player.index ) )	
			return False

		# N.B. We store a copy of key player info in case they leave before the ban activates
		try:
			player_name = player.getName()
		except RuntimeError:
			# player has already left?
			player_name = None

		try:
			player_profileid = player.getProfileId()
		except RuntimeError:
			# player has already left?
			player_profileid = self.validateBanProfileId( None )

		try:
			player_address = player.getAddress()
		except RuntimeError:
			# player has already left?
			player_address = None

		cdkeyhash = self.validateBanCdKeyHash( mm_utils.get_cd_key_hash( player ) )
		player_address = self.validateBanAddress( player_address )
		player.mmBanDetails = {
			'reason': self.validateBanReason( banReason ),
			'period': self.validateBanPeriod( banPeriod ),
			'type' : self.validateBanType( banType ),
			'method': self.validateBanMethod( banMethod, cdkeyhash, player_address ),
			'by': self.validateBannedBy( bannedBy ),
			'name': self.validatePlayerName( player_name ),
			'profileid': player_profileid,
			'address': player_address,
			'cdkeyhash': cdkeyhash 
		}

		if mm_utils.BanMethod.key == player.mmBanDetails['method']:
			if player.mmBanDetails['cdkeyhash'] is None:
				# Can't ban this player: Ban by cdkeyhash and no cdkeyhash information
				self.mm.error( "Ban failed ( Unable to determine cdkeyhash for player %d '%s' )" % ( player.index, player_name ) )	
				return False

		elif mm_utils.BanMethod.address == player.mmBanDetails['method']:
			if player.mmBanDetails['address'] is None:
				# Can't ban this player: Ban by address and no address information
				self.mm.error( "Ban failed ( Unable to determine address for player %d '%s' )" % ( player.index, player_name ) )	
				return False

		banDelay = self.validateBanDelay( banDelay )

		if 0 != banDelay:
			msg = self.__config['banMessage'] % ( player.mmBanDetails['name'], player.mmBanDetails['reason'] )
			mm_utils.msg_player( player.index, msg )

			self.__banTimers[player.index] = bf2.Timer( self.banPlayerNow, banDelay, 1, player )
		else:
			self.banPlayerNow( player )

	def banPlayerNow( self, player=None, banReason=None, banPeriod=None, banType=None, banMethod=None, bannedBy=None ):
		"""Ban a player."""
		try:
			if not hasattr( player, 'mmBanDetails' ):
				# Not comming from banPlayer
				try:
					player_name = player.getName()
				except RuntimeError, detail:
					# player has already left
					player_name = None

				try:
					player_profileid = player.getProfileId()
				except RuntimeError, detail:
					# player has already left
					player_profileid = self.validateBanProfileId( None )

				try:
					player_address = player.getAddress()
				except RuntimeError, detail:
					# player has already left
					player_address = None

				cdkeyhash = self.validateBanCdKeyHash( mm_utils.get_cd_key_hash( player ) )
				player_address = self.validateBanAddress( player_address )
				player.mmBanDetails = {
					'reason': self.validateBanReason( banReason ),
					'period': self.validateBanPeriod( banPeriod ),
					'type' : self.validateBanType( banType ),
					'method': self.validateBanMethod( banMethod, cdkeyhash, player_address ),
					'by': self.validateBannedBy( bannedBy ),
					'name': self.validatePlayerName( player_name ),
					'profileid': player_profileid,
					'address': player_address,
					'cdkeyhash': cdkeyhash
				}
			else:
				# Check the details have been validated
				player.mmBanDetails['reason'] = self.validateBanReason( player.mmBanDetails['reason'] )
				player.mmBanDetails['period'] = self.validateBanPeriod( player.mmBanDetails['period'] )
				player.mmBanDetails['by'] = self.validateBannedBy( player.mmBanDetails['by'] )
				player.mmBanDetails['type'] = self.validateBanType( player.mmBanDetails['type'] )
				player.mmBanDetails['name'] = self.validatePlayerName( player.mmBanDetails['name'] )
				player.mmBanDetails['cdkeyhash'] = self.validateBanCdKeyHash( player.mmBanDetails['cdkeyhash'] )
				player.mmBanDetails['address'] = self.validateBanAddress( player.mmBanDetails['address'] )
				player.mmBanDetails['method'] = self.validateBanMethod( player.mmBanDetails['method'], player.mmBanDetails['cdkeyhash'], player.mmBanDetails['address'] )

			# Remove the ban timer
			if self.__banTimers.has_key( player.index ):
				self.__banTimers[player.index].destroy()
				del self.__banTimers[player.index]

			# Check we have enough info to ban this player
			if mm_utils.BanMethod.key == player.mmBanDetails['method']:
				if player.mmBanDetails['cdkeyhash'] is None:
					# Can't ban this player: Ban by cdkeyhash and no cdkeyhash information
					self.mm.error( "Ban failed ( Unable to determine cdkeyhash for player %d '%s' )" % ( player.index, player.mmBanDetails['name'] ) )	
					return False

			elif mm_utils.BanMethod.address == player.mmBanDetails['method']:
				if player.mmBanDetails['address'] is None:
					# Can't ban this player: Ban by address and no address information
					self.mm.error( "Ban failed ( Unable to determine address for player %d '%s' )" % ( player.index, player.mmBanDetails['name'] ) )	
					return False

			ban = self.__addBan(
				player.mmBanDetails['method'],
				player.mmBanDetails['name'],
				player.mmBanDetails['period'],
				player.mmBanDetails['address'],
				player.mmBanDetails['cdkeyhash'],
				player.mmBanDetails['profileid'],
				player.mmBanDetails['by'],
				player.mmBanDetails['reason'],
				None
			)

			# Workaround for early connection bans not working
			if player.mmBanDetails['profileid'] != self.validateBanProfileId( None ):
				# valid profileid
				try:
					if player.mmBanDetails['profileid'] == player.getProfileId():
						# Yep still the same player so kick them
						host.rcon_invoke( "admin.kickPlayer %d" % ( player.index ) )

				except RuntimeError:
					# Player has already left
					pass

			if ban is None:
				return False

		except Exception, detail:
			self.mm.error( "Error (%s)" % ( detail ), True )
			return False

		return True

	def kickPlayer( self, player, kickReason=None, kickDelay=None, kickType=mm_utils.KickBanType.rcon ):
		"""Kick a player with a reason."""
		if self.__kickTimers.has_key( player.index ):
			# Already scheduled for a kick
			self.mm.warn( "Kick failed ( Kick already in progress for player %d )" % ( player.index ) )	
			return False

		if kickType != mm_utils.KickBanType.rcon:
			self.mm.warn( "Unsupported kick type '%d' (using %d instead)" % ( kickType, mm_utils.KickBanType.rcon ) )
			kickType = mm_utils.KickBanType.rcon

		try:
			player_name = player.getName()
		except RuntimeError:
			# player has already left?
			player_name = self.validatePlayerName( None )

		# Rcon kick method
		kickDelay = self.validateKickDelay( kickDelay );
		kickReason = self.validateKickReason( kickReason )
		msg = self.__config['kickMessage'] % ( player_name, kickReason );
		mm_utils.msg_player( player.index, msg )
		player.mmKickReason = kickReason
		player.mmKickType = kickType
		self.__kickTimers[player.index] = bf2.Timer( self.kickPlayerNow, kickDelay, 1, player )

		return True

	def kickPlayerNow( self, player, kickType=None ):
		"""Kick a player."""
		if kickType is None:
			if not hasattr( player, 'mmKickType' ):
				kickType = mm_utils.KickBanType.rcon
			else:
				kickType = player.mmKickType				

		if kickType != mm_utils.KickBanType.rcon:
			mm.warn( "Unsupported kick type '%d' (using %d instead)" % ( kickType, mm_utils.KickBanType.rcon ) )

		if self.__kickTimers.has_key( player.index ):
			self.__kickTimers[player.index].destroy()
			del self.__kickTimers[player.index]

		# Log the kick
		if hasattr( player, 'mmKickReason' ):
			reason = self.validateKickReason( player.mmKickReason )			
		else:
			reason = self.validateKickReason( None )

		self.mm.info( "Kicked '%s'[%d] => '%s'" % ( player.getName(), player.getProfileId(), reason ) )

		# Kick the player
		host.rcon_invoke( "admin.kickPlayer %d" % ( player.index ) )

	def onGameStatusChanged( self, status ):
		"""Removes old round bans."""
		try:
			if bf2.GameStatus.PreGame == status:
				# Starting a new round remove old round bans
				for banKey in self.__roundBans:
					self.expireBan( banKey, True )

				self.__roundBans = {}

				self.saveBanlist()

			# BF2 reloads banlist.con from disk on change so correct what its got by clearing
			# and reloading our banlist
			host.rcon_invoke( "admin.clearBanList" )

			by_key = mm_utils.BanMethod.key
			for banKey in self.__bans:
				ban = self.__bans[banKey]
				if by_key == ban['method']:
					host.rcon_invoke( "admin.addKeyToBanList %s %s" % ( ban['cdkeyhash'], ban['period'] ) )
				else:
					host.rcon_invoke( "admin.addAddressToBanList %s %s" % ( ban['address'], ban['period'] ) )

		except Exception, details:
			self.mm.error( "Oooops: %s" % details, True )

	def onPlayerDisconnect( self, player ):
		"""Remove any kicks scheduled for this player."""
		if 1 != self.__state:
			return 0

		# Note: we dont remove bans scheduled for this player as they will be successful
		# Players cant be kicked once they have left so destroy if it exists
		if self.__kickTimers.has_key( player.index ):
			self.__kickTimers[player.index].destroy()
			del self.__kickTimers[player.index]

	def loadBans( self ):
		"""Load the server bans."""
		if not mm_utils.fileexists( self.__banFileName ):
			self.mm.info( "Importing legacy ban information" )
			# We dont currently have a ban file so check for legacy bans
			# read in server bans
			# N.B. these will be overwritten later if we have full information about them
			ban_re = re.compile( '(Key|AccountId):\s+(\S+)\s+(\S+)' )
			for line in host.rcon_invoke( 'admin.listBannedKeys' ).split( '\n' ):
				line = line.strip()
				match = ban_re.search( line )
				if match is not None:
					cdkeyhash = self.validateBanCdKeyHash( match.group(2) )
					self.__addBan( mm_utils.BanMethod.key, None, match.group(3), None, cdkeyhash, None, None, None, None, True )
				elif line:
					self.mm.error( "BanManager: Unknown ban format '%s'" % line )

			if not self.mm.isBattleFieldHeroes():
				ban_re = re.compile( 'IP:\s+(\S+)\s+(\S+)' )
				for line in host.rcon_invoke( 'admin.listBannedAddresses' ).split( '\n' ):
					line = line.strip()
					match = ban_re.search( line )
					if match is not None:
						address = self.validateBanAddress( match.group(1) )
						self.__addBan( mm_utils.BanMethod.address, None, match.group(2), address, None, None, None, None, None, True )
					elif line:
						self.mm.error( "BanManager: Unknown ban format '%s'" % line )
		else:
			# Clear all legacy bans
			host.rcon_invoke( "admin.clearBanList" )

		# Ensure the ban file exists
		# Note: we dont use 'r' and test for errno.ENOENT as that may be incorrect
		# if a subdir doesnt exist
		try:
			banFile = open( self.__banFileName, 'a+' )

		except RuntimeError, detail:
			self.mm.error( "Failed to open '%s' (%s)" % ( self.__banFileName, detail ), True )
			return False

		banFile.close()

		# Load the bans from our file
		try:
			banFile = open( self.__banFileName, 'r' )

		except RuntimeError, detail:
			self.mm.error( "Failed to open '%s' (%s)" % ( self.__banFileName, detail ), True )
			self.banFile = None
			return None

		ban_re = re.compile( r'<(?P<tag>datetime|nick|method|period|address|cdkeyhash|profileid|by|reason)>(.*)</(?P=tag)>' )

		by_key = mm_utils.BanMethod.key

		for line in banFile:
			line = line.strip()
			if "<ban>" == line:
				# a ban entry
				ban = {}

			elif "<?xml version=\"1.0\" encoding=\"utf-8\" ?>" == line:
				# header ignore
				pass
			elif "<?xml version=\"1.0\" encoding=\"iso-8859-1\" ?>" == line:
				# header ignore
				pass
			elif "<banlist>" == line:
				# start root item ignore
				pass
			elif "</banlist>" == line:
				# end root item ignore
				pass
			else:
				match = ban_re.search( line )
				if match is not None:
					ban[match.group(1)] = mm_utils.xml_unescape( match.group(2) )

				elif "</ban>" == line and ban.has_key( 'method' ):
					# Add ban to the server ban

					if not ban.has_key( 'cdkeyhash' ):
						ban['cdkeyhash'] = None;

					if not ban.has_key( 'address' ):
						address = None

					if not ban.has_key( 'reason' ):
						ban['reason'] = None

					if not ban.has_key( 'period' ):
						ban['period'] = None

					if not ban.has_key( 'method' ):
						ban['method'] = None

					if not ban.has_key( 'by' ):
						ban['by'] = None

					if not ban.has_key( 'nick' ):
						ban['nick'] = None

					if not ban.has_key( 'profileid' ):
						ban['profileid'] = None

					if not ban.has_key( 'datetime' ):
						ban['datetime'] = None

					self.__addBan( ban['method'], ban['nick'], ban['period'], ban['address'], ban['cdkeyhash'], ban['profileid'], ban['by'], ban['reason'], ban['datetime'], True )
				else:
					self.mm.error( "BanManager: Unexpected line '%s'" % line )

		banFile.close()

		# bans may have been updated from the server so write them out
		return self.saveBanlist()

	def init( self ):
		"""Provides default initialisation."""

		# Load the configuration
		self.__config = self.mm.getModuleConfig( configDefaults )
		self.__banFileName = self.mm.configPath() + '/' + self.__config['banFilename']

		# Load the bans
		self.loadBans()

		# Register our base handlers
		host.registerGameStatusHandler( self.onGameStatusChanged )

		# Register our rcon command handlers
		self.mm.registerRconCmdHandler( 'bm', { 'method': self.cmdExec, 'subcmds': self.__cmds, 'level': 1 } )

		if 0 == self.__state:
			host.registerHandler( 'PlayerDisconnect', self.onPlayerDisconnect, 1 )

		# Register your game handlers and provide any
		# other dynamic initialisation here

		# Update to the running state
		self.__state = 1

	def shutdown( self ):
		"""Shutdown and stop processing."""

		# Unregister game handlers and do any other
		# other actions to ensure your module no longer affects
		# the game in anyway

		# Unregister our game handlers
		host.unregisterGameStatusHandler( self.onGameStatusChanged )
		self.mm.unregisterRconCmdHandler( 'bm' )

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
	return BanManager( modManager )

