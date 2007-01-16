from Sprite import Sprite
from Numeric import *
from OpenGL.GL import *
import math

class Billboard(Sprite):
    def _normalize(self, v):
        return v  / sqrt(add.reduce(v * v))
    
    def _cross(self, b, c):
        return array([b[1] * c[2] - c[1] * b[2],
            b[2] * c[0] - c[2] * b[0],
            b[0] * c[1] - c[0] * b[1]], 'd')
    
    def translate(self):
        Sprite.translate(self)
        
        glPushMatrix()
        # This assumes that the camera is at (0, 0, 0)!  Really this is not a good assumption.
        objToCamProj = self._normalize(array([-self.x, 0, -self.z], 'd'))
        lookAt = array([0, 0, 1], 'd')
        upAux = self._cross(lookAt, objToCamProj)
        angleCosine = add.reduce(lookAt * objToCamProj)
        if angleCosine < 0.99990 and angleCosine > -0.9999:
            glRotatef(math.acos(angleCosine) * 180 / 3.14, *upAux)
        
        objToCam = self._normalize(array([-self.x, -self.y, -self.z], 'd'))
        angleCosine = add.reduce(objToCamProj * objToCam)
        if angleCosine < 0.99990 and angleCosine > -0.9999:
            glRotatef(acos(angleCosine)*180/3.14, 1, 0, 0)
        else:
            glRotatef(acos(angleCosine)*180/3.14, -1, 0, 0)
        
    def untranslate(self):
        glPopMatrix()
        Sprite.untranslate(self)
        
        