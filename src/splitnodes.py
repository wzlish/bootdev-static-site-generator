from textnode import TextNode, TextType

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