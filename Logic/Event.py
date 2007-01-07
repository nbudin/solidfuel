class Event:
    def __init__(self, copyEvent=None):
        if copyEvent is None:
            self._responders = []
            self._active = True
        else:
            self._responders = copyEvent._responders
            self._active = copyEvent._active

    def addResponder(self, resp):
        self._responders.append(resp)

    def removeResponder(self, resp):
        self._responders.remove(resp)

    def trigger(self, *args, **kwargs):
        if self._active:
            for resp in self._responders:
                resp(*args, **kwargs)
    
    def setActive(self, value):
        self._active = value
    
    def getActive(self):
	    return self._active
