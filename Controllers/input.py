import pygame
from pygame.locals import *
from solidfuel.Logic import EventGroup, Event

class Input(EventGroup):
    def update(self, event):
        pass
        
class Keyboard(Input):
    def __init__(self):
        self.down = Event()
        self.up = Event()
        self.items = [self.down, self.up]
        
    def update(self, e):
        if e.type == KEYDOWN:
            self.down.trigger(e.key)
        elif e.type == KEYUP:
            self.up.trigger(e.key)

class Mouse(Input):
    def __init__(self):
        self.lastpos = None
        self.pos = None
        
        self.move = Event()
        self.down = Event()
        self.up = Event()
        self.items = [self.move, self.down, self.up]
    def update(self, e):
        if e.type == MOUSEMOTION:
            self.lastpos = self.pos
            self.pos = e.pos
            self.move.trigger(e.rel)
        elif e.type == MOUSEBUTTONDOWN:
            self.down.trigger(e.button)
        elif e.type == MOUSEBUTTONUP:
            self.up.trigger(e.button)