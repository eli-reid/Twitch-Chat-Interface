from lib.twitchMessageHandler.modals.message import message as Message

class parse(object):
    """
    parses incomming data from IRC chat 
    outputs : message 
    """

    def badges(tags):
        """parse badges list"""
        try:
            if "badges" in tags and type(tags["badges"])==str:
                badges={}
                explode=tags["badges"].split(",")
                for item in explode:
                    parts = item.split("/")
                    if parts[1] == None:
                        return
                    badges[parts[0]]=parts[1]
                tags["badges-raw"]=tags["badges"]
                tags["badges"]=badges

            if "badges" in tags and type(tags["badges"]) == bool:
                tags["badges-raw"] = None

            return tags
        except:
            pass

    def emotes(tags)->list:
        """ parse emotes to list"""
        try:
            if "emotes" in tags and type(tags["emotes"])==str:
                emoticons = tags["emotes"].split("/")
                emotes={}
                for emoticon in emoticons:
                    part = emoticon.split(":")
                    if part[1] == None:
                        return
                    emotes[part[0]] = part[1].split(",")

                tags["emotes-raw"] = tags["emotes"]
                tags["emotes"] = emotes;
            if "emotes" in tags and type(tags["emotes"])==bool:
                tags["emotes-raw"] = None
            return tags
        except:
            pass


   
    def parse(self,data :str)->Message:

        message :Message = Message()
        position=0
        nextspace=0
   
        if len(data)<1:
            return None

        if data.startswith(chr(64)): #starts with @ symbol
            nextspace = data.find(" ")
            
            if nextspace == -1: #invalid message form 
                return None

            tags =  data[1:nextspace].split(";")

            for tag in tags:
                pair=tag.split("=")
                message.tags[pair[0]]=pair[1] or True

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

   