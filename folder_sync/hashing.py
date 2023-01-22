import hashlib
import logging
from pathlib import Path
from typing import Union

from _hashlib import HASH  # For typehints

from .log import add_console_handler

hashLogger = logging.getLogger(__name__)
add_console_handler(hashLogger)

__all__ = ["hash_dir", "hash_file", "hash_path"]


def updt_hash_file(file: Union[str, Path], _hash: HASH) -> HASH:
    file = Path(file)
    if not Path(file).is_file():
        hashLogger.error(f"{file} is not a file")
        return _hash

    _hash.update(file.name.encode())

    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            _hash.update(chunk)

    return _hash


def updt_hash_dir(directory: Union[str, Path], _hash: HASH) -> HASH:
    directory = Path(directory)
    if not directory.is_dir():
        hashLogger.error(f"{directory} is not a directory")
        return _hash

    for path in sorted(directory.iterdir(), key=lambda p: str(p).lower()):
        if path.is_file():
            _hash = updt_hash_file(path, _hash)

        elif path.is_dir():
            _hash.update(path.name.encode())
            _hash = updt_hash_dir(path, _hash)

    return _hash


def hash_dir(directory: Union[str, Path]):
    return updt_hash_dir(directory, hashlib.md5()).hexdigest()


def hash_file(file: Union[str, Path]):
    return updt_hash_file(file, hashlib.md5()).hexdigest()


def hash_path(path: Union[str, Path]):
    if Path(path).is_dir():
        return hash_dir(path)

    if Path(path).is_file():
        return hash_file(path)

    hashLogger.error(f"{path} is not a file or directory")
    raise ValueError(f"{path} is not a file or directory")


# ENDFILE
