from solidfuel.Graphics import Text
from SpriteWrapper import SpriteWrapper

class Label(SpriteWrapper):
    def __init__(self, font, text, color):
        self.setFont(font)
        self.setColor(color)
        self.setText(text)
        SpriteWrapper.__init__(self)
        
    def setFont(self, font):
        self._font = font
        
    def setText(self, text):
        self._text = text
    
    def setColor(self, color):
        self._color = tuple([int(x * 255) for x in color])
        
    def _getUpdatedSprite(self):
        return Text(self._font, self._text, self._color)