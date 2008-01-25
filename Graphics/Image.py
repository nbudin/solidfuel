# -*- tab-width: 4 -*-

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from solidfuel import config
from OpenGL.GL.EXT.texture_filter_anisotropic import *


class Image:
    nextTextures = None
    def __init__(self, f, filenamehint = None):
        self._texture = None
        if filenamehint is not None:
            surf = pygame.image.load(f, filenamehint)
        else:
            surf = pygame.image.load(f)
        self.initFromSurface(surf)

    def initFromSurface(self, surf):
        self.nativeW = self.w = surf.get_width()
        self.nativeH = self.h = surf.get_height()

        texdata = pygame.image.tostring(surf, "RGBA", 1)

        if Image.nextTextures is None:
            Image.nextTextures = list(glGenTextures(1000))
        self._texture = Image.nextTextures.pop()
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
