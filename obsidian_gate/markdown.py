__all__ = [
    "ObsidianRenderer",
    "obsidian_plugin",
]

import re

import mistune
from mistune.renderers.html import HTMLRenderer
from mistune.inline_parser import InlineParser


class ObsidianRenderer(HTMLRenderer):
    def __init__(self):
        super().__init__()
        self.assets = []
        self.register("wikilink", self.render_wikilink)

    # def render_wikilink(self, target, label, is_embed):
    def render_wikilink(self, _, raw):
        is_embed, target, label = raw["is_embed"], raw["target"], raw["label"]
        if is_embed or any(target.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".pdf"]):
            self.assets.append(target)
        return f'<a href="{target}">{label}</a>'

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

# Set up markdown parser
renderer = ObsidianRenderer()
markdown = mistune.Markdown(renderer=renderer)
obsidian_plugin(markdown)

# Example usage
md = """
Here's a regular image: ![[image1.png]]

A link to a note: [[NoteName]]
A link with alias: [[Folder/Note2|Title]]

A standard image: ![Alt](pic.jpg)
An external link: [File](docs/file.pdf)

%%private%%
This is a secret section.
With multiple lines!
%%/private%%
"""

html = markdown(md)
print("Assets found:", renderer.assets)
print(html)
