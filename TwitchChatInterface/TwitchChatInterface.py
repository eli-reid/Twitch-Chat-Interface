import queue
import IrcController
import MessageHandler
import time
import threading
from EventHandler import EventHandler
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
        # private property
        self._channels: list = settings.get('channels')
        self._user: str = settings.get('user')
        self._password: str = settings.get('password')
        self._caprequest: str = settings.get('caprequest')
        self._server = IrcController.IrcController(settings.get("server"),settings.get("port"))
        self._messageHandler: MessageHandler = MessageHandler.MessageHandler()
        self._sendQ: queue.SimpleQueue = queue.SimpleQueue()
        # public properties
        self.event: EventHandler = EventHandler
        self.COMMANDS: COMMANDS = self._messageHandler.COMMANDS
        self.startWithThread=threading.Thread(target=self.start, daemon=True).start
        
        # Register System Event functions
        self.event.on(self.COMMANDS.CONNECTED,self._onConnected)
        self.event.on(self.COMMANDS.NOTICE,self._onNotice)
        self.event.on(self.COMMANDS.ROOMSTATE,self._onRoomState)

    

    def start(self):
        self._server.connect()
        self._login()
        threading.Thread(target=self._emptyMsgQ, daemon=True).start()
        while True:
            time.sleep(.1)
            data = self._server.receive()
            messageParts: list(str) = data.split("\r\n")
            print("\n".join(messageParts))
            #print("*" * 30," MSG RAW ","*" * 30,"\r",messageParts,"\r","*" * 30," MSG RAW ","*" * 30)
            for messagePart in messageParts:               
                event, msg = self._messageHandler.handleMessage(messagePart)
                if event is not None:
                    self.event.emit(self, event, msg) 
                    
        
    def _emptyMsgQ(self):
          while True:
              if not self._sendQ.empty():
                self._server.send(self._sendQ.get())
                time.sleep(1)

    def _login(self):
        self._sendQ.put(f"CAP REQ :{self._caprequest}")
        self._sendQ.put(f"PASS {self._password}")          
        self._sendQ.put(f"NICK {self._user}",)

    def _onConnected(self, sender, obj):
        print("Connected")
        if self._channels is not None:
            self.join(self._channels) 

    def _onRoomState(self, sender, obj):
        print(obj.channel,obj.tags)

    def _onNotice(self,sender, message):
        self.event.emit(self, message.id, message) 
    
    def join(self, channels: list):
        try:
            for channel in channels:
                self._sendQ.put(f"JOIN {channel}" if '#' in channel else f"JOIN #{channel}")
        except Exception as error:
            raise Exception (error)

    def sendMessage(self, channel: str, message: str):
        time.sleep(4)
        self._sendQ.put(f"PRIVMSG #{channel} :{message}")

    def sendWhisper(self, channel: str, username: str, message: str):
        self._sendQ.put(f"PRIVMSG #{channel} :/w {username} {message}")

    def timeoutUser(self, channel: str, username: str, duration: int):
        self._sendQ.put(f"PRIVMSG #{channel} :/timeout {username} {duration}")
   
    def onMessage(self, func):
        self.event.on(self.COMMANDS.MESSAGE, func)
    
    def onWhisper(self, func):
        self.event.on(self.COMMANDS.WHISPER, func)

    def onRoomState(self, func):
        self.event.on(self.COMMANDS.ROOMSTATE, func)

    def onMsgId(self, msgid, func):
        self.event.on(msgid, func)
    
    def onNotice(self, func):
        self.event.on(self.COMMANDS.NOTICE, func)


 
        