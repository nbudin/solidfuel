from solidfuel.Logic import Event, Condition

class Action:
    def __init__(self, curve):
        self._curve = curve
        self._lastUpdate = 0
        self.updated = Event()

    def conflictsWith(self, other):
        return False

    def overlaps(self, other):
        return ((other.start() <= self.start() <= other.end()) or
                (other.start() <= self.end() <= other.end()))

    def start(self):
        return self._curve.start()

    def end(self):
        return self._curve.end()

    def length(self):
        return self._curve.length()

    def _innerStarted(self):
        return self._lastUpdate >= self.start()

    def _innerFinished(self):
        return self._lastUpdate >= self.end()
        
    def started(self):
        c = Condition(self._innerStarted)
        self.updated.addResponder(c.poll)
        return c

    def finished(self):
        c = Condition(self._innerFinished)
        self.updated.addResponder(c.poll)
        return c
    
    def update(self, time):
        self._lastUpdate = time
        self.updated.trigger()

class Fade(Action):
    def __init__(self, curve, sprite):
        Action.__init__(self, curve)
        self.sprite = sprite

    def conflictsWith(self, other):
        return (issubclass(other.__class__, Fade) and self.overlaps(other))

    def update(self, time):
        self.sprite.opacity = self._curve.value(time)
        Action.update(self, time)
