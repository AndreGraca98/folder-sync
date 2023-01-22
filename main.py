import argparse
import logging
import time
from pathlib import Path

from src import FolderSynchronizer, add_console_handler, set_log_cfg

rootLogger = logging.getLogger(__name__)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Syncronize files between two directories"
    )
    parser.add_argument(
        "--src", type=str, dest="src", required=True, help="Source directory"
    )
    parser.add_argument(
        "--dst", type=str, dest="dst", required=True, help="Destination directory"
    )
    parser.add_argument(
        "--interval",
        "--sync-interval",
        type=int,
        default=60 * 60,
        dest="sync_interval",
        help="Sync interval in seconds. Defaults to 1 hour.",
    )

    parser.add_argument(
        "--log-path",
        "--log-file",
        type=str,
        dest="log_file",
        default=str(Path(__file__).parent / "sync.log"),
        help="Log file path",
    )
    parser.add_argument(
        "--log-lvl",
        "--log-level",
        type=str,
        dest="log_level",
        default="INFO",
        help="Log level",
    )

    # parser.add_argument(
    #     "--exclude", type=str, help="Exclude files matching this pattern"
    # )
    # parser.add_argument(
    #     "--dry-run", action="store_true", help="Dry run the syncronization"
    # )

    return parser


def main(args: argparse.Namespace):
    synchronizer = FolderSynchronizer(args.src, args.dst)

    rootLogger.debug(f"files_to_create_on_dst: {synchronizer.files_to_create_on_dst}")
    rootLogger.debug(f"files_to_update_on_dst: {synchronizer.files_to_update_on_dst}")
    rootLogger.debug(
        f"files_to_remove_from_dst: {synchronizer.files_to_remove_from_dst}"
    )

    synchronizer.sync()


def main_loop():
    parser = get_parser()
    args = parser.parse_args()

    set_log_cfg(args.log_file, args.log_level)

    add_console_handler(rootLogger)

    while True:
        try:
            main(args)
            time.sleep(args.sync_interval)
        except KeyboardInterrupt:
            rootLogger.info("Stoping periodic sync...")
            break
        except Exception as e:
            rootLogger.error(f"{e}")
            break


def setup_cronjob():
    pass


if __name__ == "__main__":
    main_loop()


# ENDFILE
