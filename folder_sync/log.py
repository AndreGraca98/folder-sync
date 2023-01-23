import logging
from pathlib import Path
from typing import Union

__all__ = ["add_console_handler", "set_log_cfg", "fmt"]
fmt = (
    "%(asctime)s : %(levelname)s : %(name)s::%(funcName)s::line%(lineno)d : %(message)s"
)

# "%(asctime)s : %(levelname)s ::line%(lineno)d : %(message)s"
# "%(asctime)s : %(levelname)s : %(funcName)s::line%(lineno)d : %(message)s"


def add_console_handler(logger):
    consoleHandler = logging.StreamHandler()
    logFormatter = logging.Formatter(fmt)
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)


def set_log_cfg(log_file: Union[str, Path], log_level: str):
    # Create directory if it does not exist
    log_file = Path(log_file).resolve()
    if log_file.is_dir():
        log_file = log_file / ".folders_sync.log"

    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=str(log_file),
        filemode="a",
        level=log_level,
        format=fmt,
    )

    print(f"Logging to {log_file} ...")
    # logging.getLogger().info(f"Logging to {log_file}")


# ENDFILE
