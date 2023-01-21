import logging

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


def set_log_cfg(log_file: str, log_level: str):
    logging.basicConfig(
        filename=log_file,
        filemode="w",
        level=log_level,
        format=fmt,
    )


# ENDFILE
