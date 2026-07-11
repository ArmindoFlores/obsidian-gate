import typing

if typing.TYPE_CHECKING:
    from markdown_it.token import Token


class AccessController:
    def __init__(self) -> None:
        pass

    def can_view(self, token: "Token") -> bool:
        return False
