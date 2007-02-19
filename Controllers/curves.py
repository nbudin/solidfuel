# -*- tab-width: 4 -*-

import math, random

class Curve:
    def __init__(self, start, length=None):
        self._start = start
        self._length = length
        if self._length is not None:
            self._end = start + length
        else:
            self._end = None

    def start(self):
        return self._start

    def length(self):
        return self._length

    def end(self):
        return self._end
        
    def value(self, time):
        raise "This is an abstract class."

class LinearCurve(Curve):
    def __init__(self, start, length, startvalue, amount):
        Curve.__init__(self, start, length)
        self._startvalue = startvalue
        self._amount = amount
        self._endvalue = startvalue + amount
        self._amountpersecond = self._amount / self._length
    def value(self, time):
        if time < self._start:
    		return self._startvalue
    	elif time < self._end:
    		return self._startvalue + (time - self._start) * self._amountpersecond
    	else:
    		return self._endvalue
		
class ParabolicCurve(Curve):
	# y = coefficient * x^2 + startvalue
	def __init__(self, start, startvalue, coefficient=None, length=None, until=None, decelerate=False):
		if coefficient is not None and until is not None:
			# until = coefficient * length^2 + startvalue
			# until - startvalue = coefficient * length^2
			# (until - startvalue) / coefficient = length^2
			# sqrt((until - startvalue) / coefficient) = length
			length = math.sqrt((until - startvalue) / coefficient)
		elif coefficient is not None and length is not None:
			until = coefficient * (length**2) + startvalue
		else:
			# until = coefficient * length^2 + startvalue
			# until - startvalue = coefficient * length^2
			# (until - startvalue) / (length^2) = coefficient
			coefficient = (until - startvalue) / (length**2)
		Curve.__init__(self, start, length)
		self._startvalue = startvalue
		self._endvalue = until
		self._coefficient = coefficient
		self._decelerate = decelerate
	def value(self, time):
		x = (time - self._start)
		if self._decelerate:
			x -= self._length
		y = self._coefficient * (x ** 2) + self._startvalue
		if self._decelerate:
			y -= self._endvalue
			y *= -1
		return y
		
class SineWave(Curve):
    def __init__(self, start, period, max=1.0, min=0.0):
        Curve.__init__(self, start)
        self._freq = (2 * 3.14159) / period
        self._amplitude = (max - min) / 2.0
        self._y = min + self._amplitude
    def value(self, time):
        return self._amplitude * math.sin(self._freq * (time - self._start)) + self._y
        
class CatmullRomSpline(Curve):
    def __init__(self, start, startvalue):
        self._points = [(start, startvalue)]
    def _findIndex(self, time):
        for i in range(len(self._points)):
            if time < self._points[i][0]:
                return i
        return len(self._points)
    def addPoint(self, time, value):
        self._points.insert(self._findIndex(time), (time, value))
    def start(self):
        return self._points[0][0]
    def end(self):
        return self._points[-1][0]
    def length(self):
        return self.end() - self.start()
    def value(self, time):
        if time <= self._points[0][0]:
            return self._points[0][1]
        if time >= self._points[-1][0]:
            return self._points[-1][1]
            
        timeIndex = self._findIndex(time)
        startpoint = self._points[timeIndex - 1]
        endpoint = self._points[timeIndex]
        tdelta = endpoint[0] - startpoint[0]
        
        # "smooth" start and endpoints for tangents
        if timeIndex > 1:
            prevpoint = self._points[timeIndex - 2]
        else:
            prevpoint = (startpoint[0] - tdelta, startpoint[1])
        if timeIndex < len(self._points) - 1:
            nextpoint = self._points[timeIndex + 1]
        else:
            nextpoint = (endpoint[0] + tdelta, endpoint[1])
        
        # s ranges linearly from 0.0 - 1.0 within each pair of points
        s = (time - startpoint[0]) / (endpoint[0] - startpoint[0])
        # hermite basis functions
        h1 = 2*(s**3) - 3*(s**2) + 1
        h2 = -2*(s**3) + 3*(s**2)
        h3 = s**3 - 2*(s**2) + s
        h4 = s**3 - s**2
        
        t1 = ((0.5 * (startpoint[1] - prevpoint[1]) / (startpoint[0] - prevpoint[0])) +
              (0.5 * (endpoint[1] - startpoint[1]) / (endpoint[0] - startpoint[0])))
        t2 = ((0.5 * (endpoint[1] - startpoint[1]) / (endpoint[0] - startpoint[0])) +
              (0.5 * (nextpoint[1] - endpoint[1]) / (nextpoint[0] - endpoint[0])))
        
        value =  h1*startpoint[1] + h2*endpoint[1] + h3*t1 + h4*h2
        return value

class Tremor(Curve):
    def __init__(self, start, length, magnitude=1.0):
        Curve.__init__(self, start, length)
        self._magnitude = magnitude
        
    def value(self, time):
        if time < self._start:
            return 0.0
        elif time > self._end:
            return 0.0
        cmag = self._magnitude * (1.0 - ((time - self._start) / self._length))
        return (random.random() * (2*cmag)) - cmag

class Motion(Curve):
    def __init__(self, start, startvalue, speed, accelspeed):
        Curve.__init__(self, start)
        self._lastUpdate = self._start
        self._lastValue = startvalue
        self._speed = speed
        self._speedCurve = None
        self._accelSpeed = accelspeed
        
    def changeSpeed(self, time, newSpeed):
        curSpeed = self.speed(time)
        self._lastValue = self.value(time)
        self._lastUpdate = time
        diff = abs(newSpeed - curSpeed)
        targetTime = time + (diff / self._accelSpeed)
        self._speedCurve = CatmullRomSpline(time, curSpeed)
        self._speedCurve.addPoint(targetTime, newSpeed)
    
    def speed(self, time):
        if self._speedCurve is None:
            return self._speed
        else:
            if time > self._speedCurve.end():
                self._speed = self._speedCurve.value(time)
                self._speedCurve = None
                return self._speed
            else:
                return self._speedCurve.value(time)
            
    def value(self, time):
        return self._lastValue + ((time - self._lastUpdate) * self.speed(time))