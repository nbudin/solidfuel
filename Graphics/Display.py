from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from solidfuel import config
from OpenGL.GL.EXT.texture_filter_anisotropic import *

from Node import Node
from Translatable import Translatable

class Display(Node):
	def __init__(self, width, height, flags=0):
		self.w = width
		self.h = height

		pygame.display.init()
		pygame.display.set_mode((self.w, self.h), DOUBLEBUF|OPENGL|flags)
		
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
		
		if config.use_anisotropic:
			try:
				glGetString(GL_EXTENSIONS).index("GL_EXT_texture_filter_anisotropic")
				glInitTextureFilterAnisotropicEXT()
			except:
				config.use_anisotropic = 0
		
		Node.__init__(self)
	
	def setCaption(self, caption):
		pygame.display.set_caption(caption)
		
	def render(self, node = None):
		if node is not None:
			if issubclass(node.__class__, Translatable):
				node.translate()
			node.draw()
			for child in node.children:
				self.render(child)
			if issubclass(node.__class__, Translatable):
				node.untranslate()
		else:
			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
			glLoadIdentity()
			glTranslatef(0, 0, -6)
			for child in self.children:
				self.render(child)
			pygame.display.flip()
			
