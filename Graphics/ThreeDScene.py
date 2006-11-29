from Translator import Translator
from Node import Node
from Display import getDisplay
from OpenGL.GL import *
from OpenGL.GLU import *

class ThreeDScene(Translator, Node):
	def __init__(self):
		Translator.__init__(self)
		Node.__init__(self)
		self.cameraX = self.cameraY = 0.0
		self.cameraZ = -6.0
		self.pitch = self.yaw = self.roll = 0.0
		
	def translate(self):
		glMatrixMode(GL_PROJECTION)
		glPushMatrix()
		glLoadIdentity()
		d = getDisplay()
		gluPerspective(45.0, float(d.w)/float(d.h), 0.1, 100.0)
		glEnable(GL_DEPTH_TEST)
		
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glLoadIdentity()
		glTranslatef(self.cameraX, self.cameraY, self.cameraZ)
		glRotatef(self.roll, 0, 0, 1)
		glRotatef(self.pitch, 1, 0, 0)
		glRotatef(-self.yaw, 0, 1, 0)
		
	def untranslate(self):
		glDisable(GL_DEPTH_TEST)
		glMatrixMode(GL_PROJECTION)
		glPopMatrix()
		
		glMatrixMode(GL_MODELVIEW)
		glPopMatrix()