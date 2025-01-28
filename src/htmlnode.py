#!/usr/bin/python3

class HTMLNode():
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError("Nuffin here guv")

	def props_to_html(self):
		return " " + " ".join(f'{k}="{v}"' for k,v in self.props.items()) if self.props else ""

	def __repr__(self):
		return f"HTMLNode(tag:{self.tag},\n value:{self.value}, children:{self.children}, props:{self.props})"

class LeafNode(HTMLNode):
	def __init__(self, tag, value=None, props=None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		if not self.value and not self.tag=="img":
			raise ValueError("No value set")
		if not self.tag:
			return self.value


		if self.tag=="img":
			return f'<{self.tag}{self.props_to_html()}>'
		else:
			return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
	def __init__(self, tag, children=None, props=None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		if not self.tag:
			raise ValueError("No tag set")

		if not self.children:
			raise ValueError("No children set")

		childhtml = "".join(child.to_html() for child in self.children)
		return f'<{self.tag}{self.props_to_html()}>{childhtml}</{self.tag}>'
