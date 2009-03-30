# -*- tab-width: 4 -*-

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.raw import GL as simple
import pygame
from pygame.locals import *
from solidfuel import config
from OpenGL.GL.EXT.texture_filter_anisotropic import *
from types import StringType, FileType

class Image:
    nextTextures = None
    def __init__(self, f, filenamehint = None):
        self._texture = None
        if issubclass(f.__class__, pygame.Surface):
            surf = f
        else:
            if filenamehint is not None:
                surf = pygame.image.load(f, filenamehint)
            else:
                surf = pygame.image.load(f)
        self.initFromSurface(surf)

    def initFromSurface(self, surf):
        self.nativeW = self.w = surf.get_width()
        self.nativeH = self.h = surf.get_height()
        self._surf = surf

        if Image.nextTextures is None:
            Image.nextTextures = list(glGenTextures(1000))

        nt = Image.nextTextures.pop()
        try:
            self._texture = simple.GLuint(int(nt))
        except:
            self._texture = nt
        glBindTexture(GL_TEXTURE_2D, self._texture)
        if config.use_anisotropic:
            try:
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, 2.0)
            except:
                config.use_anisotropic = 0
        if not config.use_anisotropic:
            glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)

        self.updateFromSurface()

    def updateFromSurface(self):
        glBindTexture(GL_TEXTURE_2D, self._texture)
        texdata = pygame.image.tostring(self._surf, "RGBA", 1)
        gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, self._surf.get_width(), self._surf.get_height(),
            GL_RGBA, GL_UNSIGNED_BYTE, texdata)

    def delTexture(self):
        # return to texture pool
        Image.nextTextures.append(self._texture)

