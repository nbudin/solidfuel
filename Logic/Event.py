class Event:
    def __init__(self):
        self._responders = []
        self._active = True

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
