from pathlib import Path


class Vault:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root) if isinstance(root, str) else root

    def path_from_reference(self, reference: str) -> str | None:
        return None
