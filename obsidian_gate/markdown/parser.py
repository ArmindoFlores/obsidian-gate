from pathlib import Path

from markdown_it import MarkdownIt

from .plugins import wikilinks_plugin
from ..vault import Vault


def make_markdown_parser(vault: "Vault", reference_prefix: str | None) -> MarkdownIt:
    md = MarkdownIt("gfm-like2")
    md.use(wikilinks_plugin, vault, reference_prefix)
    return md


def make_markdown_parser_for_rendering() -> MarkdownIt:
    md = MarkdownIt("gfm-like2")
    md.use(wikilinks_plugin, None, None)
    return md


def parse_file(vault_root: str | Path, file: Path, reference_prefix: str | None = None) -> list[dict]:
    md = make_markdown_parser(Vault(vault_root), reference_prefix)
    return [
        dict(token.as_dict()) for token in md.parse(file.read_text())
    ]
