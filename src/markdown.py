import re
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode, ParentNode

def extract_markdown_images(text):
	pattern = re.compile("!\\[(.*?)\\]\\((.*?)\\)")
	return [m.groups() + m.span() for m in re.finditer(pattern, text)]

def extract_markdown_links(text):
	pattern = re.compile("(?<!\\!)\\[(.*?)\\]\\((.*?)\\)")
	return [m.groups() + m.span() for m in re.finditer(pattern, text)]

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	output = []
	for old_node in old_nodes:

		if old_node.text_type != TextType.TEXT:
			output.append(old_node)
			continue

		new_nodes = []
		blocks = old_node.text.split(delimiter)
		if not len(blocks) % 2:
			raise ValueError("Invalid markdown")
		for i in range(len(blocks)):
			if blocks[i] == "":
				continue
			if not i%2:
				new_nodes.append(TextNode(blocks[i], TextType.TEXT))
				continue
			new_nodes.append(TextNode(blocks[i], text_type))
		output.extend(new_nodes)
	return output


def _split_imagelink_helper(old_nodes, target_node):
	output = []
	for old_node in old_nodes:

		if old_node.text_type != TextType.TEXT:
			output.append(old_node)
			continue

		new_nodes = []
		pos = 0
		extracted = extract_markdown_images(old_node.text) if target_node == TextType.IMAGE else extract_markdown_links(old_node.text)
		for elem in extracted:
			start, end = elem[2:]
			if start>pos and len(old_node.text[pos:start])>0:
				new_nodes.append(TextNode(old_node.text[pos:start],TextType.TEXT))
			new_nodes.append(TextNode(elem[0], target_node, elem[1]))
			pos = end

		if pos<len(old_node.text) and len(old_node.text[pos:])>0:
			new_nodes.append(TextNode(old_node.text[pos:],TextType.TEXT))
		output.extend(new_nodes)

	return output

split_nodes_image = lambda n: _split_imagelink_helper(n, TextType.IMAGE)
split_nodes_link = lambda n: _split_imagelink_helper(n, TextType.LINK)

def text_to_textnodes(text):

	delims = [	("**", TextType.BOLD),
	            ("*", TextType.ITALIC),
				("_", TextType.ITALIC),
				("`", TextType.CODE)]

	output = [TextNode(text, TextType.TEXT)]
	for delim in delims:
		output = split_nodes_delimiter(output, delim[0], delim[1])
	output = split_nodes_image(output)
	output = split_nodes_link(output)

	return output

def markdown_to_blocks(text):
	blocks = [[]]
	for line in text.strip().splitlines():
		line = line.strip()
		if len(line)==0:
			if len(blocks[-1])>0:
				blocks[-1] = "\n".join(blocks[-1])
				blocks.append([])
			continue
		blocks[-1].append(line)

	blocks[-1] = "\n".join(blocks[-1])
	return blocks

def block_to_block_type(block):
	if block[:7].replace("#","",6)[0]==" ":
		return "heading"

	if len(block)>5 and block[:3] == block[-3:] == "```":
		return "code"

	linetype = set()
	for k,v in enumerate(block.split("\n"), 1):
		if len(linetype)>1:
			return "paragraph"
		if v[:1] == ">":
			linetype.add("quote")
			continue
		if v[:2] == "* " or v[:2] == "- ":
			linetype.add("unordered_list")
			continue
		if v.startswith(f"{k}. "):
			linetype.add("ordered_list")
			continue
		return "paragraph"

	return next(iter(linetype)) if len(linetype)==1 else "paragraph"

def get_leaf_nodes(text):
	return [text_node_to_html_node(n) for n in text_to_textnodes(text)]

def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	blocks_html = []
	for block in blocks:
		block_type = block_to_block_type(block)
		match block_type:
			case "heading":
				h_size = len(block[:block.index(" ")])
				text = block[block.index(" ")+1:]
				blocks_html.append(ParentNode(f"h{h_size}",get_leaf_nodes(text)))

			case "code":
				text = block[3:-3]
				children = [ParentNode(f"code",get_leaf_nodes(text))]
				blocks_html.append(ParentNode(f"pre",children))

			case "quote":
				text = "\n".join(line[1:] for line in block.split("\n"))
				blocks_html.append(ParentNode("blockquote",get_leaf_nodes(text.strip())))

			case "unordered_list" | "ordered_list":
				children = []
				for line in block.split("\n"):
					children.append(ParentNode(f"li",get_leaf_nodes(line[line.index(" ")+1:])))
				list_type = "ul" if block_type == "unordered_list" else "ol"
				blocks_html.append(ParentNode(list_type,children))

			case "paragraph":
				blocks_html.append(ParentNode("p",get_leaf_nodes(block)))

	return ParentNode("div",blocks_html)

def extract_title(markdown):

	for block in markdown.split("\n"):
		if block[:2] == "# ":
			return block[2:].strip()
	raise Exception("No valid h1 title")
