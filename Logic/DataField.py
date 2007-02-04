from Event import Event
from Condition import Condition

class DataField:
    def __init__(self, value=None):
        self._value = value
        self._setEvent = Event()
    
    def set(self, value):
        self._value = value
        self._setEvent.trigger(value)
    
    def get(self):
        return self._value
        
    def equals(self, value):
        return self._value == value
        
    def __str__(self):
        return str(self._value)
        
    def __repr__(self):
        return "\%s/" % (str(self.get()))
        
    def _mkcond(self, value, method, pollEvent):
        def pollFunc():
            return method(value)
        cond = Condition(pollFunc)
        def wrapPoll(*args, **kwargs):
            cond.poll()
        pollEvent.addResponder(wrapPoll)
        return cond
        
    def _equalsCond(self, value):
        return self._mkcond(value, self.equals, self._setEvent)