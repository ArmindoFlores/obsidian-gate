__all__ = [
    "build_handler",
]

import argparse
import json
import os
import re
import shutil
import tempfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from . import parser, utils


def collect_files(path):
    site_files_dict = {}
    site_files_list = []
    exclude_pattern = re.compile(r"^\.")
    for obj, _ in utils.walkdir(path, exclude_pattern):
        path = Path(obj)
        parent = site_files_dict
        for part in path.parts[:-1]:
            parent = parent.setdefault(part, {})
        parent[path.parts[-1]] = "file"
        site_files_list.append(str(path))
    return site_files_dict, site_files_list

def html_for(environment, filename, file_contents, args):
    page_title = utils.strip_md_extension(os.path.basename(filename))
    template = environment.get_template("default_page_template.html")
    rendered = template.render(
        content=file_contents,
        page_title=page_title,
        vault_name=args.site_name,
        stylesheet=args.styles,
    )
    return rendered

def render_index_to_html(index, level=0, path=""):
    html = ""
    indent = "  " * level

    for key, value in index.items():
        name = utils.strip_md_extension(key)
        if isinstance(value, dict):
            html += f"{indent}<div class=\"index-group\">\n"
            html += f"{indent}  <strong>{key}</strong><br/>\n"
            html += render_index_to_html(value, level + 1, path + "/" + key)
            html += f"{indent}</div>\n"
        else:
            html += f"{indent}  <div class=\"index-item\">&bull; <a href=\"{path}/{name}.html\">{name}</a></div>\n"

    return html

def build_handler(args: argparse.Namespace):
    os.makedirs(args.destination, exist_ok=True)

    if not os.path.exists(args.source) or not os.path.isdir(args.source):
        print(f"Directory does not exist: '{args.source}'")
        return 1

    # 1st step - collect all files
    files_dict, files_list = collect_files(args.source)
    
    # 2nd step - parse the files to strip out content and turn them
    # into HTML
    with tempfile.TemporaryDirectory() as tempdir:
        filtered_file_list, assets = parser.parse_and_strip(files_list, args.source, tempdir, args)

        # 3rd step - build a working static site
        environment = Environment(loader=FileSystemLoader(utils.relative_path("resources")))

        for file in filtered_file_list:
            new_file_path = os.path.join(args.destination, file)[:-2] + "html"
            generated_file_path = os.path.join(tempdir, file)[:-2] + "html"
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
            with open(new_file_path, "w") as new_file:
                with open(generated_file_path, "r") as generated_file:
                    new_file.write(html_for(
                        environment,
                        file,
                        generated_file.read(),
                        args
                    ))

        # Add index page
        template = environment.get_template("main_page_template.html")
        output = template.render(
            vault_name=args.site_name,
            stylesheet=args.styles,
            content=render_index_to_html(files_dict)
        )
        with open(os.path.join(args.destination, "index.html"), "w") as f:
            f.write(output)

        # Add search script
        js_path = os.path.join(args.destination, "js")
        os.makedirs(js_path, exist_ok=True)
        with open(utils.relative_path("resources/search_script.js"), "r") as source:
            with open(os.path.join(js_path, "search_script.js"), "w") as dest:
                dest.write(f"var pages = {json.dumps([file[:-3] for file in filtered_file_list], indent=4)};\n")
                dest.write(source.read())

        # Add styles
        styles_path = os.path.join(args.destination, "styles")
        os.makedirs(styles_path, exist_ok=True)
        shutil.copyfile(utils.relative_path("resources/default.css"), os.path.join(styles_path, "default.css"))

    return 0
