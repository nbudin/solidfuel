from Label import Label
from solidfuel.Graphics import Rectangle
from solidfuel.Controllers import Clickable
from solidfuel.Logic import Event

class ToggleGroup(set):
    def __init__(self, default=None):
        set.__init__(self)
        self._value = None
        self._curSelect = None
        self._default = default
        self._byValue = {}
        self._toggleProxies = {}
        self.changed = Event()
        
    def _itemToggled(self, item, value, isSet):
        if self._curSelect and self._curSelect is not item:
            self._curSelect._toggleInner(False)
        if isSet:
            self._value = value
            self._curSelect = item
        else:
            self._value = self._default
            self._curSelect = None
        self.changed.trigger(self._value)
    
    def remove(self, x):
        x.toggled.removeResponder(self._toggleProxies[x])
        if self._curSelect is x:
            self._itemToggled(x, None, False)
        del self._byValue[x._value]
        set.remove(self, x)
        
    def add(self, x):
        if self._byValue.has_key(x._value):
            raise KeyError("This ToggleGroup already has a Toggle with value "+x._value)
        self._toggleProxies[x] = lambda value, isSet: self._itemToggled(x, value, isSet)
        x.toggled.addResponder(self._toggleProxies[x])
        set.add(self, x)
        self._byValue[x._value] = x
        
class FieldDrivenToggleGroup(ToggleGroup):
    def __init__(self, field, default=None):
        ToggleGroup.__init__(self, default)
        self.changed.addResponder(self._setField)
        self._field = field
        self._field._setEvent.addResponder(self._fieldChanged)
        
    def ready(self):
        self._fieldChanged(self._field.get())
        
    def _fieldChanged(self, value):
        if self._byValue.has_key(value):
            self._byValue[value].toggle(True)
        elif self._curSelect is not None:
            self._curSelect.toggle(False)
    
    def _setField(self, value):
        if value is not None:
            self._field.set(value)

class Toggle(Rectangle, Clickable):
    def __init__(self, unsetColor=(1.0,1.0,1.0), setColor=(0.0,0.0,0.0), opacity=1.0, 
        borderColor=(0.0,0.0,0.0), borderWidth=1.0, value=True):
        
        Rectangle.__init__(self)
        Clickable.__init__(self)
        self.clicked.addResponder(self._clicked)
        self.toggled = Event()
        
        self._value = value
        self._isSet = False
        
        self.unsetColor = unsetColor
        self.setColor = setColor
        self._setFillColor()
        
        self.fillOpacity = opacity
        self.borderColor = borderColor
        self.borderWidth = borderWidth
                
    def _setFillColor(self):
        if self._isSet:
            self.fillColor = self.setColor
        else:
            self.fillColor = self.unsetColor
            
    def _clicked(self, button):
        if button == 1:
            self.toggle()
            
    def _toggleInner(self, isSet):
        self._isSet = isSet
        self._setFillColor()
            
    def toggle(self, isSet=None):
        if isSet is None:
            isSet = (not self._isSet)
        self._toggleInner(isSet)
        self.toggled.trigger(self._value, self._isSet)