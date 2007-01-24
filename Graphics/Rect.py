# -*- tab-width: 4 -*-

from OpenGL.GL import *

from Box import Box
from Visible import Visible
import pygame

class Rectangle(Box, Visible):
	fillDisplayList = None
	def __init__(self):
		Box.__init__(self)
		Visible.__init__(self)
		self.fillColor = (0.0, 0.0, 0.0)
		self.borderColor = (1.0, 1.0, 1.0)
		self.borderWidth = 1.0
		self.rotX = 0.0
		self.rotY = 0.0
		self.rotZ = 0.0
		self.borderOpacity = 1.0
		self.fillOpacity = 1.0
		if Rectangle.fillDisplayList is None:
			self._genDisplayLists()

	def _genDisplayLists(self):
		Rectangle.fillDisplayList = glGenLists(1)

		glNewList(Rectangle.fillDisplayList, GL_COMPILE)
		glBegin(GL_QUADS)
		glVertex3f(-1, 1, 0)
		glVertex3f(1, 1, 0)
		glVertex3f(1, -1, 0)
		glVertex3f(-1, -1, 0)
		glEnd()
		glEndList()
		
	def draw(self):
		if self.borderOpacity <= 0.0 and self.fillOpacity <= 0.0:
			return
		glPushMatrix()
		glTranslated(self.w / 2, self.h / 2, 0)
		glScaled(self.w / 2, self.h / 2, 0)
		glRotate(self.rotX, 1, 0, 0)
		glRotate(self.rotY, 0, 1, 0)
		glRotate(self.rotZ, 0, 0, 1)
		if self.fillOpacity > 0.0:
		    glColor(self.fillColor[0], self.fillColor[1], self.fillColor[2], self.fillOpacity)
		    glEnable(GL_LINE_SMOOTH)
		    glLineWidth(self.borderWidth)
		    glCallList(Rectangle.fillDisplayList)
		    glDisable(GL_LINE_SMOOTH)
		if self.borderOpacity > 0.0:
		    glColor(self.borderColor[0], self.borderColor[1], self.borderColor[2], self.borderOpacity)
		    
            xmax = 1 + ((self.borderWidth / 2.0) * (1.0 / self.w))
            xmin = xmax * -1
            ymax = 1 + ((self.borderWidth / 2.0) * (1.0 / self.h))
            ymin = ymax * -1
		    glBegin(GL_LINES)
    		# left side
    		glVertex3f(-1, ymax, 0)
    		glVertex3f(-1, ymin, 0)
    		# top side
    		glVertex3f(xmin, 1.0, 0)
    		glVertex3f(xmax, 1.0, 0)
    		# right side
    		glVertex3f(1.0, ymin, 0)
    		glVertex3f(1.0, ymax, 0)
    		# bottom side
    		glVertex3f(xmin, -1.0, 0)
    		glVertex3f(xmax, -1.0, 0)
    		glEnd()
		glPopMatrix()
		
