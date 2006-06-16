from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from solidfuel import config

class Image:
	def __init__(self, filename):
		self._texture = 0    
		surf = pygame.image.load(filename)
		self.w = surf.get_width()
		self.h = surf.get_height()

		texdata = pygame.image.tostring(surf, "RGBA", 1)

		self._texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, self._texture)
		if config.use_anisotropic:
			try:
				glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, 2.0)
			except:
				config.use_anisotropic = 0
		if not config.use_anisotropic:
			glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
			glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
			gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, surf.get_width(), surf.get_height(), 
				GL_RGBA, GL_UNSIGNED_BYTE, texdata)

		del surf
		del texdata

	def __del__(self):
		# I would like to delete the texture here, but for some reason
		# I get a segfault whenever I try it
		glDeleteTextures((self._texture,))
