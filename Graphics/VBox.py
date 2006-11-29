from Box import Box
import solidfuel.constants
import pygame

class VBox(Box):
	def __init__(self, x=0.0, y=0.0, w=0.0, h=0.0, padding=0.0, justify=solidfuel.constants.CENTER):
		Box.__init__(self, x, y, w, h)
		self.padding = padding
		self.justify = justify
		
	def pack(self):
		curY = 0.0
		totalW = 0.0
		for child in self.children:
			child.y = curY
			curY -= child.h
			curY -= self.padding
			if totalW < child.w:
				totalW = child.w
		for child in self.children:
			if self.justify & solidfuel.constants.LEFT:
				child.x = 0
			elif self.justify & solidfuel.constants.RIGHT:
				child.x = totalW - child.w
			elif self.justify & solidfuel.constants.CENTER:
				child.x = totalW / 2 - child.w / 2
		self.h = -(curY + self.padding)
		self.w = totalW
			