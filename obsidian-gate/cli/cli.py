import argparse
from errno import EINVAL, ENOENT
from pathlib import Path
from sys import stderr
from typing import NoReturn

from .. import markdown, utils


def make_parser():
    parser = argparse.ArgumentParser(description="Obsidian Gate command-line utility")
    subparsers = parser.add_subparsers(title="subcommand", dest="command", required=True)

    parse_parser = subparsers.add_parser("parse", help="Parse the contents of a Markdown file in an Obsidian vault")
    parse_parser.add_argument("source", help="Path to your file")
    parse_parser.add_argument("--vault", help="Path to your vault's root directory")
    parse_parser.add_argument("--reference-prefix", help="A prefix to prepend to all wikilinks")
    parse_parser.set_defaults(func=cli_parse_command)

    build_parser = subparsers.add_parser("build", help="Parse the contents of a Markdown file in an Obsidian vault")
    build_parser.set_defaults(func=lambda _: None)

    return parser


def infer_vault_if_needed(args: argparse.Namespace) -> None:
    if not hasattr(args, "vault") or args.vault is not None:
        return
    
    # If no vault was specified but a source file was, find a vault from that root
    if hasattr(args, "source") and args.source is not None:
        args.vault = utils.find_vault(args.source)
    # Else, find a vault from the current working directory
    else:
        args.vault = utils.find_vault(".")


def ensure_vault(args: argparse.Namespace, message: str | None = None) -> bool:
    if not hasattr(args, "vault") or args.vault is None:
        print(message or "No vault was specified and none could be inferred (try using --vault)", file=stderr)
        return False
    return True


def cli_parse_command(args: argparse.Namespace) -> int:
    source_file = Path(args.source).resolve()
    if not source_file.exists() or not source_file.is_file():
        print(f"Not a file: {source_file!s}", file=stderr)
        return ENOENT
    
    if not ensure_vault(args):
        return EINVAL
    
    result = markdown.parser.parse_file(args.vault, source_file, args.reference_prefix)
    rendered = markdown.renderer.render(result)
    print(rendered)
    return 0


def main(args: argparse.Namespace) -> int:
    infer_vault_if_needed(args)
    return args.func(args)


def run() -> NoReturn:
    args = make_parser().parse_args()
    raise SystemExit(main(args))


if __name__ == "__main__":
    run()
