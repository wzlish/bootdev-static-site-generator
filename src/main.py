#!/usr/bin/python3
from generate import copy_dir, generate_pages_recursive
from sys import argv


def main():

    basepath = argv[1] if (len(argv)>1 and argv[1]) else "/"
    copy_dir("static/", "docs/")
    generate_pages_recursive(basepath, "content/","docs/", "template.html")

main()
