import threading  
import re 
import socket
import time
from lib.events.eventHandler import eventHandler as _EVENT
from modals.enums import eventsEnum 
from lib.twitchMessageHandler.messageHandler import messageHandler
import queue
from datetime import datetime

class twitchChatInterface(object):
    """
        creates connection to twitch chat irc server and receives chat messages 
        then emits events for the type of message received  
    """
    # IRC Command constants 
    _CAPREQUEST :str = "CAP REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership"
    _PASS :str = "PASS {}"
    _NICK :str = "NICK {}"
    _JOIN :str = "JOIN #{}"
    _PONG :str = "PONG :{}"
    _PING :str = "PING :{}"
    


    def __init__(self,settings :dict):
        """set values from settings"""
        now = datetime.now()
        self.start_time = now.strftime("%H:%M:%S")
        
        self._sendMessageQ = queue.SimpleQueue()
        self._messageHandler = messageHandler()
        self.EVENTS :eventsEnum = eventsEnum
        # Register Event functions
        
        _EVENT.onError(self._ERROR)
        _EVENT.on(self.EVENTS.ERROR,self._ERROR)
        _EVENT.on(self._messageHandler.SERVEREVENTS.CONNECTED,self._CONNECTED)
        _EVENT.on(self._messageHandler.COMMANDS.PING,self._onPING)
        _EVENT.on(self._messageHandler.COMMANDS.PONG,self._onPONG)
        
        # Populate settings values
        self._server :str = settings['server']
        self._port :int = settings['port']
        self._user :str = settings['user']
        self._password :str = settings['password']
        self._chatrooms :list = settings['chatrooms']

        # Set helper Varibles
        self._disconnect :bool = False
        self._lastPing = time.time()
        self._pingWait = 5*60
           
    def connect(self)->None:
        """ 
        Connect to IRC server
        """
        try:
            # Create new socket and connect
            self._socket :socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self._server,self._port))
            # Send login cradentials
            self.send(self._PASS.format(self._password))
            self.send(self._NICK.format(self._user))
            self.send(self._CAPREQUEST)
            # Start listing for server response
            self._listen :threading.Thread = threading.Thread(target=self._awaitResponse(), daemon=True)
            self._listen.start()
        except Exception as err:
            _EVENT.emit(self.connect,self.EVENTS.ERROR,err)
        return
    
    def disconnect(self)->None:
        """ diconnnect """
        self._disconnect  = True
        return

    def send(self,message :str)->None:

        ## ADD Q ###
        if not message.endswith("\r\n"):
            message += "\r\n"
        try:
            self._socket.send(message.encode())
        except Exception as err:
           _EVENT.emit(self._awaitResponse, self.EVENTS.ERROR, err)
        return 

    def joinRooms(self,rooms):
        for room in rooms:
            self.send(self._JOIN.format(room))
            time.sleep(3)
        return

    
    def _awaitResponse(self)->None:
        """   """
        while self._disconnect == False:
            try:
                if time.time() - self._lastPing > self._pingWait:
                    print("ping timer")
                    self._lastPing = time.time()
                    print(self._PING.format("tmi.twitch.tv"))
                    dataLength :int= len(self._PING.format("tmi.twitch.tv").encode())
                    while dataLength > 0:
                        dataLength -= self._socket.send(self._PING.format("tmi.twitch.tv").encode())
                data :str = self._socket.recv(4096).decode()
                if len(data)>0:
                    self._messageHandler.messageHandler(data)
                    _EVENT.emit(self,self.EVENTS.RECEIVED, data)
            except Exception as err:
                _EVENT.emit(self._awaitResponse,self.EVENTS.ERROR,err)

        self._socket.close()
        _EVENT.emit(self,self.EVENTS.DISCONNECTED)




    # Event functions 
     
    def _ERROR(self,sender,obj):
        print("ERROR:  ",sender, obj)
        self.disconnect()

    def _CONNECTED(self,sender,obj):
        joinRoomsThread=threading.Thread(daemon=True,target=self.joinRooms,kwargs={'rooms':self._chatrooms})
        joinRoomsThread.start()
    
    def _onPING(self,sender,obj):
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Start Time:",self.start_time,"Current Time:", current_time)
            print(self._PONG.format("tmi.twitch.tv"))
            dataLength :int= len(self._PONG.format("tmi.twitch.tv").encode())
            while dataLength > 0:
                dataLength -= self._socket.send(self._PONG.format("tmi.twitch.tv").encode())
        except Exception as err:
           _EVENT.emit(self, self.EVENTS.ERROR, err)
        return 
     
    def _onPONG(self,sender,obj):
        try:
            print(self._PING.format("tmi.twitch.tv"))
            dataLength :int= len(self._PING.format("tmi.twitch.tv").encode())
            while dataLength > 0:
                dataLength -= self._socket.send(self._PING.format("tmi.twitch.tv").encode())
        except Exception as err:
           _EVENT.emit(self, self.EVENTS.ERROR, err)
        return   
        
    # Event setter fucntions
    def onMESSAGE(self,func):
        self._messageHandler._EVENT.on(self._messageHandler.SERVEREVENTS.MESSAGE,func)
    
    def onCONNECTED(self,func):
        self._messageHandler._EVENT.on(self._messageHandler.SERVEREVENTS.CONNECTED,func)

    def onJOIN(self,func):
        self._messageHandler._EVENT.on(self._messageHandler.SERVEREVENTS.JOIN,func)

    def onSUBS_OFF(self,func):
        self._messageHandler._EVENT.on(self._messageHandler.MESSAGEIDS.SUBS_OFF,func)

    def onSUBS_ON(self,func):
        self._messageHandler._EVENT.on(self._messageHandler.MESSAGEIDS.SUBS_ON,func)


    


    