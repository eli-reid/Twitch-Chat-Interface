import threading  
import socket
import time
import queue
from lib.events.eventHandler import eventHandler as _EVENT 
from lib.twitchMessageHandler.messageHandler import  MessageHandler as _messageHandler, COMMANDS, SERVEREVENTS, MESSAGEIDS, EVENTS
from datetime import datetime

      
class TwitchChatInterface(object):
    """
        creates connection to twitch chat irc server and receives chat messages 
        then emits events for the type of message received  
    """
    # Event setter static fucntions
 
    # IRC Command constants 
    _CAPREQUEST :str = "CAP REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership"
    _PASS :str = "PASS {}"           
    _NICK :str = "NICK {}"
    _JOIN :str = "JOIN #{}"
    _PONG :str = "PONG :{}"
    _PING :str = "PING :{}"
    
    def __init__(self,settings :dict):
        """set values from settings"""
         
        # Set outside access to  constants 
        self.COMMANDS :COMMANDS = COMMANDS 
        self.SERVEREVENTS :SERVEREVENTS = SERVEREVENTS
        self.MESSAGEIDS :MESSAGEIDS  = MESSAGEIDS 
        self.on :On = self.On()
        # Register System Event functions
        _EVENT.onError(self._ERROR)
        _EVENT.on(SERVEREVENTS.ERROR,self._ERROR)
        _EVENT.on(SERVEREVENTS.CONNECTED,self._CONNECTED)
        _EVENT.on(COMMANDS.PING,self._onPING)
        _EVENT.on(COMMANDS.PONG,self._onPONG)
        
        # Populate settings values
        self._server :str = settings['server']
        self._port :int = settings['port']
        self._user :str = settings['user']
        self._password :str = settings['password']
        self._chatrooms :list = settings['chatrooms']
        self._pingWait :int = 5*60
        
        # Set helper Varibles
        self._disconnect :bool = False
        self._lastPing :time = time.time()
        self._sendMessageQ :queue = queue.SimpleQueue()
        self._socket :socket = socket.socket()
             

    def connect(self)->None:
        """ 
        Connect to IRC server
        """
        try:
            # Create new socket and connect
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM,) as self._socket : 
                self._socket.connect((self._server,self._port))

                # Send login cradentials
                self.send(self._CAPREQUEST)
                self.send(self._PASS.format(self._password))
                self.send(self._NICK.format(self._user))
                
                
                # Start listing for server response
                self._listenThread  :threading.Thread = threading.Thread(target=self._awaitResponse(), daemon=True)
                self._listenThread.start()

        except Exception as err:
            _EVENT.emit(self.connect, SERVEREVENTS.ERROR, err)
        return
    
    def disconnect(self)->None:
        """ diconnnect """
        self._disconnect  = True
        return

    def send(self,message :str)->None:
        self._socket.setblocking(1)
        ## ADD Q and timer###
        if not message.endswith("\r\n"):
            message += "\r\n"
        try:
            self._socket.send(message.encode())
        except Exception as err:
           _EVENT.emit(self._awaitResponse, SERVEREVENTS.ERROR, err)
        return 

    def joinRooms(self,rooms)->None:
        for room in rooms:
            self.send(self._JOIN.format(room))
            time.sleep(3)
        return

    def _awaitResponse(self)->None:
        """   """
        while self._disconnect == False:

            # disable sockets errror supression to maintian local event loop
            self._socket.setblocking(0)

            # start keep alive ping thread
            self._pingTimer()           
            try:
                #Check for received data and handle any data
                data :str = self._socket.recv(4096).decode()
                print (data)
                _messageHandler.messageHandler(data)
                _EVENT.emit(self,SERVEREVENTS.RECEIVED, data)
            except:
                #Ignoring error from Socket.recev, reports error if no data avilable
                pass 
        _EVENT.emit(self,SERVEREVENTS.DISCONNECTED)

    def _pingTimer(self):
        """ pingtimer"""

        try:
            if time.time() - self._lastPing > self._pingWait:
                self.send(self._PING.format(SERVEREVENTS.TMI_TWITCH_TV))
        except Exception as err:
           _EVENT.emit(self, SERVEREVENTS.ERROR, err)

    # System Event functions 
    def _ERROR(self,sender,obj):
        print("ERROR:  ",sender, obj)
        self.disconnect()

    def _CONNECTED(self,sender,obj):
        joinRoomsThread=threading.Thread(target=self.joinRooms,kwargs={'rooms':self._chatrooms})
        joinRoomsThread.start()
    
    def _onPING(self,sender,obj):
        try:
            self._lastPing = time.time()
            self.send(self._PONG.format("tmi.twitch.tv"))
        except Exception as err:
           _EVENT.emit(self, SERVEREVENTS.ERROR, err)
        return 
     
    def _onPONG(self,sender,obj):
        try:
            self._lastPing = time.time()
            self.send(self._PING.format("tmi.twitch.tv"))
        except Exception as err:
           _EVENT.emit(self, SERVEREVENTS.ERROR, err)
        return   

    class On():
        """ 
        supply a function you want to call during an event 
        IE: 
            self.on.eventConnected(myFunction)

            How to Declare myfucntion: 
                Requires 2 input varibles 
                    sender: is the obj or name of class or function responsible for event
                    obj: is of type Message look at documents for more information on Message class type.

                    def myFunction(sender,obj)
                        return
        """
        def __init__(self):
            self.ServerEvent  :ServerEvent 
            self.CommandEvent :CommandEvent
            self.MsgIdEvent :MsgIdEvent
           
           # events handle by standard message type 
        def eventDisconnected(self,func):  
            self.ServerEvent.DISCONNECTED(func)

        def eventMessage(self,func):
            self.ServerEvent.MESSAGE(func)

        def eventJoin(self,func):  
            self.ServerEvent.JOIN(func)

        def eventError(self,func): 
            self.ServerEvent.ERROR(func)

        def eventLoginError(self,func):  
            self.ServerEvent.LOGIN_UNSUCCESSFUL(func)   
            
        def eventWhisper(self,func): 
            self.ServerEvent.WHISPER(func)

        def eventConnected(self,func): 
            self.ServerEvent.CONNECTED(func)

        def eventReconnect(self,func):
            self.CommandEvent.RECONNECT(func)
        
        # events handled by other message types - ie: evnetSubsOff is handled by ROOMSTATE event vs NOTICE event message.id "subs-off" 
        def eventSubsOff(func):
                _EVENT.on(EVENTS.SUBSOFF, func)
 
        def eventSubsOn(func):
                _EVENT.on(EVENTS.SUBSON, func)
 
        
        class ServerEvent:
            def LOGIN_UNSUCCESSFUL(func) ->None:
                _EVENT.on(SERVEREVENTS.LOGIN_UNSUCCESSFUL, func)

            def MESSAGE(func) ->None:
                _EVENT.on(SERVEREVENTS.MESSAGE, func)

            def JOIN(func) ->None:
                _EVENT.on(SERVEREVENTS.JOIN, func)

            def RECEIVED(func) ->None:
                _EVENT.on(SERVEREVENTS.RECEIVED, func)

            def CONNECTED(func) ->None:
                _EVENT.on(SERVEREVENTS.CONNECTED , func)

            def ERROR(func) ->None:
                _EVENT.on(SERVEREVENTS.ERROR, func)

            def DISCONNECTED (func) ->None:
                _EVENT.on(SERVEREVENTS.DISCONNECTED , func)

            def USERNAME(func) ->None:
                _EVENT.on(SERVEREVENTS.USERNAME, func)

            def NAMES(func) ->None:
                _EVENT.on(SERVEREVENTS. NAMES, func)

            def WHISPER(func) ->None:
                _EVENT.on(SERVEREVENTS.WHISPER, func)

            def PART(func) ->None:
                _EVENT.on(SERVEREVENTS.PART, func)

            def TMI_TWITCH_TV (func) ->None:
                _EVENT.on(SERVEREVENTS.TMI_TWITCH_TV , func)

        class CommandEvent:
            def PING(func) ->None:
                _EVENT.on(COMMANDS.PING, func)

            def PONG(func) ->None:
                _EVENT.on(COMMANDS.PONG, func)

            def CLEARMSG(func) ->None:
                _EVENT.on(COMMANDS.CLEARMSG, func)

            def HOSTTARGET(func) ->None:
                _EVENT.on(COMMANDS.HOSTTARGET, func)

            def NOTICE(func) ->None:
                _EVENT.on(COMMANDS.NOTICE, func)

            def RECONNECT(func) ->None:
                _EVENT.on(COMMANDS.RECONNECT, func)

            def ROOMSTATE(func) ->None:
                _EVENT.on(COMMANDS.ROOMSTATE, func)

            def USERNOTICE(func) ->None:
                _EVENT.on(COMMANDS.USERNOTICE, func)

            def USERSTATE(func) ->None:
                _EVENT.on(COMMANDS.USERSTATE, func)

        class MsgIdEvent:
            def ALREADY_BANNED(func) ->None:
                _EVENT.on(MESSAGEIDS.ALREADY_BANNED, func)

            def ALREADY_EMOTE_ONLY_OFF(func) ->None:
                _EVENT.on(MESSAGEIDS.ALREADY_EMOTE_ONLY_OFF, func)


            def ALREADY_EMOTE_ONLY_ON(func) ->None:
                _EVENT.on(MESSAGEIDS.ALREADY_EMOTE_ONLY_ON, func)

            def ALREADY_R9K_OFF(func) ->None:
                _EVENT.on(MESSAGEIDS.ALREADY_R9K_OFF, func)

            def ALREADY_R9K_ON(func) ->None:
                _EVENT.on(MESSAGEIDS.ALREADY_R9K_ON, func)

            def ALREADY_SUBS_OFF(func) ->None:
                _EVENT.on(MESSAGEIDS.ALREADY_SUBS_OFF, func)

            def ALREADY_SUBS_ON(func) ->None:
                _EVENT.on(MESSAGEIDS.ALREADY_SUBS_ON, func)

            def BAD_BAN_ADMIN(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_BAN_ADMIN, func)

            def BAD_BAN_ANON(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_BAN_ANON, func)

            def BAD_BAN_BROADCASTER(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_BAN_BROADCASTER, func)

            def BAD_BAN_GLOBAL_MOD(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_BAN_GLOBAL_MOD, func)

            def BAD_BAN_MOD(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_BAN_MOD, func)

            def BAD_BAN_SELF(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_BAN_SELF,func)
            def BAD_BAN_STAFF(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_BAN_STAFF, func)

            def BAD_COMMERCIAL_ERROR(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_COMMERCIAL_ERROR, func)

            def BAD_DELETE_MESSAGE_BROADCASTER(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_DELETE_MESSAGE_BROADCASTER, func)

            def BAD_DELETE_MESSAGE_MOD(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_DELETE_MESSAGE_MOD, func)

            def BAD_HOST_ERROR(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_HOST_ERROR, func)

            def BAD_HOST_HOSTING(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_HOST_HOSTING, func)

            def BAD_HOST_RATE_EXCEEDED(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_HOST_RATE_EXCEEDED, func)

            def BAD_HOST_REJECTED(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_HOST_REJECTED, func)

            def BAD_HOST_SELF(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_HOST_SELF, func)

            def BAD_MARKER_CLIENT(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_MARKER_CLIENT, func)

            def BAD_MOD_BANNED(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_MOD_BANNED, func)

            def BAD_MOD_MOD(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_MOD_MOD, func)

            def BAD_SLOW_DURATION(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_SLOW_DURATION, func)

            def BAD_TIMEOUT_ADMIN(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_TIMEOUT_ADMIN, func)

            def BAD_TIMEOUT_ANON(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_TIMEOUT_ANON, func)

            def BAD_TIMEOUT_BROADCASTER(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_TIMEOUT_BROADCASTER, func)

            def BAD_TIMEOUT_DURATION(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_TIMEOUT_DURATION, func)

            def BAD_TIMEOUT_GLOBAL_MOD(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_TIMEOUT_GLOBAL_MOD, func)

            def BAD_TIMEOUT_MOD(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_TIMEOUT_MOD, func)

            def BAD_TIMEOUT_SELF(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_TIMEOUT_SELF, func)

            def BAD_TIMEOUT_STAFF(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_TIMEOUT_STAFF, func)

            def BAD_UNBAN_NO_BAN(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_UNBAN_NO_BAN, func)

            def BAD_UNHOST_ERROR(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_UNHOST_ERROR, func)

            def BAD_UNMOD_MOD(func) ->None:
                _EVENT.on(MESSAGEIDS.BAD_UNMOD_MOD, func)

            def BAN_SUCCESS(func) ->None:
                _EVENT.on(MESSAGEIDS.BAN_SUCCESS, func)

            def CMDS_AVAILABLE(func) ->None:
                _EVENT.on(MESSAGEIDS.CMDS_AVAILABLE, func)

            def COLOR_CHANGED(func) ->None:
                _EVENT.on(MESSAGEIDS.COLOR_CHANGED, func)

            def COMMERCIAL_SUCCESS(func) ->None:
                _EVENT.on(MESSAGEIDS.COMMERCIAL_SUCCESS, func)

            def DELETE_MESSAGE_SUCCESS(func) ->None:
                _EVENT.on(MESSAGEIDS.DELETE_MESSAGE_SUCCESS, func)

            def EMOTE_ONLY_OFF(func) ->None:
                _EVENT.on(MESSAGEIDS.EMOTE_ONLY_OFF, func)

            def EMOTE_ONLY_ON(func) ->None:
                _EVENT.on(MESSAGEIDS.EMOTE_ONLY_ON, func)

            def FOLLOWERS_OFF(func) ->None:
                _EVENT.on(MESSAGEIDS.FOLLOWERS_OFF, func)

            def FOLLOWERS_ON(func) ->None:
                _EVENT.on(MESSAGEIDS.FOLLOWERS_ON, func)

            def FOLLOWERS_ONZERO(func) ->None:
                _EVENT.on(MESSAGEIDS.FOLLOWERS_ONZERO, func)

            def HOST_OFF(func) ->None:
                _EVENT.on(MESSAGEIDS.HOST_OFF, func)

            def HOST_ON(func) ->None:
                _EVENT.on(MESSAGEIDS.HOST_ON, func)

            def HOST_SUCCESS(func) ->None:
                _EVENT.on(MESSAGEIDS.HOST_SUCCESS, func)

            def HOST_SUCCESS_VIEWERS(func) ->None:
                _EVENT.on(MESSAGEIDS.HOST_SUCCESS_VIEWERS, func)

            def HOST_TARGET_WENT_OFFLINE(func) ->None:
                _EVENT.on(MESSAGEIDS.HOST_TARGET_WENT_OFFLINE, func)

            def HOSTS_REMAINING(func) ->None:
                _EVENT.on(MESSAGEIDS.HOSTS_REMAINING, func)

            def INVALID_USER(func) ->None:
                _EVENT.on(MESSAGEIDS.INVALID_USER, func)

            def MOD_SUCCESS(func) ->None:
                _EVENT.on(MESSAGEIDS.MOD_SUCCESS, func)

            def MSG_BANNED(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_BANNED, func)

            def MSG_BAD_CHARACTERS(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_BAD_CHARACTERS, func)

            def MSG_CHANNEL_BLOCKED(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_CHANNEL_BLOCKED, func)

            def MSG_CHANNEL_SUSPENDED(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_CHANNEL_SUSPENDED, func)

            def MSG_DUPLICATE(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_DUPLICATE, func)

            def MSG_EMOTEONLY(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_EMOTEONLY, func)

            def MSG_FACEBOOK(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_FACEBOOK, func)

            def MSG_FOLLOWERSONLY(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_FOLLOWERSONLY, func)

            def MSG_FOLLOWERSONLY_FOLLOWED(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_FOLLOWERSONLY_FOLLOWED, func)

            def MSG_FOLLOWERSONLY_ZERO(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_FOLLOWERSONLY_ZERO, func)

            def MSG_R9K(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_R9K, func)

            def MSG_RATELIMIT(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_RATELIMIT, func)

            def MSG_REJECTED(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_REJECTED, func)

            def MSG_REJECTED_MANDATORY(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_REJECTED_MANDATORY, func)

            def MSG_ROOM_NOT_FOUND(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_ROOM_NOT_FOUND, func)

            def MSG_SLOWMODE(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_SLOWMODE, func)

            def MSG_SUBSONLY(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_SUBSONLY, func)

            def MSG_SUSPENDED(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_SUSPENDED, func)

            def MSG_TIMEDOUT(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_TIMEDOUT, func)

            def MSG_VERIFIED_EMAIL(func) ->None:
                _EVENT.on(MESSAGEIDS.MSG_VERIFIED_EMAIL, func)

            def NO_HELP(func) ->None:
                _EVENT.on(MESSAGEIDS.NO_HELP, func)

            def NO_MODS(func) ->None:
                _EVENT.on(MESSAGEIDS.NO_MODS, func)

            def NOT_HOSTING(func) ->None:
                _EVENT.on(MESSAGEIDS.NOT_HOSTING, func)

            def NO_PERMISSION(func) ->None:
                _EVENT.on(MESSAGEIDS.NO_PERMISSION, func)

            def R9K_OFF(func) ->None:
                _EVENT.on(MESSAGEIDS.R9K_OFF, func)

            def R9K_ON(func) ->None:
                _EVENT.on(MESSAGEIDS.R9K_ON, func)

            def RAID_ERROR_ALREADY_RAIDING(func) ->None:
                _EVENT.on(MESSAGEIDS.RAID_ERROR_ALREADY_RAIDING, func)

            def RAID_ERROR_FORBIDDEN(func) ->None:
                _EVENT.on(MESSAGEIDS.RAID_ERROR_FORBIDDEN, func)

            def RAID_ERROR_SELF(func) ->None:
                _EVENT.on(MESSAGEIDS.RAID_ERROR_SELF, func)

            def RAID_ERROR_TOO_MANY_VIEWERS(func) ->None:
                _EVENT.on(MESSAGEIDS.RAID_ERROR_TOO_MANY_VIEWERS, func)

            def RAID_ERROR_UNEXPECTED(func) ->None:
                _EVENT.on(MESSAGEIDS.RAID_ERROR_UNEXPECTED, func)

            def RAID_NOTICE_MATURE(func) ->None:
                _EVENT.on(MESSAGEIDS.RAID_NOTICE_MATURE, func)

            def RAID_NOTICE_RESTRICTED_CHAT(func) ->None:
                _EVENT.on(MESSAGEIDS.RAID_NOTICE_RESTRICTED_CHAT, func)

            def ROOM_MODS(func) ->None:
                _EVENT.on(MESSAGEIDS.ROOM_MODS, func)

            def SLOW_OFF(func) ->None:
                _EVENT.on(MESSAGEIDS.SLOW_OFF, func)

            def SLOW_ON(func) ->None:
                _EVENT.on(MESSAGEIDS.SLOW_ON, func)

            def SUBS_OFF(func) ->None:
                _EVENT.on(MESSAGEIDS.SUBS_OFF, func)

            def SUBS_ON(func) ->None:
                _EVENT.on(MESSAGEIDS.SUBS_ON, func)

            def TIMEOUT_NO_TIMEOUT(func) ->None:
                _EVENT.on(MESSAGEIDS.TIMEOUT_NO_TIMEOUT, func)

            def TIMEOUT_SUCCESS(func) ->None:
                _EVENT.on(MESSAGEIDS.TIMEOUT_SUCCESS, func)

            def TOS_BAN(func) ->None:
                _EVENT.on(MESSAGEIDS.TOS_BAN, func)

            def TURBO_ONLY_COLOR(func) ->None:
                _EVENT.on(MESSAGEIDS.TURBO_ONLY_COLOR, func)

            def UNBAN_SUCCESS(func) ->None:
                _EVENT.on(MESSAGEIDS.UNBAN_SUCCESS, func)

            def UNMOD_SUCCESS(func) ->None:
                _EVENT.on(MESSAGEIDS.UNMOD_SUCCESS, func)

            def UNRAID_ERROR_NO_ACTIVE_RAID(func) ->None:
                _EVENT.on(MESSAGEIDS.UNRAID_ERROR_NO_ACTIVE_RAID, func)

            def UNRAID_ERROR_UNEXPECTED(func) ->None:
                _EVENT.on(MESSAGEIDS.UNRAID_ERROR_UNEXPECTED, func)

            def UNRAID_SUCCESS(func) ->None:
                _EVENT.on(MESSAGEIDS.UNRAID_SUCCESS, func)

            def UNRECOGNIZED_CMD(func) ->None:
                _EVENT.on(MESSAGEIDS.UNRECOGNIZED_CMD, func)

            def UNSUPPORTED_CHATROOMS_CMD(func) ->None:
                _EVENT.on(MESSAGEIDS.UNSUPPORTED_CHATROOMS_CMD, func)

            def UNTIMEOUT_BANNED(func) ->None:
                _EVENT.on(MESSAGEIDS.UNTIMEOUT_BANNED, func)

            def UNTIMEOUT_SUCCESS(func) ->None:
                _EVENT.on(MESSAGEIDS.UNTIMEOUT_SUCCESS, func)

            def USAGE_BAN(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_BAN, func)

            def USAGE_CLEAR(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_CLEAR, func)

            def USAGE_COLOR(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_COLOR, func)

            def USAGE_COMMERCIAL(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_COMMERCIAL, func)

            def USAGE_DISCONNECT(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_DISCONNECT, func)

            def USAGE_EMOTE_ONLY_OFF(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_EMOTE_ONLY_OFF, func)

            def USAGE_EMOTE_ONLY_ON(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_EMOTE_ONLY_ON, func)

            def USAGE_FOLLOWERS_OFF(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_FOLLOWERS_OFF, func)

            def USAGE_FOLLOWERS_ON(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_FOLLOWERS_ON, func)

            def USAGE_HELP(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_HELP, func)

            def USAGE_HOST(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_HOST, func)

            def USAGE_MARKER(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_MARKER, func)

            def USAGE_ME(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_ME, func)

            def USAGE_MOD(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_MOD, func)

            def USAGE_MODS(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_MODS, func)

            def USAGE_R9K_OFF(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_R9K_OFF, func)

            def USAGE_R9K_ON(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_R9K_ON, func)

            def USAGE_RAID(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_RAID, func)

            def USAGE_SLOW_OFF(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_SLOW_OFF, func)

            def USAGE_SLOW_ON(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_SLOW_ON, func)

            def USAGE_SUBS_OFF(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_SUBS_OFF, func)

            def USAGE_SUBS_ON(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_SUBS_ON, func)

            def USAGE_TIMEOUT(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_TIMEOUT, func)

            def USAGE_UNBAN(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_UNBAN, func)

            def USAGE_UNHOST(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_UNHOST, func)

            def USAGE_UNMOD(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_UNMOD, func)

            def USAGE_UNRAID(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_UNRAID, func)

            def USAGE_UNTIMEOUT(func) ->None:
                _EVENT.on(MESSAGEIDS.USAGE_UNTIMEOUT, func)

            def WHISPER_BANNED(func) ->None:
                _EVENT.on(MESSAGEIDS.WHISPER_BANNED, func)

            def WHISPER_BANNED_RECIPIENT(func) ->None:
                _EVENT.on(MESSAGEIDS.WHISPER_BANNED_RECIPIENT, func)

            def WHISPER_INVALID_ARGS(func) ->None:
                _EVENT.on(MESSAGEIDS.WHISPER_INVALID_ARGS, func)

            def WHISPER_INVALID_LOGIN(func) ->None:
                _EVENT.on(MESSAGEIDS.WHISPER_INVALID_LOGIN, func)
     
    