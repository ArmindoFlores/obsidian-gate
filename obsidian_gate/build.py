__all__ = [
    "build_handler",
]

import argparse
import os
import re
import shutil
import tempfile
from pathlib import Path

from . import parser, utils


def collect_files(path):
    site_files = {}
    exclude_pattern = re.compile(r"^\.")
    for obj, _ in utils.walkdir(path, exclude_pattern):
        path = Path(obj)
        parent = site_files
        for part in path.parts[:-1]:
            parent = parent.setdefault(part, {})
        parent[path.parts[-1]] = "file"
    return site_files

def build_handler(args: argparse.Namespace):
    os.makedirs(args.destination, exist_ok=True)

    if not os.path.exists(args.source) or not os.path.isdir(args.source):
        print(f"Directory does not exist: '{args.source}'")
        return 1

    # 1st step - collect all files
    files = collect_files(args.source)
    
    # 2nd step - parse the files to strip out content and turn them
    # into valid Markdown
    with tempfile.TemporaryDirectory() as tempdir:
        parser.parse_and_strip(files, args.source, tempdir)
        shutil.copytree(tempdir, "output", dirs_exist_ok=True)

    return 0
