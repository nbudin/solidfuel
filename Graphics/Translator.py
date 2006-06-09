from OpenGL.GL import *
from Translatable import Translatable

class Translator(Translatable):
	def __init__():
		self.x = 0.0
		self.y = 0.0
	
	def translate():
		glPushMatrix()
		glTranslated(self.x, self.y, 0)
		
	def untranslate():
		glPopMatrix()
