import argparse
import os

import yaml


def _walk_file_tree(path, files):
    for name, subdir in files.items():
        new_path = os.path.join(path, name)
        if subdir == "file":
            yield path, name
        else:
            yield from _walk_file_tree(new_path, subdir)

def walk_file_tree(files):
    return _walk_file_tree(".", files)

def parse_normal_line(state, text):

    return state, text

def parse_yaml(file):
    first_line = file.readline()
    if first_line != "---\n":
        file.seek(0)
        return False
    lines = []
    while True:
        line = file.readline()
        if line == "":
            file.seek(0)
            return False
        if line == "---" or line == "---\n":
            break
        lines.append(line)
    content = "".join(lines)
    properties = yaml.safe_load(content)
    return properties.get("private", False)

def parse_markdown(file):
    # FIXME: parse this markdown, remove comments, and collect assets
    return file.read()

def parse_and_strip_file_to(source_filename, destination_filename):
    should_skip = False
    try:
        with open(source_filename, "r") as source_file:
            with open(destination_filename, "w") as destination_file:
                should_skip = parse_yaml(source_file)
                if should_skip:
                    return
                destination_file.write(parse_markdown(source_file))
    finally:
        # Handle file deletion
        if should_skip:
            os.remove(destination_filename)

def parse_and_strip(files, source, destination):
    for parent, file in walk_file_tree(files):
        # Create an output directory for this file
        current_file_destination_dir = os.path.join(destination, parent)
        current_file_destination = os.path.abspath(os.path.join(current_file_destination_dir, file))
        current_file_source = os.path.abspath(os.path.join(source, parent, file))
        os.makedirs(current_file_destination_dir, exist_ok=True)

        # Parse its contents and write it new directory
        parse_and_strip_file_to(
            current_file_source,
            current_file_destination,
        )


def parse_handler(args: argparse.Namespace):
    return 0
