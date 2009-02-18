from Label import Label
from solidfuel.Graphics import Rectangle
from solidfuel.Controllers import Clickable

class Button(Rectangle, Clickable):
    def __init__(self, font, label, backgroundColor=None, opacity=1.0, borderColor=(0.0,0.0,0.0), 
        borderWidth=1.0, prelightColor=None, textColor=(1.0, 1.0, 1.0), textPrelightColor=None, padding=5.0):
        
        Rectangle.__init__(self)
        Clickable.__init__(self)
        if backgroundColor is None:
            self.opacity = 0.0
        else:
            self.normalColor = self.fillColor = backgroundColor
            self.fillOpacity = opacity
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.prelightColor = prelightColor
        self.textColor = textColor
        self.textPrelightColor = textPrelightColor
        self.padding = padding
        
        self._label = Label(font, label, textColor)
        self.addChild(self._label)
        self._layout()
        
    def _layout(self):
        self._label.update()
        center = self.getCenter()
        self.h = self._label.h + self.padding*2
        self.w = self._label.w + self.padding*2
        self._label.setCenter(self.getCenterRel())
        self.setCenter(center)
        
    def setTextColor(self, color, update=True):
        self._label.setColor(color)
        if update: 
            self._layout()
        
    def setLabel(self, label, update=True):
        self._label.setText(label)
        if update: 
            self._layout()
        
    def setFont(self, font, update=True):
        self._label.setFont(font)
        if update: 
            self._layout()
    
    def _focused(self):
        Clickable._focused(self)
        if self.prelightColor is not None:
            self.fillColor = self.prelightColor
        if self.textPrelightColor is not None:
            self.setTextColor(self.textPrelightColor)
            
    def _unfocused(self):
        Clickable._unfocused(self)
        self.fillColor = self.normalColor
        if self.textPrelightColor is not None:
            self.setTextColor(self.textColor)
