import Tao.Sdl
import Tao.OpenGl
import Tao.OpenGl.Glu
import System.Runtime.InteropServices

class Image:
    private _texture as int
    public w = 0.0
    public h = 0.0

    texture:
        get:
            return _texture
    
    def constructor(filename as string):
        self._texture = 0    
        surfptr = SdlImage.IMG_Load(filename)
        if surfptr.Equals(System.IntPtr.Zero):
            raise "Error loading image " + filename
        
        surf = cast(Sdl.SDL_Surface, Marshal.PtrToStructure(surfptr, typeof(Sdl.SDL_Surface)))

        # fix this later, it is inefficent, we should figure out SDL_BYTEORDER at compile time
        if Sdl.SDL_BYTEORDER == Sdl.SDL_LIL_ENDIAN:
            texsurfptr = Sdl.SDL_CreateRGBSurface(Sdl.SDL_SWSURFACE, surf.w, surf.h, 32,
                                                  0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000)
        else:    
            texsurfptr = Sdl.SDL_CreateRGBSurface(Sdl.SDL_SWSURFACE, surf.w, surf.h, 32,
                                                  0xFF000000, 0x00FF0000, 0x0000FF00, 0x000000FF)
        texsurf = cast(Sdl.SDL_Surface, Marshal.PtrToStructure(texsurfptr, typeof(Sdl.SDL_Surface)))

        self.w = surf.w
        self.h = surf.h
        
        area = Sdl.SDL_Rect(0, 0, surf.w, surf.h)
        if surf.flags & Sdl.SDL_SRCALPHA:
            Sdl.SDL_SetAlpha(surfptr, 0, 0)
        Sdl.SDL_BlitSurface(surfptr, area, texsurfptr, area)


        Gl.glGenTextures(1, self._texture) 
        Gl.glBindTexture(Gl.GL_TEXTURE_2D, self._texture)
        ext = Marshal.PtrToStringAuto(Gl.glGetString(Gl.GL_EXTENSIONS))
        if ext =~ /GL_EXT_texture_filter_anisotropic/:
            Gl.glTexParameterf(Gl.GL_TEXTURE_2D, Gl.GL_TEXTURE_MAX_ANISOTROPY_EXT, 2.0f)
        else:
            Gl.glTexParameteri(Gl.GL_TEXTURE_2D,Gl.GL_TEXTURE_MIN_FILTER,Gl.GL_LINEAR)
            Gl.glTexParameteri(Gl.GL_TEXTURE_2D,Gl.GL_TEXTURE_MAG_FILTER,Gl.GL_LINEAR)
        Glu.gluBuild2DMipmaps(Gl.GL_TEXTURE_2D, 4, area.w, area.h, 
                              Gl.GL_RGBA, Gl.GL_UNSIGNED_BYTE, texsurf.pixels)

        Sdl.SDL_FreeSurface(surfptr)
        Sdl.SDL_FreeSurface(texsurfptr)
        
    def destructor():
		# I would like to delete the texture here, but for some reason
		# I get a segfault whenever I try it
		#Gl.glDeleteTextures(1, self.texture)
		pass
