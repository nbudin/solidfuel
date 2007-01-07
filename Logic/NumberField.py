from DataField import DataField
from Event import Event
from Condition import Condition

class NumberField(DataField): 
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
    
    def subtract(self, amount=1):
        self.set(self._value - amount)
    
    def multiply(self, amount):
        self.set(self._value * amount)
        
    def divide(self, amount):
        self.set(self._value / amount)