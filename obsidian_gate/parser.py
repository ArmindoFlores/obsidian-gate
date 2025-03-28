import argparse
import os


def _walk_file_tree(path, files):
    for name, subdir in files.items():
        new_path = os.path.join(path, name)
        if subdir == "file":
            yield path, name
        else:
            yield from _walk_file_tree(new_path, subdir)

def walk_file_tree(files):
    return _walk_file_tree(".", files)

def parse_and_strip_file_to(source_filename, destination_filename):
    with open(source_filename, "r") as source_file:
        with open(destination_filename, "w") as destination_file:
            # TODO: PARSE!
            destination_file.write(source_file.read())

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
