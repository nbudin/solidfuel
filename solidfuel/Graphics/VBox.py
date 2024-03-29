# -*- tab-width: 4 -*-

from Box import Box
import solidfuel.constants
import pygame

class VBox(Box):
	def __init__(self, x=0.0, y=0.0, w=0.0, h=0.0, padding=0.0, justify=solidfuel.constants.CENTER):
		Box.__init__(self, x, y, w, h)
		self.padding = padding
		self.justify = justify
		
	def pack(self):
	    # This is more complex than HBox because the coordinate system is Y-flipped
		curY = 0.0
		totalW = 0.0
		totalH = 0.0
		# pass 1: space all children relative to each other
		revchildren = self.children[:]
		revchildren.reverse()
		for child in revchildren:
			child.y = curY
			curY += child.h
			curY += self.padding
			if totalW < child.w:
				totalW = child.w
		# pass 2: justify all children
		for child in self.children:
			if self.justify & solidfuel.constants.LEFT:
				child.x = 0
			elif self.justify & solidfuel.constants.RIGHT:
				child.x = totalW - child.w
			elif self.justify & solidfuel.constants.CENTER:
				child.x = totalW / 2 - child.w / 2
		if self.children:
		    self.h = self.children[0].y + self.children[0].h
		else:
		    self.h = 0.0
		self.w = totalW
			