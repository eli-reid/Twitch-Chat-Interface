""" """
import re
from lib.events.eventHandler import eventHandler as _EVENT
from lib.twitchMessageHandler.modals.const import   COMMANDS, MESSAGEIDS, SERVEREVENTS, EVENTS, TAGS
from lib.twitchMessageHandler.modals.dataTypes import Message, Channel
class MessageHandler():
    """
    Handles twitch message and emits events based on Commands and msgid tags
    Commands: CommandsEnum
    """

    @staticmethod
    def messageHandler(data: str)->None:
        """               """
        messageParts: list(str) = data.split("\r\n")
        for messagePart in messageParts:

            try:
                message = _Parser.parse(messagePart)
            except Exception as err:
                _EVENT.emit(MessageHandler, SERVEREVENTS.ERROR, err)

            if message != None:
                try:
                    # Populate message values
                    message.channel: str = message.params[0] if len(message.params) > 0 else None
                    message.text: str = message.params[1] if len(message.params) > 1 else None
                    message.id: str = message.tags["msg-id"] if "msg-id" in message.tags else None
                    message.raw: str = messagePart
                    message.username: str = message.tags["display-name"] \
                        if "display-name" in message.tags else None

                    # Parse badges and emotes
                    message.tags = _Parser.badges(_Parser.emotes(message.tags))

                except Exception as err:
                    _EVENT.emit("Populate message values (MessageHandler):", SERVEREVENTS.ERROR, err)

                # Transform IRCv3 Tags
                try:
                    if message.tags:
                        for key in message.tags:
                            if key != "emote-sets" and key != "ban-duration" and key != "bits":
                                if type(message.tags[key]) == bool:
                                    message.tags[key] = None
                                elif message.tags[key] == '1':
                                    message.tags[key] = True
                                elif message.tags[key] == '0':
                                    message.tags[key] = False
                                elif type(message.tags[key]) == str:
                                    pass
                except Exception as err:
                    _EVENT.emit("IRCv3 Transformer (MessageHandler):", SERVEREVENTS.ERROR, err)

                # Handle message with no prfix
                if message.prefix == None:
                    try:
                        if message.command == COMMANDS.PING:
                            _EVENT.emit(MessageHandler, COMMANDS.PING)
                        elif message.command == COMMANDS.PONG:
                            _EVENT.emit(MessageHandler, COMMANDS.PONG)
                        else:
                            _EVENT.emit(MessageHandler, SERVEREVENTS.ERROR,\
                               "Could not parse message with no prefix:\n {}".format(message))
                    except Exception as err:
                        _EVENT.emit("Handle message no prifix (MessageHandler):", SERVEREVENTS.ERROR, err)

                # Handle message with prefix "tmi.twitch.tv"
                elif message.prefix == SERVEREVENTS.TMI_TWITCH_TV:

                    # Handle command  bot Username
                    if message.command == SERVEREVENTS.USERNAME:
                        username = message.params[0]

                    # Handle command CONNECTED (372
                    elif message.command == SERVEREVENTS.CONNECTED:  # Connected to server
                        _EVENT.emit(MessageHandler, SERVEREVENTS.CONNECTED)

                    # Handle command CLEARCHAT
                    elif message.command == COMMANDS.CLEARCHAT:
                        _EVENT.emit(MessageHandler, COMMANDS.CLEARCHAT, message)

                    # Handle command CLEARMSG
                    elif message.command == COMMANDS.CLEARMSG:
                        message.username = message.tags["display-name"] or message.tags["login"]
                        message.id = message.tags["target-msg-id"] or None
                        _EVENT.emit(MessageHandler, COMMANDS.CLEARMSG, message)

                    # Handle command HOSTTARGET
                    elif message.command == COMMANDS.HOSTTARGET:
                        _EVENT.emit(MessageHandler, COMMANDS.HOSTTARGET, message)

                    # Chatroom NOTICE check msgid tag
                    elif message.command == COMMANDS.NOTICE:
                        _EVENT.emit(MessageHandler, COMMANDS.NOTICE, message)

                        if message.id == MESSAGEIDS.ALREADY_BANNED:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.ALREADY_BANNED, message)

                        elif message.id == MESSAGEIDS.ALREADY_EMOTE_ONLY_OFF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.ALREADY_EMOTE_ONLY_OFF, message)

                        elif message.id == MESSAGEIDS.ALREADY_EMOTE_ONLY_ON:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.ALREADY_EMOTE_ONLY_ON, message)

                        elif message.id == MESSAGEIDS.ALREADY_R9K_OFF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.ALREADY_R9K_OFF, message)

                        elif message.id == MESSAGEIDS.ALREADY_R9K_ON:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.ALREADY_R9K_ON, message)

                        elif message.id == MESSAGEIDS.ALREADY_SUBS_OFF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.ALREADY_SUBS_OFF, message)

                        elif message.id == MESSAGEIDS.ALREADY_SUBS_ON:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.ALREADY_SUBS_ON, message)

                        elif message.id == MESSAGEIDS.BAD_BAN_ADMIN:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_BAN_ADMIN, message)

                        elif message.id == MESSAGEIDS.BAD_BAN_ANON:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_BAN_ANON, message)

                        elif message.id == MESSAGEIDS.BAD_BAN_BROADCASTER:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_BAN_BROADCASTER, message)

                        elif message.id == MESSAGEIDS.BAD_BAN_GLOBAL_MOD:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_BAN_GLOBAL_MOD, message)

                        elif message.id == MESSAGEIDS.BAD_BAN_MOD:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_BAN_MOD, message)

                        elif message.id == MESSAGEIDS.BAD_BAN_SELF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_BAN_SELF, message)

                        elif message.id == MESSAGEIDS.BAD_BAN_STAFF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_BAN_STAFF, message)

                        elif message.id == MESSAGEIDS.BAD_COMMERCIAL_ERROR:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_COMMERCIAL_ERROR, message)

                        elif message.id == MESSAGEIDS.BAD_DELETE_MESSAGE_BROADCASTER:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_DELETE_MESSAGE_BROADCASTER, message)

                        elif message.id == MESSAGEIDS.BAD_DELETE_MESSAGE_MOD:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_DELETE_MESSAGE_MOD, message)

                        elif message.id == MESSAGEIDS.BAD_HOST_ERROR:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_HOST_ERROR, message)

                        elif message.id == MESSAGEIDS.BAD_HOST_HOSTING:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_HOST_HOSTING, message)

                        elif message.id == MESSAGEIDS.BAD_HOST_RATE_EXCEEDED:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_HOST_RATE_EXCEEDED, message)

                        elif message.id == MESSAGEIDS.BAD_HOST_REJECTED:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_HOST_REJECTED, message)

                        elif message.id == MESSAGEIDS.BAD_HOST_SELF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_HOST_SELF, message)

                        elif message.id == MESSAGEIDS.BAD_MARKER_CLIENT:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_MARKER_CLIENT, message)

                        elif message.id == MESSAGEIDS.BAD_MOD_BANNED:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_MOD_BANNED, message)

                        elif message.id == MESSAGEIDS.BAD_MOD_MOD:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_MOD_MOD, message)

                        elif message.id == MESSAGEIDS.BAD_SLOW_DURATION:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_SLOW_DURATION, message)

                        elif message.id == MESSAGEIDS.BAD_TIMEOUT_ADMIN:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_TIMEOUT_ADMIN, message)

                        elif message.id == MESSAGEIDS.BAD_TIMEOUT_ANON:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_TIMEOUT_ANON, message)

                        elif message.id == MESSAGEIDS.BAD_TIMEOUT_BROADCASTER:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_TIMEOUT_BROADCASTER, message)

                        elif message.id == MESSAGEIDS.BAD_TIMEOUT_DURATION:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_TIMEOUT_DURATION, message)

                        elif message.id == MESSAGEIDS.BAD_TIMEOUT_GLOBAL_MOD:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_TIMEOUT_GLOBAL_MOD, message)

                        elif message.id == MESSAGEIDS.BAD_TIMEOUT_MOD:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_TIMEOUT_MOD, message)

                        elif message.id == MESSAGEIDS.BAD_TIMEOUT_SELF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_TIMEOUT_SELF, message)

                        elif message.id == MESSAGEIDS.BAD_TIMEOUT_STAFF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_TIMEOUT_STAFF, message)

                        elif message.id == MESSAGEIDS.BAD_UNBAN_NO_BAN:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_UNBAN_NO_BAN, message)

                        elif message.id == MESSAGEIDS.BAD_UNHOST_ERROR:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_UNHOST_ERROR, message)

                        elif message.id == MESSAGEIDS.BAD_UNMOD_MOD:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAD_UNMOD_MOD, message)

                        elif message.id == MESSAGEIDS.BAN_SUCCESS:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.BAN_SUCCESS, message)

                        elif message.id == MESSAGEIDS.CMDS_AVAILABLE:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.CMDS_AVAILABLE, message)

                        elif message.id == MESSAGEIDS.COLOR_CHANGED:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.COLOR_CHANGED, message)

                        elif message.id == MESSAGEIDS.COMMERCIAL_SUCCESS:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.COMMERCIAL_SUCCESS, message)

                        elif message.id == MESSAGEIDS.DELETE_MESSAGE_SUCCESS:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.DELETE_MESSAGE_SUCCESS, message)

                        elif message.id == MESSAGEIDS.EMOTE_ONLY_OFF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.EMOTE_ONLY_OFF, message)

                        elif message.id == MESSAGEIDS.EMOTE_ONLY_ON:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.EMOTE_ONLY_ON, message)

                        elif message.id == MESSAGEIDS.FOLLOWERS_OFF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.FOLLOWERS_OFF, message)

                        elif message.id == MESSAGEIDS.FOLLOWERS_ON:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.FOLLOWERS_ON, message)

                        elif message.id == MESSAGEIDS.FOLLOWERS_ONZERO:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.FOLLOWERS_ONZERO, message)

                        elif message.id == MESSAGEIDS.HOST_OFF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.HOST_OFF, message)

                        elif message.id == MESSAGEIDS.HOST_ON:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.HOST_ON, message)

                        elif message.id == MESSAGEIDS.HOST_SUCCESS:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.HOST_SUCCESS, message)

                        elif message.id == MESSAGEIDS.HOST_SUCCESS_VIEWERS:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.HOST_SUCCESS_VIEWERS, message)

                        elif message.id == MESSAGEIDS.HOST_TARGET_WENT_OFFLINE:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.HOST_TARGET_WENT_OFFLINE, message)

                        elif message.id == MESSAGEIDS.HOSTS_REMAINING:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.HOSTS_REMAINING, message)

                        elif message.id == MESSAGEIDS.INVALID_USER:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.INVALID_USER, message)

                        elif message.id == MESSAGEIDS.MOD_SUCCESS:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MOD_SUCCESS, message)

                        elif message.id == MESSAGEIDS.MSG_BANNED:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_BANNED, message)

                        elif message.id == MESSAGEIDS.MSG_BAD_CHARACTERS:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_BAD_CHARACTERS, message)

                        elif message.id == MESSAGEIDS.MSG_CHANNEL_BLOCKED:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_CHANNEL_BLOCKED, message)

                        elif message.id == MESSAGEIDS.MSG_CHANNEL_SUSPENDED:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_CHANNEL_SUSPENDED, message)

                        elif message.id == MESSAGEIDS.MSG_DUPLICATE:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_DUPLICATE, message)

                        elif message.id == MESSAGEIDS.MSG_EMOTEONLY:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_EMOTEONLY, message)

                        elif message.id == MESSAGEIDS.MSG_FACEBOOK:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_FACEBOOK, message)

                        elif message.id == MESSAGEIDS.MSG_FOLLOWERSONLY:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_FOLLOWERSONLY, message)

                        elif message.id == MESSAGEIDS.MSG_FOLLOWERSONLY_FOLLOWED:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_FOLLOWERSONLY_FOLLOWED, message)

                        elif message.id == MESSAGEIDS.MSG_FOLLOWERSONLY_ZERO:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_FOLLOWERSONLY_ZERO, message)

                        elif message.id == MESSAGEIDS.MSG_R9K:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_R9K, message)

                        elif message.id == MESSAGEIDS.MSG_RATELIMIT:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_RATELIMIT, message)

                        elif message.id == MESSAGEIDS.MSG_REJECTED:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_REJECTED, message)

                        elif message.id == MESSAGEIDS.MSG_REJECTED_MANDATORY:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_REJECTED_MANDATORY, message)

                        elif message.id == MESSAGEIDS.MSG_ROOM_NOT_FOUND:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_ROOM_NOT_FOUND, message)

                        elif message.id == MESSAGEIDS.MSG_SLOWMODE:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_SLOWMODE, message)

                        elif message.id == MESSAGEIDS.MSG_SUBSONLY:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_SUBSONLY, message)

                        elif message.id == MESSAGEIDS.MSG_SUSPENDED:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_SUSPENDED, message)

                        elif message.id == MESSAGEIDS.MSG_TIMEDOUT:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_TIMEDOUT, message)

                        elif message.id == MESSAGEIDS.MSG_VERIFIED_EMAIL:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.MSG_VERIFIED_EMAIL, message)

                        elif message.id == MESSAGEIDS.NO_HELP:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.NO_HELP, message)

                        elif message.id == MESSAGEIDS.NO_MODS:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.NO_MODS, message)

                        elif message.id == MESSAGEIDS.NOT_HOSTING:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.NOT_HOSTING, message)

                        elif message.id == MESSAGEIDS.NO_PERMISSION:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.NO_PERMISSION, message)

                        elif message.id == MESSAGEIDS.R9K_OFF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.R9K_OFF, message)

                        elif message.id == MESSAGEIDS.R9K_ON:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.R9K_ON, message)

                        elif message.id == MESSAGEIDS.RAID_ERROR_ALREADY_RAIDING:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.RAID_ERROR_ALREADY_RAIDING, message)

                        elif message.id == MESSAGEIDS.RAID_ERROR_FORBIDDEN:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.RAID_ERROR_FORBIDDEN, message)

                        elif message.id == MESSAGEIDS.RAID_ERROR_SELF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.RAID_ERROR_SELF, message)

                        elif message.id == MESSAGEIDS.RAID_ERROR_TOO_MANY_VIEWERS:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.RAID_ERROR_TOO_MANY_VIEWERS, message)

                        elif message.id == MESSAGEIDS.RAID_ERROR_UNEXPECTED:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.RAID_ERROR_UNEXPECTED, message)

                        elif message.id == MESSAGEIDS.RAID_NOTICE_MATURE:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.RAID_NOTICE_MATURE, message)

                        elif message.id == MESSAGEIDS.RAID_NOTICE_RESTRICTED_CHAT:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.RAID_NOTICE_RESTRICTED_CHAT, message)

                        elif message.id == MESSAGEIDS.ROOM_MODS:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.ROOM_MODS, message)

                        elif message.id == MESSAGEIDS.SLOW_OFF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.SLOW_OFF, message)

                        elif message.id == MESSAGEIDS.SLOW_ON:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.SLOW_ON, message)

                        elif message.id == MESSAGEIDS.SUBS_OFF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.SUBS_OFF, message)

                        elif message.id == MESSAGEIDS.SUBS_ON:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.SUBS_ON, message)

                        elif message.id == MESSAGEIDS.TIMEOUT_NO_TIMEOUT:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.TIMEOUT_NO_TIMEOUT, message)

                        elif message.id == MESSAGEIDS.TIMEOUT_SUCCESS:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.TIMEOUT_SUCCESS, message)

                        elif message.id == MESSAGEIDS.TOS_BAN:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.TOS_BAN, message)

                        elif message.id == MESSAGEIDS.TURBO_ONLY_COLOR:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.TURBO_ONLY_COLOR, message)

                        elif message.id == MESSAGEIDS.UNBAN_SUCCESS:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.UNBAN_SUCCESS, message)

                        elif message.id == MESSAGEIDS.UNMOD_SUCCESS:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.UNMOD_SUCCESS, message)

                        elif message.id == MESSAGEIDS.UNRAID_ERROR_NO_ACTIVE_RAID:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.UNRAID_ERROR_NO_ACTIVE_RAID, message)

                        elif message.id == MESSAGEIDS.UNRAID_ERROR_UNEXPECTED:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.UNRAID_ERROR_UNEXPECTED, message)

                        elif message.id == MESSAGEIDS.UNRAID_SUCCESS:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.UNRAID_SUCCESS, message)

                        elif message.id == MESSAGEIDS.UNRECOGNIZED_CMD:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.UNRECOGNIZED_CMD, message)

                        elif message.id == MESSAGEIDS.UNSUPPORTED_CHATROOMS_CMD:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.UNSUPPORTED_CHATROOMS_CMD, message)

                        elif message.id == MESSAGEIDS.UNTIMEOUT_BANNED:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.UNTIMEOUT_BANNED, message)

                        elif message.id == MESSAGEIDS.UNTIMEOUT_SUCCESS:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.UNTIMEOUT_SUCCESS, message)

                        elif message.id == MESSAGEIDS.USAGE_BAN:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_BAN, message)

                        elif message.id == MESSAGEIDS.USAGE_CLEAR:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_CLEAR, message)

                        elif message.id == MESSAGEIDS.USAGE_COLOR:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_COLOR, message)

                        elif message.id == MESSAGEIDS.USAGE_COMMERCIAL:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_COMMERCIAL, message)

                        elif message.id == MESSAGEIDS.USAGE_DISCONNECT:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_DISCONNECT, message)

                        elif message.id == MESSAGEIDS.USAGE_EMOTE_ONLY_OFF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_EMOTE_ONLY_OFF, message)

                        elif message.id == MESSAGEIDS.USAGE_EMOTE_ONLY_ON:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_EMOTE_ONLY_ON, message)

                        elif message.id == MESSAGEIDS.USAGE_FOLLOWERS_OFF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_FOLLOWERS_OFF, message)

                        elif message.id == MESSAGEIDS.USAGE_FOLLOWERS_ON:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_FOLLOWERS_ON, message)

                        elif message.id == MESSAGEIDS.USAGE_HELP:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_HELP, message)

                        elif message.id == MESSAGEIDS.USAGE_HOST:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_HOST, message)

                        elif message.id == MESSAGEIDS.USAGE_MARKER:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_MARKER, message)

                        elif message.id == MESSAGEIDS.USAGE_ME:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_ME, message)

                        elif message.id == MESSAGEIDS.USAGE_MOD:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_MOD, message)

                        elif message.id == MESSAGEIDS.USAGE_MODS:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_MODS, message)

                        elif message.id == MESSAGEIDS.USAGE_R9K_OFF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_R9K_OFF, message)

                        elif message.id == MESSAGEIDS.USAGE_R9K_ON:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_R9K_ON, message)

                        elif message.id == MESSAGEIDS.USAGE_RAID:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_RAID, message)

                        elif message.id == MESSAGEIDS.USAGE_SLOW_OFF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_SLOW_OFF, message)

                        elif message.id == MESSAGEIDS.USAGE_SLOW_ON:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_SLOW_ON, message)

                        elif message.id == MESSAGEIDS.USAGE_SUBS_OFF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_SUBS_OFF, message)

                        elif message.id == MESSAGEIDS.USAGE_SUBS_ON:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_SUBS_ON, message)

                        elif message.id == MESSAGEIDS.USAGE_TIMEOUT:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_TIMEOUT, message)

                        elif message.id == MESSAGEIDS.USAGE_UNBAN:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_UNBAN, message)

                        elif message.id == MESSAGEIDS.USAGE_UNHOST:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_UNHOST, message)

                        elif message.id == MESSAGEIDS.USAGE_UNMOD:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_UNMOD, message)

                        elif message.id == MESSAGEIDS.USAGE_UNRAID:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_UNRAID, message)

                        elif message.id == MESSAGEIDS.USAGE_UNTIMEOUT:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.USAGE_UNTIMEOUT, message)

                        elif message.id == MESSAGEIDS.WHISPER_BANNED:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.WHISPER_BANNED, message)

                        elif message.id == MESSAGEIDS.WHISPER_BANNED_RECIPIENT:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.WHISPER_BANNED_RECIPIENT, message)

                        elif message.id == MESSAGEIDS.WHISPER_INVALID_ARGS:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.WHISPER_INVALID_ARGS, message)

                        elif message.id == MESSAGEIDS.WHISPER_INVALID_LOGIN:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.WHISPER_INVALID_LOGIN, message)

                        elif message.id == MESSAGEIDS.WHISPER_INVALID_SELF:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.WHISPER_INVALID_SELF, message)

                        elif message.id == MESSAGEIDS.WHISPER_LIMIT_PER_MIN:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.WHISPER_LIMIT_PER_MIN, message)

                        elif message.id == MESSAGEIDS.WHISPER_LIMIT_PER_SEC:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.WHISPER_LIMIT_PER_SEC, message)

                        elif message.id == MESSAGEIDS.WHISPER_RESTRICTED:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.WHISPER_RESTRICTED, message)

                        elif message.id == MESSAGEIDS.WHISPER_RESTRICTED_RECIPIENT:
                            _EVENT.emit(MessageHandler, MESSAGEIDS.WHISPER_RESTRICTED_RECIPIENT, message)
                        else:
                            if message.raw.find("Login unsuccessful") > 0 \
                                    or message.raw.find("Login authentication failed") > 0:
                                _EVENT.emit(MessageHandler, SERVEREVENTS.LOGIN_UNSUCCESSFUL, \
                                    "Login authentication failed")

                            elif message.raw.find("Error logging in") > 0 \
                                    or message.raw.find("Improperly formatted auth") > 0:
                                _EVENT.emit(MessageHandler, SERVEREVENTS.LOGIN_UNSUCCESSFUL,\
                                   "Login authentication failed")

                            elif message.raw.find("Invalid NICK") > 0:
                                _EVENT.emit(MessageHandler, SERVEREVENTS.LOGIN_UNSUCCESSFUL, "Invalid User")

                    # Handle command RECONNECT
                    elif message.command == COMMANDS.RECONNECT:
                        _EVENT.emit(MessageHandler, COMMANDS.RECONNECT)

                    # Handle command ROOMSTATE
                    elif message.command == COMMANDS.ROOMSTATE:
                        _EVENT.emit(MessageHandler, COMMANDS.ROOMSTATE, message)

                    # Handle command USERNOTICE
                    elif message.command == COMMANDS.USERNOTICE:
                        _EVENT.emit(MessageHandler, COMMANDS.USERNOTICE, message)

                    # Handle command USERSTATE
                    elif message.command == COMMANDS.USERSTATE:
                        _EVENT.emit(MessageHandler, COMMANDS.USERSTATE, message)

                # Handle message with prefix jtv
                elif message.prefix == "jtv":
                    print(message.params)

                else:
                    if message.command == SERVEREVENTS.MESSAGE:
                        message.username: str = message.prefix[:message.prefix.find("!")]
                        _EVENT.emit(MessageHandler, SERVEREVENTS.MESSAGE, message)

                    elif message.command == SERVEREVENTS.NAMES:
                        _EVENT.emit(MessageHandler, SERVEREVENTS.NAMES, message)
                        pass
        return

class _Parser(object):
    """
    parses incomming data from IRC chat
   : Returns: parsed message type
    """
    @staticmethod
    def badges(tags)->dict:
        """parse badges dict"""
        try:
            if "badges" in tags and type(tags["badges"]) == str:
                badges = {}
                explode = tags["badges"].split(",")
                for item in explode:
                    parts = item.split("/")
                    if parts[1] == None:
                        return
                    badges[parts[0]] = parts[1]
                tags["badges-raw"] = tags["badges"]
                tags["badges"] = badges

            if "badges" in tags and type(tags["badges"]) == bool:
                tags["badges-raw"] = None

            return tags
        except:
            pass
    @staticmethod
    def emotes(tags)->list:
        """ parse emotes to list"""
        try:
            if "emotes" in tags and type(tags["emotes"]) == str:
                emoticons = tags["emotes"].split("/")
                emotes = {}
                for emoticon in emoticons:
                    part = emoticon.split(":")
                    if part[1] == None:
                        return
                    emotes[part[0]] = part[1].split(",")

                tags["emotes-raw"] = tags["emotes"]
                tags["emotes"] = emotes
            if "emotes" in tags and type(tags["emotes"]) == bool:
                tags["emotes-raw"] = None
            return tags
        except:
            pass


    @staticmethod
    def parse(data: str)->Message:
        if type(data) != str:
            raise TypeError("_Parse.parse require input of type str")

        message: Message = Message()
        position: int = 0
        nextspace = 0

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
            postion += 1

        if data[position] == chr(58):
            nextspace = data.find(chr(32), position)

            if nextspace == -1:
                return None

            message.prefix = data[position+1:nextspace]
            position = nextspace + 1

            while data[position] == chr(32):
                postion += 1

        nextspace = data.find(" ", position)

        if nextspace == -1:
            if len(data) > position:
                #possible out of range err
                message.command = data[position:]
                return message

            return None
        message.command = data[position:nextspace]

        position = nextspace + 1

        while data[position] == chr(32):
            postion += 1
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
                    postion += 1
                continue

            if nextspace == -1:
                message.params.append(data[position:])
                break

        return message
