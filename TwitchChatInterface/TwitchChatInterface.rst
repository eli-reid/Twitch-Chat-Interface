


Twitch Chat Interface
=====================
.. codeauthor:: Eli Reid <EliR@EliReid.com>

.. autoclass::  TwitchChatInterface.TwitchChatInterface
    :members: connect, disconnect, send, joinRooms


********************************
TwitchChatInterface Event System
********************************
Register a callback function for twitch irc events

*EXAMPLE*:  all the events work in the same manner

:function: on.eventConnect(func) 
              
    :param func: takes callable function 
            
:function: myCallbackFunc(sender: any, obj: message) 
                
    :param sender: who is responsible for the event being triggered

    :param obj: will be of type message 

TwitchChatInterface.on
-----------------------
.. autoclass::  TwitchChatInterface.TwitchChatInterface.On
    :members: eventConnected, eventDisconnected, eventMessage, eventJoin, eventError, eventLoginError, eventWhisper, eventConnected, eventReconnect, eventSubsOff, eventSubsOn
    :undoc-members:

on.CommandEvent
^^^^^^^^^^^^^^^
.. autoclass::  TwitchChatInterface.TwitchChatInterface.On.CommandEvent
    :members: 
    :undoc-members:

on.ServerEvent
^^^^^^^^^^^^^^ 
.. autoclass::  TwitchChatInterface.TwitchChatInterface.On.ServerEvent
    :members: 
    :undoc-members:

on.MsgIdEvent
^^^^^^^^^^^^^^ 
.. autoclass::  TwitchChatInterface.TwitchChatInterface.On.MsgIdEvent
    :members: 
    :undoc-members:


