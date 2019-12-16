=========
Constants
=========
Contains all reqired values from the Twitch irc commands and event name values

.. automodule:: TwitchChatInterface
	:noindex:
	
TwichChatInterface.EVENTS
-------------------------

.. autoattribute:: TwitchChatInterface.EVENTS.SUBSON
.. autoattribute:: TwitchChatInterface.EVENTS.SUBSOFF

TwichChatInterface.SERVEREVENTS
-------------------------------

.. autoattribute:: TwitchChatInterface.SERVEREVENTS.LOGIN_UNSUCCESSFUL
.. autoattribute:: TwitchChatInterface.SERVEREVENTS.MESSAGE
.. autoattribute:: TwitchChatInterface.SERVEREVENTS.JOIN
.. autoattribute:: TwitchChatInterface.SERVEREVENTS.RECEIVED
.. autoattribute:: TwitchChatInterface.SERVEREVENTS.CONNECTED
.. autoattribute:: TwitchChatInterface.SERVEREVENTS.ERROR
.. autoattribute:: TwitchChatInterface.SERVEREVENTS.DISCONNECTED
.. autoattribute:: TwitchChatInterface.SERVEREVENTS.USERNAME
.. autoattribute:: TwitchChatInterface.SERVEREVENTS.NAMES
.. autoattribute:: TwitchChatInterface.SERVEREVENTS.WHISPER
.. autoattribute:: TwitchChatInterface.SERVEREVENTS.PART
.. autoattribute:: TwitchChatInterface.SERVEREVENTS.TMI_TWITCH_TV

TwichChatInterface.COMMANDS
---------------------------

.. autoattribute:: TwitchChatInterface.COMMANDS.PING
.. autoattribute:: TwitchChatInterface.COMMANDS.PONG
.. autoattribute:: TwitchChatInterface.COMMANDS.HOSTTARGET
.. autoattribute:: TwitchChatInterface.COMMANDS.NOTICE
.. autoattribute:: TwitchChatInterface.COMMANDS.RECONNECT
.. autoattribute:: TwitchChatInterface.COMMANDS.GLOBALUSERSTATE
.. autoattribute:: TwitchChatInterface.COMMANDS.CLEARCHAT
.. autoattribute:: TwitchChatInterface.COMMANDS.CLEARMSG
.. autoattribute:: TwitchChatInterface.COMMANDS.ROOMSTATE
.. autoattribute:: TwitchChatInterface.COMMANDS.USERNOTICE
.. autoattribute:: TwitchChatInterface.COMMANDS.USERSTATE

TwichChatInterface.MESSAGEIDS
-----------------------------

.. autoattribute:: TwitchChatInterface.MESSAGEIDS.ALREADY_BANNED
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.ALREADY_EMOTE_ONLY_OFF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.ALREADY_EMOTE_ONLY_ON
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.ALREADY_R9K_OFF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.ALREADY_R9K_ON
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.ALREADY_SUBS_OFF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.ALREADY_SUBS_ON
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_BAN_ADMIN
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_BAN_ANON
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_BAN_BROADCASTER
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_BAN_GLOBAL_MOD
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_BAN_MOD
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_BAN_SELF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_BAN_STAFF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_COMMERCIAL_ERROR
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_DELETE_MESSAGE_BROADCASTER
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_DELETE_MESSAGE_MOD
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_HOST_ERROR
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_HOST_HOSTING
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_HOST_RATE_EXCEEDED
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_HOST_REJECTED
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_HOST_SELF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_MARKER_CLIENT
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_MOD_BANNED
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_MOD_MOD
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_SLOW_DURATION
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_TIMEOUT_ADMIN
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_TIMEOUT_ANON
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_TIMEOUT_BROADCASTER
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_TIMEOUT_DURATION
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_TIMEOUT_GLOBAL_MOD
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_TIMEOUT_MOD
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_TIMEOUT_SELF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_TIMEOUT_STAFF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_UNBAN_NO_BAN
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_UNHOST_ERROR
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAD_UNMOD_MOD
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.BAN_SUCCESS
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.CMDS_AVAILABLE
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.COLOR_CHANGED
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.COMMERCIAL_SUCCESS
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.DELETE_MESSAGE_SUCCESS
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.EMOTE_ONLY_OFF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.EMOTE_ONLY_ON
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.FOLLOWERS_OFF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.FOLLOWERS_ON
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.FOLLOWERS_ONZERO
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.HOST_OFF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.HOST_ON
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.HOST_SUCCESS
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.HOST_SUCCESS_VIEWERS
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.HOST_TARGET_WENT_OFFLINE
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.HOSTS_REMAINING
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.INVALID_USER
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MOD_SUCCESS
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_BANNED
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_BAD_CHARACTERS
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_CHANNEL_BLOCKED
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_CHANNEL_SUSPENDED
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_DUPLICATE
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_EMOTEONLY
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_FACEBOOK
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_FOLLOWERSONLY
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_FOLLOWERSONLY_FOLLOWED
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_FOLLOWERSONLY_ZERO
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_R9K
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_RATELIMIT
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_REJECTED
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_REJECTED_MANDATORY
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_ROOM_NOT_FOUND
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_SLOWMODE
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_SUBSONLY
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_SUSPENDED
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_TIMEDOUT
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.MSG_VERIFIED_EMAIL
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.NO_HELP
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.NO_MODS
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.NOT_HOSTING
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.NO_PERMISSION
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.R9K_OFF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.R9K_ON
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.RAID_ERROR_ALREADY_RAIDING
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.RAID_ERROR_FORBIDDEN
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.RAID_ERROR_SELF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.RAID_ERROR_TOO_MANY_VIEWERS
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.RAID_ERROR_UNEXPECTED
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.RAID_NOTICE_MATURE
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.RAID_NOTICE_RESTRICTED_CHAT
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.ROOM_MODS
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.SLOW_OFF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.SLOW_ON
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.SUBS_OFF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.SUBS_ON
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.TIMEOUT_NO_TIMEOUT
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.TIMEOUT_SUCCESS
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.TOS_BAN
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.TURBO_ONLY_COLOR
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.UNBAN_SUCCESS
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.UNMOD_SUCCESS
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.UNRAID_ERROR_NO_ACTIVE_RAID
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.UNRAID_ERROR_UNEXPECTED
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.UNRAID_SUCCESS
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.UNRECOGNIZED_CMD
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.UNSUPPORTED_CHATROOMS_CMD
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.UNTIMEOUT_BANNED
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.UNTIMEOUT_SUCCESS
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_BAN
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_CLEAR
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_COLOR
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_COMMERCIAL
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_DISCONNECT
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_EMOTE_ONLY_OFF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_EMOTE_ONLY_ON
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_FOLLOWERS_OFF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_FOLLOWERS_ON
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_HELP
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_HOST
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_MARKER
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_ME
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_MOD
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_MODS
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_R9K_OFF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_R9K_ON
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_RAID
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_SLOW_OFF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_SLOW_ON
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_SUBS_OFF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_SUBS_ON
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_TIMEOUT
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_UNBAN
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_UNHOST
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_UNMOD
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_UNRAID
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.USAGE_UNTIMEOUT
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.WHISPER_BANNED
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.WHISPER_BANNED_RECIPIENT
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.WHISPER_INVALID_ARGS
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.WHISPER_INVALID_LOGIN
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.WHISPER_INVALID_SELF
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.WHISPER_LIMIT_PER_MIN
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.WHISPER_LIMIT_PER_SEC
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.WHISPER_RESTRICTED
.. autoattribute:: TwitchChatInterface.MESSAGEIDS.WHISPER_RESTRICTED_RECIPIENT

TwichChatInterface.TAGS
-----------------------
