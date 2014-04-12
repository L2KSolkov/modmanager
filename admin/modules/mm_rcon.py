# vim: ts=4 sw=4 noexpandtab
"""Battlefield 2 -- ModManager remote console module.

===== Config =====
 # The port to enable rcon on
 mm_rcon.rconPort 4711
 
 # The IP to listen on
 mm_rcon.rconIp "0.0.0.0"
 
 # The basic admin password
 mm_rcon.rconBasicPassword ""
 
 # The super admin password
 mm_rcon.rconPassword ""
 
 # The depth of the listen queue to use
 mm_rcon.rconListenQueue 5
 
 # Allow batching
 mm_rcon.allowBatching 1
 
 # Enable port lingering
 mm_rcon.enableLinger 0
  
 # The level a user gets when using the rconBasicPassword
 mm_rcon.basicAuthLevel 50
 
 # The level a user gets when using the rconPassword ( super password )
 mm_rcon.superAuthLevel 100
 
 # Log all rcon commands executed by admins at info level ( disabled by default )
 mm_rcon.logCommands 0
 
 # The time to linger for
 mm_rcon.lingerFor 1
 
 # Enable Address / port reuse
 mm_rcon.reuseAddress 1
 
 # The message to broadcast when a player becomes admin ( rcon login <password> )
 mm_rcon.loginMessage "Player '%s' became a server administrator"
 
 # The message to broadcast when a player give up admin ( rcon logout )
 mm_rcon.logoutMessage "Player '%s' gave up administrator rights"
 
 # Lock settings so they cant be changed from their initial values
 mm_rcon.addLockedSetting "sv.coopBotCount"
 
 # Restrict gametypes so they cant be used
 mm_rcon.addRestrictedGametype "bf2.gpm_coop"
 
 # Enable advanced map size validation via map.desc files
 # This is disabled by default as custom maps often have invalid .desc files
 mm_rcon.advancedMapSizeValidation 0

===== Rcon commands =====
 # Authenticate with the server must be called before using any other methods
 # for players the parameter is the password for rcon users this is the
 # password hash generated using the given salt
 login <password|password_hash>
 
 # Logout of rcon, this removes all the users privaledges
 logout
 
 # List the rcon users
 users
 
 # Execute a console command
 exec
  
 # Kick a player from the server with a message
 kick <playerid> "<reason>"
  
 # Ban a player from the server with a message
 ban <playerid> "<reason>"
 
 # Ban a player for a specified timer period from the server with a message.
 banby <playerid> <bannedby> <period> "<reason>"
 
 # Display the current banlist
 banlist
 
 # Clear the current banlist
 clearbans
 
 # Unban a player with an optional reason.
 unban <address|cdkey> "<reason>"
 
 # List the players on the server
 list
 
 # Prints your profileid ( in game only )
 profileid
 
 # Print a list of players and their profileid's
 profileids
  
 # Display help, if a command is named detailed help is displayed on
 # just this command
 help [command]
 
 # Change to a specific map gametype and optional size
 map <map> <gametype> [<size>]

===== Enhancements =====
* ModManager compatible
* Optimised update()
* Added IP and Listen queue options
* Added dynamic handlers to enable flexible expansion for:
** Commands
** Authentication.
** Authentication notification
** Client Connect
** Client Disconnect
* Added interactive command help
* Added sub command framework
* Added an additional logout command
* Now sets linger and reuse on the listen socket
* Added DOS repetative connect protection
* Added player admin login / logout broadcast
* Single install, multi server friendly ( for GSP's )

===== Notes =====
* Don't disable reuseAddress ( set to 0 ) as this can cause rcon to stop responding
* Set loginMessage / logoutMessage to "" to disable them

===== Original Info =====

This is a very simple, TCP based remote console which does simple MD5 digest
password authentication. It can be configured via the admin/default.cfg file.
Recognized options are 'port' and 'password'.

Implementation guidelines for this file (and for your own rcon modules):

- All socket operations MUST be non-blocking. If your module blocks on a  socket the game server will hang.

- Do as little work as possible in update() as it runs in the server main loop.

Other notes:

- To get end-of-message markers (0x04 hex) after each reply, begin your
  commands with an ascii 0x02 code. This module will then append the
  end-of-message marker to all results. This is useful if you need to wait
  for a complete response.

===== History =====
 v8.7 - 15/05/2013
 Fixed typo
 
 v8.6 - 14/05/2013
 Added dependant_day_night for Heroes
 
 v8.5 - 29/01/2013
 Added compatibility for long values

 v8.4 - 11/12/2012
 Added ruin_snow for Heroes

 v8.3 - 10/12/2012
 Added karkand_rush for P4F

 v8.2 - 22/10/2012
 Added new gametype to Play4Free
 
 v8.1 - 19/09/2012
 Corrected spelling of dependant_day
 
 v8.0 - 17/07/2012
 Added dependent_day to Heroes

 v7.13 - 17/07/2012
 Added ruin_day to Heroes

 v7.12 - 21/06/2012
 Added river to Heores
 
 v7.11 - 24/05/2012
 Added Trail to Play 4 Free
 
 v7.10 - 17/04/2012
 Added Lunar Landing to Heroes

 v7.9 - 23/02/2012
 Added Mashtuur City to Play 4 Free

 v7.8 - 24/01/2012
 Added royal_rumble_day to Battlefield Heroes

 v7.7 - 13/12/2011
 Added royal_rumble_snow to Battlefield Heroes

 v7.6 - 08/12/2011
 Added dalian_plant to Battlefield Play 4 Free

 v7.5 - 21/11/2011:
 Added CTF gametype to Battlefield Heroes
 
 v7.4 - 18/10/2011:
 Added royal_rumble for Battlefield Heroes

 v7.3 - 10/08/2011:
 Added Dragon Valley for Battlefield Play 4 Free

 v7.2 - 06/07/2011:
 Added wicked_wake for Battlefield Hereos

 v7.1 - 09/06/2011:
 Added Basra (downtown) for Battlefield Play 4 Free
 
 v7.0 - 31/03/2011:
 Added Sharqi for Battlefield Play 4 Free
 
 v6.9 - 28/03/2011:
 Re-added woodlands to Battlefield Heroes

 v6.8 - 28/02/2011:
 Added gulf_of_oman to BFP4F

 v6.7 - 12/10/2010:
 Added BFP4F Support

 v6.6 - 25/11/2010:
 Added the new official christmas maps to Battlefield Heroes

 v6.5 - 07/09/2010:
 Added the new official map Molokai to Battlefield 2142

 v6.4 - 07/09/2010:
 Added the new official map woodlands to Battlefield Heroes

 v6.3 - 19/04/2010:
 Added the new official map ruin and new gametype gpm_hoth to Battlefield Heroes

 v6.2 - 26/01/2010:
 Added the new official maps smack2_night, seaside_skirmish_night and lake_night to Battlefield Heroes

 v6.1 - 12/11/2009:
 Added the new official map mayhem to Battlefield Heroes

 v6.0 - 12/10/2009:
 Added the new official Battlefield 2142 maps

 v5.9 - 01/10/2009:
 Added the new official Battlefield heroes map heat

 v5.8 - 15/06/2009:
 Made maplist checks case insensitive
 
 v5.7 - 03/06/2009:
 Added smack2 map to list of ranked server maps for Heroes
 
 v5.6 - 03/06/2009:
 Changed maplist.listAvailable to maplist.listAll to match bfheroes release
 
 v5.5 - 31/05/2009:
 Added listlocked command to support better user interaction in bfhcc
 
 v5.4 - 13/01/2009:
 Added Heroes support and removed duplicate maps in bf2
 Added maplist.listavailable support method for bfhcc

 v5.3 - 01/05/2008:
 Added new v1.50 maps wake_island_2142 and operation_shingle

 v5.2 - 01/07/2007:
 Fixed an issue mapValidateSize of coop / none standard gametypes
 
 v5.1 - 26/06/2007:
 Added Highway Tampa to the ranked map list
 Exposed kickPlayer, banPlayer and banPlayerId for use with IGA
 
 v5.0 - 22/06/2007:
 Fixed a bug in map list validation which would prevent invalid maps from being removed
 
 v4.9 - 31/05/2007:
 Fix for authedAllowed being not defined in some situations
 
 v4.8 - 08/12/2006:
 Added the new maps for Northern Front

 v4.7 - 08/12/2006:
 Enhanced mapRun to support None gametype / size parameters
 
 v4.6 - 03/11/2006:
 Kick and Ban handlers now support player names as well as player id's

 v4.5 - 27/10/2006:
 Enhanced mapRun to deal with mixed up case maps and gametype.
 
 v4.4 - 17/10/2006:
 map and admin.runLevel commands now return OK to the rcon client
 N.B. No error checking is possible as the underlying rcon commands produce no output.
 
 v4.3 - 10/10/2006:
 Corrected error in maplist.append processing
 
 v4.2 - 10/10/2006:
 Added basic and advanced map size validation. Advanced via map.desc is disabled by default

 v4.1 - 04/10/2006:
 Added run map ability which enhances the way bf2142 implements admin.runLevel as well as adding it to BF2
 Added rcon command: map <map> <gametype> [<size>]
 Added enhanced map management functions which enables maplist.XXXX commands to behave as expected
 
 v4.0 - 29/10/2006:
 Fixed unregister call which now gets called by bf2142
 
 v3.9 - 19/09/2006:
 Added logged warning messages for important failures of rcon commands
 
 v3.8 - 18/09/2006:
 Added 2142 maps
 
 v3.7 - 30/08/2006:
 Added supported games

 v3.6 - 16/08/2006:
 Added verdun official 2142 map
 Added 2142 compatibility

 v3.5 - 04/07/2006:
 Added road_to_jalalabad offical map

 v3.4 - 20/05/2006:
 Added Armored Fury maps to the official map list
 Added lockedSettings config option which allows admins to lock settings from being changed
 Added allowedGametypes config option which allows admins to restrict the gametypes that can be played
 Added modDir helper method
 
 v3.3 - 24/03/2006:
 Enhanced error catching

 v3.2 - 22/02/2006:
 Now uses banmanager.kickPlayer hence requires MM v1.2
 Changed authed message format to be more prominent
 Kick and Ban methods now use advanced argument parsing which supports quoted and arguments
 
 v3.1 - 19/02/2006:
 Updated parameter list for admin.removeAddressFromBanList and admin.removeKeyFromBanList
 Added number argument validation checks to exec overridden methods
 Both admin.removeAddressFromBanList and admin.removeKeyFromBanList now return an error string if the remove failed
 
 v3.0 - 15/02/2006:
 Now correctly deals with admin.addAddressToBanList and admin.addKeyToBanList including an extended 3rd argument "reason"
 Fixed admin.banplayer ban type
 exec admin.banPlayer and exec admin.banPlayerKey now support an extended 3rd argument "reason"
 Added banby rcon command which takes a parameter denoting who did the ban
 Unban now takes an optional reason

 v2.9 - 13/02/2006:
 Error case trap for connection reset added
 Added banlist rcon method
 Added clearbans rcon method
 Added unban rcon method
 Updated ranked restricted maps for BF2 v1.2 patch
 
 v2.8 - 05/02/2006:
 Added maplist rcon command which has a low auth level for use with bf2cc
 
 v2.7 - 02/02/2006:
 Now uses the Ban Manager for baning players

 v2.6 - 28/11/2005:
 Fix for errors on accept causing rcon to stop functioning
 
 v2.5 - 17/11/2005:
 Added Special Forces official Maps

 v2.4 - 06/10/2005:
 Fixed logCommands option
 
 v2.3 - 04/10/2005:
 Added new offcial map
 
 v2.2 - 22/09/2005:
 Added rcon methods profileid and profileids. N.B. profileid is an unauthed method
 
 v2.1 - 20/09/2005:
 Fix for BF2CC maplist management ( strips quotes from map names )
 
 v2.0 - 18/08/2005:
 Added log option for all commands used
 Added checks for official maps on ranked servers
 Added flush on DOS disconnects
 
 v1.9 - 17/08/2005:
 Corrected unauthorised message print
 Extra security checks now prevent the use of blank passwords
 Fixed users command


 v1.8 - 12/08/2005:
 If both basic and super passwords are the same the user is authed
 with at super level
 
 v1.7 - 30/07/2005:
 Added crash protection against long game.sayAll and game.sayTeam
 Added multi level authentication support
 Added standard kick, ban and player list rcon methods

 v1.6 - 30/07/2005:
 Added DOS protection
 Updated logout / login messages

 v1.5 - 26/07/2005:
 Command help format updated
 Added server broadcast messages for player login / logout
 Updated documentation

 v1.4 - 27/06/2005:
 Security logout issue fixed

 v1.3 - 25/06/2005:
 Additional error checking to prevent crashes.

 v1.2 - 22/06/2005:
 Various optimisations

 v1.1 - 20/06/2005:
 Updated to ModManager format

 v1.0:
 Based of the default remote console module by:
 Copyright (c)2004 Digital Illusions CE AB
 Author: Andreas `dep' Fredriksson
"""

import mm_utils
import socket
import errno
import types
import md5
import string
import random
import struct
import sys
import host
import bf2
import re

__version__ = 8.5

__required_modules__ = {
	'modmanager': 1.6
}

__supports_reload__ = False

__supported_games__ = {
	'bf2': True,
	'bf2142': True,
	'bfheroes': True,
	'bfp4f': True
}

__description__ = "ModManager Rcon v%s" % __version__

__all__ = [
	# Module specific options
	"rconPort",
	"rconIp",
	"rconBasicPassword",
	"rconPassword",
	"rconListenQueue",
	"allowBatching",
	"enableLinger",
	"reuseAddress",
	"basicAuthLevel",
	"superAuthLevel",
	"logCommands",

	# Module specific methods
	"registerCmdHandler",
	"unregisterCmdHandler",
	"registerAuthHandler",
	"unregisterAuthHandler",
	"registerAuthedHandler",
	"unregisterAuthedHandler",
	"registerConnectHandler",
	"unregisterConnectHandler",
	"registerDisconnectHandler",
	"unregisterDisconnectHandler",

	# ModManager methods
	"mm_load",
]

__cmd_login__ = 'login'
__cmd_logout__ = 'logout'
__cmd_users__ = 'users'
__cmd_exec__ = 'exec'
__cmd_kick_player__ = 'kick'
__cmd_ban_player__ = 'ban'
__cmd_ban_player_by__ = 'banby'
__cmd_ban_list__ = 'banlist'
__cmd_unban__ = 'unban'
__cmd_clear_bans__ = 'clearbans'
__cmd_profileid__ = 'profileid'
__cmd_list_players__ = 'list'
__cmd_list_player_profiles__ = 'profileids'
__cmd_maplist__ = 'maplist'
__cmd_map__ = 'map'
__cmd_list_locked_settings__ = 'listlocked'
__cmd_help__ = 'help'

__help_cmds__ = [ __cmd_help__, '?', '' ]

__builtin_cmds__ = [
	__cmd_login__,
	__cmd_logout__,
	__cmd_users__,
	__cmd_exec__,
	__cmd_kick_player__,
	__cmd_ban_player__,
	__cmd_ban_player_by__,
	__cmd_ban_list__,
	__cmd_unban__,
	__cmd_clear_bans__,
	__cmd_profileid__,
	__cmd_list_players__,
	__cmd_list_player_profiles__,
	__cmd_maplist__,
	__cmd_map__,
	__cmd_list_locked_settings__,
	__cmd_help__
]

configDefaults = {
	#
	# Rcon settings
	#
	'rconPort': 4711,
	'rconIp': '0.0.0.0',
	'rconBasicPassword': '',
	'rconPassword': '',
	'rconListenQueue': 5,
	'allowBatching': 1,
	'enableLinger': 0,
	'lingerFor': 1,
	'reuseAddress': 1,
	'superAuthLevel': 100,
	'basicAuthLevel': 50,
	'logCommands': 0,
	'loginMessage': "%s became a server administrator",
	'logoutMessage': "%s gave up administrator rights",
	'lockedSettings': [],
	'restrictedGametypes': [],
	'defaultGametype': 'gpm_cq',
	'advancedMapSizeValidation': 0,
}


# The server itself.
class AdminServer(object):
	"""Core Rcon server."""
	def __init__( self, modManager ):
		"""Create an Rcon server listerning on the requested port."""
		self.mm = modManager
		self.__config = modManager.getModuleConfig( configDefaults )
		self.__validatedMapList = False
		self.__lockedSettings = {}
		self.__restrictedGametypes = {}
		self.__game = self.mm.getGameString()
		self.__nextLevel = None
		self.__tempLevels = []
		self.__mapDetails = {}
		self.__officialMaps = {
			'bf2': {
				'dalian_plant': 1,
				'daqing_oilfields': 1,
				'dragon_valley': 1,
				'fushe_pass': 1,
				'greatwall': 1,
				'gulf_of_oman': 1,
				'highway_tampa': 1,
				'kubra_dam': 1,
				'mashtuur_city': 1,
				'midnight_sun': 1,
				'operation_clean_sweep': 1,
				'operationharvest': 1,
				'operationroadrage': 1,
				'operationsmokescreen': 1,
				'road_to_jalalabad': 1,
				'sharqi_peninsula': 1,
				'songhua_stalemate': 1,
				'strike_at_karkand': 1,
				'taraba_quarry': 1,
				'wake_island_2007': 1,
				'zatar_wetlands': 1,
				'operation_blue_pearl': 1,
			},
			'xpack': {
				'devils_perch': 1,
				'ghost_town': 1,
				'iron_gator': 1,
				'leviathan': 1,
				'mass_destruction': 1,
				'night_flight': 1,
				'surge': 1,
				'warlord': 1,
			},
			'bf2142': {
				'belgrade': 1,
				'bridge_at_remagen': 1,
				'camp_gibraltar': 1,
				'cerbere_landing': 1,
				'fall_of_berlin': 1,
				'highway_tampa': 1,
				'liberation_of_leipzig': 1,
				'minsk': 1,
				'operation_shingle': 1,
				'port_bavaria': 1,
				'shuhia_taiba': 1,
				'sidi_power_plant': 1,
				'suez_canal': 1,
				'tunis_harbor': 1,
				'verdun': 1,
				'wake_island_2142': 1,
				'operation_blue_pearl': 1,
				'yellow_knife': 1,
				'strike_at_karkand': 1,
				'molokai': 1,
			},
			'bfheroes': {
				'lake': 1,
				'seaside_skirmish': 1,
				'village': 1,
				'smack2': 1,
				'heat': 1,
				'mayhem': 1,
				'lake_night': 1,
				'seaside_skirmish_night': 1,
				'smack2_night': 1,
				'ruin': 1,
				'woodlands': 1,
				'smack2_snow': 1,
				'village_snow': 1,
				'woodlands_snow': 1,
				'heat_snow': 1,
				'lake_snow': 1,
				'wicked_wake': 1,
				'royal_rumble': 1,
				'royal_rumble_snow': 1,
				'royal_rumble_day': 1,
				'lunar': 1,
				'river': 1,
				'ruin_day': 1,
				'dependant_day': 1,
				'ruin_snow': 1,
				'dependant_day_night': 1,
			},
			'main': {
				'strike_at_karkand': 1,
				'gulf_of_oman': 1,
				'sharqi': 1,
				'downtown': 1,
				'dragon_valley': 1,
				'dalian_plant': 1,
				'mashtuur_city': 1,
				'trail':1,
				'karkand_rush':1,
			}
		}

		# Parse in locked settings
		for restrict in self.__config['lockedSettings']:
			self.__lockedSettings[restrict.lower()] = 1

		# Parse in restricted gametypes
		for restrict in self.__config['restrictedGametypes']:
			self.__restrictedGametypes[restrict.lower()] = 1

		# Note: We use __var for all our private vars to prevent
		# someone altering them by mistake as python doesnt have
		# any really concept of private member variables

		self.mm.info( "Starting ModManager Rcon v%s on %s:%d" % ( __version__, self.__config['rconIp'], self.__config['rconPort'] ) )

		# contains our current connected clients
		self.__peers = []

		# Note: we use dict's here not list's to prevent duplication
		# and to gives us an easy way to check if the unregisters
		# are in fact valid, although this could be achieved with list.count

		# contains the handlers that want notification of client connections
		self.__connectHandlers = {}

		# contains the handlers that want notification of client disconnections
		self.__disconnectHandlers = {}

		# contains the handlers that can process authentications
		self.__authHandlers = {}

		# contains the handlers that want notification of client auths
		self.__authedHandlers = {}

		# contains clients which have connected
		# The client can be checked to see it they a authed using ctx.authed
		self.__clients = {}

		# rcon commands supported
		self.__cmds = {}

		# rcon commands supported then the user is unauthed ( auth level 0 )
		self.__unauthedCmds = {}

		if not self.__config['allowBatching']:
			self.mm.warn( "Batching disabled, this is not recommended" )

		# open the socket
		self.openSocket()

		# register our built in command handlers
		self.registerCmdHandler( __cmd_login__, { 'method': self.cmdLogin, 'args': '<password|digest>' , 'level': 0 } )
		self.registerCmdHandler( __cmd_logout__, { 'method': self.cmdLogout, 'level': 0 } )
		self.registerCmdHandler( __cmd_users__, { 'method': self.cmdUsers, 'level': 20 } )
		self.registerCmdHandler( __cmd_kick_player__, { 'method': self.kickPlayer, 'args': '<playerid> "<reason>"', 'level': 5 } )
		self.registerCmdHandler( __cmd_ban_player__, { 'method': self.banPlayer, 'args': '<playerid> <period> "<reason>"', 'level': 10 } )
		self.registerCmdHandler( __cmd_ban_player_by__, { 'method': self.banPlayerBy, 'args': '<playerid> <bannedby> <period> "<reason>"', 'level': 10 } )
		self.registerCmdHandler( __cmd_ban_list__, { 'method': self.cmdBanList, 'level': 5 } )
		self.registerCmdHandler( __cmd_unban__, { 'method': self.cmdUnBan, 'args': '<address|cdkeyhash>', 'level': 10 } )
		self.registerCmdHandler( __cmd_clear_bans__, { 'method': self.cmdClearBanList, 'level': 10 } )
		self.registerCmdHandler( __cmd_list_players__, { 'method': self.cmdListPlayers, 'level': 5 } )
		self.registerCmdHandler( __cmd_profileid__, { 'method': self.cmdProfileId, 'level': 0 } )
		self.registerCmdHandler( __cmd_list_player_profiles__, { 'method': self.cmdListPlayerProfiles, 'level': 5 } )
		self.registerCmdHandler( __cmd_list_locked_settings__, { 'method': self.cmdListLockedSettings, 'level': 5 } )
		self.registerCmdHandler( __cmd_maplist__, { 'method': self.cmdMapList, 'level': 5 } )
		self.registerCmdHandler( __cmd_map__, { 'method': self.cmdMap, 'args': '<map> <gametype> [<size>]', 'level': 5 } )
		self.registerCmdHandler( __cmd_exec__, { 'method': self.cmdExec, 'args': '[arg1] [arg2] ... [argn]', 'level': 90 } )
		self.registerCmdHandler( __cmd_help__, { 'method': self.cmdHelp, 'aliases': [ '?' ], 'level': 0 } )

		# register our built in auth methods
		self.registerAuthHandler( self.basicAuth, self.basicAllowed )
		self.registerAuthedHandler( self.clientAuthed )

		# register the fact we are interested in updates
		self.mm.registerUpdates( self.update )

		# All initialisation done
		self.mm.info( "ModManager Rcon started" )

	def modManager( self ):
		"""Return the mod manager."""
		return self.mm

	def rconSuperPassword( self ):
		"""Return our rcon password."""
		return self.__config['rconPassword']

	def rconBasicPassword( self ):
		"""Return our basic rcon password."""
		return self.__config['rconBasicPassword']

	def allowBatching( self ):
		"""Return if batching is allowed."""
		return self.__config['allowBatching']

	def registerCmdHandler( self, cmd, detail ):
		"""Registers a new command handler.

		Valid detail members are:
		method:		The function to call ( mandatory )
		override:	If True then this handler will override any existing handler ( default: True )
		help:		Full help on the command ( default: method.__doc__ )
		desc:		Basic description of the command ( default: 1st line of method.__doc__ )
		args:		Text version of the args supported e.g. <param1> <param2> ( default: '' )
		"""
		if detail.has_key( 'override' ) and detail['override']:
			override = True
		else:
			override = False

		if self.__cmds.has_key( cmd ):
			if not override:
				self.mm.error( "Failed to register command '%s' ( handler already exists )" % cmd, True )
				return 0
			self.mm.info( "Overriding command handler '%s'" % cmd )
		else:
			self.mm.info( "Rcon command handler '%s' registered" % cmd )

		detail = self.__fillCmdDetails( cmd, detail )
		if detail is None:
			# sub command failure
			return 0

		# keep a seperate list of unauthed commands for speed
		if 0 == detail['level']:
			self.__unauthedCmds[cmd] = detail

		self.__cmds[cmd] = detail

		# Add the aliases
		for alias in detail['aliases']:
			if self.__cmds.has_key( alias ):
				if not override:
					self.mm.error( "Failed to register command alias '%s' ( handler already exists )" % alias, True )
					return 0
				self.mm.info( "Overriding command handler '%s' (alias)" % alias )
			else:
				self.mm.info( "Rcon command handler '%s' registered (alias)" % alias )
			self.__cmds[alias] = detail

		return 1

	def __fillCmdDetails( self, cmd, detail ):
		"""Ensure we have all the members."""
		if not detail.has_key( 'method' ):
			self.mm.error( "Failed to register command '%s' ( no method specified )" % cmd, True )
			return None

		handler = detail['method']
		if handler.__doc__:
			default_help = handler.__doc__
			default_desc = handler.__doc__.split( "\n", 1 )[0]
		else:
			if detail.has_key( 'desc' ):
				default_help = detail['desc']
			elif detail.has_key( 'help' ):
				default_desc = detail['help'].split( "\n", 1 )[0]
			else:
				default_help = 'Unknown'
				default_desc = 'Unknown'

		defaults = { 'override': False, 'desc': default_desc, 'help': default_help, 'args': '', 'subcmds': {}, 'aliases': [], 'restricted': 0, 'alias': 0, 'level': 100 }

		for opt in defaults:
			if not detail.has_key( opt ):
				detail[opt] = defaults[opt]

		# recurse
		subcmds = detail['subcmds']
		# use a temporary for aliases to avoid dict size changes
		aliases = {}
		for subcmd in subcmds:
			details = self.__fillCmdDetails( subcmd, subcmds[subcmd] )
			if details is None:
				# Sub command failure
				return None

			subcmds[subcmd] = details
			for alias in details['aliases']:
				# ensure we have a copy and dont alter the original
				alias_details = dict( details )
				alias_details['alias'] = 1
				aliases[alias] = alias_details

		for alias in aliases:
			if subcmds.has_key( alias ):
				self.mm.error( "Failed to register sub command alias '%s' ( handler already exists )" % alias, True )
			else:
				subcmds[alias] = aliases[alias]

		return detail

	def unregisterCmdHandler( self, cmd ):
		"""Unregisters a command handler."""
		if not self.__cmds.has_key( cmd ):
			self.mm.error( "Failed to unregister command '%s' ( unknown handler )" % cmd, True )
			return 0

		del self.__cmds[cmd]

		if self.__unauthedCmds.has_key( cmd ):
			del self.__unauthedCmds[cmd]

		self.mm.debug( 2, "Rcon command handler '%s' unregistered" % cmd )
		return 1

	def registerConnectHandler( self, handler ):
		"""Registers a new connect handler."""
		self.__connectHandlers[handler] = 1
		self.mm.debug( 2, "Rcon connect handler '%s' registered" % mm_utils.method_name( handler ) )
		return 1

	def unregisterConnectHandler( self, handler ):
		"""Unregisters a connect handler."""
		if not self.__connectHandlers.has_key( handler ):
			self.mm.error( "Failed to unregister disconnect '%s' ( unknown handler )" % mm_utils.method_name( handler ), True )
			return 0

		del self.__connectHandlers[handler]
		self.mm.debug( 2, "Rcon connect handler '%s' unregistered" % mm_utils.method_name( handler ) )
		return 1

	def registerDisconnectHandler( self, handler ):
		"""Registers a new disconnect handler."""
		self.__disconnectHandlers[handler] = 1
		self.mm.debug( 2, "Rcon disconnect handler '%s' registered" % mm_utils.method_name( handler ) )
		return 1

	def unregisterDisconnectHandler( self, handler ):
		"""Unregisters a disconnect handler."""
		if not self.__disconnectHandlers.has_key( handler ):
			self.mm.error( "Failed to unregister disconnect '%s' ( unknown handler )" % mm_utils.method_name( handler ), True )
			return 0

		del self.__disconnectHandlers[handler]
		self.mm.debug( 2, "Rcon disconnection handler '%s' unregistered" % mm_utils.method_name( handler ) )
		return 1

	def registerAuthHandler( self, auth_method, check_method ):
		"""Registers a new auth handler."""
		self.__authHandlers[auth_method] = check_method
		self.mm.debug( 2, "Rcon auth handler '%s' registered" % mm_utils.method_name( auth_method ) )
		return 1

	def unregisterAuthHandler( self, handler ):
		"""Unregisters a auth handler."""
		if not self.__authHandlers.has_key( handler ):
			self.mm.error( "Failed to unregister auth '%s' ( unknown handler )" % mm_utils.method_name( handler ), True )
			return 0

		del self.__authHandlers[handler]
		self.mm.debug( 2, "Rcon disconnection auth '%s' unregistered" % mm_utils.method_name( handler ) )
		return 1

	def registerAuthedHandler( self, handler ):
		"""Registers a new authed handler."""
		self.__authedHandlers[handler] = 1
		self.mm.debug( 2, "Rcon auth handler '%s' registered" % mm_utils.method_name( handler ) )
		return 1

	def unregisterAuthedHandler( self, handler ):
		"""Unregisters a authed handler."""
		if not self.__authedHandlers.has_key( handler ):
			self.mm.error( "Failed to unregister authed '%s' ( unknown handler )" % mm_utils.method_name( handler ), True )
			return 0

		del self.__authedHandlers[handler]
		self.mm.debug( 2, "Rcon authed handler '%s' unregistered" % mm_utils.method_name( handler ) )
		return 1

	def onRemoteCommand( self, client, cmd ):
		"""Process a remote request.

		Called when a user types 'rcon ' followed by any string in a client
		console window or when a TCP client sends a complete line to be
		evaluated.
		"""

		interactive = True

		# Is this a non-interactive client?
		if len(cmd) > 0 and cmd[0] == '\x02':
			cmd = cmd[1:]
			interactive = False

		ctx = self.getContext( client )

		( subcmd, args ) = mm_utils.lsplit( cmd.strip(), ' ', 2 )

		# you can only login unless you are authenticated
		if not ctx.authedLevel and not self.__unauthedCmds.has_key( subcmd ):
			ctx.write( "error: not authenticated: you can only invoke the following commands:\n%s\n" % ( ', '.join( self.__unauthedCmds.keys() ) ) )
			self.mm.warn( "Client %s tried to invoke '%s' without auth" % ( ctx.getName(), subcmd ) )
			if ctx.isSocket():
				# DOS protection disconnect them
				ctx.flush( interactive )

				# shutdown the connection
				# Note the calling method will remove the __peer and __client references
				ctx.conn.close( 'DOS protection' )
				return
		else:
			if self.__cmds.has_key( subcmd ):
				cmd_details = self.__cmds[subcmd]
				if self.__unauthedCmds.has_key( subcmd ) or ctx.authedAllowed( ctx, cmd_details ):
					try:
						ctx.currentCmd = cmd
						ctx.currentBaseCmd = subcmd
						if cmd_details['subcmds'] and args in __help_cmds__:
							# Show help on this command
							self.__cmds[__cmd_help__]['method']( ctx, subcmd )
						elif cmd_details['restricted'] and host.ss_getParam('ranked'):
							msg = "Restricted: Sorry command '%s' is not permitted on ranked servers" % subcmd
							self.mm.debug( 1, msg )
							ctx.write( msg )
						else:
							# Run the command
							if self.__config['logCommands']:
								self.mm.info( 'rcon: cmd %s' % cmd )
							cmd_details['method']( ctx, args )
					except Exception, detail:
						msg = "Failed to process command '%s' (%s)" % ( subcmd, detail )
						self.mm.error( msg, True )
						ctx.write( msg )
				else:
					ctx.write( "error: you are not authorised to use the command '%s' it requires level %d you are only level %d\n" % ( subcmd, cmd_details['level'], ctx.authedLevel ) )
					self.mm.warn( "Client %s tried to invoke '%s' without sufficient auth level" % ( ctx.getName(), subcmd ) )
			else:
				msg = "rcon: unknown command: '%s'\n" % subcmd
				self.mm.warn( msg )
				ctx.write( msg )

		if not ctx.authedLevel and ctx.isSocket():
			# DOS protection disconnect them
			ctx.flush( interactive )

			# shutdown the connection
			# Note the calling method will remove the __peer and __client references
			ctx.conn.close( 'DOS protection' )

			return

		# Now send any info created by the command
		ctx.send( interactive )

	def getContext( self, client ):
		"""Return a CommandContext.

		Looks up in the existing authed list and returns.
		If not found creates a new one and returns that
		"""
		if not self.__clients.has_key( client ):
			self.__clients[client] = CommandContext( client )

		return self.__clients[client]

	def onChatMessage(self, playerid, text, channel, flags):
		"""Called whenever a player issues a chat string."""
		self.mm.debug( 3, 'chat: pid=%d text=\'%s\' channel=%s flags=%s' % ( playerid, text, channel, flags ) )

	def openSocket(self):
		"""Set up the listening TCP Rcon socket."""
		try:
			self.__socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
			if self.__config['enableLinger']:
				linger = struct.pack( "ii", self.__config['lingerFor'], 0 )
				self.__socket.setsockopt( socket.SOL_SOCKET, socket.SO_LINGER, linger )
			if self.__config['reuseAddress']:
				self.__socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
			self.__socket.bind( ( self.__config['rconIp'] , self.__config['rconPort'] ) )
			self.__socket.listen( self.__config['rconListenQueue'] )
			self.__socket.setblocking( 0 )
		except Exception, detail:
			self.mm.error( 'Failed to bind rcon socket, only in-game rcon will be enabled (%s)' % detail, True )
			self.__socket = None

	def update( self ):
		"""Process the server update.

		WARNING: update is called very frequently!! Don't go crazy with logic here.
		"""
		if self.__socket is None:
			# No socket, just return
			return

		# without blocking, check for new connections
		try:
			sock, peeraddr = self.__socket.accept()
			peer = AdminConnection( self, sock, peeraddr, self.__game )
			self.__peers.append( peer )

			# inform the connect handlers of the new client
			ctx = CommandContext( peer )
			for handler in self.__connectHandlers:
				try:
					handler( ctx )
				except:
					self.mm.error( "Handler '%s' failed to process connect" % mm_utils.method_name( handler ), True )

		except Exception, detail:
			error = detail[0]
			if errno.EWOULDBLOCK != error and errno.EAGAIN != error:
				self.mm.error( "Rcon accept error (%s)" % detail, True )
				# raising an error here appears to break rcon so we now just continue processing
				#raise socket.error, detail

		# update clients and removing the clients that fail their update
		peers = []
		for peer in self.__peers:
			if peer.update():
				peers.append( peer )
			else:
				self.__removeClientCtx( peer )

		# now keep the remaining clients
		self.__peers = peers

	def onPlayerDisconnect( self, player ):
		"""Remove the disconnecting player."""
		return self.__removeClientCtx( player.index )

	def __removeClientCtx( self, client ):
		"""Remove the auth of a disconnecting player / client.

		When players disconnect, remove them from the auth map if they were
		authenticated so that the next user with the same id doesn't get rcon
		access.
		"""
		self.mm.debug( 1, "Client disconnected informing handlers" )

		ctx = self.getContext( client )

		# delete the closed connection from our clients list
		del self.__clients[client]

		# Note: __peer is cleared by the calling method so we dont need
		# to do anything with it here

		for handler in self.__disconnectHandlers:
			try:
				handler( ctx )
			except:
				self.mm.error( "Handler '%s' failed to process disconnect" % mm_utils.method_name( handler ), True )

	def cmdLogin( self, ctx, cmd ):
		"""Authenticates with the server.

		You must call this before you can use any other commands
		"""
		authed_level = 0
		authed_by = None
		authed_allower = None

		# ask each auth handler in turn to auth the client
		for handler in self.__authHandlers:
			try:
				authed_level = handler( ctx, cmd )
				if authed_level:
					# this handler authed the client
					authed_by = mm_utils.method_name( handler )
					authed_allower = self.__authHandlers[handler]
					break
			except:
				self.mm.error( "Auth handler '%s' failed" % mm_utils.method_name( handler ), True )

		# Update the context
		ctx.authedLevel = authed_level
		ctx.authedBy = authed_by
		ctx.authedAllowed = authed_allower

		# tell each authed handler about the clients new authed status
		for handler in self.__authedHandlers:
			try:
				handler( ctx )
			except:
				self.mm.error( "Handler '%s' failed to process authed" % mm_utils.method_name( handler ), True )

	def cmdLogout( self, ctx, cmd ):
		"""Logout from rcon."""
		ctx.authedLevel = 0
		ctx.authedBy = None
		ctx.authedChecker = None
		ctx.authedAllowed = ctx.notAllowed

		# Set the logout flag so the handlers know whats happening
		ctx.logout = True

		# tell each authed handler about the clients new authed status
		for handler in self.__authedHandlers:
			try:
				handler( ctx )
			except:
				self.mm.error( "Handler '%s' failed to process authed" % mm_utils.method_name( handler ), True )

		# Unset the logout flag
		ctx.logout = False

	def clientAuthed( self, ctx ):
		"""Add the client to the authed list."""
		if ctx.authedLevel:
			# client was successful authed
			self.mm.info( "Authed '%s' by %s at level %d" % ( ctx.getName(), ctx.authedBy, ctx.authedLevel ) )
			ctx.write('Authentication successful, rcon ready.\n')
			if ctx.isInGame() and self.__config['loginMessage']:
				# player logged in inform the players on the server
				mm_utils.msg_server( self.__config['loginMessage'] % ctx.getShortName() )

		elif ctx.logout:
			# client requested logout
			self.mm.info( '%s logged out' % ( ctx.getName() ) )
			ctx.write( 'Logout successful.\n' )
			if ctx.isInGame() and self.__config['logoutMessage']:
				# player logged out inform the players on the server
				mm_utils.msg_server( self.__config['logoutMessage'] % ctx.getShortName() )
		else:
			# client was denied auth by all handlers
			self.mm.warn( "%s failed authentication" % ctx.getName() )
			ctx.write( 'Authentication failed.\n' )

	def basicAuth( self, ctx, cmd ):
		""" Basic authentication handler.

		This authorises a user based on the password set in our config.
		"""

		password = cmd.strip()
		# Note: we dont log failures as there may be more auth handlers
		if ctx.isInGame():
			# We're called by an in-game rcon client, use plain-text password
			# (encoded into bf2 network stream).
			if self.__config['rconPassword'] and password == self.__config['rconPassword']:
				return self.__config['superAuthLevel']
			elif self.__config['rconBasicPassword'] and password == self.__config['rconBasicPassword']:
				return self.__config['basicAuthLevel']

		else:
			# tcp client, require seeded digest to match instead of password
			if password == ctx.conn.superDigest:
				return self.__config['superAuthLevel']
			elif password == ctx.conn.basicDigest:
				return self.__config['basicAuthLevel']

		return 0

	def basicAllowed( self, ctx, details ):
		"""Basic method allowed handler.

		Checks to see if the user is allowed to use the method.
		"""
		if ctx.authedLevel >= details['level']:
			return True
		else:
			return False

	def cmdUsers( self, ctx, cmd ):
		"""List the all logged in rcon users."""

		# Note: we use the original format here to maintain compatibility
		ctx.write('active rcon users:\n')
		for key in self.__clients:
			c = self.__clients[key]
			if c.authedLevel:
				ctx.write( '%s\n' % c.getName() )

	def modDir( self ):
		"""Return the current mod directory"""
		modDirs = str( host.sgl_getModDirectory() ).replace( '\\', '/' ).split( '/' )
		return modDirs[modDirs.__len__() - 1]
		
	def allowMap( self, map_name ):
		"""Return True if the named map is permitted by the ranked mod / map name False otherwise"""
		if host.ss_getParam('ranked'):
			# ranked server validation of maps
			modDir = self.modDir()
			if self.__officialMaps.has_key( modDir ) and self.__officialMaps[modDir].has_key( map_name.lower() ):
				return True
			else:
				return False
		else:
			# unranked allow all maps
			return True

	def restrictedGametype( self, gametype ):
		"""Return True if the gametype is restricted False otherwise"""
		fulltype = "%s.%s" % ( self.modDir(), gametype )
		if self.__restrictedGametypes.has_key( fulltype ):
			return True
		else:
			return False

	def cmdExec( self, ctx, cmd ):
		"""Execute a console command on the server."""
		self.mm.info( "cmdExec '%s' by %s" % ( cmd, ctx.getName() ) )
		try:
			( subcmd, args ) = mm_utils.lsplit( cmd.strip(), ' ', 2 )
			subcmd_orig = subcmd
			subcmd = subcmd.lower()
			if 'game.sayall' == subcmd:

				if args is None or "" == args:
					ctx.write( "Error: Too few arguments, the min no of arguments is 1!\n" )
					return

				# crash protection for long messages
				args = args.strip( '"\' ' )
				if 243 < len( args ):
					self.mm.warn( "Truncating long message '%s'" % args )
					cmd = '%s "%s"' % ( subcmd, args[0:243] )

			elif 'game.sayteam' == subcmd:
				# crash protection for long messages
				( teamid, msg ) = mm_utils.lsplit( args.strip(), ' ', 2 )

				if teamid is None or "" == teamid or msg is None or "" == msg:
					ctx.write( "Error: Too few arguments, the min no of arguments is 2!\n" )
					return

				msg = msg.strip( '"\' ' )
				if 243 < len( msg ):
					self.mm.warn( "Truncating long message '%s'" % msg )
					cmd = '%s %s "%s"' % ( subcmd, teamid, msg[0:243] )

			elif 'admin.banplayerkey' == subcmd:
				# Use the ban manager to ban by key
				( playerid, banPeriod, banReason ) = mm_utils.lsplit( args, None, 3, '' )

				if playerid is None or "" == playerid:
					ctx.write( "Error: Too few arguments, the min no of arguments is 1!\n" )
					return

				playerid = mm_utils.get_int( ctx, playerid, 'playerid' )

				if 0 > playerid:
					ctx.write( 'Player not found.\n' )
					return

				try:
					player = bf2.playerManager.getPlayerByIndex( playerid )

					if player is None:
						ctx.write( 'Player not found.\n' )
					else:
						self.mm.banManager().banPlayer( player, banReason, banPeriod, mm_utils.KickBanType.rcon, mm_utils.BanMethod.key, ctx.getName() )

				except:
					ctx.write( 'Player not found.\n' )
					self.mm.error( "Failed to get player %d" % playerid, True )

				return

			elif 'admin.banplayer' == subcmd:
				# Use the ban manager to ban by ip
				( playerid, banPeriod, banReason ) = mm_utils.lsplit( args, None, 3, '' )

				if playerid is None or "" == playerid:
					ctx.write( "Error: Too few arguments, the min no of arguments is 1!\n" )
					return

				playerid = mm_utils.get_int( ctx, playerid, 'playerid' )

				if 0 > playerid:
					ctx.write( 'Player not found.\n' )
					return

				try:
					player = bf2.playerManager.getPlayerByIndex( playerid )

					if player is None:
						ctx.write( 'Player not found.\n' )
					else:
						self.mm.banManager().banPlayer( player, banReason, banPeriod, mm_utils.KickBanType.rcon, mm_utils.BanMethod.address, ctx.getName() )

				except:
					ctx.write( 'Player not found.\n' )
					self.mm.error( "Failed to get player %d" % playerid, True )

				return

			elif 'admin.addaddresstobanlist' == subcmd:
				# User the ban manager to unban by ip
				# N.B. we support an extended ban reason here
				( address, banPeriod, banReason ) = mm_utils.lsplit( args, None, 3, '' )

				if address is None or "" == address:
					ctx.write( "Error: Too few arguments, the min no of arguments is 1!\n" )
					return

				if banReason is None:
					banReason = 'Unknown (rcon ban)'

				self.mm.banManager().banPlayerAddress( address, banPeriod, banReason, ctx.getName() )
				return

			elif 'admin.addkeytobanlist' == subcmd:
				# User the ban manager to ban by key
				# N.B. we support an extended ban reason here
				( cdkey, banPeriod, banReason ) = mm_utils.lsplit( args, None, 3, '' )

				if cdkey is None or "" == cdkey:
					ctx.write( "Error: Too few arguments, the min no of arguments is 1!\n" )
					return

				if banReason is None:
					banReason = 'Unknown (rcon ban)'

				self.mm.banManager().banPlayerKey( cdkey, banPeriod, banReason, ctx.getName() )
				return

			elif 'admin.removeaddressfrombanlist' == subcmd:
				# User the ban manager to unban by ip
				( ban, msg ) = mm_utils.lsplit( args, None, 2, '' )

				if ban is None or "" == ban:
					ctx.write( "Error: Too few arguments, the min no of arguments is 1!\n" )
					return

				if ban is None or "" == ban:
					ctx.write( "Error: Too few arguments, the min no of arguments is 1!\n" )
					return

				# Note: we dont return anything on success to maintain backwards compatibility
				if not self.mm.banManager().unbanPlayer( ban, msg ):
					ctx.write( "Failed to remove ban ( Ban not found? )" )

				return

			elif 'admin.removekeyfrombanlist' == subcmd:
				# User the ban manager to unban by key
				( ban, msg ) = mm_utils.lsplit( args, None, 2, '' )

				if ban is None or "" == ban:
					ctx.write( "Error: Too few arguments, the min no of arguments is 1!\n" )
					return

				# Note: we dont return anything on success to maintain backwards compatibility
				if not self.mm.banManager().unbanPlayer( ban, msg ):
					ctx.write( "Failed to remove ban ( Ban not found? )" )

				return

			elif 'admin.clearbanlist' == subcmd:
				# User the ban manager to unban by key
				self.mm.banManager().clearBanList()
				return

			elif 'admin.runlevel' == subcmd:
				( map_name, gametype, size ) = mm_utils.largs( args.strip().lower(), ' ', 3, None )

				# Currently BF2 doesnt support this and BF2142's implementation is not optimal so
				# we replace this with an internal implementation
				self.mapRun( ctx, map_name, gametype, size )
				return

			elif 'maplist.remove' == subcmd:
				self.mapRemove( ctx, int( args.strip() ) )
				return

			elif 'maplist.append' == subcmd:
				( map_name, gametype, size ) = mm_utils.largs( args.strip().lower(), ' ', 3, None )
				self.mapAppend( ctx, map_name, gametype, size )
				return

			elif 'maplist.insert' == subcmd:
				( mapid, map_name, gametype, size ) = mm_utils.largs( args.strip().lower(), ' ', 4, None )
				self.mapInsert( self, ctx, int( mapid ), map_name, gametype, size )
				return

			elif 'maplist.clear' == subcmd:
				self.maplistClear( ctx )
				return

			elif 'maplist.listall' == subcmd:
				self.maplistAvailable( ctx )
				return

			elif self.__lockedSettings.has_key( subcmd ):
				if '' != args:
					msg = "Setting %s is locked and can't be changed\n" % subcmd_orig
					ctx.write( msg )
					self.mm.warn( msg )
					return

			ctx.write( host.rcon_invoke( cmd ) )
		except Exception:
			self.mm.error( "Failed to invoke '%s'" % cmd, True )


	def mapGametypeAllowed( self, ctx, map_name, gametype ):
		"""Check to see the the map_name and gametype are allowed."""
		if not self.allowMap( map_name ):
			# A response compatible with the original calls
			ctx.write( "0\n" )
			msg = "Map %s can't be used on a ranked server\n" % map_name
			ctx.write( msg )
			self.mm.warn( msg )
			return False

		elif self.restrictedGametype( gametype ):
			# A response compatible with the original calls
			ctx.write( "0\n" )
			msg = "Gametype '%s' is restricted and can't be used on this server\n" % gametype
			ctx.write( msg )
			self.mm.warn( msg )
			return False

		return True

	def maplistClear( self, ctx=None ):
		"""Clears the maplist, maintaing the details of temporary maps in the process."""
		ret = host.rcon_invoke( 'maplist.clear' )
		if ctx is not None:
			ctx.write( ret )

		self.__tempLevels = []
		self.__nextLevel = None

	def maplistAvailable( self, ctx=None ):
		"""Returns the available maps the maplist, maintaing the details of temporary maps in the process."""

		# Try native support first
		ret = host.rcon_invoke( 'maplist.listall' )
		if not ret.startswith( 'Unknown object or method!' ):
			if ctx is not None:
				ctx.write( ret )
		else:
			# Fall back to internal list
			modDir = self.modDir()
			if self.__officialMaps.has_key( modDir ) and ctx is not None:
				maps = self.__officialMaps[modDir].keys()
				maps.sort()
				for map in maps:
					ctx.write( "%s\n" % map )

	def mapRemove( self, ctx, idx ):
		"""Removes a map from the run list, maintaining the details of temporary maps in the process."""

		next_idx = int( host.rcon_invoke( 'admin.nextLevel' ).strip() )

		ret = host.rcon_invoke( 'maplist.remove %d' % ( idx ) )

		# Tell the rcon user the result
		ctx.write( ret )

		if 0 == int( ret.strip() ):
			return False

		# Ensure we maintain the correct values for the indexes of the maps to be removed
		tempLevels = []
		for i in self.__tempLevels:
			if idx < i:
				tempLevels.append( i - 1 )
			elif idx != i:
				tempLevels.append( i )

		self.__tempLevels = tempLevels

		# Move the nextLevel pointer if needed
		if self.__nextLevel is not None:
			if self.__nextLevel > idx:
				# we removed a level below the next level so decrement it
				self.__nextLevel -= 1

			elif self.__nextLevel == idx:
				# we removed the level which was to be the next level
				# Try to go to the next one
				max_idx = int( host.rcon_invoke( 'maplist.mapCount' ).strip() ) - 1
				if self.__nextLevel + 1 > max_idx:
					# Fell off the end so next level is the first level
					self.__nextLevel = 0
				else:
					# We can just increment so do so
					self.__nextLevel += 1

		# Maintain the current next level to run
		if next_idx > idx:
			host.rcon_invoke( 'admin.nextLevel %d' % ( next_idx - 1 ) )

		elif next_idx == idx:
			# we removed the level which was to be the next level
			max_idx = int( host.rcon_invoke( 'maplist.mapCount' ).strip() ) - 1
			if next_idx + 1 > max_idx:
				# Fell off the end so next level is the first level
				host.rcon_invoke( 'admin.nextLevel %d' % ( 0 ) )
			else:
				# We can just increment so do so
				host.rcon_invoke( 'admin.nextLevel %d' % ( next_idx + 1 ) )

	def mapAppend( self, ctx, map_name, gametype, size ):
		"""Appends a map into the run list if valid, maintaining the details of temporary maps in the process."""
		if not self.mapGametypeAllowed( ctx, map_name, gametype ):
			return False

		if size is not None:
			size = self.mapValidateSize( map_name, gametype, size )
			if size is None:
				ctx.write( "0\n" )
				ctx.write( "Map %s doesnt support gametype %s ( unable to determine valid size )" )
				return False
			ret = host.rcon_invoke( 'maplist.append %s %s %s' % ( map_name, gametype, size ) )
		else:
			ret = host.rcon_invoke( 'maplist.append %s %s' % ( map_name, gametype ) )

		return True


	def mapInsert( self, ctx, idx, map_name, gametype, size ):
		"""Inserts a map into the run list if valid, maintaining the details of temporary maps in the process."""
		if not self.mapGametypeAllowed( ctx, map_name, gametype ):
			return False

		if size is not None:
			size = self.mapValidateSize( map_name, gametype, size )
			if size is None:
				ctx.write( "0\n" )
				ctx.write( "Map %s doesnt support gametype %s ( unable to determine valid size )" )
				return False
			ret = host.rcon_invoke( 'maplist.insert %d %s %s %s' % ( idx, map_name, gametype, size ) )
		else:
			ret = host.rcon_invoke( 'maplist.insert %d %s %s' % ( idx, map_name, gametype ) )

		# Tell the rcon user the result
		ctx.write( ret )

		if 0 == int( ret.strip() ):
			return False

		# Ensure we maintain the correct values for the indexes of the maps to be removed
		tempLevels = []
		for i in self.__tempLevels:
			if idx < i:
				tempLevels.append( i + 1 )
			elif idx != i:
				tempLevels.append( i )

		self.__tempLevels = tempLevels

		# Move the nextLevel pointer if needed
		if self.__nextLevel is not None and self.__nextLevel >= idx:
			# we added a level below or equal to the next level so increment it
			self.__nextLevel += 1


	def mapRun( self, ctx, map_name, gametype, size ):
		"""Run's a specific map, gametype and size without requiring it to already be in the server maplist"""
		self.mm.debug( 2, "mapRun: %s, %s, %s" % ( map_name, gametype, size ) )
		if not self.mapGametypeAllowed( ctx, map_name, gametype ):
			return False

		# Make a note of the current maplist so that we can restore it later
		maplist = []
		max_idx = 0
		for line in host.rcon_invoke( 'maplist.list' ).split( '\n' ):
			if "" != line:
				( idx, cur_map_name, cur_gametype, cur_size ) = mm_utils.largs( line.lower(), None, 4, None )
				max_idx = int( idx.strip( ':' ) )
				self.mm.debug( 2, "%s == %s and %s == %s and %s == %s" % ( map_name, cur_map_name, gametype, cur_gametype, size, cur_size ) )
				if map_name == cur_map_name and ( gametype is None or gametype == cur_gametype ) and ( size is None or size == cur_size ):
					# We found a match in the current maplist lets use it
					if self.__nextLevel is None:
						self.__nextLevel = int( host.rcon_invoke( 'admin.nextLevel' ).strip() )
					host.rcon_invoke( 'admin.nextLevel %d' % max_idx )
					ctx.write( host.rcon_invoke( 'admin.runNextLevel' ) )
					return

		# we didnt find a match for the request map so we now add one remembering the current
		# state so we can revert to how we where
		if self.__nextLevel is None:
			self.__nextLevel = int( host.rcon_invoke( 'admin.nextLevel' ).strip() )

		# Add the map to the maplist
		if size is not None:
			host.rcon_invoke( 'maplist.append %s %s %s' % ( map_name, gametype, size ) )
		else:
			if gametype is None:
				( default_gametype, default_size ) = self.mapDefaults()
				gametype = default_gametype
			host.rcon_invoke( 'maplist.append %s %s' % ( map_name, gametype ) )

		# Remember what we added and run the map
		max_idx += 1
		host.rcon_invoke( 'admin.nextLevel %s' % max_idx )
		self.__tempLevels.append( max_idx )
		# Run admin.runNextLevel doesnt return anything useful so we assume it always succeeds
		host.rcon_invoke( 'admin.runNextLevel' )
		ctx.write( "OK\n" )


	def mapDefaults( self ):
		"""Returns the default gametype and player size"""
		default_gametype = self.__config['defaultGametype']
		default_size = int( host.ss_getParam( 'maxPlayers' ) )
		if 'gpm_cq' == default_gametype or 'gpm_nv' == default_gametype:
			# Conquest supports 16, 32 and 64 players types
			if ( 16 != default_size and 32 != default_size and 64 != default_size ):
				# Not a direct match find one
				if 16 > default_size:
					default_size = 16
				elif 16 < default_size and 32 > default_size:
					default_size = 32
				else:
					default_size = 64

		elif 'gpm_ti' == default_gametype:
			# Titan only supports 48
			default_size = 48

		elif 'gpm_coop' == default_gametype:
			# Coop only supports 16
			default_size = 16

		elif 'gpm_ca' == default_gametype:
			# Conquest Assault only supports 64
			default_size = 64

		elif 'gpm_hoth' == default_gametype:
			# V2 Vengence only supports 16
			default_size = 16
		
		elif 'gpm_ctf' == default_gametype:
			# Capture the Flag only supports 16
			default_size = 16

		elif 'gpm_sa' == default_gametype:
			# Squad Assault only supports 32
			default_size = 32

		elif 'gpm_rush' == default_gametype:
			# Rush only supports 32
			default_size = 32

			
		return ( default_gametype, default_size )


	def mapValidateSize( self, map_name, gametype, size ):
		"""Ensures that the map supports the requested size for the specified gametype returns the corrected size."""
		try:
			try:
				size = int( size )
			except:
				self.warn( "Invalid map size '%s' specified (defaulting)" % ( size ) )
				size = int( host.ss_getParam( 'maxPlayers' ) )

			self.mm.debug( 5, "SIZE1: %d" % ( size ) )
			if 'gpm_cq' == gametype or 'gpm_nv' == gametype:
				# Conquest supports 16, 32 and 64 players types
				if ( 16 != size and 32 != size and 64 != size ):
					# Not a direct match find one
					if 16 > size:
						size = 16
					elif 16 < size and 32 > size:
						size = 32
					else:
						size = 64

			elif 'gpm_tdm' == gametype:
				# Heroes tdm only supports 16
				size = 16

			elif 'gpm_hoth' == gametype:
				# Heroes tdm only supports 16
				size = 16

			elif 'gpm_ti' == gametype:
				# Titan only supports 48
				size = 48

			elif 'gpm_coop' == gametype:
				# Coop only supports 16
				size = 16

			elif 'gpm_ca' == gametype:
				# Conquest Assault only supports 64
				default_size = 64

			if 1 != self.__config['advancedMapSizeValidation']:		
				return size
		
			self.mm.debug( 5, "SIZE2: %d" % ( size ) )
			if not self.__mapDetails.has_key( map_name ):
				try:
					desc_file = "%s/levels/%s/info/%s.desc" % ( host.sgl_getModDirectory().replace( '\\', '/' ), map_name, map_name )
					mode_re = re.compile( r'<mode\s+type="(.*?)">', re.IGNORECASE )
					players_re = re.compile( r'\s+players="(\d+)"', re.IGNORECASE )

					self.mm.debug( 4, "Loading map desc file: '%s'" % ( desc_file ) )
					f = open( desc_file, 'r' )
					modes = {}
					mode_name = None
					for line in f.readlines():
						self.mm.debug( 5, "LINE: %s" % ( line ) )
						if mode_name is None:
							# Looking for gametype
							match = mode_re.search( line )
							if match is not None:
								mode_name = match.group(1)
								self.mm.debug( 3, "MODE: '%s'" % ( mode_name ) )
								modes[mode_name] = {}
						else:
							# looking for sizes
							match = players_re.search( line )
							if match is not None:
								self.mm.debug( 3, "SIZE: '%s'" % ( match.group(1) ) )
								modes[mode_name][int(match.group(1))] = 1
							elif -1 != line.find( "</mode>" ):
								# end of sizes
								self.mm.debug( 5, "MODE End" )
								mode_name = None

					self.__mapDetails[map_name] = modes
					f.close()

				except RuntimeError, detail:
					self.mm.warn( "Failed to process map description file '%s' (%s)" % ( desc_file, detail ) )

			# Apply full validation if possible
			if self.__mapDetails.has_key( map_name ):
				if self.__mapDetails[map_name].has_key( gametype ):
					details = self.__mapDetails[map_name][gametype]
					if not details.has_key( size ):
						# this is not a valid size so find one
						# here we look for the closest numberical match to the value given
						min_diff = 99
						closest_size = 0
						for s in details.keys():
							if size > s:
								diff = size - s
							else:
								diff = s - size

							if diff < min_diff:
								min_diff = diff
								closest_size = s

						if 0 != closest_size:
							size = closest_size
							self.mm.debug( 5, "SIZE3: %d" % ( size ) )
						else:
							self.mm.error( "Failed to find a valid size for map '%s' gametype '%s' requested %d" % ( map_name, gametype, size ) )
							size = None
		except Exception:
			self.mm.error( "OOPS!", True )

		return size

	def kickPlayer( self, ctx, cmd, wild=False ):
		"""Kick a player from the server with a message."""
		self.mm.debug( 2, "kickPlayer '%s' by %s" % ( cmd, ctx.getName() ) )

		( playerid, reason ) = mm_utils.largs( cmd, None, 2, '' )

		player = mm_utils.find_player( playerid, wild )

		if player is None:
			ctx.write( 'Error: player %s not found\n' % playerid )
			self.mm.error( "Failed to find player %s" % playerid )
		else:
			if reason is not None:
				reason = reason.strip( '" ' )
			self.mm.banManager().kickPlayer( player, reason )
			ctx.write( 'Player %s kicked\n' % playerid )

	def cmdBanList( self, ctx, cmd ):
		"""Ban a player for a specified timer period from the server with a message."""
		self.mm.debug( 2, "cmdBanList by %s" % ( ctx.getName() ) )
		self.mm.banManager().banList( ctx )


	def cmdUnBan( self, ctx, cmd ):
		"""Unban a player with an optional reason."""
		self.mm.debug( 2, "cmdUnBan '%s' by %s" % ( cmd, ctx.getName() ) )
		( ban, msg ) = mm_utils.largs( cmd, None, 2, '' )
		if self.mm.banManager().unbanPlayer( ban, msg ):
			ctx.write( 'Unban successful\n' )
		else:
			ctx.write( 'Unban failed (ban not found)\n' )


	def cmdClearBanList( self, ctx, cmd ):
		"""Ban a player for a specified timer period from the server with a message."""
		self.mm.debug( 2, "cmdClearBanList by %s" % ( ctx.getName() ) )
		if self.mm.banManager().clearBanList():
			ctx.write( "Banlist cleared\n" )
		else:
			ctx.write( "Banlist failed to clear\n" )
	

	def banPlayer( self, ctx, cmd, wild=False ):
		"""Ban a player for a specified timer period from the server with a message."""
		self.mm.debug( 2, "banPlayer '%s' by %s" % ( cmd, ctx.getName() ) )

		( playerid, banPeriod, banReason ) = mm_utils.largs( cmd, None, 3, '' )

		player = mm_utils.find_player( playerid, wild )

		if player is None:
			ctx.write( 'Error: player %s not found\n' % playerid )
			self.mm.error( "Failed to find player %s" % playerid )
		else:
			if banReason is not None:
				banReason = banReason.strip( '" ' )
			self.mm.banManager().banPlayer( player, banReason, banPeriod, None, None, ctx.getName() )
			ctx.write( "Player '%s' (%s) banned\n" % ( player.getName(), playerid ) )

	def banPlayerBy( self, ctx, cmd, wild=False ):
		"""Ban a player for a specified timer period from the server with a message."""
		self.mm.debug( 2, "banPlayerBy '%s' by %s" % ( cmd, ctx.getName() ) )

		( playerid, bannedBy, banPeriod, banReason ) = mm_utils.largs( cmd, None, 4, '' )

		player = mm_utils.find_player( playerid, wild )

		if player is None:
			ctx.write( 'Error: player %s not found\n' % playerid )
			self.mm.error( "Failed to find player %s" % playerid )
		else:
			if banReason is not None:
				banReason = banReason.strip( '" ' )
			self.mm.banManager().banPlayer( player, banReason, banPeriod, None, None, bannedBy )
			ctx.write( "Player '%s' (%s) banned\n" % ( player.getName(), playerid ) )

	def cmdProfileId( self, ctx, cmd ):
		"""Prints your profileid ( in game only )."""
		if ctx.isInGame():
			try:
				player = bf2.playerManager.getPlayerByIndex( ctx.player )
				ctx.write( "Your profileid is %s\n" % player.getProfileId() )
			except:
				ctx.write( "Error: failed to find playerid %d\n" % ctx.player )			
		else:
			ctx.write( "Error: You can only use this command in game\n" )

	def cmdListPlayerProfiles( self, ctx, cmd ):
		"""Print a list of players and their profileid's"""
		for p in bf2.playerManager.getPlayers():
			ctx.write( "#%2d %d %s\n" % ( p.index, p.getProfileId(), p.getName() ) )

	def cmdListLockedSettings( self, ctx, cmd ):
		"""Print a list of locked settings"""
		for setting in self.__lockedSettings.keys():
			ctx.write( "%s\n", setting )

	def cmdMapList( self, ctx, cmd ):
		"""Prints the maplist of the server"""
		ctx.write( host.rcon_invoke( 'maplist.list' ) )

	def cmdMap( self, ctx, cmd ):
		"""Changes the server to a specific map"""
		( map_name, gametype, size ) = mm_utils.largs( cmd.strip().lower(), ' ', 3, None )
		self.mapRun( ctx, map_name, gametype, size )
		
	def cmdListPlayers( self, ctx, cmd ):
		"""List the players on the server."""
		try:
			ctx.write( host.rcon_invoke( 'admin.listPlayers' ) )
		except Exception:
			self.mm.error( "Failed to invoke 'admin.listPlayers'", True )


	def cmdSaveConfig( self, ctx, cmd ):
		"""Save the current ModManager configuration."""
		error = self.mm.saveConfig()
		if not error:
			ctx.write( "Config saved\n" )
		else:
			ctx.write( "Failed to saved config\n" )
			self.mm.error( "Failed to save config '%s' (%s)" % ( self.mm.configFile(), error ) )

	def cmdHelp( self, ctx, cmd ):
		"""Displays list the available commands or displays help on the specified command."""
		return self.__writeCmdsHelp( ctx, 0, cmd, self.__cmds )

	def __writeCmdsHelp( self, ctx, level, cmd, cmds ):
		"""Return the list of available commands or help on the specified command."""
		( subcmd, remaining ) = mm_utils.lsplit( cmd.strip(), ' ', 2 )
		if subcmd:
			# help on a specific command
			if cmds.has_key( subcmd ):
				# we know about this command
				details = cmds[subcmd]
				self.__writeCmdHelp( ctx, cmd, level, details, 'help' )
				# Recurse
				self.__writeCmdsHelp( ctx, level + 1, remaining, details['subcmds'] )
			else:
				ctx.write( "Unknown command '%s'\n" % cmd )
		else:
			# just list the available commands
			if 0 == level:
				ctx.write( 'Available commands: (commands marked with a * are restricted on ranked servers)\n' )
			next_level = level + 1

			# sort the commands
			cmd_keys = cmds.keys()
			cmd_keys.sort()
			for cmd in cmd_keys:
				details = cmds[cmd]
				if 0 == details['alias'] and ( 0 == details['level'] or ctx.authedAllowed( ctx, details ) ):
					# None alias command print it out
					self.__writeCmdHelp( ctx, cmd, next_level, details, 'desc' )
					# Recurse
					self.__writeCmdsHelp( ctx, next_level, remaining, details['subcmds'] )

	def __writeCmdHelp( self, ctx, cmd, level, details, want ):
		"""Return the details about the command and sub commands to the client."""
		if details['restricted']:
			restricted = '*'
		else:
			restricted = ''
		if details['args']:
			ctx.write( "%s%s%s %s: %s\n" % ( '  ' * level, restricted, cmd, details['args'], details[want] ) )
		else:
			ctx.write( "%s%s%s: %s\n" % ( '  ' * level, restricted, cmd, details[want] ) )

	def onGameStatusChanged( self, status ):
		# TODO: remove __validatedMapList check when unregisterGameStatusHandler is fixed
		if not self.__validatedMapList and self.mm.gamePlaying and bf2.GameStatus.PreGame == self.mm.lastGameStatus:
			# Only ever need to do once so unregister
			host.unregisterGameStatusHandler( self.onGameStatusChanged )
			self.validateMaplist()

		# Check if we need to remove any maps we have added
		if self.__nextLevel is not None and self.mm.gamePlaying and bf2.GameStatus.PreGame == self.mm.lastGameStatus:
			# We have just started playing and we have temporary levels to remove
			idx = int( host.rcon_invoke( 'admin.currentLevel' ).strip() )
			if idx not in self.__tempLevels:
				# This is not a temporary level
				# Remove all temporary levels
				for idx in self.__tempLevels:
					host.rcon_invoke( 'maplist.remove %d' % idx )

				# Set the next level back to what it was
				host.rcon_invoke( 'maplist.nextLevel %d' % self.__nextLevel )

				# Clear out our internals
				self.__nextLevel = None
				self.__tempLevels = []
				
	def validateMaplist( self ):
		"""Check the maplist is valid"""
		self.mm.info( "Validating maplist..." )
		maplist = []
		( default_gametype, default_size ) = self.mapDefaults()
		fixed = False
		for line in host.rcon_invoke( 'maplist.list' ).split( '\n' ):
			if "" != line:
				( idx, map_name, gametype, size ) = mm_utils.largs( line, None, 4, '' )
				if not self.allowMap( map_name ):
					self.mm.warn( "Map %s can't be used on a ranked server, removing\n" % map_name )
					fixed = True
					continue

				if self.restrictedGametype( gametype ):
					# This gametype is restricted and must be removed
					self.mm.warn( "Gametype '%s' for map '%s' is restricted, changing to '%s'" % ( gametype, map_name, default_gametype ) )
					gametype = default_gametype
					fixed = True

				if '' != size:
					try:
						size = int( size )
					except:
						self.mm.warn( "Invalid map size '%s' specified (defaulting)" % ( size ) )
						size = default_size

					new_size = self.mapValidateSize( map_name, gametype, size )
					if new_size is None:
						# Coundn't determine size fall back to auto
						# Note: This could mean the map doesnt support the requested gametype so
						# so this behaviour may change in the future
						size = ''
						fixed = True

					elif new_size != size:
						size = new_size
						fixed = True

				maplist.append( [ map_name, gametype, size ] )

		if fixed:
			# apply the changes need to clear and re-add as gametype combinations
			# are rejected by the server
			self.mm.info( 'Fixing / restricting maplist:' )
			self.maplistClear()
			for entry in maplist:
				( map, gametype, size ) = entry
				if '' == size:
					size = default_size
				self.mm.info( 'maplist.append "%s" "%s" %s' % ( map, gametype, size ) )
				host.rcon_invoke( 'maplist.append "%s" "%s" %s' % ( map, gametype, size ) )

			host.rcon_invoke( 'maplist.save' )
			self.mm.warn( "Maplist was altered restarting map" )
			host.rcon_invoke( 'admin.restartMap' )
		else:
			self.mm.info( "No maplist changes required" )

		self.__validatedMapList = True

	#
	# Game methods
	#

	def shutdown( self ):
		"""Shutdown rcon, closing the socket."""
		self.mm.unregisterUpdates( self.update )
		for peer in self.__peers:
			peer.shutdown()
			self.__disconnectClient( peer )
		self.__peers = []

		if self.__socket:
			self.__socket.close()
			self.__socket = None

		# N.B. onGameStatusChanged is unregisted by itself

	def init( self ):
		"""Provides default initialisation."""
		# state for in-game rcon connections
		host.registerHandler( 'RemoteCommand', self.onRemoteCommand, 1 )
		host.registerHandler( 'PlayerDisconnect', self.onPlayerDisconnect, 1 )
		host.registerHandler( 'ChatMessage', self.onChatMessage, 1 )

		# Register our base handlers
		host.registerGameStatusHandler( self.onGameStatusChanged )

class CommandContext( object ):
	"""Context passed to remote command implementations.

	This is used for handlers to write output to either:
	1. Remote tcp socket
	2. in-game client executing 'rcon <command>'.
	"""

	def __init__( self, client ):
		if isinstance( client, ( int, long ) ):
			self.player = client
			self.conn = None
		elif isinstance( client, AdminConnection ):
			self.player = None
			self.conn = client
		else:
			raise TypeError( "client must be either player index or AdminConnection not '%s'" % type( client ) )
		self.logout = False
		self.authedLevel = 0
		self.authedBy = None
		self.authedAllowed = self.notAllowed
		self.authedChecker = None
		self.currentCmd = ''
		self.currentBaseCmd = ''
		self.output = []
		self.cmdCount = 0

	def notAllowed( self, ctx, details ):
		"""Default allowed handler.

		Checks to see if the user is allowed to use the method.
		"""
		return False

	def isInGame(self):
		"""Return if the client is an in-game player."""
		return self.player is not None

	def isSocket(self):
		"""Return if the client is a remote TCP socket."""
		return self.conn is not None

	def key( self ):
		"""Return the auth key, either player or conn."""
		if self.conn is not None:
			return self.conn
		else:
			return self.player

	def getShortName( self ):
		if self.conn is not None:
			return 'rcon'
		elif self.player == -1:
			return 'server console'
		else:
			try:
				player = bf2.playerManager.getPlayerByIndex( self.player )
				return player.getName()
			except:
				return 'unknown'


	def getName( self ):
		"""Return a descriptive name for this context."""
		if self.conn is not None:
			return 'tcp: %s:%d' % ( self.conn.addr[0], self.conn.addr[1] )
		else:
			if self.player == -1:
				return '-1 (local server console)'
			else:
				try:
					player = bf2.playerManager.getPlayerByIndex( self.player )
					return '%d from %s name=\'%s\'' % ( self.player, player.getAddress(), player.getName() )
				except:
					return '%d (no info)' % self.player

	def write( self, text ):
		"""Enqueue data to send."""
		self.output.append(text)

	def flush( self, interactive=False ):
		"""Flush any remaining output."""
		self.send( interactive )
		if self.isSocket():
			self.conn.flush()

	def send( self, interactive=False ):
		feedback = ''.join( self.output )
		# clear the contexts output
		self.output = []
		if self.isSocket():
			if interactive:
				self.conn.outbuf.enqueue( feedback )
			else:
				self.conn.outbuf.enqueue( feedback + '\x04' )
		else:
			host.rcon_feedback( self.player, feedback )

class OutputBuffer(object):
	"""A stateful output buffer.

	This knows how to enqueue data and ship it out without blocking.
	"""

	def __init__( self, modManager, socket, allowBatching ):
		self.mm = modManager
		self.allowBatching = allowBatching
		self.socket = socket
		self.data = []
		self.index = 0

	def enqueue(self, str):
		try:
			self.data.append(str)
		except Exception, e:
			self.mm.error( "Failed to enqueue '%s' (%s)" % ( str, e ), True )

	def update(self):
		while len(self.data) > 0:
			try:
				item = self.data[0]
				scount = self.socket.send(item[self.index:])
				self.index += scount
				if self.index == len(item):
					del self.data[0]
					self.index = 0
			except socket.error, detail:
				if detail[0] != errno.EWOULDBLOCK:
					self.mm.error( "Failed to send", True )
					return detail[1]
			if not self.allowBatching:
				break
		return None

class AdminConnection(object):
	"""Each TCP connection is represented by an object of this class."""

	def __init__( self, srv, socket, addr, game ):
		# convenience vars
		self.allowBatching = srv.allowBatching()
		self.mm = srv.mm

		self.server = srv
		self.socket = socket
		self.addr = addr
		self.socket.setblocking( 0 )
		self.buffer = ''
		self.seed = self.make_seed( 16 )
		self.basicDigest = self.digest( srv.rconBasicPassword() )
		self.superDigest = self.digest( srv.rconSuperPassword() )
		self.outbuf = OutputBuffer( self.mm, self.socket, self.allowBatching )

		self.mm.debug( 1, 'new rcon/admin connection from %s:%d' % ( addr[0], addr[1] ) )

		# Welcome message *must* end with \n\n
		self.outbuf.enqueue('### %s ModManager Rcon v%s.\n' % ( game, __version__ ) )
		self.outbuf.enqueue('### Digest seed: %s\n' % (self.seed))
		self.outbuf.enqueue('\n') # terminate welcome message with extra LF

	def make_seed( self, seed_length ):
		"""Returns a seed string of random characters.

		This is used as a salt to protect password sniffing.
		"""

		return ''.join([string.ascii_letters[random.randint(0, len(string.ascii_letters)-1)] for x in xrange(0, seed_length)])

	def digest( self, password ):
		"""Concats a seed string with the password.

		Returns an ASCII-hex MD5 digest.
		"""
		if not password:
			return None
		m = md5.new()
		m.update( self.seed )
		m.update( password )
		return m.hexdigest()

	def update( self ):
		if not self.socket:
			# socket already closed e.g. DOS protection
			return 0

		err = None
		# Process incoming requests
		try:
			while not err:
				data = self.socket.recv(1024)
				if data:
					self.buffer += data
					while not err:
						nlpos = self.buffer.find('\n')
						if nlpos != -1:
							self.server.onRemoteCommand( self, self.buffer[0:nlpos] )
							self.buffer = self.buffer[nlpos+1:] # keep rest of buffer
						else:
							if len(self.buffer) > 128:
								err = 'data format error: no newline in message'
							break
						if not self.allowBatching:
							break
				else:
					err = 'peer disconnected'

				if not self.socket:
					# socket already closed e.g. DOS protection
					return 0

				if not self.allowBatching:
					break

		except socket.error, detail:
			if detail[0] != errno.EWOULDBLOCK:
				err = detail[1]
				if detail[0] != errno.EPIPE and detail[0] != errno.ECONNRESET:
					# only print error if the client didnt disconnect
					self.mm.error( "rcon: update failed %s" % detail )

		if not err:
			# Send any output
			err = self.outbuf.update()

		if err:
			self.close( err )
			return 0

		return 1

	def flush( self ):
		"""Flush any remaining output."""
		err = self.outbuf.update()

		if err:
			self.close( err )
			return 0

		return 1

	def close( self, err = 'unknown' ):
		self.mm.debug( 1, 'rcon: closing %s:%d (%s)' % ( self.addr[0], self.addr[1], err ) )
		# ensure we close down as best we can
		if self.socket is not None:
			try:
				self.socket.shutdown(2)
			except:
				self.mm.error( 'rcon: failed to shutdown client connection %s:%d (%s)' % ( self.addr[0], self.addr[1], err ) )

			try:
				self.socket.close()
			except:
				self.mm.error( 'rcon: failed to close client connection %s:%d (%s)' % ( self.addr[0], self.addr[1], err ), True )
			self.socket = None
		return 1

# These functions are called by ModManager

def mm_load( modManager ):
	"""ModManager method called just after the module is loaded.

	Any global initialisation should be done here.
	"""
	return AdminServer( modManager )
