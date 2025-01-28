#!/usr/bin/python3
import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
       
        test_node = HTMLNode("a", "This Is A Link", None, {"href":"https://google.com", "class":"linkadink"})
        test_output = test_node.props_to_html()
        expected_output =  ' href="https://google.com" class="linkadink"'
        self.assertEqual(test_output, expected_output)

        test_node = HTMLNode("img", None, None, {"src":"./image.jpg", "class":"testimage", "alt":"Alt Text"})
        test_output = test_node.props_to_html()
        expected_output =  ' src="./image.jpg" class="testimage" alt="Alt Text"'
        self.assertEqual(test_output, expected_output)

        test_node = HTMLNode("body", None, None, {"id":"bodhot","class":"hotbod"})
        test_output = test_node.props_to_html()
        expected_output =  ' id="bodhot" class="hotbod"'
        self.assertEqual(test_output, expected_output)

    def test_leaf_to_html(self):

        test_node = LeafNode("a", "This Is A Link", {"href":"https://google.com", "class":"linkadink"})
        test_output = test_node.to_html()
        expected_output = '<a href="https://google.com" class="linkadink">This Is A Link</a>'
        self.assertEqual(test_output,expected_output)

    def test_parent_to_html(self):
        test_node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],)
        test_output = test_node.to_html()
        expected_output = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(test_output, expected_output)

        test_node = ParentNode(
        "div",
        [
            ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]),
        ],
        {"class": "content"})
        test_output = test_node.to_html()
        expected_output = '<div class="content"><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>'
        self.assertEqual(test_output, expected_output)

        with self.assertRaises(Exception) as err:
            ParentNode().to_html()
        self.assertTrue("No tag set", err.exception)

        with self.assertRaises(Exception) as err:
            ParentNode("body").to_html()
        self.assertTrue("No children set", err.exception)
        

if __name__ == "__main__":
    unittest.main()

