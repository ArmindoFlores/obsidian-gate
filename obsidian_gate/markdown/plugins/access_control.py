import re
import typing

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

    from markdown_it import MarkdownIt
    from markdown_it.renderer import RendererProtocol
    from markdown_it.rules_block import StateBlock
    from markdown_it.rules_inline import StateInline
    from markdown_it.token import Token
    from markdown_it.utils import EnvType, OptionsDict

ACCESS_CONTROL_TOKEN_NAME = "private_section"
PRIVATE_DELIMITER_START = "%%private%%"
PRIVATE_DELIMITER_END = "%%/private%%"
PRIVATE_RE = re.compile(r"%%private%%(.*?)%%\/private%%", re.DOTALL)


def push_private_token(state: "StateInline | StateBlock", matched_content: str, inline: bool) -> "Token":
    token = state.push(ACCESS_CONTROL_TOKEN_NAME, "", 0)
    token.content = matched_content
    token.block = not inline
    token.children = (
        state.md.parseInline(token.content, state.env) if inline
        else state.md.parse(token.content, state.env)
    )
    return token


def private_inline_parser(state: "StateInline", silent: bool) -> bool:
    start = state.pos
    end = state.posMax
    
    # Minimum size of a wikilink: len("%%private%%%%/private%%") = 23
    if start + 23 > end:
        return False
    
    matched_content = PRIVATE_RE.match(state.src[start:])
    if matched_content is None:
        return False

    if not silent:
        push_private_token(state, matched_content.group(1), True)

    state.pos = start + matched_content.end()
    state.posMax = end
    return True


def private_block_parser(state: "StateBlock", start_line: int, end_line: int, silent: bool) -> bool:
    start = state.bMarks[start_line] + state.tShift[start_line]
    maximum = state.eMarks[start_line]
    if not state.src[start:maximum].startswith(PRIVATE_DELIMITER_START):
        return False

    matched_content = PRIVATE_RE.match(state.src[start:])
    if matched_content is None:
        return False

    if not silent:
        push_private_token(state, matched_content.group(1), False)

    next_line = start_line
    endpos = start + matched_content.end() - 1
    while next_line < end_line:
        if endpos >= state.bMarks[next_line] and endpos <= state.eMarks[next_line]:
            break
        next_line += 1

    state.line = next_line + 1
    return True


def render_inner(self: "RendererProtocol", tokens: "Sequence[Token] | None", options: "OptionsDict", env: "EnvType"):
    if tokens is None:
        return ""
    return self.render(tokens, options, env)


def render_private_section(self: "RendererProtocol", tokens: "Sequence[Token]", idx: int, options: "OptionsDict", env: "EnvType") -> str:
    token = tokens[idx]
    if "access_controller" not in options:
        return render_inner(self, token.children, options, env)
    ac = options["access_controller"]
    if ac.can_view(token):
        return render_inner(self, token.children, options, env)
    return ""


def access_control_plugin(md: "MarkdownIt") -> None:
    md.inline.ruler.before("text", "private_inline", private_inline_parser)
    md.block.ruler.after("code", "private_block", private_block_parser)
    md.add_render_rule(ACCESS_CONTROL_TOKEN_NAME, render_private_section)
