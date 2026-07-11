from pathlib import Path

from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin

from .plugins import wikilinks_plugin
from .plugins.frontmatter import frontmatter_rendering_plugin
from ..vault import Vault


def make_markdown_parser(vault: "Vault", reference_prefix: str | None) -> MarkdownIt:
    md = MarkdownIt("gfm-like2")
    md.use(wikilinks_plugin, vault, reference_prefix)
    md.use(front_matter_plugin)
    md.use(frontmatter_rendering_plugin)
    md.use(footnote_plugin)
    return md


def make_markdown_parser_for_rendering() -> MarkdownIt:
    return make_markdown_parser(None, None)  # ty:ignore[invalid-argument-type]


def parse_file(vault_root: str | Path, file: Path, reference_prefix: str | None = None) -> list[dict]:
    md = make_markdown_parser(Vault(vault_root), reference_prefix)
    return [
        dict(token.as_dict()) for token in md.parse(file.read_text())
    ]
