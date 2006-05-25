namespace SolidFuel.Graphics

import Tao.OpenGl

class Sprite(IVisible, Translator):
	private _image as Image
	
	public w:
		get:
			return self._image.w
		set:
			self._image.w = value

	public h:
		get:
			return self._image.h
		set:
			self._image.h = value

	def constructor(filename as string):
		self._image = Image(filename)

	def constructor(image as Image):
		self._image = image
		
	def translate():
		Gl.glPushMatrix()
		Gl.glTranslated(cast(int, x + (self.w / 2)), cast(int, y + (self.h / 2)), 0)
		Gl.glScaled(self.w / 2, self.h / 2, 0)
		Gl.glRotatef(rotX, 1, 0, 0)
		Gl.glRotatef(rotY, 0, 1, 0)
		Gl.glRotatef(rotZ, 0, 0, 1)
	
	def draw():
		Gl.glBindTexture(Gl.GL_TEXTURE_2D, self._image.texture)
		Gl.glBegin(Gl.GL_QUADS)
		Gl.glTexCoord2d(0, 0)
		Gl.glVertex3f(-1, 1, 0)
		Gl.glTexCoord2d(1, 0)
		Gl.glVertex3f(1, 1, 0)
		Gl.glTexCoord2d(1, 1)
		Gl.glVertex3f(1, -1, 0)
		Gl.glTexCoord2d(0, 1)
		Gl.glVertex3f(-1, -1, 0)
		Gl.glEnd()
		
	def drawWithTranslation():
		translate()
		draw()
		untranslate()
		
	AspectRatio as double:
		get:
			return cast(double, self.w) / cast(double, self.h)
	
	def scaleW(w as double):
		ar = self.AspectRatio
		self.w = w
		self.h = w / ar
		
	def scaleH(h as double):
		ar = self.AspectRatio
		self.h = h
		self.w = h * ar
		
