# -*- tab-width: 4 -*-

from OpenGL.GL import *
from Translatable import Translatable

class Translator(Translatable):
	def __init__(self):
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
	
	def translate(self):
		glTranslated(self.x, self.y, self.z)
		
	def untranslate(self):
        glTranslated(-self.x, -self.y, -self.z)
