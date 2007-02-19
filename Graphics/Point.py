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
    
    def draw(self):
        glEnable(GL_POINT_SMOOTH)
		glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glColor(self.color[0], self.color[1], self.color[2], self.opacity)
		glBegin(GL_POINTS)
        glVertex3f(0.0, 0.0, 0.0)
        glEnd()