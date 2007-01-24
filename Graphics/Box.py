from Translator import Translator
from Node import Node
import pygame

class Box(Node, Translator):
	def __init__(self, x=0.0, y=0.0, w=0.0, h=0.0):
		Translator.__init__(self)
		Node.__init__(self)
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		
	def aspectRatio(self):
		return self.w / self.h

	def scale(self, factor):
		self.w *= factor
		self.h *= factor

	def scaleW(self, w):
		ar = self.aspectRatio()
		self.w = w
		self.h = w / ar

	def scaleH(self, h):
		ar = self.aspectRatio()
		self.h = h
		self.w = h * ar

	def setCenter(self, center):
		self.x = center[0] - self.w / 2
		self.y = center[1] - self.h / 2

	def getCenter(self):
		return (self.x + self.w / 2, self.y + self.h / 2)
		
	def getCenterRel(self):
	    return (self.w / 2, self.h / 2)