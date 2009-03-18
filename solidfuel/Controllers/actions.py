# -*- tab-width: 4 -*-

from solidfuel.Logic import Event, Condition
from solidfuel.Graphics import Sprite, Rectangle
from curves import InstantCurve
import math
import pygame

class Action:
    def __init__(self, curves=None):
        if not hasattr(curves, '__len__') and curves is not None:
            self._curve = curves
            curves = [curves]
        if curves is None:
            curves = []
        self._curves = filter(lambda c: c is not None, curves)
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
        return min([c.start() for c in self._curves])

    def end(self):
        if self._curves is None:
            return None
        return max([c.end() for c in self._curves])

    def length(self):
        return self.end() - self.start()

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

class CallFunction(Action):
    def __init__(self, time, func, *args, **kwargs):
        Action.__init__(self, InstantCurve(time, 1.0))
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self.started.addResponder(self._call)

    def _call(self):
        self._func(*self._args, **self._kwargs)
        
class Fade(Action):
    def __init__(self, curve, sprite):
        Action.__init__(self, curve)
        self.sprite = sprite

    def conflictsWith(self, other):
        return (issubclass(other.__class__, Fade) and self.overlaps(other) and self.sprite is other.sprite)

    def update(self, time):
        if issubclass(self.sprite.__class__, Rectangle):
            self.sprite.fillOpacity = self._curve.value(time)
            self.sprite.borderOpacity = self._curve.value(time)
        else:
            self.sprite.opacity = self._curve.value(time)
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
		Action.__init__(self, (pitchCurve, yawCurve, rollCurve))
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
			

			
class Track(Action):
    def __init__(self, scene, xCurve=None, yCurve=None, zCurve=None):
        Action.__init__(self, (xCurve, yCurve, zCurve))
        self.scene = scene
        self.xCurve = xCurve
        self.yCurve = yCurve
        self.zCurve = zCurve
        
    def update(self, time):
        if self.xCurve is not None:
			self.scene.cameraX = self.xCurve.value(time)
		if self.yCurve is not None:
			self.scene.cameraY = self.yCurve.value(time)
		if self.zCurve is not None:
			self.scene.cameraZ = self.zCurve.value(time)
			
class Rotate(Action):
    def __init__(self, obj, xCurve=None, yCurve=None, zCurve=None):
        Action.__init__(self, (xCurve, yCurve, zCurve))
        self.obj = obj
        self.xCurve = xCurve
        self.yCurve = yCurve
        self.zCurve = zCurve

    def update(self, time):
        if self.xCurve is not None:
			self.obj.rotX = self.xCurve.value(time)
		if self.yCurve is not None:
			self.obj.rotY = self.yCurve.value(time)
		if self.zCurve is not None:
			self.obj.rotZ = self.zCurve.value(time)
			
class Resize(Action):
    def __init__(self, obj, wCurve=None, hCurve=None):
        Action.__init__(self, (wCurve, hCurve))
        self.obj = obj
        self.wCurve = wCurve
        self.hCurve = hCurve
    
    def update(self, time):
        if self.wCurve is not None:
            self.obj.w = self.wCurve.value(time)
        if self.hCurve is not None:
            self.obj.h = self.hCurve.value(time)
        
class Move3D(Action):
    def __init__(self, obj, curve):
        Action.__init__(self, curve)
        self._obj = obj
    
    def update(self, time):
        (self._obj.x, self._obj.y, self._obj.z) = self._curve.value(time)
        
class Move3DSeparateAxes(Action):
    def __init__(self, obj, xCurve=None, yCurve=None, zCurve=None):
        curves = []
        if xCurve: curves.append(xCurve)
        if yCurve: curves.append(yCurve)
        if zCurve: curves.append(zCurve)
        Action.__init__(self, curves)
        self._obj = obj
        self._xCurve = xCurve
        self._yCurve = yCurve
        self._zCurve = zCurve
    
    def update(self, time):
        if self._xCurve:
            self._obj.x = self._xCurve.value(time)
        if self._yCurve:
            self._obj.y = self._yCurve.value(time)
        if self._zCurve:
            self._obj.z = self._zCurve.value(time)
        
class Track3D(Action):
    def __init__(self, scene, curve):
        Action.__init__(self, curve)
        self._scene = scene
    
    def update(self, time):
        (self._scene.cameraX, self._scene.cameraY, self._scene.cameraZ) = self._curve.value(time)

class PlayMedia(Action):
    def __init__(self, start, times=1, delay=0.0):
        Action.__init__(self)
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
        return (self._sound.get_length() * self._times) + (self._delay * (self._times-1))
    
    def _playMedia(self):
        raise "This is an abstract class."

    def update(self, time):
        if self._lastPlayed is None:
            self._playMedia()
            self._lastPlayed = self._start
            return
        
        end = self.end()
        if end is not None and time >= end:
            return
        
        nextPlay = self._lastPlayed + (self._delay + self._sound.get_length())
        if time >= nextPlay:
            self._playMedia()
            self._lastPlayed = nextPlay


class PlaySound(PlayMedia):
    def __init__(self, sound, start, times=1, delay=0.0):
        PlayMedia.__init__(self, start, times, delay)
        self._sound = sound
    
    def _playMedia(self):
        self._sound.play()

            
class PlayMovie(PlayMedia):
    def __init__(self, movie, start, times=1, delay=0.0):
        PlayMedia.__init__(self)
        self._movie = movie
        
    def _playMedia(self):
        self._movie.play()

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
