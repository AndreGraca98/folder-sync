import argparse
import logging

from src.log import add_console_handler, set_log_cfg
from src.sync import hello

rootLogger = logging.getLogger(__name__)


def get_parser():
    parser = argparse.ArgumentParser(
        description="Syncronize files between two directories"
    )
    parser.add_argument("--src", type=str, help="Source directory")
    parser.add_argument("--dst", type=str, help="Destination directory")
    parser.add_argument("--sync-interval", type=int, help="Sync interval in seconds")
    parser.add_argument(
        "--log-path",
        "--log-file",
        type=str,
        dest="log_file",
        default="sync.log",
        help="Log file path",
    )
    parser.add_argument("--log-level", type=str, default="DEBUG", help="Log level")

    parser.add_argument(
        "--exclude", type=str, help="Exclude files matching this pattern"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Dry run the syncronization"
    )

    return parser


def main():

    parser = get_parser()
    args = parser.parse_args()
    print(args)

    set_log_cfg(args.log_file, args.log_level)

    add_console_handler(rootLogger)

    rootLogger.info("Hello world from main")
    rootLogger.debug("DEBUG from main")

    hello()

    rootLogger.info("after hello from main")


if __name__ == "__main__":
    main()


# ENDFILE
