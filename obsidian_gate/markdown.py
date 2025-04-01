__all__ = [
    "parser",
]

import os

import mistune
from mistune.renderers.html import HTMLRenderer
from mistune.plugins import (
    abbr,
    def_list,
    footnotes,
    formatting,
    math,
    ruby,
    spoiler,
    task_lists,
    table,
    url,
)

from . import utils


class ObsidianRenderer(HTMLRenderer):
    def __init__(self, files, extra_args):
        super().__init__()
        self.assets = []
        self.files = files
        self.extra_args = extra_args
        self.register("wikilink", self.render_wikilink)   

    def find(self, asset):
        for file in self.files:
            file_name = os.path.basename(file)
            if file_name == asset:
                return utils.strip_md_extension(file)

    def render_wikilink(self, _, raw):
        is_embed, target, label = raw["is_embed"], raw["target"], raw["label"]
        if is_embed or any(target.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".pdf"]):
            target_location = self.find(target)
            image_size = ""
            if label is not None:
                try:
                    size = int(label)
                    image_size = f'width="{size}"'
                except ValueError:
                    pass
            self.assets.append(target_location)
            return f'<img src="{"/missing.png" if target_location is None else "/" + target_location}" ' + (image_size) + '/>'
        
        target_location = self.find(target + ".md")
        if target_location is not None and self.extra_args.html_ext:
            target_location += ".html"

        return f'<a{" class=\"missing\"" if target_location is None else ""} href="{"#" if target_location is None else "/" + target_location}">{label}</a>'

def obsidian_plugin(md: mistune.Markdown):
    def parse_wikilink(_, m, state):
        raw = m.group("wikilink_content")
        is_embed = m.group("wikilink_tag").startswith("!")
        if "|" in raw:
            target, label = raw.split("|", 1)
        else:
            target = label = raw
        
        state.append_token({"type": "wikilink", "raw": {"target": target.strip(), "label": label.strip(), "is_embed": is_embed}})
        return m.end()

    def parse_comment(_, m, __):
        return m.end()

    # Register wikilink
    md.inline.register(
        "wikilink", 
        r"(?P<wikilink_tag>!?\[\[(?P<wikilink_content>.+?)\]\])",
        parse_wikilink,
        "link"
    )

    # Register multiline comment
    md.block.register(
        "comment", 
        r"(?P<comment_block>%%private%%(?P<comment_content>[\s\S]*?)%%/private%%)",
        parse_comment
    )

def get_renderer_and_parser(files, extra_args):
    renderer = ObsidianRenderer(files, extra_args)
    parser = mistune.Markdown(renderer=renderer)
    obsidian_plugin(parser)
    abbr.abbr(parser)
    def_list.def_list(parser)
    footnotes.footnotes(parser)
    formatting.strikethrough(parser)
    formatting.subscript(parser)
    formatting.superscript(parser)
    formatting.mark(parser)
    math.math(parser)
    ruby.ruby(parser)
    spoiler.spoiler(parser)
    task_lists.task_lists(parser)
    table.table(parser)
    url.url(parser)
    return renderer, parser

if __name__ == "__main__":
    # Example usage
    md = """
Here's a regular image: ![[image1.png]]

A link to a note: [[NoteName]]
A link with alias: [[Folder/Note2|Title]]

A standard image: ![Alt](pic.jpg)
An external link: [File](docs/file.pdf)

~~strikethrough~~
H~2~O should be formatted
This is a big number: 10^10^
==mark me==

%%private%%
This is a secret section.
With multiple lines!
%%/private%%
    """

    renderer, parser = get_renderer_and_parser({})
    html = parser(md)
    print("Assets found:", renderer.assets)
    print(html)
