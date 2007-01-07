from Event import Event

class Condition:
    def __init__(self, pf):
        if issubclass(pf.__class__, Condition):
            self._pollFunc = pf._pollFunc
            self.status = pf.status
            self.changed = pf.changed
        else:
            self._pollFunc = pf
            self.status = self._pollFunc()
            self.changed = Event()

    def poll(self):
        oldStatus = self.status
        self.status = self._pollFunc()
        if self.status != oldStatus:
            self.changed.trigger(self.status)
            
    def parentChanged(self, newStatus):
        self.poll()

    def getStatus(self):
        return self.status

    def __invert__(self):
        nc = Condition(lambda: not self.status)
        self.changed.addResponder(nc.parentChanged)
        return nc

    def __and__(self, other):
        nc = Condition(lambda: self.status and other.status)
        self.changed.addResponder(nc.parentChanged)
        other.changed.addResponder(nc.parentChanged)
        return nc

    def __or__(self, other):
        nc = Condition(lambda: self.status or other.status)
        self.changed.addResponder(nc.parentChanged)
        other.changed.addResponder(nc.parentChanged)
        return nc
