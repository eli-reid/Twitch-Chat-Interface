import threading  
import socket
import time
import queue

from lib.events.eventHandler import eventHandler as _EVENT 
from lib.twitchMessageHandler.messageHandler import  MessageHandler as _messageHandler, COMMANDS, SERVEREVENTS, MESSAGEIDS, EVENTS, TAGS
from datetime import datetime

class TwitchChatInterface(object):

    """
    TwitchChatInterface 
    .. codeauthor:: Eli Reid <EliR@EliReid.com>
   
    Bulids connection, receives chat messages from server and emits corrisponding events! 
    """
    
    def __init__(self,settings: dict):
        """
        """

        # Set outside access to  constants 
        self.COMMANDS: COMMANDS = COMMANDS
        self.SERVEREVENTS: SERVEREVENTS = SERVEREVENTS
        self.MESSAGEIDS: MESSAGEIDS  = MESSAGEIDS 
        self.TAGS: TAGS = TAGS
        self.on: On =  On
        
        # Register System Event functions
        _EVENT.onError(self._ERROR)
        _EVENT.on(SERVEREVENTS.ERROR,self._ERROR)
        _EVENT.on(SERVEREVENTS.CONNECTED,self._CONNECTED)
        _EVENT.on(SERVEREVENTS.RECEIVED,self._RECEIVED)
        _EVENT.on(COMMANDS.PING,self._onPING)
        _EVENT.on(COMMANDS.PONG,self._onPONG)
                
        # Populate settings values
        self._server: str = settings['server']
        self._port: int = settings['port']
        self._user: str = settings['user']
        self._password: str = settings['password']
        self._chatrooms: list = settings['chatrooms']
        self._pingWait: int = 5*60
        
        # Set helper Varibles
        self._disconnect: bool = False
        self._lastPing: time = time.time()
        self._sendMessageQ: queue = queue.SimpleQueue()
        self._socket: socket = socket.socket()
        
        # IRC Command constants 
        self._CAPREQUEST: str = "CAP REQ: twitch.tv/tags twitch.tv/commands twitch.tv/membership"
        self._PASS: str = f"PASS {self._password}"           
        self._NICK: str = f"NICK {self._user}"
        self._JOIN: str = "JOIN #{}"
        self._PONG: str = f"PONG: {SERVEREVENTS.TMI_TWITCH_TV}"
        self._PING: str = f"PING: {SERVEREVENTS.TMI_TWITCH_TV}"

    def connect(self)->None:
        """ 
        Connect to IRC server
        """
        try:
            # Create new socket and connect
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM,) as self._socket:  
                self._socket.connect((self._server,self._port))

                # Send login cradentials
                self.send(self._CAPREQUEST)
                self.send(self._PASS)
                self.send(self._NICK)
                                
                # Start listing for server response
                self._listenThread:  threading.Thread = threading.Thread(target=self._awaitResponse(), daemon=True)
                self._listenThread.start()

        except Exception as err:
            _EVENT.emit(self.connect, SERVEREVENTS.ERROR, err)
        return
    
    def disconnect(self)->None:
        """ diconnnect """
        self._disconnect  = True
        return

    def send(self,message: str)->None:
        """ send"""
        self._socket.setblocking(1)
        ## ADD Q and timer###
        if not message.endswith("\r\n"):
            message += "\r\n"
        try:
            self._socket.send(message.encode())
        except Exception as err:
           _EVENT.emit(self._awaitResponse, SERVEREVENTS.ERROR, err)
        return 

    def joinRooms(self,rooms: list)->None:
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
                data: str = self._socket.recv(4096).decode()
                
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

    def _RECEIVED(self, sender,data):
        try:
            _messageHandler.messageHandler(data)
        except Exception as err:
            print (err)
        return

    def _onPING(self,sender,obj):
        try:
            self._lastPing = time.time()
            self.send(self._PONG)
        except Exception as err:
           _EVENT.emit(self, SERVEREVENTS.ERROR, err)
        return 
     
    def _onPONG(self,sender,obj):
        try:
            self._lastPing = time.time()
            self.send(self._PING)
        except Exception as err:
           _EVENT.emit(self, SERVEREVENTS.ERROR, err)
        return   

class On():
         
    """ 
           
        .. code-block:: python
                        
            def myCallbackFunc(sender: any, obj: message):
                print("I am connected")
                return
                        
            on.eventConnect(myCallbackFunc)

        .. note::  obj is normally of type **message**
            

        ...to-do:: ROOMSTATE changes
    """
  
    def __init__(self):
        self.ServerEvent:  ServerEvent = self.ServerEvent()
        self.CommandEvent: CommandEvent = self.CommandEvent()
        self.MsgIdEvent: MsgIdEvent = self.MsgIdEvent()
           
        # events handle by standard message type 
    def eventDisconnected(self,func)->None:
        self.ServerEvent.DISCONNECTED(func)

    def eventMessage(self,func)->None:
        self.ServerEvent.MESSAGE(func)

    def eventJoin(self,func)->None:  
        self.ServerEvent.JOIN(func)

    def eventError(self,func)->None: 
        self.ServerEvent.ERROR(func)

    def eventLoginError(self,func)->None:  
        self.ServerEvent.LOGIN_UNSUCCESSFUL(func)   
            
    def eventWhisper(self,func)->None: 
        self.ServerEvent.WHISPER(func)

    def eventConnected(self,func)->None: 
        self.ServerEvent.CONNECTED(func)

    def eventReconnect(self,func)->None:
        self.CommandEvent.RECONNECT(func)

    def eventSlowModeOn(func):
        pass

    # events handled by other message types - ie: evnetSubsOff is handled by ROOMSTATE event vs NOTICE event message.id "subs-off" 
    def eventSubsOff(self, func)->None:
            _EVENT.on(EVENTS.SUBSOFF, func)
 
    def eventSubsOn(self, func)->None:
            _EVENT.on(EVENTS.SUBSON, func)
 
    class ServerEvent:
        """
        .. code-block:: python
                        
            def myCallbackFunc(sender: any, obj: message):
                # enter your code here for this event
                return
                        
            On.ServerEvent.DISCONNECTED(myCallbackFunc)

        .. note::  obj is normally of type **message** unless noted 
        """
        def LOGIN_UNSUCCESSFUL(self, func) ->None:
            _EVENT.on(SERVEREVENTS.LOGIN_UNSUCCESSFUL, func)

        def MESSAGE(self, func) ->None:
            _EVENT.on(SERVEREVENTS.MESSAGE, func)

        def JOIN(self, func) ->None:
            _EVENT.on(SERVEREVENTS.JOIN, func)

        def RECEIVED(self, func) ->None:
            _EVENT.on(SERVEREVENTS.RECEIVED, func)

        def CONNECTED(self, func) ->None:
            _EVENT.on(SERVEREVENTS.CONNECTED , func)

        def ERROR(self, func) ->None:
            _EVENT.on(SERVEREVENTS.ERROR, func)

        def DISCONNECTED (self, func) ->None:
            _EVENT.on(SERVEREVENTS.DISCONNECTED , func)

        def USERNAME(self, func) ->None:
            _EVENT.on(SERVEREVENTS.USERNAME, func)

        def NAMES(self, func) ->None:
            _EVENT.on(SERVEREVENTS. NAMES, func)

        def WHISPER(self, func) ->None:
            _EVENT.on(SERVEREVENTS.WHISPER, func)

        def PART(self, func) ->None:
            _EVENT.on(SERVEREVENTS.PART, func) 

    class  CommandEvent:
        """
        .. code-block:: python
                        
            def myCallbackFunc(sender: any, obj: message):
                # enter your code here for this event
                return
                        
            On.CommandEvent.CLEARMSG(myCallbackFunc)

        .. note::  obj is normally of type **message** unless noted 
        """
        def PING(self, func) ->None:
            _EVENT.on(COMMANDS.PING, func)

        def PONG(self, func) ->None:
            _EVENT.on(COMMANDS.PONG, func)

        def CLEARMSG(self, func) ->None:
            _EVENT.on(COMMANDS.CLEARMSG, func)

        def HOSTTARGET(self, func) ->None:
            _EVENT.on(COMMANDS.HOSTTARGET, func)

        def NOTICE(self, func) ->None:
            _EVENT.on(COMMANDS.NOTICE, func)

        def RECONNECT(self, func) ->None:
            _EVENT.on(COMMANDS.RECONNECT, func)

        def ROOMSTATE(self, func) ->None:
            _EVENT.on(COMMANDS.ROOMSTATE, func)

        def USERNOTICE(self, func) ->None:
            _EVENT.on(COMMANDS.USERNOTICE, func)

        def USERSTATE(self, func) ->None:
            _EVENT.on(COMMANDS.USERSTATE, func)

    class MsgIdEvent:
        """
            
        .. code-block:: python
                        
            def myCallbackFunc(sender: any, obj: message):
                # enter your code here for this event
                return
                        
            TwitchChatInterface.On.MsgIdEvent.ALREADY_BANNED(myCallbackFunc)

        .. note:: obj is normally of type **message** unless noted 

            
        .. note:: TwitchChatInterface.on.MsgIdEvents can also be used using measge.id
                    from TwitchChatInterface.On.CommandEvents.NOTICE event object

            
        .. code-block:: python
                        
            def myCallbackFunc(sender: any, obj: message):
                # Check value agianst built-in consant TwitchChatInterface.MESSAGEIDS.ALREADY_BANNED
                if obj.id == TwitchChatInterface.MESSAGEIDS.ALREADY_BANNED
                    return
                        
            TwitchChatInterface.On.CommandEvents.NOTICE(myCallbackFunc)

        """
        def ALREADY_BANNED(self, func) ->None:
            _EVENT.on(MESSAGEIDS.ALREADY_BANNED, func)

        def ALREADY_EMOTE_ONLY_OFF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.ALREADY_EMOTE_ONLY_OFF, func)

        def ALREADY_EMOTE_ONLY_ON(self, func) ->None:
            _EVENT.on(MESSAGEIDS.ALREADY_EMOTE_ONLY_ON, func)

        def ALREADY_R9K_OFF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.ALREADY_R9K_OFF, func)

        def ALREADY_R9K_ON(self, func) ->None:
            _EVENT.on(MESSAGEIDS.ALREADY_R9K_ON, func)

        def ALREADY_SUBS_OFF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.ALREADY_SUBS_OFF, func)

        def ALREADY_SUBS_ON(self, func) ->None:
            _EVENT.on(MESSAGEIDS.ALREADY_SUBS_ON, func)

        def BAD_BAN_ADMIN(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_BAN_ADMIN, func)

        def BAD_BAN_ANON(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_BAN_ANON, func)

        def BAD_BAN_BROADCASTER(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_BAN_BROADCASTER, func)

        def BAD_BAN_GLOBAL_MOD(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_BAN_GLOBAL_MOD, func)

        def BAD_BAN_MOD(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_BAN_MOD, func)

        def BAD_BAN_SELF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_BAN_SELF,func)

        def BAD_BAN_STAFF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_BAN_STAFF, func)

        def BAD_COMMERCIAL_ERROR(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_COMMERCIAL_ERROR, func)

        def BAD_DELETE_MESSAGE_BROADCASTER(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_DELETE_MESSAGE_BROADCASTER, func)

        def BAD_DELETE_MESSAGE_MOD(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_DELETE_MESSAGE_MOD, func)

        def BAD_HOST_ERROR(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_HOST_ERROR, func)

        def BAD_HOST_HOSTING(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_HOST_HOSTING, func)

        def BAD_HOST_RATE_EXCEEDED(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_HOST_RATE_EXCEEDED, func)

        def BAD_HOST_REJECTED(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_HOST_REJECTED, func)

        def BAD_HOST_SELF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_HOST_SELF, func)

        def BAD_MARKER_CLIENT(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_MARKER_CLIENT, func)

        def BAD_MOD_BANNED(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_MOD_BANNED, func)

        def BAD_MOD_MOD(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_MOD_MOD, func)

        def BAD_SLOW_DURATION(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_SLOW_DURATION, func)

        def BAD_TIMEOUT_ADMIN(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_TIMEOUT_ADMIN, func)

        def BAD_TIMEOUT_ANON(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_TIMEOUT_ANON, func)

        def BAD_TIMEOUT_BROADCASTER(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_TIMEOUT_BROADCASTER, func)

        def BAD_TIMEOUT_DURATION(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_TIMEOUT_DURATION, func)

        def BAD_TIMEOUT_GLOBAL_MOD(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_TIMEOUT_GLOBAL_MOD, func)

        def BAD_TIMEOUT_MOD(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_TIMEOUT_MOD, func)

        def BAD_TIMEOUT_SELF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_TIMEOUT_SELF, func)

        def BAD_TIMEOUT_STAFF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_TIMEOUT_STAFF, func)

        def BAD_UNBAN_NO_BAN(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_UNBAN_NO_BAN, func)

        def BAD_UNHOST_ERROR(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_UNHOST_ERROR, func)

        def BAD_UNMOD_MOD(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAD_UNMOD_MOD, func)

        def BAN_SUCCESS(self, func) ->None:
            _EVENT.on(MESSAGEIDS.BAN_SUCCESS, func)

        def CMDS_AVAILABLE(self, func) ->None:
            _EVENT.on(MESSAGEIDS.CMDS_AVAILABLE, func)

        def COLOR_CHANGED(self, func) ->None:
            _EVENT.on(MESSAGEIDS.COLOR_CHANGED, func)

        def COMMERCIAL_SUCCESS(self, func) ->None:
            _EVENT.on(MESSAGEIDS.COMMERCIAL_SUCCESS, func)

        def DELETE_MESSAGE_SUCCESS(self, func) ->None:
            _EVENT.on(MESSAGEIDS.DELETE_MESSAGE_SUCCESS, func)

        def EMOTE_ONLY_OFF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.EMOTE_ONLY_OFF, func)

        def EMOTE_ONLY_ON(self, func) ->None:
            _EVENT.on(MESSAGEIDS.EMOTE_ONLY_ON, func)

        def FOLLOWERS_OFF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.FOLLOWERS_OFF, func)

        def FOLLOWERS_ON(self, func) ->None:
            _EVENT.on(MESSAGEIDS.FOLLOWERS_ON, func)

        def FOLLOWERS_ONZERO(self, func) ->None:
            _EVENT.on(MESSAGEIDS.FOLLOWERS_ONZERO, func)

        def HOST_OFF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.HOST_OFF, func)

        def HOST_ON(self, func) ->None:
            _EVENT.on(MESSAGEIDS.HOST_ON, func)

        def HOST_SUCCESS(self, func) ->None:
            _EVENT.on(MESSAGEIDS.HOST_SUCCESS, func)

        def HOST_SUCCESS_VIEWERS(self, func) ->None:
            _EVENT.on(MESSAGEIDS.HOST_SUCCESS_VIEWERS, func)

        def HOST_TARGET_WENT_OFFLINE(self, func) ->None:
            _EVENT.on(MESSAGEIDS.HOST_TARGET_WENT_OFFLINE, func)

        def HOSTS_REMAINING(self, func) ->None:
            _EVENT.on(MESSAGEIDS.HOSTS_REMAINING, func)

        def INVALID_USER(self, func) ->None:
            _EVENT.on(MESSAGEIDS.INVALID_USER, func)

        def MOD_SUCCESS(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MOD_SUCCESS, func)

        def MSG_BANNED(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_BANNED, func)

        def MSG_BAD_CHARACTERS(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_BAD_CHARACTERS, func)

        def MSG_CHANNEL_BLOCKED(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_CHANNEL_BLOCKED, func)

        def MSG_CHANNEL_SUSPENDED(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_CHANNEL_SUSPENDED, func)

        def MSG_DUPLICATE(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_DUPLICATE, func)

        def MSG_EMOTEONLY(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_EMOTEONLY, func)

        def MSG_FACEBOOK(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_FACEBOOK, func)

        def MSG_FOLLOWERSONLY(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_FOLLOWERSONLY, func)

        def MSG_FOLLOWERSONLY_FOLLOWED(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_FOLLOWERSONLY_FOLLOWED, func)

        def MSG_FOLLOWERSONLY_ZERO(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_FOLLOWERSONLY_ZERO, func)

        def MSG_R9K(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_R9K, func)

        def MSG_RATELIMIT(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_RATELIMIT, func)

        def MSG_REJECTED(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_REJECTED, func)

        def MSG_REJECTED_MANDATORY(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_REJECTED_MANDATORY, func)

        def MSG_ROOM_NOT_FOUND(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_ROOM_NOT_FOUND, func)

        def MSG_SLOWMODE(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_SLOWMODE, func)

        def MSG_SUBSONLY(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_SUBSONLY, func)

        def MSG_SUSPENDED(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_SUSPENDED, func)

        def MSG_TIMEDOUT(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_TIMEDOUT, func)

        def MSG_VERIFIED_EMAIL(self, func) ->None:
            _EVENT.on(MESSAGEIDS.MSG_VERIFIED_EMAIL, func)

        def NO_HELP(self, func) ->None:
            _EVENT.on(MESSAGEIDS.NO_HELP, func)

        def NO_MODS(self, func) ->None:
            _EVENT.on(MESSAGEIDS.NO_MODS, func)

        def NOT_HOSTING(self, func) ->None:
            _EVENT.on(MESSAGEIDS.NOT_HOSTING, func)

        def NO_PERMISSION(self, func) ->None:
            _EVENT.on(MESSAGEIDS.NO_PERMISSION, func)

        def R9K_OFF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.R9K_OFF, func)

        def R9K_ON(self, func) ->None:
            _EVENT.on(MESSAGEIDS.R9K_ON, func)

        def RAID_ERROR_ALREADY_RAIDING(self, func) ->None:
            _EVENT.on(MESSAGEIDS.RAID_ERROR_ALREADY_RAIDING, func)

        def RAID_ERROR_FORBIDDEN(self, func) ->None:
            _EVENT.on(MESSAGEIDS.RAID_ERROR_FORBIDDEN, func)

        def RAID_ERROR_SELF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.RAID_ERROR_SELF, func)

        def RAID_ERROR_TOO_MANY_VIEWERS(self, func) ->None:
            _EVENT.on(MESSAGEIDS.RAID_ERROR_TOO_MANY_VIEWERS, func)

        def RAID_ERROR_UNEXPECTED(self, func) ->None:
            _EVENT.on(MESSAGEIDS.RAID_ERROR_UNEXPECTED, func)

        def RAID_NOTICE_MATURE(self, func) ->None:
            _EVENT.on(MESSAGEIDS.RAID_NOTICE_MATURE, func)

        def RAID_NOTICE_RESTRICTED_CHAT(self, func) ->None:
            _EVENT.on(MESSAGEIDS.RAID_NOTICE_RESTRICTED_CHAT, func)

        def ROOM_MODS(self, func) ->None:
            _EVENT.on(MESSAGEIDS.ROOM_MODS, func)

        def SLOW_OFF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.SLOW_OFF, func)

        def SLOW_ON(self, func) ->None:
            _EVENT.on(MESSAGEIDS.SLOW_ON, func)

        def SUBS_OFF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.SUBS_OFF, func)

        def SUBS_ON(self, func) ->None:
            _EVENT.on(MESSAGEIDS.SUBS_ON, func)

        def TIMEOUT_NO_TIMEOUT(self, func) ->None:
            _EVENT.on(MESSAGEIDS.TIMEOUT_NO_TIMEOUT, func)

        def TIMEOUT_SUCCESS(self, func) ->None:
            _EVENT.on(MESSAGEIDS.TIMEOUT_SUCCESS, func)

        def TOS_BAN(self, func) ->None:
            _EVENT.on(MESSAGEIDS.TOS_BAN, func)

        def TURBO_ONLY_COLOR(self, func) ->None:
            _EVENT.on(MESSAGEIDS.TURBO_ONLY_COLOR, func)

        def UNBAN_SUCCESS(self, func) ->None:
            _EVENT.on(MESSAGEIDS.UNBAN_SUCCESS, func)

        def UNMOD_SUCCESS(self, func) ->None:
            _EVENT.on(MESSAGEIDS.UNMOD_SUCCESS, func)

        def UNRAID_ERROR_NO_ACTIVE_RAID(self, func) ->None:
            _EVENT.on(MESSAGEIDS.UNRAID_ERROR_NO_ACTIVE_RAID, func)

        def UNRAID_ERROR_UNEXPECTED(self, func) ->None:
            _EVENT.on(MESSAGEIDS.UNRAID_ERROR_UNEXPECTED, func)

        def UNRAID_SUCCESS(self, func) ->None:
            _EVENT.on(MESSAGEIDS.UNRAID_SUCCESS, func)

        def UNRECOGNIZED_CMD(self, func) ->None:
            _EVENT.on(MESSAGEIDS.UNRECOGNIZED_CMD, func)

        def UNSUPPORTED_CHATROOMS_CMD(self, func) ->None:
            _EVENT.on(MESSAGEIDS.UNSUPPORTED_CHATROOMS_CMD, func)

        def UNTIMEOUT_BANNED(self, func) ->None:
            _EVENT.on(MESSAGEIDS.UNTIMEOUT_BANNED, func)

        def UNTIMEOUT_SUCCESS(self, func) ->None:
            _EVENT.on(MESSAGEIDS.UNTIMEOUT_SUCCESS, func)

        def USAGE_BAN(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_BAN, func)

        def USAGE_CLEAR(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_CLEAR, func)

        def USAGE_COLOR(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_COLOR, func)

        def USAGE_COMMERCIAL(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_COMMERCIAL, func)

        def USAGE_DISCONNECT(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_DISCONNECT, func)

        def USAGE_EMOTE_ONLY_OFF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_EMOTE_ONLY_OFF, func)

        def USAGE_EMOTE_ONLY_ON(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_EMOTE_ONLY_ON, func)

        def USAGE_FOLLOWERS_OFF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_FOLLOWERS_OFF, func)

        def USAGE_FOLLOWERS_ON(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_FOLLOWERS_ON, func)

        def USAGE_HELP(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_HELP, func)

        def USAGE_HOST(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_HOST, func)

        def USAGE_MARKER(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_MARKER, func)

        def USAGE_ME(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_ME, func)

        def USAGE_MOD(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_MOD, func)

        def USAGE_MODS(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_MODS, func)

        def USAGE_R9K_OFF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_R9K_OFF, func)

        def USAGE_R9K_ON(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_R9K_ON, func)

        def USAGE_RAID(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_RAID, func)

        def USAGE_SLOW_OFF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_SLOW_OFF, func)

        def USAGE_SLOW_ON(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_SLOW_ON, func)

        def USAGE_SUBS_OFF(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_SUBS_OFF, func)

        def USAGE_SUBS_ON(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_SUBS_ON, func)

        def USAGE_TIMEOUT(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_TIMEOUT, func)

        def USAGE_UNBAN(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_UNBAN, func)

        def USAGE_UNHOST(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_UNHOST, func)

        def USAGE_UNMOD(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_UNMOD, func)

        def USAGE_UNRAID(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_UNRAID, func)

        def USAGE_UNTIMEOUT(self, func) ->None:
            _EVENT.on(MESSAGEIDS.USAGE_UNTIMEOUT, func)

        def WHISPER_BANNED(self, func) ->None:
            _EVENT.on(MESSAGEIDS.WHISPER_BANNED, func)

        def WHISPER_BANNED_RECIPIENT(self, func) ->None:
            _EVENT.on(MESSAGEIDS.WHISPER_BANNED_RECIPIENT, func)

        def WHISPER_INVALID_ARGS(self, func) ->None:
            _EVENT.on(MESSAGEIDS.WHISPER_INVALID_ARGS, func)

        def WHISPER_INVALID_LOGIN(self, func) ->None:
            _EVENT.on(MESSAGEIDS.WHISPER_INVALID_LOGIN, func)
     
    