import argparse
import sys

from . import build


def get_parser():
    parser = argparse.ArgumentParser(
        description="Transform your Obsidian vault into a website"
    )
    subparsers = parser.add_subparsers(title="subcommands", dest="command", required=True)

    # Build subcommand
    build_parser = subparsers.add_parser("build", help="Build static site from vault contents")
    build_parser.add_argument("source", help="Path to your vault")
    build_parser.add_argument("destination", help="Directory to store the static site files")
    build_parser.add_argument("--styles", "-S", help="A CSS file to style the website")
    build_parser.add_argument("--site-name", "-N", default="Vault", help="A name for this website")
    build_parser.add_argument("--html-ext", action="store_true", help="Whether to append '.html' to relative links")
    build_parser.set_defaults(func=build.build_handler)

    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    sys.exit(args.func(args))

if __name__ == "__main__":
    main()
