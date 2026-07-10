from markdown_it.token import Token

from .parser import make_markdown_parser


def render(data: list[dict]) -> str:
    tokens = [Token.from_dict(d) for d in data]
    return make_markdown_parser(None, None).renderer.render(tokens, {}, {})
