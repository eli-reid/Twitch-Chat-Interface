


Twitch Chat Interface
=====================
.. automodule:: TwitchChatInterface

.. codeauthor:: Eli Reid <EliR@EliReid.com>

.. autoclass:: TwitchChatInterface
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
.. autoclass::  TwitchChatInterface.on
    :members: eventConnected, eventDisconnected, eventMessage, eventJoin, eventError, eventLoginError, eventWhisper, eventConnected, eventReconnect, eventSubsOff, eventSubsOn
    :undoc-members:

on.CommandEvent
^^^^^^^^^^^^^^^
.. autoclass:: TwitchChatInterface.on.CommandEvent
    :members: 
    :undoc-members:

on.ServerEvent
^^^^^^^^^^^^^^ 
.. autoclass:: TwitchChatInterface.on.ServerEvent
    :members: 
    :undoc-members:

on.MsgIdEvent
^^^^^^^^^^^^^^ 
.. autoclass:: TwitchChatInterface.on.MsgIdEvent
    :members: 
    :undoc-members:


