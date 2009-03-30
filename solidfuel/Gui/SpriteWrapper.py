from solidfuel.Graphics import Translator, Box

class SpriteWrapper(Translator, Box):
    def __init__(self):
        Translator.__init__(self)
        Box.__init__(self)
        self._sprite = None
        self.update()
        self.untranslate()
        
    def update(self):
        if hasattr(self, '_sprite') and self._sprite:
            scale = (self.w / self._sprite.nativeW, self.h / self._sprite.nativeH)
            self.removeChild(self._sprite)
        else:
            scale = (1.0, 1.0)

        oldSprite = self._sprite
        self._sprite = self._getUpdatedSprite()
        if oldSprite is not None:
            oldSprite.delTexture()
        
        if self._sprite is not None:
            self.addChild(self._sprite)
            self.w = self._sprite.nativeW * scale[0]
            self.h = self._sprite.nativeH * scale[1]
        
    def translate(self):
        if not self._sprite:
            return
            
        self._sprite.w = self.w
        self._sprite.h = self.h
        self._sprite.rotX = self.rotX
        self._sprite.rotY = self.rotY
        self._sprite.rotZ = self.rotZ
        self._sprite.opacity = self.opacity
        Translator.translate(self)
        
    def untranslate(self):
        if not self._sprite:
            return
            
        Translator.untranslate(self)
        self.w = self._sprite.w
        self.h = self._sprite.h
        self.rotX = self._sprite.rotX
        self.rotY = self._sprite.rotY
        self.rotZ = self._sprite.rotZ
        self.opacity = self._sprite.opacity
        
