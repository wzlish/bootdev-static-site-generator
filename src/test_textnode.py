#!/usr/bin/python3
import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

        node = TextNode(False, TextType.BOLD)
        node2 = TextNode(False, TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("TunnelSnakesRule", TextType.BOLD, None)
        node2 = TextNode("TunnelSnakesRule", TextType.BOLD, None)
        self.assertEqual(node, node2)

        node = TextNode("CutieBoots", TextType.BOLD)
        node_to_html = text_node_to_html_node(node).to_html()
        self.assertEqual(node_to_html, "<b>CutieBoots</b>")

        node = TextNode("boot.dev", TextType.LINK, "https://www.boot.dev")
        node_to_html = text_node_to_html_node(node).to_html()
        self.assertEqual(node_to_html, '<a href="https://www.boot.dev">boot.dev</a>')

        node = TextNode("alt text", TextType.IMAGE, "./test.jpg")
        node_to_html = text_node_to_html_node(node).to_html()
        self.assertEqual(node_to_html, '<img src="./test.jpg" alt="alt text">')

if __name__ == "__main__":
    unittest.main()