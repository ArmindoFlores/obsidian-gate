from markdown_it.token import Token

from .parser import make_markdown_parser_for_rendering


def render(data: list[dict]) -> str:
    tokens = [Token.from_dict(d) for d in data]
    md = make_markdown_parser_for_rendering()
    return md.renderer.render(tokens, md.options, {})
