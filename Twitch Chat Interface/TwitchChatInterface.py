import threading  
import re 
import socket

from lib.events.eventHandler import eventHandler as _EVENT
from modals.enums import eventsEnum, msgIdEnum 
  


class twitchChatInterface(object):
    """
        creates connect ion to twitch chat irc server and receives chat messages 
    """
    # IRC Command constants 
    _CAPREQUEST :str = "CAP REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership"
    _PASS :str = "PASS {}"
    _NICK :str = "NICK {}"
    _JOIN :str = "JOIN #{}"
    _PONG :str = "PONG :tmi.twitch.tv"

    #__GLOBALUSERSTATE = GlobalUserState

    def __init__(self,settings :dict):
        """setting in JSON format"""
        self.msgId :msgIdEnum = msgIdEnum
        self.EVENTS :eventsEnum = eventsEnum
        _EVENT.on(self.EVENTS.RECEIVED,_messageHandler)
        self._server :str = settings['server']
        self._port :int = settings['port']
        self._user :str = settings['user']
        self._password :str = settings['password']
        self._chatrooms :list = settings['chatrooms']
        self._listen :threading.Thread = threading.Thread(target= self._awaitResponse(),daemon=True)
        self._disconnect :bool = False
    
    def connect(self)->None:
        """ connect """
        try:
            self._socket :socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self.__server,self.__port))
            self.send(self._PASS.format(self.__password))
            self.send(self._NICK.format(self.__user))
            self.send(self._CAPREQUEST)
            self._chatThread.start()
        except Exception as err:
            _EVENT.emit(self._awaitresponse,self.EVENTS.ERROR,err)
        return
    
    def disconnect(self)->None:
        """ diconnnect """
        self._disconnect  = True
        return

    def joinrooms(self,rooms):
        for room in rooms:
            self.send(self.__JOIN.format(room))
        return

    def send(self,message :str)->None:
        if not message.endswith("\r\n"):
            message +="\r\n"
        try:
            print (msg)
            self._socket.send(message.encode())
        except exception as err:
           _EVENT.emit(self._awaitresponse,self.EVENTS.ERROR,err)
        return self
    
    
    
    
    
    
    
    def _awaitresponse(self)->None:
        """   """
        while not self._disconnect:
            try:
                data :str = self._socket.recv(4096).decode()
                _EVENT.emit(self,self.EVENTS.RECEIVED, data)
            except socket.error as err:
                _EVENT.emit(self._awaitresponse,self.EVENTS.ERROR,err)
        
        self._socket.close()
        _EVENT.emit(self,self.EVENTS.DISCONNECTED)
    


    