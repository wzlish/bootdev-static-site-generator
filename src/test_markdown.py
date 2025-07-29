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
	block_to_block_type,
	markdown_to_html_node,
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
	def test_block_to_block_type_header(self):

		self.assertEqual("heading", block_to_block_type("# a"))
		self.assertEqual("heading", block_to_block_type("###### a"))
		self.assertNotEqual("heading", block_to_block_type("#a"))
		self.assertNotEqual("heading", block_to_block_type("####### a"))

	def test_block_to_block_type_code(self):

		self.assertEqual("code", block_to_block_type("``` some text ```"))
		self.assertEqual("code", block_to_block_type("``` other text\n with another line ```"))
		self.assertNotEqual("code", block_to_block_type("``` malformed closing tag ``"))
		self.assertNotEqual("code", block_to_block_type("missing opening tag```"))

	def test_block_to_block_type_quote(self):

		self.assertEqual("quote", block_to_block_type("> a quote \n> another line"))

	def test_block_to_block_type_unordered_list(self):

		self.assertEqual("unordered_list", block_to_block_type("* just one line"))
		self.assertEqual("unordered_list", block_to_block_type("* line one \n* line two"))
		self.assertEqual("unordered_list", block_to_block_type("- line one \n- line two"))

	def test_block_to_block_type_ordered_list(self):

		self.assertEqual("ordered_list", block_to_block_type("1. a line \n2. another line"))
		self.assertEqual("ordered_list", block_to_block_type("1. a line \n2. another line\n3. a third line"))
		self.assertNotEqual("ordered_list", block_to_block_type("1. first \n3. a wrong line"))
		self.assertNotEqual("ordered_list", block_to_block_type("1.nospace \n2. another line"))

	def test_block_to_block_type_paragraph(self):

		self.assertEqual("paragraph", block_to_block_type("This is normal text"))
		self.assertEqual("paragraph", block_to_block_type("This is normal ```text but with random code tags```"))


	def test_block_to_block_type_mixedlines(self):

		self.assertEqual("paragraph", block_to_block_type("> a quote \n1. a list item"))
		self.assertEqual("paragraph", block_to_block_type("1. a num \n>amalformedquote"))
		self.assertEqual("paragraph", block_to_block_type("- unordered list \n```code```"))

	def test_markdown_to_html_node(self):

		markdown = """ hi """
		expected_output = """<div><p>hi</p></div>"""
		self.assertEqual(markdown_to_html_node(markdown).to_html(),expected_output)

		markdown = """### hello

		hi howdy """
		expected_output = """<div><h3>hello</h3><p>hi howdy</p></div>"""
		self.assertEqual(markdown_to_html_node(markdown).to_html(),expected_output)

		markdown = """####### seven heading fail """
		expected_output = """<div><p>####### seven heading fail</p></div>"""
		self.assertEqual(markdown_to_html_node(markdown).to_html(),expected_output)

		markdown = """>A quote is here

		- list item 1
		- list item 2
		- list item **bold** """
		expected_output = """<div><blockquote>A quote is here</blockquote><ul><li>list item 1</li><li>list item 2</li><li>list item <b>bold</b></li></ul></div>"""
		self.assertEqual(markdown_to_html_node(markdown).to_html(),expected_output)

		markdown = """1. Numbered
		2. List with a [link](https://google.com)
		3. And *some italics*"""
		expected_output = '''<div><ol><li>Numbered</li><li>List with a <a href="https://google.com">link</a></li><li>And <i>some italics</i></li></ol></div>'''
		self.assertEqual(markdown_to_html_node(markdown).to_html(),expected_output)

		markdown = """ Italic _testy test_ test?"""
		expected_output = """<div><p>Italic <i>testy test</i> test?</p></div>"""
		self.assertEqual(markdown_to_html_node(markdown).to_html(),expected_output)

if __name__ == "__main__":
	unittest.main()
