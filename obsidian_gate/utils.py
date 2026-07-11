from pathlib import Path


def find_vault(start: str | Path) -> Path | None:
    path = Path(start) if isinstance(start, str) else start
    while path.parent != path:
        if not path.is_file():
            obsidian_folder_path = path / ".obsidian"
            if obsidian_folder_path.exists() and obsidian_folder_path.is_dir():
                return path
        path = path.parent
    return None


def href_from_note_path(prefix: str | None, path: str) -> str:
    href = prefix or ""
    if not href.endswith("/") and not path.startswith("/"):
        href += "/"
    href += path
    return href
