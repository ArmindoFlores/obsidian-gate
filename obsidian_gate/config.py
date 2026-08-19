__all__ = [
    "DATABASE_DRIVER",
    "DATABASE_ENGINE",
    "DATABASE_HOST",
    "DATABASE_NAME",
    "DATABASE_PASSWORD",
    "DATABASE_PORT",
    "DATABASE_USERNAME",
]

import os
import typing

import dotenv

dotenv.load_dotenv()

@typing.overload
def _getenv[T](name: str, default: None) -> str | None: ...
@typing.overload
def _getenv[T](name: str) -> str: ...
@typing.overload
def _getenv[T](name: str, default: T) -> T | str: ...
def _getenv(name, *default):
    if len(default) == 0:
        return os.environ[f"OBSIDIAN_GATE_{name}"]
    if len(default) == 1:
        return os.getenv(f"OBSIDIAN_GATE_{name}", default[0])
    raise TypeError(f"_getenv() takes at most 2 arguments ({1+len(default)} given)")


DATABASE_NAME = _getenv("DATABASE_NAME", "vault")
DATABASE_USERNAME = _getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = _getenv("DATABASE_PASSWORD")
DATABASE_HOST = _getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = int(_getenv("DATABASE_PORT", "5432"))
DATABASE_ENGINE = _getenv("DATABASE_ENGINE", "postgresql")
DATABASE_DRIVER = _getenv("DATABASE_DRIVER", "psycopg")

SESSION_REDIS_URL = _getenv("SESSION_REDIS_URL", None)
