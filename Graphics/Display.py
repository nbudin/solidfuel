from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

from Node import Node

class Display(Node):
	def __init__(width, height):
		self.w = width
		self.h = height

		pygame.init()
		pygame.display.set_mode(self.w, self.h, 32, DOUBLEBUF|OPENGL)
		
		glEnable(GL_TEXTURE_2D)
		glShadeModel(GL_SMOOTH)
		glClearColor(0.0, 0.5, 0.0, 0.0)
		glClearDepth(1.0)
		glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
		
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		glViewport(0, 0, self.w, self.h)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glFrustum(0, self.w, 0, self.h, 6.0, 100.0)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		
		Node.__init__(self)
	
	def setCaption(caption):
		pygame.display.set_caption(caption)
		
	def render(node = None):
		if node is not None:
			if issubclass(node.__class__, Translatable):
				node.translate()
			node.draw()
			for child in node.children:
				self.render(child)
			if issubclass(node.__class__, Translatable):
				node.untranslate()
		else:
			for child in self._children:
				self.render(child)
			pygame.display.flip()
			
