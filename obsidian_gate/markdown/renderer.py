from markdown_it.utils import OptionsDict
import typing
from markdown_it.token import Token

from .parser import make_markdown_parser_for_rendering


def render(data: list[dict]) -> str:
    tokens = [Token.from_dict(d) for d in data]
    return (make_markdown_parser_for_rendering()
        .renderer
        .render(tokens, typing.cast(OptionsDict, {}), {})
    )
