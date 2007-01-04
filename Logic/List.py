from Event import Event
from Condition import Condition

class List(list):
    def __init__(self, *args, **kwargs):
        list(self, *args, **kwargs)
        
        # addEvent(pos, item)
        self._addEvent = Event()
        # removeEvent(pos, item)
        self._removeEvent = Event()
        # setitemEvent(pos, item)
        self._setitemEvent = Event()
    
    def __setitem__(self, key, value):
        self._setitemEvent.trigger(key, value)
        return list.__setitem__(self, key, value)
    
    def __delitem__(self, key):
        self._removeEvent.trigger(key, self[key])
        return list.__delitem__(self, key)
    
    def append(self, item):
        self._addEvent.trigger(len(self), item)
        return list.append(self, item)
    
    def insert(self, pos, item):
        self._addEvent.trigger(pos, item)
        return list.insert(self, pos, item)
    
    def pop(self, pos=-1):
        self._removeEvent.trigger(pos, self[pos])
        return list.pop(self, pos)
    
    def remove(self, item):
        pos = self.index(item)
        del self[pos]