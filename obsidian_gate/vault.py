from pathlib import Path


class Vault:
    def __init__(self, root: str | Path, excluded_directories: list[str] | None = None) -> None:
        self.root = (Path(root) if isinstance(root, str) else root).resolve()
        self.excluded_directories = excluded_directories or []
        self._listing = self._compute_listing()

    def _reduce_path(self, path: Path) -> tuple[str, ...]:
        return Path(str(path.resolve()).removeprefix(str(self.root))[1:]).parts

    def _filter_path(self, reduced_path: tuple[str, ...]) -> bool:
        for excluded_directory in self.excluded_directories:
            if excluded_directory in reduced_path:
                return False
        return True

    def _compute_listing(self) -> list[tuple[str, ...]]:
        return [reduced_path for reduced_path in [
            self._reduce_path(path) for path in self.root.rglob("*")
        ] if self._filter_path(reduced_path)]

    def path_from_reference(self, reference: str, is_image: bool = False) -> str | None:
        reference = reference if is_image else reference + ".md"
        reference_parts = Path(reference).parts
        for vault_file in self._listing:
            matches = True
            for component1, component2 in zip(reversed(reference_parts), reversed(vault_file), strict=False):
                if component1 != component2:
                    matches = False
                    break
            if matches:
                joined = "/".join(vault_file)
                return joined if is_image else joined[:-3]
        return None
