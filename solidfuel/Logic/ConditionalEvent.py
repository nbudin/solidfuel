from Event import Event

class ConditionalEvent(Event):
    def __init__(self, cond):
        Event.__init__(self)
        self._cond = cond

    def trigger(self, *args, **kwargs):
        if self._cond.status:
            return Event.trigger(self, *args, **kwargs)
