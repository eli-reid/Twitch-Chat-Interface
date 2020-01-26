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
 