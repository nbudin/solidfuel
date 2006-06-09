from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

class Image:
    try:
        glGetString(GL_EXTENSIONS).index("GL_EXT_texture_filter_anisotropic")
    except (ValueError, AttributeError):
        use_anisotropic = 0
    else:
        use_anisotropic = 1

    def __init__(filename):
        self._texture = 0    
        surf = pygame.image.load(filename)
        self.w = surf.w
        self.h = surf.h

        texdata = pygame.image.tostring(textureSurface, "RGBA", 1)
        
        self._texture = glGenTextures(1)[0]
        glBindTexture(GL_TEXTURE_2D, self._texture)
        if Image.use_anisotropic:
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, 2.0)
        else:
            glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        gluBuild2DMipmaps(GL_TEXTURE_2D, 4, area.w, area.h, 
                          GL_RGBA, GL_UNSIGNED_BYTE, texdata)

        del surf
        del texdata
        
    def __del__():
    	# I would like to delete the texture here, but for some reason
    	# I get a segfault whenever I try it
    	glDeleteTextures(1, self._texture)
