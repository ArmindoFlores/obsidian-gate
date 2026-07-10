from collections.abc import Sequence
import dataclasses
import re
import typing

from markdown_it.common.utils import escapeHtml

if typing.TYPE_CHECKING:
    from markdown_it import MarkdownIt
    from markdown_it.renderer import RendererProtocol
    from markdown_it.rules_inline import StateInline
    from markdown_it.token import Token
    from markdown_it.utils import EnvType, OptionsDict

    from utils import href_from_note_path
    from vault import Vault

WIKILINK_RE = re.compile(r"\[\[([^\|]*?)(\|.+?)?\]\]")
WIKILINK_RULE_NAME = "wikilink"


@dataclasses.dataclass
class Wikilink:
    src: str
    length: int
    reference: str
    display_name: str | None
    exists: bool

    def parse(vault: "Vault", src: str, start: int = 0, reference_prefix: str | None = None) -> "Wikilink | None":
        m = WIKILINK_RE.match(src[start:])
        if m is None:
            return None

        end = start + m.span()[1]
        start = start + m.span()[0]
        reference_str = m.group(1)
        display_name = m.group(2)
        
        path = vault.path_from_reference(reference_str)
        if path is None:
            reference = "#"
        else:
            reference = href_from_note_path(reference_prefix, path)

        return Wikilink(
            src[start:end],
            end - start,
            reference,
            display_name,
            path is not None,
        )

def make_wikilinks_parser(vault: "Vault", reference_prefix: str | None):
    def wikilink(state: "StateInline", silent: bool) -> bool:
        """Process wikilinks ([[...]])"""
        start = state.pos
        end = state.posMax
        
        # Minimum size of a wikilink: len("[[x]]") = 5
        if start + 5 > end:
            return False
        
        parsed_wikilink = Wikilink.parse(vault, state.src, start, reference_prefix)
        if parsed_wikilink is None:
            return False

        if not silent:
            token = state.push(WIKILINK_RULE_NAME, "", 0)
            token.meta = {
                "reference": parsed_wikilink.reference,
                "display_name": parsed_wikilink.display_name,
                "missing": not parsed_wikilink.exists
            }

        state.pos = start + parsed_wikilink.length
        state.posMax = end
        return True
    return wikilink


def render_wikilink(self: "RendererProtocol", tokens: "Sequence[Token]", idx: int, options: "OptionsDict", env: "EnvType") -> str:
    token = tokens[idx]
    reference = token.meta["reference"]
    display_name = token.meta["display_name"] or reference
    missing = token.meta["missing"]
    return f'<a class="wikilink{" missing" if missing else ""}" href="{reference}">{escapeHtml(display_name)}</a>'


def wikilinks_plugin(md: "MarkdownIt", vault: "Vault", reference_prefix: str | None = None) -> None:
    md.inline.ruler.before("link", WIKILINK_RULE_NAME, make_wikilinks_parser(vault, reference_prefix))
    md.add_render_rule(WIKILINK_RULE_NAME, render_wikilink)
