# -*- tab-width:4 -*-

from Translatable import Translatable
from Translator import Translator
from Node import Node
from Display import getDisplay
from OpenGL.GL import *
from OpenGL.GLU import *

class Light(Translator):
    def __init__(self):
        Translator.__init__(self)
        self._diffuse = 0.25
        self._ambient = 0.25
        self._specular = 0.0
    
    def draw(self, n):
        const = GL_LIGHT0 + n
        glEnable(const)
        glLightfv(const, GL_POSITION, (self.x, self.y, self.z, 1.0))
        glLightfv(const, GL_AMBIENT, [self._ambient] * 4)
        glLightfv(const, GL_DIFFUSE, [self._diffuse] * 4)
        glLightfv(const, GL_SPECULAR, [self._specular] * 4)
        return const

class ThreeDScene(Translatable, Node):
	def __init__(self):
		Node.__init__(self)
		self._lights = []
		self.cameraX = self.cameraY = 0.0
		self.cameraZ = -6.0
		self.pitch = self.yaw = self.roll = 0.0
		
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		d = getDisplay()
		gluPerspective(45.0, float(d.w)/float(d.h), 0.1, 1000.0)
		self._projMatrix = glGetDoublev(GL_PROJECTION_MATRIX)
		glLoadMatrixd(getDisplay()._projMatrix)
		glMatrixMode(GL_MODELVIEW)
		
	def addLight(self, light):
	    if len(self._lights) >= GL_MAX_LIGHTS:
	        raise "Can't have more than %d lights in a scene!" % (GL_MAX_LIGHTS,)
	    self._lights.append(light)
	    
	def removeLight(self, light):
	    self._lights.remove(light)
		
	def translate(self):
		glMatrixMode(GL_PROJECTION)
		glLoadMatrixd(self._projMatrix)
		
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for flag in (GL_DEPTH_TEST, GL_LIGHTING, GL_NORMALIZE, GL_BLEND, GL_POLYGON_SMOOTH):
            glEnable(flag)
        glDisable(GL_TEXTURE_2D) # Model will handle this for us automatically
        glDisable(GL_BLEND)
        glShadeModel(GL_SMOOTH)
        for i in range(len(self._lights)):
		    self._lights[i].draw(i)
		
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glLoadIdentity()
		glTranslatef(self.cameraX, self.cameraY, self.cameraZ)
		glRotatef(self.roll, 0, 0, 1)
		glRotatef(self.pitch, 1, 0, 0)
		glRotatef(-self.yaw, 0, 1, 0)
		
	def untranslate(self):
	    glPopAttrib()
	    glShadeModel(GL_SMOOTH)

		glMatrixMode(GL_PROJECTION)
		glLoadMatrixd(getDisplay()._projMatrix)
		
		glMatrixMode(GL_MODELVIEW)
		glPopMatrix()