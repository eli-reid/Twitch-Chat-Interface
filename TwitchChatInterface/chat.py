import threading
import logging
import tkinter
from TwitchChatInterface import TwitchChatInterface

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

def main():
    def test(event):
      print(event)
      return
    def addChannel(event):
        listt.insert(tkinter.END,txt1.get(1.0, tkinter.END))

    twitchChat = TwitchChatInterface(settings)
    twitchChat._messageHandler.handleMessage("@badge-info=;badges=global_mod/1,turbo/1;color=#0D4200;display-name=ronni;emotes=25:0-4,12-16/1902:6-10;id=b34ccfc7-4977-403a-8a94-33c6bac34fb8;mod=0;room-id=1337;subscriber=0;tmi-sent-ts=1507246572675;turbo=1;user-id=1337;user-type=global_mod :ronni!ronni@ronni.tmi.twitch.tv PRIVMSG #ronni :Kappa Keepo Kappa")
    twitchChat.onMessage (handleMessage)
    twitchChat.onWhisper(handlesubs_off)
    twitchChat.start()
    main=tkinter.Tk()
    button_1 = tkinter.Button(main,text="add")
    button_1.grid(row=1)
    button_1.bind("<ButtonPress>",func=addChannel)
    txt1=tkinter.Text(main,width=15,height=1)
    txt1.grid(row=1,column = 1)
    listt=tkinter.Listbox(main)
    listt.grid(row=0)
    i = 0
    for chn in twitchChat._channels: 
         listt.insert(i, chn )
    main.title("Twitch Chat Bot")
    
    main.mainloop()
    
   

if __name__ == "__main__":
    main()
 