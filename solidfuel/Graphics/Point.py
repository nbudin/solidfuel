# -*- tab-width: 4 -*-

from VisibleNode import VisibleNode
from Translator import Translator
from OpenGL.GL import *

class Point(VisibleNode, Translator):
    def __init__(self):
        VisibleNode.__init__(self)
        Translator.__init__(self)
        self.color = (1.0, 1.0, 1.0)
        self.opacity = 1.0
        self.size = None
    
    def draw(self):
        glEnable(GL_POINT_SMOOTH)
		glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glColor(self.color[0], self.color[1], self.color[2], self.opacity)
        if self.size:
            glPointSize(self.size)
		glBegin(GL_POINTS)
        glVertex3f(0.0, 0.0, 0.0)
        glEnd()
        if self.size:
            glPointSize(1.0)