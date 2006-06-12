from OpenGL.GL import *
from Translatable import Translatable

class Translator(Translatable):
	def __init__(self):
		self.x = 0.0
		self.y = 0.0
	
	def translate(self):
		glPushMatrix()
		glTranslated(self.x, self.y, 0)
		
	def untranslate(self):
		glPopMatrix()
