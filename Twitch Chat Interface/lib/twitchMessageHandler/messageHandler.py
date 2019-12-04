import re 
from lib.events.eventHandler import eventHandler as _EVENT
from lib.twitchMessageHandler.modals.const import commands as COMMANDS, msgIds as MESSAGEIDS , serverEvents as SERVEREVENTS  
from lib.twitchMessageHandler.parse import parse as _PARSER 
class messageHandler(object):
    """
    Handles twitch message and emits events based on commands and msgid tags
    commands: commandsEnum
    """
    
    @staticmethod
    def messageHandler(data:str)->None:
        """               """
        messageParts :list(str) = data.split("\r\n")
        for messagePart in messageParts:
            print(messagePart)
            try:
                message = _PARSER.parse(messagePart)
            except Exception as err:
                _EVENT.emit(messageHandler,SERVEREVENTS.ERROR,err)
            
            if message != None:
                try:
                    # Populate message values
                    message.channel :str = message.params[0] if len(message.params)>0 else None
                    message.text :str = message.params[1] if len(message.params)>1 else None
                    message.id :str = message.tags["msg-id"] if "msg-id" in message.tags else ''
                    
                    # Parse badges and emotes
                    message.tags = _PARSER.badges(_PARSER.emotes(message.tags))
                    
                except Exception as err:
                    _EVENT.emit("Populate message values (messageHandler):",SERVEREVENTS.ERROR,err)

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
                    _EVENT.emit("IRCv3 Transformer (messageHandler):",SERVEREVENTS.ERROR,err)

                # Handle message with no prfix
                if message.prefix == None:
                    try:
                        if message.command == COMMANDS.PING:
                            _EVENT.emit(messageHandler,COMMANDS.PING)
                        elif message.command == COMMANDS.PONG:
                            _EVENT.emit(messageHandler,COMMANDS.PONG)
                        else:
                            _EVENT.emit(messageHandler,SERVEREVENTS.ERROR,"Could not parse message with no prefix:\n {}".format(message))
                    except Exception as err:
                        _EVENT.emit("Handle message no prifix (messageHandler):",SERVEREVENTS.ERROR,err)
                
                # Handle message with prefix "tmi.twitch.tv"
                elif message.prefix == SERVEREVENTS.TMI_TWITCH_TV:
                   
                    if message.command == SERVEREVENTS.USERNAME:  # Get Username
                        username = message.params[0]

                    elif message.command == SERVEREVENTS.CONNECTED:  # Connected to server
                       _EVENT.emit(messageHandler,SERVEREVENTS.CONNECTED)
                    
                    elif message.command == COMMANDS.CLEARCHAT:
                        none=None
                    elif message.command == COMMANDS.CLEARMSG:
                        none=None
                    elif message.command == COMMANDS.HOSTTARGET:
                        none=None
                     
                    # Chatroom notice check msgid tag
                    elif message.command == COMMANDS.NOTICE:
                        _EVENT.emit(messageHandler,COMMANDS.NOTICE,message)
                            
                        if message.id == MESSAGEIDS.SUBS_ON:                            _EVENT.emit(messageHandler,MESSAGEIDS.SUBS_ON, message)
                        
                        elif message.id == MESSAGEIDS.WHISPER_BANNED:
                            _EVENT.emit(messageHandler,MESSAGEIDS.SUBS_OFF, message.channel)

                        elif message.id == MESSAGEIDS.SUBS_OFF:
                            _EVENT.emit(messageHandler,MESSAGEIDS.SUBS_OFF, message.channel)
                       
                        elif message.id == MESSAGEIDS.SUBS_OFF:
                            _EVENT.emit(messageHandler,MESSAGEIDS.SUBS_OFF, message.channel)

                        elif message.id == MESSAGEIDS.SUBS_OFF:
                            _EVENT.emit(messageHandler,MESSAGEIDS.SUBS_OFF, message.channel)

                        elif message.id == MESSAGEIDS.SUBS_OFF:
                            _EVENT.emit(messageHandler,MESSAGEIDS.SUBS_OFF, message.channel)

                        elif message.id == MESSAGEIDS.SUBS_OFF:
                            _EVENT.emit(messageHandler,MESSAGEIDS.SUBS_OFF, message.channel)

                        elif message.id == MESSAGEIDS.SUBS_OFF:
                            _EVENT.emit(messageHandler,MESSAGEIDS.SUBS_OFF, message.channel)

                        elif message.id == MESSAGEIDS.SUBS_OFF:
                            _EVENT.emit(messageHandler,MESSAGEIDS.SUBS_OFF, message.channel)

                        elif message.id == MESSAGEIDS.SUBS_OFF:
                            _EVENT.emit(messageHandler,MESSAGEIDS.SUBS_OFF, message.channel)
                            
                        elif message.id == MESSAGEIDS.SUBS_OFF:
                            _EVENT.emit(messageHandler,MESSAGEIDS.SUBS_OFF, message.channel)

                        elif message.id == MESSAGEIDS.SUBS_OFF:
                            _EVENT.emit(messageHandler,MESSAGEIDS.SUBS_OFF, message.channel)

                        elif message.id == MESSAGEIDS.SUBS_OFF:
                            _EVENT.emit(messageHandler,MESSAGEIDS.SUBS_OFF, message.channel)

                        elif message.id == MESSAGEIDS.SUBS_OFF:
                            _EVENT.emit(messageHandler,MESSAGEIDS.SUBS_OFF, message.channel)

                        elif message.id == MESSAGEIDS.SUBS_OFF:
                            _EVENT.emit(messageHandler,MESSAGEIDS.SUBS_OFF, message.channel)

                        elif message.id == MESSAGEIDS.SUBS_OFF:
                            _EVENT.emit(messageHandler,MESSAGEIDS.SUBS_OFF, message.channel)

                        elif message.id == MESSAGEIDS.SUBS_OFF:
                            _EVENT.emit(messageHandler,MESSAGEIDS.SUBS_OFF, message.channel)

                        elif message.id == MESSAGEIDS.SUBS_OFF:
                            _EVENT.emit(messageHandler,MESSAGEIDS.SUBS_OFF, message.channel)


                    
                        else:
                            if message.raw.find("Login unsuccessful") > 0 \
                                    or message.raw.find("Login authentication failed")>0:
                                _EVENT.emit(messageHandler,SERVEREVENTS.LOGIN_UNSUCCESSFUL, "Login authentication failed")

                            elif message.raw.find("Login unsuccessful") > 0 \
                                    or message.raw.find("Login authentication failed")>0:
                                _EVENT.emit(messageHandler,SERVEREVENTS.LOGIN_UNSUCCESSFUL, "Login authentication failed")

                            elif message.raw.find("Login unsuccessful") > 0 \
                                    or message.raw.find("Login authentication failed")>0:
                                _EVENT.emit(messageHandler,SERVEREVENTS.LOGIN_UNSUCCESSFUL, "Login authentication failed")   


                    elif message.command == COMMANDS.RECONNECT:
                        print ("RECONNECT")
                    elif message.command == COMMANDS.ROOMSTATE:
                        none=None
                    elif message.command == COMMANDS.USERNOTICE:
                        none=None
                    elif message.command == COMMANDS.USERSTATE:
                        none=None
                    

                # Handle message with prefix jtv
                elif message.prefix == "jtv":
                    print(message.params)
                

                else: 
                    if message.command == SERVEREVENTS.MESSAGE: 
                        message.tags["username"] :str = message.prefix[:message.prefix.find("!")]
                        _EVENT.emit(messageHandler, SERVEREVENTS.MESSAGE,message)
                        print(_EVENT._events["ERROR"].getCallbacks())
                    
                    elif message.command == "353":
                        pass
                        
                         
        return 



