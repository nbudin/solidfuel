// created on 5/25/2006 at 2:37 PM

namespace SolidFuel.Graphics
import Tao.OpenGl

class Translator(ITranslatable):
	[Property(x)]
	private _x = 0.0
	[Property(y)]
	private _y = 0.0
	
	def translate():
		Gl.glPushMatrix()
		Gl.glTranslated(_x, _y, 0)
		
	def untranslate():
		Gl.glPopMatrix()
