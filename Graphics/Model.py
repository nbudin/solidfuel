from Dice3DS.example import gltexture, glmodel
from Dice3DS import dom3ds

from OpenGL.GL import *

from VisibleNode import VisibleNode
from Translator import Translator

class Model(VisibleNode, Translator):
    texcache = {}
    dlcache = {}
    bbcache = {}

    def __init__(self, filename, compile=True, buffer=None):
        VisibleNode.__init__(self)
        Translator.__init__(self)

        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0

        self.scale = 1.0

        if Model.dlcache.has_key(filename):
            self._displayList = Model.dlcache[filename]
            bb = Model.bbcache[filename]
        else:
            if buffer is None:
                self._dom = dom3ds.read_3ds_file(filename)
            else:
                self._dom = dom3ds.read_3ds_mem(buffer)
            self._model = glmodel.GLModel(self._dom, self._loadTexture)
            bb = self._model.bounding_box()
            Model.bbcache[filename] = bb
            if compile:
                self._displayList = self._model.create_dl()
                Model.dlcache[filename] = self._displayList
            else:
                self._displayList = None
        self._center = (bb[0] + bb[1]) / 2
        self._modelScale = 1.0 / max(abs(bb[0] - bb[1]))

    def translate(self):
        glPushMatrix()
        Translator.translate(self)
        glTranslate(*-self._center)
        rs = self._rs = self.scale * self._modelScale
        glScale(rs, rs, rs)
        glRotate(self.rotX, 1, 0, 0)
        glRotate(self.rotY, 0, 1, 0)
        glRotate(self.rotZ, 0, 0, 1)

    def untranslate(self):
        glPopMatrix()

    def draw(self):
        if self._displayList is not None:
            glCallList(self._displayList)
        else:
            self._model.render()

    def _loadTexture(self, filename):
        if Model.texcache.has_key(filename):
            return Model.texcache[filename]

        tex = gltexture.Texture(filename)
        Model.texcache[texfilename] = tex
        return tex
