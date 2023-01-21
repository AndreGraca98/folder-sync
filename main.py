import argparse
import logging

from src import FolderSynchronizer, add_console_handler, set_log_cfg

rootLogger = logging.getLogger(__name__)


def get_parser():
    parser = argparse.ArgumentParser(
        description="Syncronize files between two directories"
    )
    parser.add_argument("--src", type=str, dest="src", help="Source directory")
    parser.add_argument("--dst", type=str, dest="dst", help="Destination directory")
    parser.add_argument("--sync-interval", type=int, help="Sync interval in seconds")
    parser.add_argument(
        "--log-path",
        "--log-file",
        type=str,
        dest="log_file",
        default="sync.log",
        help="Log file path",
    )
    parser.add_argument("--log-level", type=str, default="INFO", help="Log level")

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

    set_log_cfg(args.log_file, args.log_level)

    add_console_handler(rootLogger)

    synchronizer = FolderSynchronizer(args.src, args.dst)

    # print("files_to_create_on_dst: ", synchronizer.files_to_create_on_dst)
    # print("files_to_update_on_dst: ", synchronizer.files_to_update_on_dst)
    # print("files_to_remove_from_dst: ", synchronizer.files_to_remove_from_dst)

    synchronizer.sync()


if __name__ == "__main__":
    main()


# ENDFILE
