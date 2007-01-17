from OpenGL.GL import *
from VisibleNode import VisibleNode
from Translator import Translator

class Particle:
    def __init__(self, pos=(0.0, 0.0, 0.0), color=(1.0, 1.0, 1.0), opacity=1.0):
        (self.r, self.g, self.b) = color
        (self.x, self.y, self.z) = pos
        self.opacity = opacity
        
    def draw(self):
        glColor4f(self.r, self.g, self.b, self.opacity)
        glBegin(GL_TRIANGLE_STRIP)
        glTexCoord2d(1,1); glVertex3f(self.x + 0.5, self.y + 0.5, self.z)
        glTexCoord2d(0,1); glVertex3f(self.x - 0.5, self.y + 0.5, self.z)
        glTexCoord2d(1,0); glVertex3f(self.x + 0.5, self.y - 0.5, self.z)
        glTexCoord2d(0,0); glVertex3f(self.x - 0.5, self.y - 0.5, self.z)
        glEnd()