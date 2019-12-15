
import TwitchChatInterface 
newsecretcode="lmjjv4oz5t2z3d0c760d5e2fyx8u1r"
settings={
  "server": "irc.chat.twitch.tv",
  "port": 6667,
  "user": "edog0049abot",
  "password": "oauth:uqyosuh6zf54is2me2jl5l8qgahtlz",
  "chatrooms": ["edog0049a" ]
}

def handleMessage(sender,message):
    print("[{0}] {1}: {2} ".format(message.channel,message.username,message.text))
    return

def handleConnect(sender,obj):
    print ("connected!",obj)
    return

def handlesubs_on(sender,obj):
    print("subs on !!", obj)
    return

def handlesubs_off(sender,obj):
    print("subs off !!", obj)
    return

def handleJoin(sender,obj):
    f="JOINED: {} ".format(obj)
    print (f) 

def main():

    twitchChat = TwitchChatInterface.TwitchChatInterface(settings)
    twitchChat.on.eventMessage(handleMessage)
    twitchChat.on.eventConnected(handleConnect)
    twitchChat.on.eventJoin =(handleJoin)
    twitchChat.on.eventWhisper
    twitchChat.connect()
    
if __name__ == "__main__":
    main()
 