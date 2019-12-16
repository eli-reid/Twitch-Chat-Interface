import threading  
import socket
import time
import queue
from onEvent import on
from eventHandler import eventHandler as _EVENT 
from messageHandler import  MessageHandler as _messageHandler
from const import COMMANDS, SERVEREVENTS, MESSAGEIDS, EVENTS, TAGS
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
        self.on: on = on()
        
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

