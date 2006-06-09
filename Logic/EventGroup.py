from Event import Event

class EventGroup:
    def __init__(self, items):
        self.items = list(items)

    def setActive(self, value):
        self._innerSetActive(value, {})

    def _innerSetActive(self, value, alreadySet):
        if alreadySet.has_key(self):
            return
        alreadySet[self] = 1
        for item in self._items:
            if issubclass(item, EventGroup):
                item.setActive(value, alreadySet)
            else:
                item.setActive(value)
  

    def trigger(self, *args, **kwargs):
        self._innerCall(args, kwargs, {})
        
    def _innerCall(self, args, kwargs, alreadyCalled):
        if alreadyCalled.has_key(self):
            return
        alreadyCalled[self] = 1
        for item in self._items:
            if issubclass(item, EventGroup):
                item._innerCall(args, kwargs, alreadyCalled)
            else:
                item.trigger(*args, **kwargs)

        
    
