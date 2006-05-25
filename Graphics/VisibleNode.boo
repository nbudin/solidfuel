// created on 5/25/2006 at 1:31 PM

namespace SolidFuel.Graphics

class VisibleNode(Node, IVisible):
	protected _visible as IVisible
	
	public Visible:
		get:
			return _visible
	
	def constructor(visible as IVisible):
		_visible = visible
		
	def draw():
		_visible.draw()