// created on 5/25/2006 at 2:37 PM

namespace SolidFuel.Graphics
import Tao.OpenGl

class Translator(ITranslatable):
	[Property(x)]
	private _x = 0.0
	[Property(y)]
	private _y = 0.0
	[Property(rotX)]
	private _rotX = 0.0
	[Property(rotY)]
	private _rotY = 0.0
	[Property(rotZ)]
	private _rotZ = 0.0
	
	def translate():
		Gl.glPushMatrix()
		Gl.glTranslated(cast(int, _x), cast(int, _y), 0)
		Gl.glRotatef(_rotX, 1, 0, 0)
		Gl.glRotatef(_rotY, 0, 1, 0)
		Gl.glRotatef(_rotZ, 0, 0, 1)
		
	def untranslate():
		Gl.glPopMatrix()
