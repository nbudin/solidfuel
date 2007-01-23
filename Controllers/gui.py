from solidfuel.Graphics import Box, Sprite

class Cursor(Sprite):
    def __init__(self, image, hotspot=None):
        Sprite.__init__(self, image)
        if hotspot is None:
            self.hotspot = (0, 0)
        else:
            self.hotspot = hotspot

class Gui(Box):
    def __init__(self, cursor, *widgets):
        Box.__init__(self)
        self._widgets = widgets
        self._cursor = cursor
        self._lastover = []
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
    def _mouseMove(self, amount):
        (self._cursor.x, self._cursor.y) = self._mouse.pos
    def _mouseDown(self, button):
        pass
    def _mouseUp(self, button):
        pass
    def _keyDown(self, key):
        pass
    def _keyUp(self, key):
        pass