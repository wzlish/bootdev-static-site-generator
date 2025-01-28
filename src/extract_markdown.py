import re

def extract_markdown_images(text):

	pattern = re.compile("!\\[(.*?)\\]\\((.*?)\\)")
	return [m.groups() + m.span() for m in re.finditer(pattern, text)]

def extract_markdown_links(text):

	pattern = re.compile("(?<!\\!)\\[(.*?)\\]\\((.*?)\\)")
	return [m.groups() + m.span() for m in re.finditer(pattern, text)]