from Sprite import Sprite

class Text(Sprite):
	def __init__(self, font, text, color):
		surf = font.render(text, 1, color)
		Sprite.__init__(self, surf)