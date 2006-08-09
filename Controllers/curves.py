class Curve:
    def __init__(self, start, length):
        self.start = start
        self.length = length
        self.end = start + length
        
    def value(self, time):
        raise "This is an abstract class."

class LinearCurve(Curve):
    def __init__(self, start, length, startvalue, amount):
        Curve.__init__(self, start, length)
        self.startvalue = startvalue
        self.amount = amount
        self.endvalue = startvalue + amount
        self.amountpersecond = self.amount / self.length
    def value(self, time):
        if time < self.start:
		return self.startvalue
	elif time < self.end:
		return (time - self.start) * self.amountpersecond
	else:
		return self.endvalue

