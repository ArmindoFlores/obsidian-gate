import re
import typing

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

    from markdown_it import MarkdownIt
    from markdown_it.renderer import RendererProtocol
    from markdown_it.rules_block import StateBlock
    from markdown_it.token import Token
    from markdown_it.utils import EnvType, OptionsDict

ADMONITION_TOKEN_NAME = "obsidian_admonition"
ADMONITION_DELIMITER_RE = re.compile(r"^>\s*\[!([a-zA-Z0-9_\-]+)\]\s*(.*)$")


def admonition_parser(state: "StateBlock", start_line: int, end_line: int, silent: bool) -> bool:
    start = state.bMarks[start_line] + state.tShift[start_line]
    maximum = state.eMarks[start_line]

    matched_delimiter = ADMONITION_DELIMITER_RE.match(state.src[start:maximum])
    if matched_delimiter is None:
        return False

    if silent:
        return True

    tag, title = matched_delimiter.groups()
    token = state.push(ADMONITION_TOKEN_NAME, "", 0)
    token.children = []
    token.meta = {
        "tag": tag,
        "title": title,
    }

    next_line = start_line + 1
    while next_line < end_line:
        line_content = state.src[state.bMarks[next_line]:state.eMarks[next_line]]
        if not line_content.startswith(">"):
            break
        token.children.extend(state.md.parseInline(line_content[1:].strip(), state.env))
        next_line += 1

    state.line = next_line
    return True


def render_admonition(self: "RendererProtocol", tokens: "Sequence[Token]", idx: int, options: "OptionsDict", env: "EnvType") -> str:
    token = tokens[idx]
    tag, title = token.meta["tag"], token.meta["title"]
    inner = self.render(token.children or [], options, env)
    return f'<div class="admonition admonition-tag-{tag}"><div class="admonition-header">{title}</div><div class="admonition-content">{inner}</div></div>'


def admonitions_plugin(md: "MarkdownIt") -> None:
    md.block.ruler.before("blockquote", "obsidian_admonition", admonition_parser)
    md.add_render_rule(ADMONITION_TOKEN_NAME, render_admonition)
