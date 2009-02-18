# -*- tab-width: 4 -*-

from OpenGL.GL import *
from Translatable import Translatable
from solidfuel.Math import Vector

class Translator(Translatable):
	def __init__(self):
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
	
    def getPos(self):
        return Vector(self.x, self.y, self.z)
	
	def translate(self):
		glTranslated(float(self.x), float(self.y), float(self.z))
		
	def untranslate(self):
        glTranslated(float(-self.x), float(-self.y), float(-self.z))
