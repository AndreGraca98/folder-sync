# Synchronize two folders

Synchronize two folders: source and replica. Keep a full, identical copy of source folder at replica folder.

## Contents

- [Synchronize two folders](#synchronize-two-folders)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Usage](#usage)
  - [NOTE](#note)

## Requirements

Python>=3.9

## Usage

```bash
usage: main.py [-h] --src SRC --dst DST [--sync-interval SYNC_INTERVAL] [--log-path LOG_FILE] [--log-level LOG_LEVEL]

Syncronize files between two directories

optional arguments:
  -h, --help            show this help message and exit
  --src SRC             Source directory
  --dst DST             Destination directory
  --sync-interval SYNC_INTERVAL
                        Sync interval in seconds
  --log-path LOG_FILE, --log-file LOG_FILE
                        Log file path
  --log-level LOG_LEVEL
                        Log level
```

## NOTE

- Synchronization must be one-way: after the synchronization content of the
replica folder should be modified to exactly match content of the source
folder
- Synchronization should be performed periodically
- File creation/copying/removal operations should be logged to a file and to the
console output
- Folder paths, synchronization interval and log file path should be provided
using the command line arguments
- It is undesirable to use third-party libraries that implement folder
synchronization
- It is allowed (and recommended) to use external libraries implementing other
well-known algorithms. For example, there is no point in implementing yet
another function that calculates MD5 if you need it for the task – it is
perfectly acceptable to use a third-party (or built-in) library
