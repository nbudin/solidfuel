# -*- tab-width: 4 -*-

from OpenGL.GL import *

from Image import Image
from VisibleNode import VisibleNode
from Translator import Translator
import pygame
from math import cos, sin

TWOPI = 2 * 3.14159
PID2 = 3.14159 / 2

class Sphere(VisibleNode, Translator):
	displayList = None
	precision = 16
	
	def __init__(self, radius, image=None):
	    VisibleNode.__init__(self)
	    Translator.__init__(self)
	    
	    self.rotX = self.rotY = self.rotZ = 0.0
	    
	    self._image = image
	    self._radius = radius
	    if Sphere.displayList is None:
	        self._genDisplayList()
	        
	def _genDisplayList(self):
		Sphere.displayList = glGenLists(1)
		glNewList(Sphere.displayList, GL_COMPILE)

        n = Sphere.precision
        for j in range(n / 2):
            theta1 = j * TWOPI / n - PID2
            theta2 = (j + 1) * TWOPI / n - PID2
            
            glBegin(GL_QUAD_STRIP)
            for i in range(n):
                theta3 = i * TWOPI / n
                
                px = cos(theta2) * cos(theta3)
                py = sin(theta2)
                pz = cos(theta2) * sin(theta3)
                
                glNormal3f(px, py, pz)
                glTexCoord2f(i/n, 2*(j+1)/n)
                glVertex3f(px, py, pz)
                
                px = cos(theta1) * cos(theta3)
                py = sin(theta1)
                pz = cos(theta1) * sin(theta3)
                
                glNormal3f(px, py, pz)
                glTexCoord2f(i/n, 2*j/n)
                glVertex3f(px, py, pz)
            glEnd()

		glEndList()
	
	def draw(self):
		glPushMatrix()
		glPushAttrib(GL_ALL_ATTRIB_BITS)
		glScaled(self._radius, self._radius, self._radius)
		glRotate(self.rotX, 1, 0, 0)
		glRotate(self.rotY, 0, 1, 0)
		glRotate(self.rotZ, 0, 0, 1)
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
        if self._image:
		    glBindTexture(GL_TEXTURE_2D, self._image._texture)
		glCallList(Sphere.displayList)
        glPopAttrib()
		glPopMatrix()