from solidfuel.Graphics import Box, Sprite, Translatable
from solidfuel.Logic import Event
from OpenGL.GL import *
from pygame import Rect

class Cursor(Sprite):
    def __init__(self, image, hotspot=None):
        Sprite.__init__(self, image)
        if hotspot is None:
            self.hotspot = (0, 0)
        else:
            self.hotspot = hotspot
    def translate(self):
        Sprite.translate(self)
        glTranslated(-self.hotspot[0], -self.hotspot[1], 0)
    
    def untranslate(self):
        glTranslated(self.hotspot[0], self.hotspot[1], 0)
        Sprite.untranslate(self)

class Widget:
    def __init__(self):
        self.mouseUp = Event()
        self.mouseDown = Event()
        self.mouseMove = Event()
        self.mouseOver = Event()
        self.mouseOut = Event()
        self.keyDown = Event()
        self.keyUp = Event()
        self._gui = None
        
    def register(self, gui):
        if self._gui:
            self.unregister()
        self._gui = gui
        self._gui.addWidget(self)
        
    def unregister(self):
        if self._gui:
            self._gui.removeWidget(self)
            self._gui = None
            
    def __del__(self):
        self.unregister()
            
class MouseTracking(Widget):
    def __init__(self):
        Widget.__init__(self)
        self._mouseIn = False
        self._focusLock = False
        self.mouseOver.addResponder(self._focused)
        self.mouseOut.addResponder(self._unfocused)
        self.focus = Event()
        self.unfocus = Event()
        
    def _focused(self):
        if not self._mouseIn:
            self._mouseIn = True
            self.focus.trigger()
        
    def _unfocused(self):
        if self._mouseIn and not self._focusLock:
            self._mouseIn = False
            self.unfocus.trigger()

class Clickable(MouseTracking):
    def __init__(self):
        MouseTracking.__init__(self)
        self._clicking = False
        self.mouseDown.addResponder(self._clickStart)
        self.mouseUp.addResponder(self._clickEnd)
        self.clicked = Event()
    
    def _clickStart(self, button):
        if self._focused and not self._clicking:
            self._clicking = button
            self._focusLock = True
    
    def _clickEnd(self, button):
        if self._focused and self._clicking == button:
            self.clicked.trigger(button)
            self._clicking = False
            self._focusLock = False

class Gui(Box):
    def __init__(self, cursor):
        Box.__init__(self)
        self._cursor = cursor
        self.addChild(self._cursor)
        self._lastover = []
        self._widgets = []
        self._mouse = None
        self._keyboard = None
        
        self.mouseUp = Event()
        self.mouseDown = Event()
        self.mouseMove = Event()
        self.keyDown = Event()
        self.keyUp = Event()
        
    def setMouse(self, mouse):
        if self._mouse is not None:
            self._mouse.move.removeResponder(self._mouseMove)
            self._mouse.down.removeResponder(self._mouseDown)
            self._mouse.up.removeResponder(self._mouseUp)
        self._mouse = mouse
        if mouse is not None:
            self._mouse.move.addResponder(self._mouseMove)
            self._mouse.down.addResponder(self._mouseDown)
            self._mouse.up.addResponder(self._mouseUp)
            
    def setKeyboard(self, keyboard):
        if self._keyboard is not None:
            self._keyboard.down.removeResponder(self._keyDown)
            self._keyboard.up.removeResponder(self._keyUp)
        self._keyboard = keyboard
        if keyboard is not None:
            self._keyboard.down.addResponder(self._keyDown)
            self._keyboard.up.addResponder(self._keyUp)
            
    def addWidget(self, widget):
        self._widgets.append(widget)
        
    def removeWidget(self, widget):
        self._widgets.remove(widget)
        
    def addChild(self, child):
        Box.addChild(self, child)
        self.pullToTop(self._cursor)
        
    def _widgetRect(self, widget, rect=None):
        # simplistic.  doesn't account for scaling or translation.
        if rect is None:
            rect = Rect(0, 0, widget.w, widget.h)
            
        if widget is self:
            return rect
        elif widget.parent is None:
            return None
        elif issubclass(widget.__class__, Translatable):
            return self._widgetRect(widget.parent, rect.move(widget.x, widget.y))
        else:
            return self._widgetRect(widget.parent, rect)
        
    def _mouseMove(self, amount):
        # display coords are y-flipped
        (self._cursor.x, self._cursor.y) = (self._mouse.pos[0] - self.x, self._mouse.pos[1] - self.y)
        over = []
        for widget in self._widgets:
            rect = self._widgetRect(widget)
            if rect is None:
                continue
            if (rect.collidepoint(self._cursor.x, self._cursor.y) or 
                (hasattr(widget, 'mouseIn') and widget.mouseIn)):
                if widget not in self._lastover:
                    widget.mouseOver.trigger()
                over.append(widget)
                widget.mouseMove.trigger(amount)
        for widget in self._lastover:
            if widget not in over:
                widget.mouseOut.trigger()
        self._lastover = over
                
    def _mouseDown(self, button):
        for widget in self._lastover:
            widget.mouseDown.trigger(button)
            
    def _mouseUp(self, button):
        for widget in self._lastover:
            widget.mouseUp.trigger(button)
            
    def _keyDown(self, key):
        for widget in self._lastover:
            widget.keyDown.trigger(key)
            
    def _keyUp(self, key):
        for widget in self._lastover:
            widget.keyUp.trigger(key)