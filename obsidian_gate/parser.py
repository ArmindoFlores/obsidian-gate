import argparse
import os

import yaml

from . import markdown, utils


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

def parse_markdown(file, files, extra_args):
    renderer, parser = markdown.get_renderer_and_parser(files, extra_args)
    html = parser(file.read())
    assets = renderer.assets
    return html, assets

def parse_and_strip_file_to(source_filename, destination_filename, files, extra_args):
    assets = []
    should_skip = False
    try:
        with open(source_filename, "r") as source_file:
            with open(destination_filename, "w") as destination_file:
                should_skip = parse_yaml(source_file)
                if should_skip:
                    return True, []
                html, file_assets = parse_markdown(source_file, files, extra_args)
                destination_file.write(html)
                assets += file_assets
    finally:
        # Handle file deletion
        if should_skip:
            os.remove(destination_filename)
    return False, assets

def parse_and_strip(files, source, destination, extra_args):
    assets = []
    filtered_file_list = []
    for path in files:
        if not path.endswith(".md"):
            continue
        parent = os.path.dirname(path)
        file = os.path.basename(path)

        # Create an output directory for this file
        current_file_destination_dir = os.path.join(destination, parent)
        current_file_destination = os.path.abspath(os.path.join(current_file_destination_dir, file))
        current_file_destination = current_file_destination[:-2] + "html"
        current_file_source = os.path.abspath(os.path.join(source, parent, file))
        os.makedirs(current_file_destination_dir, exist_ok=True)

        # Parse its contents and write it new directory
        skipped, file_assets = parse_and_strip_file_to(
            current_file_source,
            current_file_destination,
            files,
            extra_args
        )
        if not skipped:
            assets += file_assets
            filtered_file_list.append(path)

    return filtered_file_list, assets

def parse_handler(args: argparse.Namespace):
    return 0
