from solidfuel.Logic import Event, Condition
import math

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
        return (issubclass(other.__class__, Fade) and self.overlaps(other) and self.sprite is other.sprite)

    def update(self, time):
        self.sprite.opacity = self._curve.value(time)
        Action.update(self, time)

class MoveTo(Action):
	def __init__(self, sprite, curve, source=None, destination=None):
		Action.__init__(self, curve)
		self.sprite = sprite
		self._factor = curve.value(curve.end()) - curve.value(curve.start())
		self._source = source
		self._destination = destination
		if source is not None:
			self._calcChange()
		self._length = math.sqrt(abs(destination[0] - source[0]) ** 2 +
								 abs(destination[1] - source[1]) ** 2)
				
	def _calcChange(self):
		self._change = (self._destination[0] - self._source[0], 
						self._destination[1] - self._source[1])
						
	def conflictsWith(self, other):
		return (issubclass(other.__class__, MoveTo) and self.overlaps(other) and self.sprite is other.sprite)

	def update(self, time):
		if self._source is None:
			self._source = (sprite.x, sprite.y)
			self._calcChange()
		tf = self._factor * self._curve.value(time)
		self.sprite.x = self._source[0] + (self._change[0] * tf)
		self.sprite.y = self._source[1] + (self._change[1] * tf)
		Action.update(self, time)