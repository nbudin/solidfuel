from OpenGL.GL import *
from Box import Box
from Node import Node

class RotoZoomer(Box):
	def __init__(self):
		self.zoom = 1.0
		self.rot = 0.0
		Box.__init__(self)
	
	def translate(self):
		Box.translate(self)
		glScale(self.zoom, self.zoom, self.zoom)
		glTranslated(self.w / -2, self.h / -2, 0)
		glRotate(self.rot, 0, 0, 1)