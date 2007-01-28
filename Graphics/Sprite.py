# -*- tab-width: 4 -*-

from OpenGL.GL import *

from Image import Image
from Box import Box
from Visible import Visible
import pygame

class Sprite(Image, Box, Visible):
	displayList = None
	def __init__(self, image):
		Box.__init__(self)
		Visible.__init__(self)
		if issubclass(image.__class__, Image):
			self.w = image.w
			self.h = image.h
			self.nativeW = image.nativeW
			self.nativeH = image.nativeH
			self._texture = image._texture
		elif issubclass(image.__class__, pygame.Surface):
		    self._texture = None
			Image.initFromSurface(self, image)
		else:
			Image.__init__(self, image)
		self.rotX = 0.0
		self.rotY = 0.0
		self.rotZ = 0.0
		self.opacity = 1.0
		if Sprite.displayList is None:
			self._genDisplayList()

	def _genDisplayList(self):
		Sprite.displayList = glGenLists(1)
		glNewList(Sprite.displayList, GL_COMPILE)

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

		glEndList()
		
	def draw(self):
		if self.opacity <= 0.0:
			return
		glPushMatrix()
		glTranslated(self.w / 2, self.h / 2, 0)
		glScaled(self.w / 2, self.h / 2, 0)
		glRotate(self.rotX, 1, 0, 0)
		glRotate(self.rotY, 0, 1, 0)
		glRotate(self.rotZ, 0, 0, 1)
        glEnable(GL_TEXTURE_2D)
		glColor(1.0, 1.0, 1.0, self.opacity)
		glBindTexture(GL_TEXTURE_2D, self._texture)
		glColor4f(1.0, 1.0, 1.0, self.opacity)
		glCallList(Sprite.displayList)
        glDisable(GL_TEXTURE_2D)
		glPopMatrix()
		
