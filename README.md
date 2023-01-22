# Synchronize two folders

Synchronize two folders: source and replica. Keep a full, identical copy of source folder at replica folder.

## Contents

- [Synchronize two folders](#synchronize-two-folders)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Usage](#usage)
    - [1. Sync folders once](#1-sync-folders-once)
    - [2. Sync folders using a while loop](#2-sync-folders-using-a-while-loop)
    - [3. Sync folders using cronjobs](#3-sync-folders-using-cronjobs)
  - [NOTE](#note)

## Requirements

```bash
conda create -n myenv python=3.9 -y
conda activate myenv
pip install python-crontab # https://pypi.org/project/python-crontab/
```

## Usage

```bash
usage: main.py [-h] {cronjob,inf-loop,run-once} ...

Syncronize files between two directories

positional arguments:
  {cronjob,inf-loop,run-once}
    cronjob             Syncronize files between two directories using a cronjob
    inf-loop            Syncronize files between two directories using an infinite loop
    run-once            Syncronize files between two directories

options:
  -h, --help            show this help message and exit
```

### 1. Sync folders once

```bash
python main.py run-once --src /path/to/folder --dst /path/to/new/folder --log-file ./sync.log 
```

```bash
usage: main.py run-once [-h] --src SRC --dst DST [--log-path LOG_FILE] [--log-lvl LOG_LEVEL]

optional arguments:
  -h, --help            show this help message and exit
  --src SRC             Source directory
  --dst DST             Destination directory
  --log-path LOG_FILE, --log-file LOG_FILE
                        Log file path
  --log-lvl LOG_LEVEL, --log-level LOG_LEVEL
                        Log level
  -d, --dry-run         Dry run the syncronization
```

### 2. Sync folders using a while loop

```bash
python main.py inf-loop --src /path/to/folder --dst /path/to/new/folder --log-file ./sync.log --interval 3600 
```

```bash
usage: main.py inf-loop [-h] --src SRC --dst DST [--log-path LOG_FILE] [--log-lvl LOG_LEVEL] [--interval SYNC_INTERVAL]

optional arguments:
  -h, --help            show this help message and exit
  --src SRC             Source directory
  --dst DST             Destination directory
  --log-path LOG_FILE, --log-file LOG_FILE
                        Log file path
  --log-lvl LOG_LEVEL, --log-level LOG_LEVEL
                        Log level
  --interval SYNC_INTERVAL, --sync-interval SYNC_INTERVAL
                        Sync interval in seconds. Defaults to 3600 seconds.
  -d, --dry-run         Dry run the syncronization
```

### 3. Sync folders using cronjobs

```bash
python main.py cronjob --src /path/to/folder --dst /path/to/new/folder --log-file ./sync.log --interval "@hourly" 
```

```bash
usage: main.py cronjob [-h] --src SRC --dst DST [--log-path LOG_FILE] [--log-lvl LOG_LEVEL] [--interval SYNC_INTERVAL]

optional arguments:
  -h, --help            show this help message and exit
  --src SRC             Source directory
  --dst DST             Destination directory
  --log-path LOG_FILE, --log-file LOG_FILE
                        Log file path
  --log-lvl LOG_LEVEL, --log-level LOG_LEVEL
                        Log level
  --interval SYNC_INTERVAL, --sync-interval SYNC_INTERVAL
                        Sync interval in cron format. Defaults to @hourly.  
  -d, --dry-run         Dry run the syncronization
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
