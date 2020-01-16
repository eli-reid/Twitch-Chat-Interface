"""
    Event Handler

    .. codeauthor:: Eli Reid <EliR@EliReid.com>
"""
import types
class EventHandler():
    """
    Event Handler

    """
    _events: dict = dict()

    @classmethod
    def emit(cls, sender: any, event: str, obj: object = None, once: bool = False)->None:
        """ .. function:: emit(sender, event, obj = None, once = False)

            eventHandler.emit - Event Emitter

            :param sender: what is responsible for the event
            :type sender: any

            :param event: name of event
            :type event: str

            :param obj: anything to pass to callback
            :type obj: object

            :param once: if it is a one time event
            :type once: bool

            :return: None
            :rtype: None

            :raise: TypeError if event isn't string
            :raise: TypeError if func isn't function pointer
        """


        if not isinstance(event, str):
            raise TypeError("event should of type str ")
        if not isinstance(once, bool):
            raise TypeError("Requires callback function pointer ex: myCallback(sender, obj)")
        try:
            if not cls._isRegistered(event):
                cls._register(event)
            for func in cls._events[event].getCallbackFuncs():
                func(sender, obj)
            return
        except Exception as err:
            print(isinstance(event, str))
            raise Exception(err)

    @classmethod
    def on(cls, event, func: types.FunctionType or types.MethodType)->None:
        """ .. function:: on(event, func)

            appends to list of callback functions for events

            :param event: name of event
            :type event: str

            :param func: pointer to callback function or method
            :type func: types.FunctionType or types.MethodType

            :return: None
            :rtype: None

            :raise: TypeError if event isn't string
            :raise: TypeError if func isn't function pointer
        """
    
        if not isinstance(func, (types.MethodType, types.FunctionType)):
            raise TypeError("Requires callback function pointer ex: myCallback(sender, obj)")
        try:
            if not cls._isRegistered(event):
                cls._register(event)
            cls._events[event].add(func)
            return
        except Exception as err:
            raise Exception(err)

    @classmethod
    def removeEvent(cls, event: str)->None:
        """ .. function:: removeEvent(event)

            Removes event from dictionary

            :param event: name of event
            :type event: str

            :return: True if event is registered
            :rtypr: bool

            :raise: TypeError if event isn't string
        """

        if not isinstance(event, str):
            raise TypeError("Event should of type str ")
        try:
            if cls._isRegistered(event):
                del cls._events[event]
            return
        except Exception as err:
            raise Exception(err)

    @classmethod
    def removeFunc(cls, event: str, func: types.FunctionType or types.MethodType)->None:
        """ .. function:: removeFunc(event, func)


            Removes function from events function list



            :param event: name of event
            :type event: str

            :param func: pointer to callback function or method
            :type func: types.FunctionType or types.MethodType


            :return: True if event is registered
            :rtype: bool

            :raise: TypeError if event isn't string
            :raise: TypeError if func isn't function pointer
        """
        if not isinstance(event, str):
            raise TypeError("event should of type str ")
        if not isinstance(func, (types.MethodType, types.FunctionType)):
            raise TypeError("Requires callback function pointer ex: myCallback(sender, obj)")
        try:
            cls._events[event].remove(func)
            return
        except Exception as err:
            raise Exception(err)
    @classmethod
    def _isRegistered(cls, event: str)->bool:
        """ .. funtcion:: _isRegister(event)

            See if callback function already registered


            :param event: name of event
            :type event: str

            :return: True if event is registered
            :rtypr: bool


            :raise: TypeError if event isn't string
        """
        if not isinstance(event, str):
            raise TypeError("event should be of type str")
        try:
            return event in cls._events.keys()
        except Exception as err:
            raise Exception(err)
    @classmethod
    def _register(cls, event: str)->None:
        """ .. funtcion:: _register(event)

            Add new event to dictionary


            :param event: name of event
            :type event: str

            :return: None
            :rtypr: None


            :raise: TypeError if event isn't string
        """
        if  not isinstance(event, str):
            raise TypeError("event should be of type str")
        try:
            if not cls._isRegistered(event):
                cls._events[event]: _event = _event()
            return
        except Exception as err:
            raise Exception(err)

    @classmethod
    def getEvents(cls)->list:
        """.. function:: getEvents()

            event List getter


            :returns: list of event names
            :rtype: list[str] or list[]
        """
        return list(cls._events)

    @classmethod
    def getCallbackFuncs(cls, event: str)->list:
        """ .. function:: getCallbackFuncs(event)

            List getter function

            :returns: list of function pointers or empty list
            :rtype: list[types.FunctionType] or list[]
            :raise: TypeError if event isn't string
        """

        if not isinstance(event, str):
            raise TypeError("Event should be of type str")
        try:
            return cls._events[event].getCallbackFuncs()
        except Exception as err:
            raise Exception(err)

class _event():
    """.. class:: _event


        Event object stores callback functions for an event

    """
    def __init__(self):
        #: Setup list for functions
        self._callbacks: list = []


    def add(self, func: types.FunctionType or types.MethodType)->None:
        """ .. function:: add(func)


            Append function to list of functions for event


            :param func: A callback function pointer
            :type func: types.FunctionType

            :returns: None
            :rtype: None

            :raise: TypeError if func in not function type

        """

        if not isinstance(func, (types.MethodType, types.FunctionType)):
            raise TypeError("Requires callback function pointer ex: myCallback(sender, obj)")

        try:
            self._callbacks.append(func)
            return
        except Exception as err:
            raise Exception(err)


    def remove(self, func: types.FunctionType or types.MethodType)->None:
        """ .. function:: remove(func: types.FunctionType)

            Remove callback function from event



            :param func: A callback function pointer
            :type func: types.FunctionType

            :returns: None
            :rtype: None

            :raise: TypeError if func in not function type
        """

        if not isinstance(func, (types.MethodType, types.FunctionType)):
            raise TypeError("Requires callback function pointer ex: myCallback(sender, obj)")

        try:
            #: Verify list isn't empty before trying to remove function
            if len(self._callbacks) > 0:
                self._callbacks.remove(func)
            return
        except Exception as err:
            raise Exception(err)


    def getCallbackFuncs(self)->list:
        """ .. function:: getCallbackFuncs()

            List getter function

            :returns: list of function pointers or empty list
            :rtype: list[types.FunctionType] or list[]
        """
        try:
            return list(self._callbacks)
        except Exception as err:
            raise Exception(err)
