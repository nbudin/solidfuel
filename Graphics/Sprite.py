from OpenGL.GL import *

from Image import Image
from Box import Box
from Visible import Visible
import pygame

class Sprite(Image, Box, Visible):
	def __init__(self, image):
		Box.__init__(self)
		Visible.__init__(self)
		if issubclass(image.__class__, Image):
			self.w = image.w
			self.h = image.h
			self._texture = image._texture
		elif issubclass(image.__class__, pygame.Surface):
			Image.initFromSurface(self, image)
		else:
			Image.__init__(self, image)
		self.rotX = 0.0
		self.rotY = 0.0
		self.rotZ = 0.0
		self.opacity = 1.0

	def draw(self):
		if self.opacity <= 0.0:
			return
		glPushMatrix()
		glTranslated(self.w / 2, self.h / 2, 0)
		glScaled(self.w / 2, self.h / 2, 0)
		glRotate(self.rotX, 1, 0, 0)
		glRotate(self.rotY, 0, 1, 0)
		glRotate(self.rotZ, 0, 0, 1)
		glColor(1.0, 1.0, 1.0, self.opacity)
		glBindTexture(GL_TEXTURE_2D, self._texture)
		glColor4f(1.0, 1.0, 1.0, self.opacity)
		glBegin(GL_QUADS)
		glTexCoord2d(0, 1)
		glVertex3f(-1, 1, 0)
		glTexCoord2d(1, 1)
		glVertex3f(1, 1, 0)
		glTexCoord2d(1, 0)
		glVertex3f(1, -1, 0)
		glTexCoord2d(0, 0)
		glVertex3f(-1, -1, 0)
		glEnd()
		glPopMatrix()
		
	def drawWithTranslation(self):
		translate()
		draw()
		untranslate()
		
