from Box import Box
import solidfuel.constants
import pygame

class HBox(Box):
	def __init__(self, x=0.0, y=0.0, w=0.0, h=0.0, padding=0.0, justify=solidfuel.constants.CENTER):
		Box.__init__(self, x, y, w, h)
		self.padding = padding
		self.justify = justify
		
	def pack(self):
		curX = 0.0
		totalH = 0.0
		for child in self.children:
			child.x = curX
			curX += child.w
			curX += self.padding
			if totalH < child.h:
				totalH = child.h
		for child in self.children:
			if self.justify & solidfuel.constants.TOP:
				child.y = 0
			elif self.justify & solidfuel.constants.BOTTOM:
				child.y = totalH - child.h
			elif self.justify & solidfuel.constants.CENTER:
				child.y = totalH / 2 - child.h / 2
		self.w = curX - self.padding
		self.h = totalH
		