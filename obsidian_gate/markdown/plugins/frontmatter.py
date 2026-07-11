import typing

import yaml

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

    from markdown_it import MarkdownIt
    from markdown_it.renderer import RendererProtocol
    from markdown_it.token import Token
    from markdown_it.utils import EnvType, OptionsDict


def render_frontmatter(self: "RendererProtocol", tokens: "Sequence[Token]", idx: int, _options: "OptionsDict", env: "EnvType") -> str:
    token = tokens[idx]
    yaml_content = token.content
    try:
        frontmatter = yaml.safe_load(yaml_content)
        env["frontmatter"] = frontmatter
    except yaml.YAMLError:
        pass
    return ""


def frontmatter_rendering_plugin(md: "MarkdownIt") -> None:
    md.add_render_rule("front_matter", render_frontmatter)
