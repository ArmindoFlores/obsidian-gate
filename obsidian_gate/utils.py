__all__ = [
    "walkdir",
    "walk_file_tree",
    "strip_md_extension",
]

import os


PACKAGE_DIR = os.path.dirname(__file__)

def _walkdir(root, path, exclude_pattern, include_directories):
    full_path = root if path is None else os.path.join(root, path)
    if not os.path.exists(full_path):
        return

    for entry in os.listdir(full_path):
        if exclude_pattern is not None and exclude_pattern.match(entry):
            continue
        joined_path = entry if path is None else os.path.join(path, entry)
        joined_full_path = os.path.join(root, joined_path)
        is_directory = os.path.isdir(joined_full_path)
        if include_directories or not is_directory:
            yield joined_path, is_directory
        if is_directory:
            yield from _walkdir(root, joined_path, exclude_pattern, include_directories)

def walkdir(path, exclude_pattern=None, include_directories=False):
    return _walkdir(path, None, exclude_pattern, include_directories)

def _walk_file_tree(path, files):
    for name, subdir in files.items():
        new_path = os.path.join(path, name)
        if subdir == "file":
            yield path, name
        else:
            yield from _walk_file_tree(new_path, subdir)

def walk_file_tree(files):
    return _walk_file_tree(".", files)

def strip_md_extension(string):
    split_string = string.split(".")
    if split_string[-1] == "md" and len(split_string) > 1:
        return ".".join(split_string[:-1])
    return string

def relative_path(path):
    return os.path.join(PACKAGE_DIR, path)
