from DataField import DataField
from Event import Event
from Condition import Condition

class NumberField(DataField):
    def __init__(self, value=None):
        DataField.__init__(self, value)
        self._addEvent = Event()
        self._subtractEvent = Event()
        self._multiplyEvent = Event()
        self._divideEvent = Event()
    
    def lessThan(self, other):
        return self._value < other
    
    def greaterThan(self, other):
        return self._value > other
    
    def _lessThanCond(self, value):
        return self._mkcond(value, self.lessThan, self._setEvent)
    
    def _greaterThanCond(self, value):
        return self._mkcond(value, self.greaterThan, self._setEvent)
    
    def add(self, amount=1):
        self.set(self._value + amount)
        self._addEvent.trigger(amount)
    
    def subtract(self, amount=1):
        self.set(self._value - amount)
        self._subtractEvent.trigger(amount)
    
    def multiply(self, amount):
        self.set(self._value * amount)
        self._multiplyEvent.trigger(amount)
        
    def divide(self, amount):
        self.set(self._value / amount)
        self._divideEvent.trigger(amount)