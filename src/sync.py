import logging
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Union

from .log import add_console_handler

syncLogger = logging.getLogger(__name__)
add_console_handler(syncLogger)

__all__ = ["FolderSynchronizer"]


def remove(path: Union[str, Path]) -> None:
    path = Path(path)

    if not path.exists():
        syncLogger.error(f"{path} does not exist")
        return

    if path.is_dir():
        # shutil.rmtree(str(path))  # remove directory and all its contents
        try:
            path.rmdir()  # only works if directory is empty
            syncLogger.info(f"Removed directory: {path}")
        except OSError:
            syncLogger.warn(f"Directory {path} is not empty. Removing contents first")
            # directory is not empty
            for p in path.iterdir():
                remove(p)  # recursively remove all files and directories in path
            remove(path)  # remove dir itself
            syncLogger.info(f"Removed directory: {path}")

        except Exception as e:
            syncLogger.error(f"Could not remove directory: {path}\n{e}")

    elif path.is_file() or path.is_symlink():
        path.unlink()  # missing_ok=True
        syncLogger.info(f"Removed file: {path}")

    else:
        syncLogger.error(f"{path} is not a file, directory or symlink")


def remove_paths(dst_dir: Union[str, Path], paths: Iterable[Union[str, Path]]) -> None:
    # Sort paths by length of path, i.e. files before directories
    for p in sorted(paths, key=lambda x: len(Path(x).parts), reverse=True):
        remove(Path(dst_dir) / p)


def copy(src_path: Union[str, Path], dst_path: Union[str, Path]) -> None:
    src_path = Path(src_path)
    dst_path = Path(dst_path)

    if not src_path.exists():
        syncLogger.error(f"{src_path} does not exist")
        return

    if src_path == dst_path:
        syncLogger.warn(f"Source path is the same as destination path: {src_path}")
        return

    if src_path.is_dir():
        try:
            dst_path.mkdir()  # create directory :: parents=True, exist_ok=True
            syncLogger.info(f"Created directory {dst_path}")
        except FileExistsError:
            syncLogger.warn(f"Directory {dst_path} already exists")
        except Exception as e:
            syncLogger.warn(f"{e}")

        # shutil.copytree(str(src_path), str(dst_path), symlinks=True,  ignore=shutil.ignore_patterns(''), dirs_exist_ok=True) # copies directory and all its contents

    elif src_path.is_file() or src_path.is_symlink():
        # If path is a symlink copy the link and not the contents
        # Use shutil.copy instead of shutil.copy2 to avoid copying the files metadata such as the created/modified time
        shutil.copy(str(src_path), str(dst_path), follow_symlinks=False)
        syncLogger.info(f"Copied file: {dst_path}")

    else:
        syncLogger.error(f"{src_path} is not a file, directory or symlink")


def copy_paths(
    src_dir: Union[str, Path],
    dst_dir: Union[str, Path],
    paths: Iterable[Union[str, Path]],
) -> None:
    # TODO: sorting of paths
    for p in sorted(paths, key=lambda x: len(Path(x).parts), reverse=False):
        copy(Path(src_dir) / p, Path(dst_dir) / p)


def get_mtime(path: Union[str, Path]):
    """get modified time of path"""
    # TODO: deal with different platforms
    return os.stat(str(path)).st_mtime


@dataclass
class FolderSynchronizer:
    src_dir: Path
    dst_dir: Path

    def __init__(self, src_dir: Union[str, Path], dst_dir: Union[str, Path]) -> None:
        self.src_dir = Path(src_dir).resolve()
        if not self.src_dir.is_dir():
            syncLogger.error(f"{src_dir} is not a valid directory")
            exit(1)

        self.dst_dir = Path(dst_dir).resolve()
        self.dst_dir.mkdir(parents=True, exist_ok=True)

        # Match all files and folders except '.'
        self.src_files = set(
            map(lambda x: x.relative_to(src_dir), Path(src_dir).rglob("*"))
        ) | set(map(lambda x: x.relative_to(src_dir), Path(src_dir).rglob("**/[!.]")))

        self.dst_files = set(
            map(lambda x: x.relative_to(dst_dir), Path(dst_dir).rglob("*"))
        ) | set(map(lambda x: x.relative_to(dst_dir), Path(dst_dir).rglob("**/[!.]")))

        self.files_to_create_on_dst = self.src_files - self.dst_files
        self.files_to_remove_from_dst = self.dst_files - self.src_files
        self.files_to_update_on_dst = (
            self.get_files_to_update_on_dst() - self.files_to_create_on_dst
        )

    def get_files_to_update_on_dst(self) -> None:

        files_to_update_on_dst = set()
        for src_p, dst_p in zip(self.src_files, self.dst_files):
            # If the modified time of the source file is newer than the destination file add it to the list of files to update
            # FIXME: sometimes the time changes by 1 second, so the file is copied again
            if get_mtime(self.dst_dir / dst_p) - get_mtime(self.src_dir / src_p) < 0:
                files_to_update_on_dst.add(src_p)

        return files_to_update_on_dst

    def sync(self) -> None:
        syncLogger.info(f"STARTING SYNC {self.src_dir} to {self.dst_dir}")
        remove_paths(self.dst_dir, self.files_to_remove_from_dst)
        copy_paths(self.src_dir, self.dst_dir, self.files_to_create_on_dst)
        copy_paths(self.src_dir, self.dst_dir, self.files_to_update_on_dst)
        syncLogger.info(f"FINISHED SYNC {self.src_dir} to {self.dst_dir}")


# ENDFILE
