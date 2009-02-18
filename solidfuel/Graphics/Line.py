# -*- tab-width: 4 -*-

from VisibleNode import VisibleNode
from Translator import Translator
from OpenGL.GL import *

class Line(VisibleNode):
    def __init__(self):
        VisibleNode.__init__(self)
        self.startX = self.startY = self.startZ = 0.0
        self.endX = self.endY = self.endZ = 0.0
        self.color = (1.0, 1.0, 1.0)
        self.opacity = 1.0
        self.lineWidth = 1.0
    
    def draw(self):
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glDisable(GL_LIGHTING)
        glLineWidth(self.lineWidth)
		glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glColor4f(self.color[0], self.color[1], self.color[2], self.opacity)
		glBegin(GL_LINES)
        glVertex3f(self.startX, self.startY, self.startZ)
        glVertex3f(self.endX, self.endY, self.endZ)
        glEnd()
        glPopAttrib()