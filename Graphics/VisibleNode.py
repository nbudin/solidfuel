from Visible import Visible
from Node import Node

class VisibleNode(Node, Visible):
	def __init__(self):
		Visible.__init__(self)
		Node.__init__(self)
