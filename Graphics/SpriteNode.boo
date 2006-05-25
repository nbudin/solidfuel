// created on 5/25/2006 at 3:03 PM

namespace SolidFuel.Graphics

# I fscking hate having no multiple inheritance.  Pretty much everything in this class
# wouldn't be necessary if Boo allowed multiple inheritance.

class SpriteNode(VisibleNode, ITranslatable):
	x:
		get:
			return (self._visible as ITranslatable).x
		set:
			(self._visible as ITranslatable).x = value
			
	y:
		get:
			return (self._visible as ITranslatable).y
		set:
			(self._visible as ITranslatable).y = value
	
	rotX:
		get:
			return (self._visible as ITranslatable).rotX
		set:
			(self._visible as ITranslatable).rotX = value
			
	rotY:
		get:
			return (self._visible as ITranslatable).rotY
		set:
			(self._visible as ITranslatable).rotY = value
			
	rotZ:
		get:
			return (self._visible as ITranslatable).rotZ
		set:
			(self._visible as ITranslatable).rotZ = value
			
	w:
		get:
			return (self._visible as Sprite).w
		set:
			(self._visible as Sprite).w = value
	
	h:
		get:
			return (self._visible as Sprite).h
		set:
			(self._visible as Sprite).h = value
	
	def constructor(filename as string):
		super(Sprite(filename))

	def constructor(image as Image):
		super(Sprite(image))
		
	def constructor(sprite as Sprite):
		super(sprite)
		
	def translate():
		(self._visible as ITranslatable).translate()
		
	def untranslate():
		(self._visible as ITranslatable).untranslate()
	
	def scaleW(w as double):
		(self._visible as Sprite).scaleW(w)
		
	def scaleH(h as double):
		(self._visible as Sprite).scaleH(h)