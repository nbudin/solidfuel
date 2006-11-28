import math

class Curve:
    def __init__(self, start, length):
        self._start = start
        self._length = length
        self._end = start + length

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
