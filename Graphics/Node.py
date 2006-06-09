class ChildAlreadyExistsException(Exception):
	def __init__(p, c):
		self.parent = p
		self.child = c
		Exception.__init__(self)

class Node:
	def __init__(self):
		self.children = []
		self.parent = None
		
	def addChild(newChild):
		if newChild in children:
			raise ChildAlreadyExistsException(self, newChild) 
		newChild.parent = self
		self.children.append(newChild)
	
	def removeChild(child):
		self.children.remove(child)
		child.parent = None
		
	def pullToTop(child):
		self.children.remove(child)
		children.add(child)
		
	def pushToBottom(child):
		self.children.remove(child)
		self.children.insert(0, child)
	
	def pullAbove(child, otherChild):
		if otherChild not in children:
			raise ValueError("Node.pullAbove(n1, n2): n2 not in list of children")
		self.children.remove(child)
		self.children.insert(self.children.index(otherChild) + 1, child)
	
	def pushBelow(child, otherChild):
		if otherChild not in children:
			raise ValueError("Node.pushBelow(n1, n2): n2 not in list of children")
		self.children.remove(child)
		self.children.insert(self.children.index(otherChild), child)
		
	def pullUp(child, amount=1):
		i = self.children.index(child)
		if i == -1:
			raise ValueError("Node.pullUp(child, amount): child not in list of children")
		if i < self.children.Count - amount:
			self.children.remove(child)
			self.children.insert(i + amount, child)
			
	def pushDown(child, amount):
		i = self.children.index(child)
		if i == -1:
			raise ValueError("Node.pushDown(child, amount): child not in list of children")
		if i >= amount:
			self.children.remove(child)
			self.children.insert(i - amount, child)
