#!/usr/bin/python3
from textnode import TextNode
from splitnodes import *

import re

def main():
	test = TextNode("wzl", "bold", "https://wzl.to")
	other = TextNode("wzl", "bold", "https://wzl.to")

	print(test)
	print(test.__eq__(other))



	print("testy tester")

	test = "`one codeblock`This is a test with `two codeblock`"
	match = re.findall("(.+)(`.+`)(.+)", test)

	print( match )


main()