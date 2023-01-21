import logging
from pathlib import Path

from .log import add_console_handler

syncLogger = logging.getLogger(__name__)
add_console_handler(syncLogger)


def hello():
    syncLogger.info("Hello world")
    syncLogger.warning("WARNING")


def get_files(path: str):
    return Path(path).rglob("*")


# ENDFILE
