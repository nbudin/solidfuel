# -*- tab-width: 4 -*-

from OpenGL.GL import *
from Box import Box
from Node import Node

class RotoZoomer(Box):
	def __init__(self):
		self.zoom = 1.0
		self.rot = 0.0
		Box.__init__(self)
	
	def translate(self):
	    glPushMatrix()
		Box.translate(self)
		glScale(self.zoom, self.zoom, self.zoom)
		glRotate(self.rot, 0, 0, 1)
		glTranslated(self.w / -2, self.h / 2, 0)
		
	def untranslate(self):
	    glPopMatrix()
		