# -*- tab-width: 4 -*-

from OpenGL.GL import *
from Translator import Translator
from Node import Node

class RotoZoomer(Translator, Node):
	def __init__(self):
		self.zoom = 1.0
		self.rot = 0.0
		Translator.__init__(self)
		Node.__init__(self)
	
	def translate(self):
	    glPushMatrix()
		Translator.translate(self)
		glScale(self.zoom, self.zoom, self.zoom)
		glRotate(self.rot, 0, 0, 1)
		
	def untranslate(self):
	    glPopMatrix()
		