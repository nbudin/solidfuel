// created on 5/25/2006 at 11:52 AM

namespace SolidFuel.Graphics

class ChildAlreadyExistsException(System.Exception):
	public parent as Node
	public child as Node
	
	def constructor(p as Node, c as Node):
		parent = p
		child = c
		super()

class Node:
	protected _parent as Node
	protected _children as System.Collections.ArrayList = System.Collections.ArrayList()
	
	public Parent:
		get:
			return _parent
	
	public Children:
		get:
			return _children.Clone()
	
	def addChild(newChild as Node):
		if _children.Contains(newChild):
			raise ChildAlreadyExistsException(self, newChild) 
		newChild._parent = self
		_children.Add(newChild)
	
	def removeChild(child as Node):
		_children.Remove(child)
		child._parent = null
		
	def pullToTop(child as Node):
		_children.Remove(child)
		_children.Add(child)
		
	def pushToBottom(child as Node):
		_children.Remove(child)
		_children.Insert(0, child)
	
	def pullAbove(child as Node, otherChild as Node):
		_children.Remove(child)
		_children.Insert(_children.IndexOf(otherChild) + 1, child)
	
	def pushBelow(child as Node, otherChild as Node):
		_children.Remove(child)
		_children.Insert(_children.IndexOf(otherChild), child)
		
	def pullUp(child as Node, amount as int):
		i = _children.IndexOf(child)
		if i < _children.Count - amount:
			_children.Remove(child)
			_children.Insert(i + amount, child)
			
	def pullUp(child as Node):
		self.pullUp(child, 1)
	
	def pushDown(child as Node, amount as int):
		i = _children.IndexOf(child)
		if i >= amount:
			_children.Remove(child)
			_children.Insert(i - amount, child)
	
	def pushDown(child as Node):
		self.pushDown(child, 1)