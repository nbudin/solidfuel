class Curve:
    def __init__(self, start, length):
        self._start = start
        self._length = length
        self._end = start + length
        
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
		return (time - self._start) * self._amountpersecond
	else:
		return self._endvalue

