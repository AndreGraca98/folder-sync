#!/usr/bin/env python

import argparse
import logging
import os
import time
from pathlib import Path

from folder_sync import FolderSynchronizer, add_console_handler, set_log_cfg

rootLogger = logging.getLogger(__name__)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Syncronize files between two directories"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common_arguments(parser):
        parser.add_argument(
            "--src", type=str, dest="src", required=True, help="Source directory"
        )
        parser.add_argument(
            "--dst", type=str, dest="dst", required=True, help="Destination directory"
        )

        parser.add_argument(
            "--log-path",
            "--log-file",
            type=str,
            dest="log_file",
            default=str(Path(__file__).parent.resolve() / "sync.log"),
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
        parser.add_argument(
            "-d",
            "--dry",
            "--dry-run",
            action="store_true",
            dest="dry_run",
            help="Dry run the syncronization",
        )

        # parser.add_argument(
        #     "--exclude", type=str, help="Exclude files matching this pattern"
        # )

    cronparser = subparsers.add_parser(
        "cronjob", help="Syncronize files between two directories using a cronjob"
    )
    add_common_arguments(cronparser)
    cronparser.add_argument(
        "--interval",
        "--sync-interval",
        type=str,
        dest="sync_interval",
        default="@hourly",
        help="Sync interval in cron format. Defaults to @hourly.",
    )

    infloop_parser = subparsers.add_parser(
        "inf-loop",
        help="Syncronize files between two directories using an infinite loop",
    )
    add_common_arguments(infloop_parser)
    infloop_parser.add_argument(
        "--interval",
        "--sync-interval",
        type=int,
        default=60 * 60,
        dest="sync_interval",
        help="Sync interval in seconds. Defaults to 3600 seconds.",
    )

    run_once_parser = subparsers.add_parser(
        "run-once",
        help="Syncronize files between two directories ",
    )
    add_common_arguments(run_once_parser)

    return parser


def main(args: argparse.Namespace):
    synchronizer = FolderSynchronizer(args.src, args.dst)

    rootLogger.debug(f"src_files: {synchronizer.src_files}")
    rootLogger.debug(f"dst_files: {synchronizer.dst_files}")
    rootLogger.debug(f"files union: {synchronizer.src_files & synchronizer.dst_files}")

    rootLogger.debug(f"files_to_create_on_dst: {synchronizer.files_to_create_on_dst}")
    rootLogger.debug(f"files_to_update_on_dst: {synchronizer.files_to_update_on_dst}")
    rootLogger.debug(
        f"files_to_remove_from_dst: {synchronizer.files_to_remove_from_dst}"
    )
    if not args.dry_run:
        synchronizer.sync()


def run_once(args: argparse.Namespace) -> None:

    set_log_cfg(args.log_file, args.log_level.upper())

    add_console_handler(rootLogger)

    main(args)


def main_loop(args: argparse.Namespace) -> None:

    set_log_cfg(args.log_file, args.log_level.upper())

    add_console_handler(rootLogger)

    rootLogger.info("Starting periodic sync...")
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


def setup_cronjob(args: argparse.Namespace) -> None:
    from crontab import CronTab

    interval = args.sync_interval.strip(" ")
    if not interval.startswith("@") and len(interval.split(" ")) != 5:
        rootLogger.error(
            f"Aborting... Invalid interval format: {interval} . Must be in cron format. "
        )
        exit(1)

    # TODO: use different python version ??
    cmd = f"/usr/bin/python3 {__file__} run-once --src {args.src } --dst {args.dst} --log-file {Path(args.log_file).resolve()} --log-lvl {args.log_level.upper()} {'--dry-run' if args.dry_run else ''}"

    # Add cronjob
    cron = CronTab(user=os.getlogin())
    job = cron.new(command=cmd, comment=f"SYNC: SRC={args.src} , DST={args.dst}")
    job.setall(interval)
    cron.write()

    rootLogger.info(f"Cronjob added: {job}")


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    if args.command == "cronjob":
        setup_cronjob(args)
    elif args.command == "inf-loop":
        main_loop(args)
    elif args.command == "run-once":
        run_once(args)
    else:
        rootLogger("Invalid command...")
        parser.print_help()


# ENDFILE
