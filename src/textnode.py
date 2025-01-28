#!/usr/bin/python3
from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
	TEXT = "text"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"


class TextNode():
	 def __init__(self, text, text_type, url=None):
	 	self.text = text
	 	self.text_type = text_type
	 	self.url = url

	 def __eq__(self, txtnode1, txtnode2=False):
	 	left = self if not txtnode2 else txtnode1
	 	right = txtnode2 if txtnode2 else txtnode1
	 	return left.__dict__ == right.__dict__

	 def __repr__(self):
	 	return f"TextNode(text:{self.text}, text_type:{TextType[self.text_type]}, url:{self.url})"


def text_node_to_html_node(text_node):
	#LeafNode(tag, value=None, props=None)
	match text_node.text_type:
		case TextType.TEXT:
			return LeafNode(None, text_node.text)
		case TextType.BOLD:
			return LeafNode("b", text_node.text)
		case TextType.ITALIC:
			return LeafNode("i", text_node.text)
		case TextType.CODE:
			return LeafNode("code", text_node.text)
		case TextType.LINK:
			return LeafNode("a", text_node.text, {"href":text_node.url})
		case TextType.IMAGE:
			return LeafNode("img", "", {"src":text_node.url,"alt":text_node.text})
		case _:
			raise Exception("Invalid textnode texttype")

