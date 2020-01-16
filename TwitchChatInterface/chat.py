import threading
import logging
from TwitchChatInterface import TwitchChatInterface

newsecretcode="lmjjv4oz5t2z3d0c760d5e2fyx8u1r","oauth:uqyosuh6zf54is2me2jl5l8qgahtlz", "oauth:5ke9e1ucrfioutzltxede6cg286u5a"

settings={
  "server": "irc.chat.twitch.tv",
  "port": 6667,
  "user": "edog0049a",
  "password":"oauth:uqyosuh6zf54is2me2jl5l8qgahtlz",
  "channels": ["theliljuju","edog0049a"],
  "caprequest" :"twitch.tv/tags twitch.tv/commands twitch.tv/membership" 
}

def handleMessage(sender,message):
    print("[{0}] {1}: {2} ".format(message.channel,message.username,message.text))

    return
def login_err(sender,message):
    print("fuck")
    return
def handleConnect(sender,obj):
    print ("connected!",obj)
    return

def handlesubs_on(sender,obj):
    print("subs on !!", obj)
    return

def handlesubs_off(sender,obj):
    print("Sweet NO NO ")
    return

def handleJoin(sender,obj):
    f="JOINED: {} ".format(obj)
    
    print (f) 
def test(data):
      print(data)
      return
def main():

    twitchChat = TwitchChatInterface(settings)
    twitchChat.onMessage (handleMessage)
    twitchChat.onWhisper(handlesubs_off)
    twitchChat.onMsgId(twitchChat.COMMANDS.MESSAGEIDS.ROOM_MODS,handlesubs_off)
    twitchChat.startWithThread()
    #twitchChat.start()
    twitchChat.sendMessage("edog0049a","/mods")
    while True:
        pass
   

if __name__ == "__main__":
    main()
 