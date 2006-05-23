import Tao.OpenGl

class Sprite:
	private _image as Image
	public x = 0.0
	public y = 0.0
	public rotX = 0.0
	public rotY = 0.0
	public rotZ = 0.0

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

	def destructor():
		# I would like to delete the texture here, but for some reason
		# I get a segfault whenever I try it
		#Gl.glDeleteTextures(1, self.texture)
		pass
		
	def draw():
		Gl.glBindTexture(Gl.GL_TEXTURE_2D, self._image.texture)
		Gl.glPushMatrix()
		Gl.glTranslated(cast(int, self.x + (self.w / 2)), 
				cast(int, self.y + (self.h / 2)), 0)
		Gl.glScaled(self.w / 2, self.h / 2, 0)
		Gl.glRotatef(self.rotX, 1, 0, 0)
		Gl.glRotatef(self.rotY, 0, 1, 0)
		Gl.glRotatef(self.rotZ, 0, 0, 1)
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
		Gl.glPopMatrix()
		
	aspectRatio as double:
		get:
			return cast(double, self.w) / cast(double, self.h)
	
	def scaleW(w as double):
		ar = self.aspectRatio
		self.w = w
		self.h = w / ar
		
	def scaleH(h as double):
		ar = self.aspectRatio
		self.h = h
		self.w = h * ar
		
