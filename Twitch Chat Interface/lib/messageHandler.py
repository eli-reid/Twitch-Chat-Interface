from modals.Message import message
class messageHandler(object):
    """description of class"""
    @staticmethod
    def messageHandler(sender,data)->message:
        """               """
        parts = data.split("\r\n")
        for part in parts:
           message = parse.msg(part)
           if message != None:
                try:
                    channel=message.params[0]
                except:
                    channel=None
                try:
                   message.msg = message.params[1] 
                except:
                    msg=None
                try:
                    msgid = message.tags["msg-id"]
                except:
                    msgid=None
                try:
                    message.tags = parse.badges(parse.emotes(message.tags))        
                except:
                    pass
                if message.tags:
                    for key in message.tags:
                        if key != "emote-sets" and key != "ban-duration" and key != "bits":
                            if _.isBool(message.tags[key]):
                                message.tags[key] = None
                            elif message.tags[key] == '1' or message.tags[key] == 1:
                                message.tags[key] = True
                            elif message.tags[key] == '0' or message.tags[key] == 0:
                                message.tags[key] = False 
                if message.prefix == None:
                    if data.startswith("PING"):
                        self.send(self.__PONG)
                elif message.prefix == "tmi.twitch.tv":
                    if message.command == "001":
                        self.username = message.params[0]
                    elif message.command == "372":
                        self.emit(self,"CONNECTED",self.__server)
                        self.joinrooms(self.__chatrooms)
                    elif message.command == "NOTICE":
                        none=None
                elif message.prefix.count("tmi.twitch.tv")>0 and message.prefix.count("!")>0:
                    message.tags["username"] :str = message.prefix[:message.prefix.find("!")]
                    message.displayName=message.tags["display-name"]
                
        return message


    def badges(tags):
        if type(tags["badges"])==str:
            badges={}
            explode=tags["badges"].split(",")

            for item in explode:
                parts = item.split("/")
                if parts[1] != None:
                    return
                badges[parts[0]]=parts[1]
            tags["badges-raw"]=tags["badges"]
            tags["badges"]=badges

        if _.isBool(tags["badges"]):
            tags["badges-raw"]=None

        return tags

def emotes(tags):
    if _.isString(tags["emotes"]):
        emoticons = tags["emotes"].split("/")
        emotes={}
        for item in emoticons:
            parts = item.split(":")
            if parts[1] == None:
                return
            emotes[parts[0]] = parts[1].split(",")
        tags["emotes-raw"] = tags["emotes"]
        tags["emotes"] = emotes;
        if _.isBool(tags["emotes"]):
            tags["emotes-raw"] = None
        return tags




def parse(data=""):
    message = message
    message.raw = ""
    message.tags = {}
    message.prefix = None
    message.command = None
    message.params = []
    position=0
    nextspace=0
    if len(data)<1:
        return None
    if data.startswith(chr(64)):
        nextspace = data.find(" ")
        if nextspace == -1:
            return None

        rawTags =  data[1:nextspace].split(";")

        for tag in rawTags:
            pairs=tag.split("=")
            message.tags[pairs[0]]=pairs[1] or True

        position = nextspace + 1

    while data[position] == chr(32):
        postion += 1

    if data[position] == chr(58):
        nextspace = data.find(chr(32),position)

        if nextspace == -1:
            return None

        message.prefix = data[position+1:nextspace]
        position = nextspace + 1

        while data[position] == chr(32):
            postion += 1

    nextspace = data.find(" ",position)

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
    dataLen=len(data)
    while position < dataLen :
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

