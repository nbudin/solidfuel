from solidfuel.Logic import Condition

class Action:
    def __init__(self, curve):
        self._curve = curve
        self._lastUpdate = 0

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
        return Condition(self._innerStarted)

    def finished(self):
        return Condition(self._innerFinished)
    
    def update(self, time):
        self._lastUpdate = time

class Fade(Action):
    def __init__(self, curve, sprite):
        Transition.__init__(self, curve)
        self.sprite = sprite

    def update(self, time):
        Action.update(self, time)
        self.sprite.opacity = self.curve.value(time)
