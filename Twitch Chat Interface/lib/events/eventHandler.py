
class eventHandler(object):
    """ 
    Event Handler 
    author: Eli Reid
    """
    _events :dict = dict()
    class EVENTS(object):
        ERROR="ERROR"
 
    @classmethod
    def emit(cls,sender :any, event :dict or str, obj :object = None, once :bool = False)->None:
        """
        eventHandler.emit - Event Emitter
        input : 
            sender (obj) - string, function or class reponsible for event 
            event (event) - registered name of event 
            obj (any type) - any varible or object you want to pass to the self.on function
        """
        try:
            if not cls._isRegistered(cls,event):
                cls._register(cls,event)
            for func in cls._events[event].getCallbacks():
                func(sender,obj)
            return
        except Exception as err:
            cls.emit(cls,cls.EVENTS.ERROR, err)

    @classmethod
    def on(cls,event :dict or str,func :object)->None:
        """
        Catches events and calls a stored list of functions
        Input:
            event (str) -  name of event 
            func(func) - function that is called when the event is emitted
        """
        try:
            if not cls._isRegistered(cls,event):
                cls._register(cls,event)
            cls._events[event].add(func)
            return
        except Exception as err:
            cls.emit(cls,cls.EVENTS.ERROR, err)

    @classmethod
    def removeEvent(cls,event :str)->None:
        """ Removes event from dictionary """
        try:
            del(cls._events[event])
            return 
        except Exception as err:
            cls.emit(cls,cls.EVENTS.ERROR, err)

    @classmethod
    def removeFunc(cls,event :str,func :any)->None:
        """ Removes function from events function list """
        try:
            cls._events[event].remove(func)
            return
        except Exception as err:
            cls.emit(cls,cls.EVENTS.ERROR, err)
    @classmethod
    def onError(cls,func):
        eventHandler.on(eventHandler.EVENTS.ERROR,func)
    
    def _isRegistered(cls, event :str)->bool:
        """see if event is registered """
        try:
            return True if event in cls._events.keys() else False
        except Exception as err:
            cls.emit(cls,cls.EVENTS.ERROR, err)

    def _register(cls,event :str)->None:
        """  add new events to dictionary  """
        try:
            if event not in cls._events.keys():
                cls._events[event] :_event =_event()
            return
        except Exception as err:
            cls.emit(cls,cls.EVENTS.ERROR, err)


class _event(object):
    """  Event object stores callback functions for an event   """
    def __init__(self):
        """   setup functions list    """
        self._callbacks :list[function] = []
      
    def add(self,func)->None:
        """ Append function to list of functions for event   """
        try:
            self._callbacks.append(func)
            return
        except Exception as err:
            cls.emit(cls,cls.EVENTS.ERROR, err)
   
    def remove(self,func)->None:
        """ Remove function from event   """
        try:
            self._callbacks.remove(func)
            return
        except Exception as err:
            cls.emit(cls,cls.EVENTS.ERROR, err)
    
    def getCallbacks(self)->list:
        """   functions list getter returns function list   """
        try:
            return self._callbacks
        except Exception as err:
            cls.emit(cls,cls.EVENTS.ERROR, err)

