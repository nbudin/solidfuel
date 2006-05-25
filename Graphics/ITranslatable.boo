// created on 5/25/2006 at 3:05 PM

namespace SolidFuel.Graphics

interface ITranslatable:
	x as double:
		get
		set
	
	y as double:
		get
		set
	
	rotX as double:
		get
		set
	
	rotY as double:
		get
		set
	
	rotZ as double:
		get
		set
	
	def translate()
	
	def untranslate()