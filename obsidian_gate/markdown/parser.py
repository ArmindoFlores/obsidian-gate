import typing
from pathlib import Path

from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin

from obsidian_gate.access_control import AccessController
from obsidian_gate.markdown.plugins import (
    access_control_plugin,
    admonitions_plugin,
    frontmatter_rendering_plugin,
    wikilinks_plugin,
)
from obsidian_gate.vault import Vault


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


def parse_file(vault_root: str | Path | Vault, file: Path, reference_prefix: str | None = None) -> list[dict]:
    vault = vault_root if isinstance(vault_root, Vault) else Vault(vault_root)
    md = make_markdown_parser(vault, reference_prefix)
    return [
        dict(token.as_dict()) for token in md.parse(file.read_text())
    ]


def parse_files(vault_root: str | Path | Vault, files: list[Path], reference_prefix: str | None = None) -> dict[str, list[dict]]:
    vault = vault_root if isinstance(vault_root, Vault) else Vault(vault_root)
    md = make_markdown_parser(vault, reference_prefix)
    return {
        str(file): [
            dict(token.as_dict()) for token in md.parse(file.read_text())
        ] for file in files
    }
