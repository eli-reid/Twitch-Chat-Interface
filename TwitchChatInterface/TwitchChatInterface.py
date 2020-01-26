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
        # private properties
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
        self.roomState: RoomState = MessageHandler.RoomState
        self.channels: dict = {}
        # Register System Event functions
        self.event.on(self.COMMANDS.CONNECTED,self._onConnected)
        self.event.on(self.COMMANDS.NOTICE,self._onNotice)
        self.event.on(self.COMMANDS.ROOMSTATE,self._onRoomState)
        self.event.on(self.COMMANDS.MESSAGEIDS.ROOM_MODS, self._setChannelMods)

    def start(self):
        self._server.connect()
        self._login()
        threading.Thread(target=self._emptyMsgQ, daemon=True).start()
        threading.Thread(target=self._getMsgs, daemon=True).start()     

    def _getMsgs(self):
        data=""
        while self._server.isConnected():
            time.sleep(.1)
            data = self._server.receive()
            if data is not None:
                messageParts: list(str) = data.split("\r\n")
                for messagePart in messageParts:
                    self.event.emit(self,self.COMMANDS.RECEIVED, messagePart)
                    event, msg = self._messageHandler.handleMessage(messagePart)
                    if event is not None:
                        self.event.emit(self, event, msg)

    def _emptyMsgQ(self):
          while self._server.isConnected():
              if not self._sendQ.empty():
                self._server.send(self._sendQ.get())
                time.sleep(1)

    def _login(self):
        self._sendQ.put(f"CAP REQ :{self._caprequest}")
        self._sendQ.put(f"PASS {self._password}")          
        self._sendQ.put(f"NICK {self._user}")

    def _onConnected(self, sender, obj):
        if self._channels is not None:
            self.join(self._channels) 

    def _onRoomState(self, sender, message):
        if len(message.tags) > 2:
            self._setRoomState(message.channel,message.tags)

    def _onNotice(self, sender, message):
        self.event.emit(self, message.id, message) 
    
    def getMods(self, channel):
        self.sendMessage(channel,"/mods")

    def join(self, channels: list):
        try:
            for channel in channels:
                self._sendQ.put(f"JOIN {channel}" if '#' in channel else f"JOIN #{channel}")
        except Exception as error:
            raise Exception (error)

    def _setRoomState(self, channel, tags):
        if channel not in self.channels:
            self.channels[channel]: str  = MessageHandler.Channel()

        self.channels[channel].roomID = tags.get("room-id")
        for key in tags:
            if key != "room-id":
                setattr(self.channels[channel].roomState, key.replace('-','_'), tags[key])
        self.getMods(channel)

    def _updateRoomState(self, channel, tags):
        pass
    def _setChannelMods(self, sender, message):
        self.channels[message.channel].mods = message.params[1].split(':')[1].split(',')   
        return            

    def sendMessage(self, channel: str, message: str):
        time.sleep(4)
        
        self._sendQ.put(f"PRIVMSG {'#' if '#' not in channel else ''}{channel} :{message}")
        return

    def sendWhisper(self, channel: str, username: str, message: str):
        self._sendQ.put(f"PRIVMSG {'#' if '#' not in channel else ''}{channel} :/w {username} {message}")

    def timeoutUser(self, channel: str, username: str, duration: int):
        self._sendQ.put(f"PRIVMSG #{'#' if '#' not in channel else ''}{channel} :/timeout {username} {duration}")
   
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

    def onReceived(self, func):
        self.event.on(self.COMMANDS.RECEIVED, func)


 
        