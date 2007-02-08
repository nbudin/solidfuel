from solidfuel.Logic import Event, Condition
from solidfuel.Graphics import Sprite, Rectangle
import math
import pygame

class Action:
    def __init__(self, curve=None):
        self._curve = curve
        self._lastUpdate = 0
        self.updated = Event()
        
        # these are triggered by Timelines
        self.started = Event()
        self.finished = Event()

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
        if issubclass(self.sprite.__class__, Sprite):
            self.sprite.opacity = self._curve.value(time)
        elif issubclass(self.sprite.__class__, Rectangle):
            self.sprite.fillOpacity = self._curve.value(time)
        Action.update(self, time)

class RotoZoom(Action):
	def __init__(self, rotozoomer, rotCurve, zoomCurve):
		Action.__init__(self, zoomCurve)
		self.rotCurve = rotCurve
		self.zoomCurve = zoomCurve
		self.rotozoomer = rotozoomer
		
	def conflictsWith(self, other):
		return (issubclass(other.__class__, RotoZoom) and self.overlaps(other) and self.rotozoomer is other.rotozoomer)
	
	def update(self, time):
		self.rotozoomer.rot = self.rotCurve.value(time)
		self.rotozoomer.zoom = self.zoomCurve.value(time)
		Action.update(self, time)

class Pan(Action):
	def __init__(self, scene, pitchCurve=None, yawCurve=None, rollCurve=None):
		Action.__init__(self, pitchCurve)
		self.scene = scene
		self.pitchCurve = pitchCurve
		self.yawCurve = yawCurve
		self.rollCurve = rollCurve
		
	def update(self, time):
		if self.pitchCurve is not None:
			self.scene.pitch = self.pitchCurve.value(time)
		if self.yawCurve is not None:
			self.scene.yaw = self.yawCurve.value(time)
		if self.rollCurve is not None:
			self.scene.roll = self.rollCurve.value(time)
			
class PlaySound(Action):
    def __init__(self, sound, start, times=1, delay=0.0):
        Action.__init__(self)
        self._sound = sound
        self._times = times
        self._delay = delay
        self._start = start
        self._lastPlayed = None
        
    def start(self):
        return self._start
        
    def end(self):
        if self._times < 1:
            return None
        return self.start() + self.length()
        
    def length(self):
        if self._times < 1:
            return None
        return (self._sound.get_length() * times) + (self._delay * (times-1))
        
    def update(self, time):
        if self._lastPlayed is None:
            self._sound.play()
            self._lastPlayed = self._start
            return
        
        end = self.end()
        if end is not None and time > end:
            return
        
        nextPlay = self._lastPlayed + (self._delay + self._sound.get_length())
        if time >= nextPlay:
            self._sound.play()
            self._lastPlayed = nextPlay

class MoveTo(Action):
	def __init__(self, obj, curve, source=None, destination=None):
		Action.__init__(self, curve)
		self.obj = obj
		self._factor = curve.value(curve.end()) - curve.value(curve.start())
		self._source = source
		self._destination = destination
		if source is not None:
			self._calcChange()
			sqrsum = 0.0
			for component in self._change:
			    sqrsum += abs(component) ** 2
			self._length = math.sqrt(sqrsum)
			
	def _calcChange(self):
		self._change = [self._destination[i] - self._source[i] for i in range(len(self._source))]
						
	def conflictsWith(self, other):
		return (issubclass(other.__class__, MoveTo) and self.overlaps(other) and self.sprite is other.sprite)

	def update(self, time):
		if self._source is None:
			self._source = (sprite.x, sprite.y)
			self._calcChange()
		tf = self._factor * self._curve.value(time)
		self.obj.x = self._source[0] + (self._change[0] * tf)
		self.obj.y = self._source[1] + (self._change[1] * tf)
		if len(self._source) > 2:
		    self.obj.z = self._source[2] + (self._change[2] * tf)
		Action.update(self, time)