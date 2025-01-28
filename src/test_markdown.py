#!/usr/bin/python3
import unittest
from textnode import TextNode, TextType
from markdown import (
	extract_markdown_images,
	extract_markdown_links,
	split_nodes_delimiter,
	split_nodes_image,
	split_nodes_link,
	text_to_textnodes,
	markdown_to_blocks,
 )

class TestMarkdown(unittest.TestCase):
	def test_markdown_images_eq(self):
		item1 = extract_markdown_images("[link text](https://google.com) So this is text and an image: ![a cute boots image](https://www.boot.dev/_nuxt/cuteboots.webp)")
		item2 = [("a cute boots image", "https://www.boot.dev/_nuxt/cuteboots.webp", 62, 126)]
		self.assertEqual(item1, item2)

		item1 = extract_markdown_images("![a](b) ![c](d) [e](f)")
		item2 = [("a","b",0,7), ("c","d",8,15)]
		self.assertEqual(item1, item2)

		item1 = extract_markdown_images("No valid links or images or anything")
		item2 = []
		self.assertEqual(item1, item2)

	def test_markdown_links_eq(self):
		item1 = extract_markdown_links("[link text](https://google.com) So this is text and an image: ![a cute boots image](https://www.boot.dev/_nuxt/cuteboots.webp)")
		item2 = [("link text", "https://google.com", 0, 31)]
		self.assertEqual(item1, item2)

		item1 = extract_markdown_links("![a](b) ![c](d) [e](f)")
		item2 = [("e","f", 16, 22)]
		self.assertEqual(item1, item2)

		item1 = extract_markdown_links("No valid links or images or anything")
		item2 = []
		self.assertEqual(item1, item2)
	def test_delim_bold(self):
		node = TextNode("This is text with a **bolded** word", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("bolded", TextType.BOLD),
				TextNode(" word", TextType.TEXT),
			],
			new_nodes,
		)

	def test_delim_bold_double(self):
		node = TextNode(
			"This is text with a **bolded** word and **another**", TextType.TEXT
		)
		new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("bolded", TextType.BOLD),
				TextNode(" word and ", TextType.TEXT),
				TextNode("another", TextType.BOLD),
			],
			new_nodes,
		)

	def test_delim_bold_multiword(self):
		node = TextNode(
			"This is text with a **bolded word** and **another**", TextType.TEXT
		)
		new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("bolded word", TextType.BOLD),
				TextNode(" and ", TextType.TEXT),
				TextNode("another", TextType.BOLD),
			],
			new_nodes,
		)

	def test_delim_italic(self):
		node = TextNode("This is text with an *italic* word", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("italic", TextType.ITALIC),
				TextNode(" word", TextType.TEXT),
			],
			new_nodes,
		)

	def test_delim_bold_and_italic(self):
		node = TextNode("**bold** and *italic*", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
		self.assertListEqual(
			[
				TextNode("bold", TextType.BOLD),
				TextNode(" and ", TextType.TEXT),
				TextNode("italic", TextType.ITALIC),
			],
			new_nodes,
		)

	def test_delim_code(self):
		node = TextNode("This is text with a `code block` word", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("code block", TextType.CODE),
				TextNode(" word", TextType.TEXT),
			],
			new_nodes,
		)

	def test_split_image(self):
		node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and some text", TextType.TEXT)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and some text", TextType.TEXT),
			],
			new_nodes,
		)

	def test_split_link(self):
		node = TextNode("This is text with a [link](https://boot.dev) and some text", TextType.TEXT)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("link", TextType.LINK, "https://boot.dev"),
				TextNode(" and some text", TextType.TEXT),
			],
			new_nodes,
		)

	def test_text_to_textnodes(self):

		text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		self.assertListEqual(
			[
				TextNode("This is ", TextType.TEXT),
				TextNode("text", TextType.BOLD),
				TextNode(" with an ", TextType.TEXT),
				TextNode("italic", TextType.ITALIC),
				TextNode(" word and a ", TextType.TEXT),
				TextNode("code block", TextType.CODE),
				TextNode(" and an ", TextType.TEXT),
				TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
				TextNode(" and a ", TextType.TEXT),
				TextNode("link", TextType.LINK, "https://boot.dev"),
			],
			text_to_textnodes(text),
		)

	def test_markdown_to_blocks(self):

		text = """


		# This is a heading




		This is a paragraph of text. It has some **bold** and *italic* words inside of it.

		* This is the first list item in a list block
		* This is a list item
		* This is another list item"""

		self.assertListEqual([	'# This is a heading',
			 					'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
			 					'* This is the first list item in a list block\n* This is a list item\n* This is another list item'
			 					],
			 					markdown_to_blocks(text),
			 				)

if __name__ == "__main__":
	unittest.main()