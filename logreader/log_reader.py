#!/usr/bin/env python
"""Read selected log files, copying those with failures and errors into
DIR_PROCESSED_LOGS/{log file name}.
Lines of interest are written to DIR_PROCESSED_LOGS/{log file name}_issues.log
"""

from pathlib import Path

DIR_PROCESSED_LOGS = Path("./logs")
DIR_LOGS = Path('/var/log')
LOG_FILES_WANTED = [Path("boot.log"), Path("messages"), Path("auth.log"),
                    Path("daemon.log"), Path("kern.log"), Path("some.nonsense")]
PATH_READ_LOGS = Path.cwd() / DIR_PROCESSED_LOGS


def _create_logs_dir():
    # Create dir for read logs if it doesn't exist.
    if not PATH_READ_LOGS.is_dir():
        Path(PATH_READ_LOGS).mkdir(parents=True, exist_ok=True)


def _remove_nonexistent_files(log_dir, log_files):
    # Remove non-existent files from logs to consider
    log_files_existing = log_files.copy()
    for log_file in log_files:
        if not Path(log_dir / log_file).is_file():
            print(f"Log file {log_file} does not exist. Removing from log "
                  f"reading")
            log_files_existing.remove(log_file)
    return log_files_existing


def main():
    global LOG_FILES_WANTED
    print(Path.cwd())
    _create_logs_dir()
    print(LOG_FILES_WANTED[1].name)
    LOG_FILES_WANTED = _remove_nonexistent_files(DIR_LOGS, LOG_FILES_WANTED)
    print(LOG_FILES_WANTED)


main()
