from OpenGL.GL import *

from Image import Image
from Translator import Translator

class Sprite(Image, Translator):
	def __init__(image):
		if issubclass(image.__class__, Image):
			self.w = image.w
			self.h = image.h
			self._texture = image._texture
		else:
			Image.__init__(self, image)
		self.rotX = 0.0
		self.rotY = 0.0
		self.rotZ = 0.0
		Translator.__init__(self)

	def draw():
		glPushMatrix()
		glTranslated(self.w / 2, self.h / 2, 0)
		glRotatef(rotX, 1, 0, 0)
		glRotatef(rotY, 0, 1, 0)
		glRotatef(rotZ, 0, 0, 1)
		glScaled(self.w / 2, self.h / 2, 0)
		glBindTexture(GL_TEXTURE_2D, self._texture)
		glBegin(GL_QUADS)
		glTexCoord2d(0, 0)
		glVertex3f(-1, 1, 0)
		glTexCoord2d(1, 0)
		glVertex3f(1, 1, 0)
		glTexCoord2d(1, 1)
		glVertex3f(1, -1, 0)
		glTexCoord2d(0, 1)
		glVertex3f(-1, -1, 0)
		glEnd()
		glPopMatrix()
		
	def drawWithTranslation():
		translate()
		draw()
		untranslate()
		
	def aspectRatio():
		return self.w / self.h

	def scale(factor):
		self.w *= factor
		self.h *= factor
	
	def scaleW(w):
		ar = self.aspectRatio()
		self.w = w
		self.h = w / ar
		
	def scaleH(h):
		ar = self.aspectRatio()
		self.h = h
		self.w = h * ar
		
