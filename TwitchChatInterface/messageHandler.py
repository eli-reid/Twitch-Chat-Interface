from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class RoomState():
    """ doc """
    def __init__(self):
        self.emote_only = 0
        self.followers_only = 0
        self.y = 0
        self.r9k = 0
        self.slow = 0
        self.subs_only = 0

@dataclass
class Channel:
    """ doc """
    name: str = field(default="")
    mods: list = field(default_factory=list)
    roomState: RoomState = RoomState
    def __str__(self):
        return self.name

@dataclass
class Message:
    """ message  """
    raw: str = ""
    channel: Channel = field(default_factory=Channel)
    id: str = field(default="")
    prefix: str = field(default="")
    command: str = field(default="")
    text: str = field(default="")
    username: str = field(default="")
    params: List[str] = field(default_factory=list)
    tags: Dict = field(default_factory=dict)

@dataclass
class UserNotice():
    """ doc """
    def __init__(self):
        self.badge_info = ""
        self.badges = ""
        self.color = ""
        self.display_name = ""
        self.emote_sets = ""
        self.turbo = ""
        self.user_id = ""
        self.user_type = ""

def IDEHelper(cls):

    def __eq__(self, value):
            return self._value == value
    def  __hash__(self):
        return hash(self._value)
    def  __str__(self):
        return self._value
    cls.__eq__ =__eq__
    cls.__hash__ =__hash__
    cls.__str__ =__str__
    return cls

@IDEHelper
@dataclass(frozen=True)
class _ROOMSTATE(str):
    """ doc """
    _value = "ROOMSTATE"
    EMOTE_ONLY = "emote-only"
    FOLLOWERS_ONLY = "followers-only"
    R9K = "r9k"
    SLOW = "slow"
    SUBS_ONLY = "subs-only"

@dataclass(frozen=True)
class _MESSAGEIDS:
    """[summary]


    Raises:
        ConstantError: [description]
        ConstantError: [description]
    """
    ALREADY_BANNED = "already_banned"
    ALREADY_EMOTE_ONLY_OFF = "already_emote_only_off"
    ALREADY_EMOTE_ONLY_ON = "already_emote_only_on"
    ALREADY_R9K_OFF = "already_r9k_off"
    ALREADY_R9K_ON = "already_r9k_on"
    ALREADY_SUBS_OFF = "already_subs_off"
    ALREADY_SUBS_ON = "already_subs_on"
    BAD_BAN_ADMIN = "bad_ban_admin"
    BAD_BAN_ANON = "bad_ban_anon"
    BAD_BAN_BROADCASTER = "bad_ban_broadcaster"
    BAD_BAN_GLOBAL_MOD = "bad_ban_global_mod"
    BAD_BAN_MOD = "bad_ban_mod"
    BAD_BAN_SELF = "bad_ban_self"
    BAD_BAN_STAFF = "bad_ban_staff"
    BAD_COMMERCIAL_ERROR = "bad_commercial_error"
    BAD_DELETE_MESSAGE_BROADCASTER = "bad_delete_message_broadcaster"
    BAD_DELETE_MESSAGE_MOD = "bad_delete_message_mod"
    BAD_HOST_ERROR = "bad_host_error"
    BAD_HOST_HOSTING = "bad_host_hosting"
    BAD_HOST_RATE_EXCEEDED = "bad_host_rate_exceeded"
    BAD_HOST_REJECTED = "bad_host_rejected"
    BAD_HOST_SELF = "bad_host_self"
    BAD_MARKER_CLIENT = "bad_marker_client"
    BAD_MOD_BANNED = "bad_mod_banned"
    BAD_MOD_MOD = "bad_mod_mod"
    BAD_SLOW_DURATION = "bad_slow_duration"
    BAD_TIMEOUT_ADMIN = "bad_timeout_admin"
    BAD_TIMEOUT_ANON = "bad_timeout_anon"
    BAD_TIMEOUT_BROADCASTER = "bad_timeout_broadcaster"
    BAD_TIMEOUT_DURATION = "bad_timeout_duration"
    BAD_TIMEOUT_GLOBAL_MOD = "bad_timeout_global_mod"
    BAD_TIMEOUT_MOD = "bad_timeout_mod"
    BAD_TIMEOUT_SELF = "bad_timeout_self"
    BAD_TIMEOUT_STAFF = "bad_timeout_staff"
    BAD_UNBAN_NO_BAN = "bad_unban_no_ban"
    BAD_UNHOST_ERROR = "bad_unhost_error"
    BAD_UNMOD_MOD = "bad_unmod_mod"
    BAN_SUCCESS = "ban_success"
    CMDS_AVAILABLE = "cmds_available"
    COLOR_CHANGED = "color_changed"
    COMMERCIAL_SUCCESS = "commercial_success"
    DELETE_MESSAGE_SUCCESS = "delete_message_success"
    EMOTE_ONLY_OFF = "emote_only_off"
    EMOTE_ONLY_ON = "emote_only_on"
    FOLLOWERS_OFF = "followers_off"
    FOLLOWERS_ON = "followers_on"
    FOLLOWERS_ONZERO = "followers_onzero"
    HOST_OFF = "host_off"
    HOST_ON = "host_on"
    HOST_SUCCESS = "host_success"
    HOST_SUCCESS_VIEWERS = "host_success_viewers"
    HOST_TARGET_WENT_OFFLINE = "host_target_went_offline"
    HOSTS_REMAINING = "hosts_remaining"
    INVALID_USER = "invalid_user"
    MOD_SUCCESS = "mod_success"
    MSG_BANNED = "msg_banned"
    MSG_BAD_CHARACTERS = "msg_bad_characters"
    MSG_CHANNEL_BLOCKED = "msg_channel_blocked"
    MSG_CHANNEL_SUSPENDED = "msg_channel_suspended"
    MSG_DUPLICATE = "msg_duplicate"
    MSG_EMOTEONLY = "msg_emoteonly"
    MSG_FACEBOOK = "msg_facebook"
    MSG_FOLLOWERSONLY = "msg_followersonly"
    MSG_FOLLOWERSONLY_FOLLOWED = "msg_followersonly_followed"
    MSG_FOLLOWERSONLY_ZERO = "msg_followersonly_zero"
    MSG_R9K = "msg_r9k"
    MSG_RATELIMIT = "msg_ratelimit"
    MSG_REJECTED = "msg_rejected"
    MSG_REJECTED_MANDATORY = "msg_rejected_mandatory"
    MSG_ROOM_NOT_FOUND = "msg_room_not_found"
    MSG_SLOWMODE = "msg_slowmode"
    MSG_SUBSONLY = "msg_subsonly"
    MSG_SUSPENDED = "msg_suspended"
    MSG_TIMEDOUT = "msg_timedout"
    MSG_VERIFIED_EMAIL = "msg_verified_email"
    NO_HELP = "no_help"
    NO_MODS = "no_mods"
    NOT_HOSTING = "not_hosting"
    NO_PERMISSION = "no_permission"
    R9K_OFF = "r9k_off"
    R9K_ON = "r9k_on"
    RAID_ERROR_ALREADY_RAIDING = "raid_error_already_raiding"
    RAID_ERROR_FORBIDDEN = "raid_error_forbidden"
    RAID_ERROR_SELF = "raid_error_self"
    RAID_ERROR_TOO_MANY_VIEWERS = "raid_error_too_many_viewers"
    RAID_ERROR_UNEXPECTED = "raid_error_unexpected"
    RAID_NOTICE_MATURE = "raid_notice_mature"
    RAID_NOTICE_RESTRICTED_CHAT = "raid_notice_restricted_chat"
    ROOM_MODS = "room_mods"
    SLOW_OFF = "slow_off"
    SLOW_ON = "slow_on"
    SUBS_OFF = "subs_off"
    SUBS_ON = "subs_on"
    TIMEOUT_NO_TIMEOUT = "timeout_no_timeout"
    TIMEOUT_SUCCESS = "timeout_success"
    TOS_BAN = "tos_ban"
    TURBO_ONLY_COLOR = "turbo_only_color"
    UNBAN_SUCCESS = "unban_success"
    UNMOD_SUCCESS = "unmod_success"
    UNRAID_ERROR_NO_ACTIVE_RAID = "unraid_error_no_active_raid"
    UNRAID_ERROR_UNEXPECTED = "unraid_error_unexpected"
    UNRAID_SUCCESS = "unraid_success"
    UNRECOGNIZED_CMD = "unrecognized_cmd"
    UNSUPPORTED_CHATROOMS_CMD = "unsupported_chatrooms_cmd"
    UNTIMEOUT_BANNED = "untimeout_banned"
    UNTIMEOUT_SUCCESS = "untimeout_success"
    USAGE_BAN = "usage_ban"
    USAGE_CLEAR = "usage_clear"
    USAGE_COLOR = "usage_color"
    USAGE_COMMERCIAL = "usage_commercial"
    USAGE_DISCONNECT = "usage_disconnect"
    USAGE_EMOTE_ONLY_OFF = "usage_emote_only_off"
    USAGE_EMOTE_ONLY_ON = "usage_emote_only_on"
    USAGE_FOLLOWERS_OFF = "usage_followers_off"
    USAGE_FOLLOWERS_ON = "usage_followers_on"
    USAGE_HELP = "usage_help"
    USAGE_HOST = "usage_host"
    USAGE_MARKER = "usage_marker"
    USAGE_ME = "usage_me"
    USAGE_MOD = "usage_mod"
    USAGE_MODS = "usage_mods"
    USAGE_R9K_OFF = "usage_r9k_off"
    USAGE_R9K_ON = "usage_r9k_on"
    USAGE_RAID = "usage_raid"
    USAGE_SLOW_OFF = "usage_slow_off"
    USAGE_SLOW_ON = "usage_slow_on"
    USAGE_SUBS_OFF = "usage_subs_off"
    USAGE_SUBS_ON = "usage_subs_on"
    USAGE_TIMEOUT = "usage_timeout"
    USAGE_UNBAN = "usage_unban"
    USAGE_UNHOST = "usage_unhost"
    USAGE_UNMOD = "usage_unmod"
    USAGE_UNRAID = "usage_unraid"
    USAGE_UNTIMEOUT = "usage_untimeout"
    WHISPER_BANNED = "whisper_banned"
    WHISPER_BANNED_RECIPIENT = "whisper_banned_recipient"
    WHISPER_INVALID_ARGS = "whisper_invalid_args"
    WHISPER_INVALID_LOGIN = "whisper_invalid_login"
    WHISPER_INVALID_SELF = "whisper_invalid_self"
    WHISPER_LIMIT_PER_MIN = "whisper_limit_per_min"
    WHISPER_LIMIT_PER_SEC = "whisper_limit_per_sec"
    WHISPER_RESTRICTED = "whisper_restricted"
    WHISPER_RESTRICTED_RECIPIENT = "whisper_restricted_recipient"

@IDEHelper   
@dataclass(frozen=True)
class _GLOBALUSERSTATE(str):
    """g
    """
    _value = "GLOBALUSERSTATE"
    BADGEINFO = 'badge-info'
    BADGES = 'badges'
    COLOR = 'color'
    DISPLAYNAME = 'display-name'
    EMOTESETS = 'emote-sets'
    TURBO = 'turbo'
    USERID = 'user-id'
    USERTYPE = 'user-type'

@IDEHelper
@dataclass(frozen=True)
class _CLEARCHAT(str):
    """[summary]

    Raises:
        ConstantError: [description]
        ConstantError: [description]

    Returns:
        [type] -- [description]
    """
    BAN_DURATION: str = "ban-duration"

@IDEHelper
@dataclass(frozen=True)
class _CLEARMSG(str):
    """ doc """
    LOGIN: str = "login"
    MESSAGE: str = "message"
    TARGET_MSG_ID = "target-msg-id"

@IDEHelper
@dataclass(frozen=True)
class _PRIVMSG(str):
    """ doc """

@IDEHelper
@dataclass(frozen=True)
class _USERNOTICE(str):
    """ doc """
@IDEHelper
@dataclass(frozen=True)
class _USERSTATE(str):
    """ doc """


@dataclass(frozen=True)
class COMMANDS:
    """
    :Raises: ConstantError: raise on trying to change
    """
    LOGIN_UNSUCCESSFUL = "LOGIN_UNSUCCESSFUL"
    MESSAGE = "PRIVMSG"
    JOIN = "JOIN"
    RECEIVED = "RECEIVED"
    CONNECTED = "372"
    ERROR = "ERROR"
    DISCONNECTED = "DISCONNECTED"
    USERNAME = "001"
    NAMES = "353"
    WHISPER = "WHISPER"
    PART = "PART"
    TMI_TWITCH_TV = "tmi.twitch.tv"
    HOSTTARGET: str =  "HOSTTARGET"
    NOTICE: str = "NOTICE"
    RECONNECT: str  = "RECONNECT" 
    GLOBALUSERSTATE:str = "GLOBALUSERSTATE"
    CLEARCHAT: str = "CLEARCHAT"
    CLEARMSG: str = "CLEARMSG"
    USERNOTICE: str  = "USERNOTICE"
    USERSTATE: str =  "USERSTATE"
    ROOMSTATE: _ROOMSTATE = _ROOMSTATE()
    MESSAGEIDS: _MESSAGEIDS = _MESSAGEIDS()

class MessageHandler():
    """
    Handles twitch message and emits events based on Commands and msgid tags
    Commands:
    """
    def __init__(self):
        self.COMMANDS: COMMANDS = COMMANDS()

    def handleMessage(self, msg: str)->list:
        """  handleMessage     """

        try:
            message = self._parse(msg)
            if message is None:
                return[None, None]

            # Populate message values
            message.channel.name: str = message.params[0] if len(message.params) > 0 else None
            message.text: str = message.params[1] if len(message.params) > 1 else None
            message.id: str = message.tags.get("msg-id")
            message.raw: str = msg
            message.username: str = message.tags.get("display-name")

            # Parse badges and emotes
            message.tags = self._badges(self._emotes(message.tags))

        except Exception as error:
            raise Exception(error)

        # Transform IRCv3 Tags
        try:
            if message.tags:
                for key in message.tags:
                    if key not in ("emote-sets", "ban-duration", "bits"):
                        if isinstance(message.tags[key], bool):
                            message.tags[key] = None
                        elif message.tags[key] in ('0', '1'):
                            message.tags[key] = bool(int(message.tags[key]))
        except Exception as error:
            raise Exception(error)

        # Handle message with prefix "tmi.twitch.tv"
        if message.prefix == self.COMMANDS.TMI_TWITCH_TV:
            # Handle command  bot Username
            if message.command == self.COMMANDS.USERNAME:
                username = message.params[0]
               # Chatroom NOTICE check msgid tag
            elif message.command == self.COMMANDS.NOTICE:
                
                if message.id in self.COMMANDS.MESSAGEIDS.__dict__.values():
                    return [self.COMMANDS.NOTICE, message]
                else:
                    if message.raw.replace(":tmi.twitch.tv NOTICE * :",'') in ("Login unsuccessful", "Login authentication failed", "Error logging in", "Invalid NICK"):                       
                        return [self.COMMANDS.LOGIN_UNSUCCESSFUL, \
                            message.raw.replace(":tmi.twitch.tv NOTICE * :",'')]
            else:
                return [message.command, message]
        # Handle message with prefix jtv ???????
        elif message.prefix == "jtv":
            print(message.params)
        else:
            if message.command == self.COMMANDS.MESSAGE:
                message.username: str = message.prefix[:message.prefix.find("!")]
                return [self.COMMANDS.MESSAGE, message]
            elif message.command == self.COMMANDS.WHISPER:
                return [self.COMMANDS.WHISPER, message]
            elif message.command == self.COMMANDS.NAMES:
                return [self.COMMANDS.NAMES, message]
        return [None, None]

    @staticmethod
    def _badges(tags: dict)->dict:
        """parse badges dict"""
        try:
            if ("badges" in tags and isinstance(tags.get("badges"), str)):
                badges = tags.get("badges").split(",")
                for badge in badges:
                    key, value = badge.split("/")
                    if value is None:
                        return tags
                    tags["badges"][key] = value
            return tags
        except Exception as error:
            pass


    @staticmethod
    def _emotes(tags: dict)->list:
        """ parse emotes to list"""
        try:
            if ("emotes" in tags and isinstance(tags.get("emotes"), str)):
                emoticons = tags.get("emotes").split("/")
                for emoticon in emoticons:
                    key, value = emoticon.split(":")
                    if value is None:
                        return tags
                    tags["emotes"][key] = value.split(",")
            return tags
        except:
            pass

    @staticmethod
    def _parse(data: str)->Message:
        """ doc """
        message = Message()
        if not isinstance(data, str):
            raise TypeError("_Parse.parse requires input of type str")

        position: int = 0
        nextspace: int = 0

        if len(data) < 1:
            return None

        if data.startswith(chr(64)): #starts with @ symbol
            nextspace = data.find(" ")

            if nextspace == -1: #invalid message form
                return None

            tags = data[1:nextspace].split(";")

            for tag in tags:
                pair = tag.split("=")
                message.tags[pair[0]] = pair[1] or True

            position = nextspace + 1

        while data[position] == chr(32):
            position += 1

        if data[position] == chr(58):
            nextspace = data.find(chr(32), position)

            if nextspace == -1:
                return None

            message.prefix = data[position + 1:nextspace]
            position = nextspace + 1

            while data[position] == chr(32):
                position += 1

        nextspace = data.find(" ", position)

        if nextspace == -1:
            if len(data) > position:
                message.command = data[position:]
                return message

            return None
        message.command = data[position:nextspace]

        position = nextspace + 1

        while data[position] == chr(32):
            position += 1

        dataLen = len(data)

        while position < dataLen:
            nextspace = data.find(" ", position)

            if data[position] == chr(58):#check for ':'
                message.params.append(data[position + 1:])
                break

            if nextspace != -1:
                message.params.append(data[position:nextspace])
                position = nextspace + 1

                while data[position] == chr(32):
                    position += 1
                continue

            if nextspace == -1:
                message.params.append(data[position:])
                break

        return message
