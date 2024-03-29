# -*- tab-width: 4 -*-

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from solidfuel import config
from OpenGL.GL.EXT.texture_filter_anisotropic import *

from Visible import Visible
from Node import Node
from Translatable import Translatable

def getDisplay():
	return Display.obj

class Display(Node):
	obj = None
	def __init__(self, width=None, height=None, flags=0):
		self._displayInfo = pygame.display.Info()
		Display.obj = self
		if width is None or height is None:
			flags |= FULLSCREEN
			width = self._displayInfo.current_w
			height = self._displayInfo.current_h
		self._nativeW = self.w = width
		self._nativeH = self.h = height

		pygame.display.init()
		self._flags = flags
		self.setDisplayMode()
		
		glShadeModel(GL_SMOOTH)
		glClearColor(0.0, 0.0, 0.0, 0.0)
		glClearDepth(1.0)
		glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
		
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glDepthFunc(GL_LEQUAL)

		glViewport(0, 0, self.w, self.h)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, self.w, 0, self.h, 6.0, 100.0)
		self._projMatrix = glGetDoublev(GL_PROJECTION_MATRIX)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		
		if config.use_anisotropic:
			try:
				glGetString(GL_EXTENSIONS).index("GL_EXT_texture_filter_anisotropic")
				glInitTextureFilterAnisotropicEXT()
			except:
				config.use_anisotropic = 0
		
		Node.__init__(self)

	def setDisplayMode(self):
		self._surf = pygame.display.set_mode((self.w, self.h), DOUBLEBUF|OPENGL|self._flags)

	def toggleFullscreen(self):
		self._flags ^= FULLSCREEN
		self.setDisplayMode()
	
	def setCaption(self, caption):
		pygame.display.set_caption(caption)
		
	def render(self, node = None):
		if node is not None:
			if issubclass(node.__class__, Translatable):
				node.translate()
			if issubclass(node.__class__, Visible):
				node.draw()
			try:
			    for child in node.children:
			        self.render(child)
			finally:
			    if issubclass(node.__class__, Translatable):
				    node.untranslate()
		else:
			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
			glLoadIdentity()
			glTranslatef(0, 0, -6)
			for child in self.children:
				self.render(child)
			pygame.display.flip()
	
	def getCenter(self):
		return (self.w / 2, self.h / 2)
	
	def screenshot(self, filename):
	    pygame.image.save(self._surf, filename)
