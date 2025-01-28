#!/usr/bin/python3
import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links

class TestMarkdownImages(unittest.TestCase):
    def test_eq(self):
        item1 = extract_markdown_images("[link text](https://google.com) So this is text and an image: ![a cute boots image](https://www.boot.dev/_nuxt/cuteboots.webp)")
        item2 = [("a cute boots image", "https://www.boot.dev/_nuxt/cuteboots.webp", 62, 126)]
        self.assertEqual(item1, item2)

        item1 = extract_markdown_images("![a](b) ![c](d) [e](f)")
        item2 = [("a","b",0,7), ("c","d",8,15)]
        self.assertEqual(item1, item2)

        item1 = extract_markdown_images("No valid links or images or anything")
        item2 = []
        self.assertEqual(item1, item2)

class TestMarkdownLinks(unittest.TestCase):
    def test_eq(self):
        item1 = extract_markdown_links("[link text](https://google.com) So this is text and an image: ![a cute boots image](https://www.boot.dev/_nuxt/cuteboots.webp)")
        item2 = [("link text", "https://google.com", 0, 31)]
        self.assertEqual(item1, item2)

        item1 = extract_markdown_links("![a](b) ![c](d) [e](f)")
        item2 = [("e","f", 16, 22)]
        self.assertEqual(item1, item2)

        item1 = extract_markdown_links("No valid links or images or anything")
        item2 = []
        self.assertEqual(item1, item2)

if __name__ == "__main__":
    unittest.main()