#!/usr/bin/python3
from textnode import TextNode
from generate import copy_dir, generate_pages_recursive

def main():
	copy_dir("static/", "public/")
	generate_pages_recursive("content/","public/", "template.html")

main()