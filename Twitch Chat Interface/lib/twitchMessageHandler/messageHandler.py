from lib.events.eventHandler import eventHandler as _EVENT
from lib.twitchMessageHandler.modals.const import *
from lib.twitchMessageHandler.parse import parse 
class messageHandler(object):
    """
    Handles twitch message and emits events based on commands and msgid tags
    commands: commandsEnum

    
    """
    def __init__(self):
        self._EVENT :_EVENT = _EVENT
        self._parse :parse = parse()
        self.MESSAGEIDS :msgIds = msgIds
        self.COMMANDS :commands = commands
        self.SERVEREVENTS :serverEvents = serverEvents

    def messageHandler(self,data:str)->None:
        """               """
        messageParts :list(str) = data.split("\r\n")
        for messagePart in messageParts:
            try:
                message=self._parse.parse(messagePart)
            except Exception as err:
                self._EVENT.emit(self,self.SERVEREVENTS.ERROR,err)

            if message != None:
                try:
                    # Populate message values
                    message.channel :str = message.params[0] if len(message.params)>0 else None
                    message.text :str = message.params[1] if len(message.params)>1 else None
                    message.id :str = message.tags["msg-id"] if "msg-id" in message.tags else ''
                    
                    # Parse badges and emotes
                    message.tags = parse.badges(parse.emotes(message.tags))
                    
                except Exception as err:
                    self._EVENT.emit("Populate message values (messageHandler):",self.SERVEREVENTS.ERROR,err)

                # Transform IRCv3 Tags
                try: 
                    if message.tags:
                        for key in message.tags :
                            if key != "emote-sets" and key != "ban-duration" and key != "bits":
                                if type(message.tags[key]) == bool:
                                    message.tags[key] = None
                                elif message.tags[key]  == '1':
                                    message.tags[key] = True
                                elif message.tags[key]  == '0':
                                    message.tags[key] = False
                                elif type(message.tags[key]) == str:
                                    pass
                except Exception as err:
                    self._EVENT.emit("IRCv3 Transformer (messageHandler):",self.SERVEREVENTS.ERROR,err)

                # Handle message with no prfix
                if message.prefix == None:
                    try:
                        if message.command == self.COMMANDS.PING:
                            self._EVENT.emit(self,self.COMMANDS.PING)
                        elif message.command == self.COMMANDS.PONG:
                            self._EVENT.emit(self,self.COMMANDS.PONG)
                        else:
                            self._EVENT.emit(self,self.SERVEREVENTS.ERROR,"Could not parse message with no prefix:\n {}".format(message))
                    except Exception as err:
                        self._EVENT.emit("Handle message no prifix (messageHandler):",self.SERVEREVENTS.ERROR,err)
                
                # Handle message with prefix "tmi.twitch.tv"
                elif message.prefix == "tmi.twitch.tv":
                   
                    if message.command in ["002","003","004","375", "376","CAP" ]:
                       pass
               
                    elif message.command == "001":  # Get Username
                        self.username = message.params[0]

                    elif message.command == "372":  # Connected to server
                       self._EVENT.emit(self,self.SERVEREVENTS.CONNECTED)
                    
                    elif message.command == "CLEARCHAT":
                        none=None
                    elif message.command == "CLEARMSG":
                        none=None
                    elif message.command == "HOSTTARGET":
                        none=None
                     
                    # Chatroom notice check msgid tag
                    elif message.command == self.COMMANDS.NOTICE:
                        self._EVENT.emit(self,self.COMMANDS.NOTICE,message)
                            

                        if message.id == self.MESSAGEIDS.SUBS_ON:
                            self._EVENT.emit(self,self.MESSAGEIDS.SUBS_ON, message.channel)
                        
                        elif message.id == self.MESSAGEIDS.SUBS_OFF:
                            self._EVENT.emit(self,self.MESSAGEIDS.SUBS_OFF, message.channel)
                    
                        else:
                            if message.raw.find("Login unsuccessful") > 0 \
                                    or message.raw.find("Login authentication failed")>0:
                                self._EVENT.emit(self,self.SERVEREVENTS.LOGIN_UNSUCCESSFUL, "Login authentication failed")

                            elif message.raw.find("Login unsuccessful") > 0 \
                                    or message.raw.find("Login authentication failed")>0:
                                self._EVENT.emit(self,self.SERVEREVENTS.LOGIN_UNSUCCESSFUL, "Login authentication failed")

                            elif message.raw.find("Login unsuccessful") > 0 \
                                    or message.raw.find("Login authentication failed")>0:
                                self._EVENT.emit(self,self.SERVEREVENTS.LOGIN_UNSUCCESSFUL, "Login authentication failed")   


                    elif message.command == "RECONNECT":
                        none=None
                    elif message.command == "ROOMSTATE":
                        none=None
                    elif message.command == "USERNOTICE":
                        none=None
                    elif message.command == "USERSTATE":
                        none=None
                    

                # Handle message with prefix jtv
                elif message.prefix == "jtv":
                    print(message.params)
                

                else: 
                    if message.command =='PRIVMSG': 
                        message.tags["username"] :str = message.prefix[:message.prefix.find("!")]
                        self._EVENT.emit(self,self.SERVEREVENTS.MESSAGE,message)
                    
                    elif message.command == "353":
                        pass
                        
                         
        return 



