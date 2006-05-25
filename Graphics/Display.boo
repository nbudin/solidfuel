// created on 5/25/2006 at 1:59 PM

namespace SolidFuel.Graphics

import Tao.Sdl
import Tao.OpenGl

class Display(Node):
	[Property(W)]
	_w as int
	
	[Property(H)]
	_h as int
	
	def constructor(width as int, height as int):
		_w = width
		_h = height
		
		Sdl.SDL_Init(Sdl.SDL_INIT_VIDEO | Sdl.SDL_INIT_TIMER | Sdl.SDL_INIT_EVENTTHREAD)
		Sdl.SDL_SetVideoMode(_w, _h, 32, Sdl.SDL_OPENGL)
		Sdl.SDL_GL_SetAttribute(Sdl.SDL_HWSURFACE, 1)
		Sdl.SDL_GL_SetAttribute(Sdl.SDL_GL_DOUBLEBUFFER, 1)
		
		Gl.glEnable(Gl.GL_TEXTURE_2D)
		Gl.glShadeModel(Gl.GL_SMOOTH)
		Gl.glClearColor(0.0F, 0.5F, 0.0F, 0.0F)
		Gl.glClearDepth(1.0F)
		Gl.glHint(Gl.GL_PERSPECTIVE_CORRECTION_HINT, Gl.GL_NICEST)
		
		Gl.glEnable(Gl.GL_BLEND)
		Gl.glBlendFunc(Gl.GL_SRC_ALPHA, Gl.GL_ONE_MINUS_SRC_ALPHA)

		Gl.glViewport(0, 0, _w, _h)
		Gl.glMatrixMode(Gl.GL_PROJECTION)
		Gl.glLoadIdentity()
		Gl.glFrustum(0, _w, 0, _h, 6f, 100.0f)
		Gl.glMatrixMode(Gl.GL_MODELVIEW)
		Gl.glLoadIdentity()
		
		super()
	
	def setCaption(caption as string):
		Sdl.SDL_WM_SetCaption(caption, "")
		
	def render():
		for child in self._children:
			self.render(child)
		Sdl.SDL_GL_SwapBuffers()
			
	def render(node as VisibleNode):
		if node isa ITranslatable:
			(node as ITranslatable).translate()
		node.draw()
		for child in node._children:
			self.render(child)
		if node isa ITranslatable:
			(node as ITranslatable).untranslate()
		
	def destructor():
		Sdl.SDL_Quit()