class VisibleNode(Node):
	def __init__(self, visible):
		self.visible = visible
		
	def draw(self):
		self.visible.draw()
