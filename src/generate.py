import os
import shutil
import sys
from pathlib import Path
from markdown import extract_title, markdown_to_html_node


def copy_dir(source, target, clear=True):

	source = os.path.abspath(source)
	target = os.path.abspath(target)

	if not os.path.exists(source):
		raise Exception(f"{source} does not exist")
	if not os.path.isdir(source):
		raise Exception(f"{source} is not a directory")

	if clear and os.path.exists(target):
		try:
			shutil.rmtree(target)
		except Exception as error:
			sys.exit(f"Unable to rmtree {target}: {error}")

	if not os.path.exists(target):
		os.mkdir(target)

	scan = os.scandir(source)
	for entry in scan:
		if entry.is_file():
			print(f"Copying: {os.path.join(source,entry.name)}")
			shutil.copy(os.path.join(source,entry.name), os.path.join(target,entry.name))
			continue
		if entry.is_dir():
			print(f"Going recursive for {entry.name}")
			copy_dir(os.path.join(source,entry.name), os.path.join(target,entry.name))
			continue
	scan.close()

def generate_page(basepath, template_path, markdown_path, destination):

	destination = Path(destination)

	print(f"Attempting to generate page {destination} from {markdown_path} using template {template_path}")

	with open(template_path, 'r') as file:
		template = file.read()

	with open(markdown_path, 'r') as file:
		markdown = file.read()

	content_html = markdown_to_html_node(markdown).to_html()
	content_html = content_html.replace('href="/', f'href="/{basepath}')
	content_html = content_html.replace('src="/', f'src="/{basepath}')
	template = template.replace("{{ Title }}", extract_title(markdown), 1)
	template = template.replace("{{ Content }}", content_html, 1)

	Path(destination.parent).mkdir(parents=True, exist_ok=True)
	with open(destination, "w") as file:
		file.write(template)

def generate_pages_recursive(basepath, dir_path_content, destination, template_path):

	template_path = os.path.abspath(template_path)
	scan = os.scandir(dir_path_content)
	for entry in scan:
		if entry.is_file():
			if entry.name.endswith(".md"):
				name = entry.name
				new_name = 'html'.join(name.rsplit('md', 1))
				print(f"Found {name}")
				generate_page(	basepath,
				                template_path,
								os.path.join(dir_path_content,name),
								os.path.join(destination,new_name))
			continue
		if entry.is_dir():
			print(f"Generating pages recursively for {entry.name}")
			generate_pages_recursive(	basepath,
			                            os.path.join(dir_path_content,entry.name),
										os.path.join(destination,entry.name),
										template_path)
			continue
	scan.close()
