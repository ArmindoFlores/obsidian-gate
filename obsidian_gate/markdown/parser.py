from pathlib import Path
import typing

from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin

from .plugins import (
    access_control_plugin,
    frontmatter_rendering_plugin,
    wikilinks_plugin,
    admonitions_plugin,
)
from ..access_control import AccessController
from ..vault import Vault


def make_markdown_parser(vault: "Vault", reference_prefix: str | None, extra_options: dict[str, typing.Any] | None = None) -> MarkdownIt:
    md = MarkdownIt("gfm-like2", options_update=extra_options)
    md.use(access_control_plugin)
    md.use(wikilinks_plugin, vault, reference_prefix)
    md.use(front_matter_plugin)
    md.use(admonitions_plugin)
    md.use(frontmatter_rendering_plugin)
    md.use(footnote_plugin)
    return md


def make_markdown_parser_for_rendering() -> MarkdownIt:
    return make_markdown_parser(
        None,  # ty:ignore[invalid-argument-type]
        None,
        {"access_controller": AccessController()}
    )


def parse_file(vault_root: str | Path, file: Path, reference_prefix: str | None = None) -> list[dict]:
    md = make_markdown_parser(Vault(vault_root), reference_prefix)
    return [
        dict(token.as_dict()) for token in md.parse(file.read_text())
    ]
