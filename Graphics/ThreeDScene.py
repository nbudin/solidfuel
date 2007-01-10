# -*- tab-width:4 -*-

from Translator import Translator
from Node import Node
from Display import getDisplay
from OpenGL.GL import *
from OpenGL.GLU import *

class Light(Translator):
    lightConst = [GL_LIGHT0, GL_LIGHT1, GL_LIGHT2, GL_LIGHT3, GL_LIGHT4, GL_LIGHT5, GL_LIGHT6, GL_LIGHT7]

    def __init__(self):
        Translator.__init__(self)
        self._diffuse = 0.25
        self._ambient = 0.25
        self._specular = 0.0
    
    def draw(self, n):
        const = Light.lightConst[n]
        glLightfv(const, GL_POSITION, (self.x, self.y, self.z, 1.0))
        glLightfv(const, GL_AMBIENT, [self._ambient] * 4)
        glLightfv(const, GL_DIFFUSE, [self._diffuse] * 4)
        glLightfv(const, GL_SPECULAR, [self._specular] * 4)
        return const

class ThreeDScene(Translator, Node):
	def __init__(self):
		Translator.__init__(self)
		Node.__init__(self)
		self._lights = []
		self.cameraX = self.cameraY = 0.0
		self.cameraZ = -6.0
		self.pitch = self.yaw = self.roll = 0.0
		
		glLoadIdentity()
		d = getDisplay()
		gluPerspective(45.0, float(d.w)/float(d.h), 0.1, 1000.0)
		self._projMatrix = glGetDoublev(GL_PROJECTION_MATRIX)
		
	def addLight(self, light):
	    if len(self._lights) > 7:
	        raise "Can't have more than 8 lights in a scene!"
	    self._lights.append(light)
	    
	def removeLight(self, light):
	    self._lights.remove(light)
		
	def translate(self):
		glMatrixMode(GL_PROJECTION)
		glLoadMatrixd(self._projMatrix)

        flags = GL_ENABLE_BIT
        flags |= GL_DEPTH_TEST | GL_LIGHTING | GL_NORMALIZE | GL_POLYGON_SMOOTH
        for i in range(len(self._lights)):
		    flags |= self._lights[i].draw(i)
        glPushAttrib(flags)
		
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glLoadIdentity()
		glTranslatef(self.cameraX, self.cameraY, self.cameraZ)
		glRotatef(self.roll, 0, 0, 1)
		glRotatef(self.pitch, 1, 0, 0)
		glRotatef(-self.yaw, 0, 1, 0)
		
	def untranslate(self):
	    glPopAttrib()

		glMatrixMode(GL_PROJECTION)
		glLoadMatrixd(getDisplay()._projMatrix)
		
		glMatrixMode(GL_MODELVIEW)
		glPopMatrix()