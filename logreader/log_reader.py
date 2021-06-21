#!/usr/bin/env python
"""Read selected log files.
Log files with issues are copied into
    DIR_PROCESSED_LOGS/{log file name}{timestamp}.log
Log files with issues have issues extracted and written to
    DIR_PROCESSED_LOGS/{log file name}{timestamp}_issues.log
"""

# TODO: Add error handling for IO operations
# TODO: Replace multiple instances of issues with counts instead
# TODO: Add line numbers for issue and copy files
# TODO: Place each log file's copy, issues files in separate dir

from pathlib import Path
from datetime import datetime
import re

# Constants
DIR_PROCESSED_LOGS = Path("./logs")
NAMES_FILES_LOGS = ["boot.log", "messages", "auth.log", "daemon.log",
                    "kern.log", "some.nonsense"]
PATH_DIR_LOGS = Path('/var/log')
PATH_READ_LOGS = Path.cwd() / DIR_PROCESSED_LOGS

# Globals
FILES_LOGS_PATHS = []


def _create_logs_dir():
    # Create sibling dir to store processed log files if it doesn't exist
    if not PATH_READ_LOGS.is_dir():
        Path(PATH_READ_LOGS).mkdir(parents=True, exist_ok=True)


def _remove_nonexistent_files(log_dir, log_files):
    # Return updated list with non-existent log files removed
    log_files_existing = log_files.copy()
    for log_file in log_files:
        if not Path(log_dir / log_file).is_file():
            print(f"Log file {log_file} does not exist. Removing from log "
                  f"reading")
            log_files_existing.remove(log_file)
    return log_files_existing


def _set_abs_log_file_paths(log_files):
    # Return updated list with absolute file paths for log files
    log_files_abs = []
    for i, file in enumerate(log_files):
        if Path(PATH_DIR_LOGS / file).is_file():
            log_files_abs.append(PATH_DIR_LOGS / file)
        else:
            print(f"Log file {file} will not be processed as not found")
    return log_files_abs


def _check_logfiles_for_issues(all_logfiles):
    # Routine to call functionality to check all logfiles for issues
    for file in all_logfiles:
        _check_logfile_for_issues(file)


# TODO: Add error-handling
def _check_logfile_for_issues(file_to_read):
    # Find lines in log file matching issue keywords
    logs_copy_made = False
    logs_issues_file = ""
    regex = re.compile(r"error|failed|warning", re.IGNORECASE)

    with open(file_to_read, "r") as file:
        for line in file:
            cols = [col.strip() for col in line.split(":") if col]
            for col in cols:
                if regex.search(col) is not None:
                    if not logs_copy_made:
                        logs_copy_file = _create_log_file_copy(file_to_read)
                        logs_issues_file = _get_logs_issues_filename(logs_copy_file)
                        logs_copy_made = logs_copy_file is not None
                        print(f"Issues found in {file_to_read.name}:\n"
                              f"See {logs_copy_file} directory for logs copy\n"
                              f"See {logs_issues_file} directory for issues")
                    _write_line_to_file(logs_issues_file, col)
                    # print(f"write \n{col}\nto\n{logs_issues_file}")
    file.close()


def _get_formatted_timestamp():
    # Return ISO8601-formatted timestamp for filenames
    time_stamp = datetime.now().isoformat()
    time_stamp = time_stamp.replace(":", "")
    return time_stamp[:time_stamp.index(".")]


def _get_filenames(file_to_create_for, time_stamp):
    # Return name for log copy, extracted log line files
    filename = file_to_create_for.name.replace(file_to_create_for.suffix, "")
    extracted_log_filename = \
        f"{filename}_extracts_{time_stamp}{file_to_create_for.suffix}"
    copy_log_filename = \
        f"{filename}_{time_stamp}{file_to_create_for.suffix}"

    return copy_log_filename, extracted_log_filename


# TODO: Include error handling for file-creation
def _create_log_file_copy(file_to_copy):
    # Create copy of passed log file
    time_stamp = _get_formatted_timestamp()
    filename = file_to_copy.name.replace(file_to_copy.suffix, "")
    dest_filename = f"{filename}_{time_stamp}{file_to_copy.suffix}"
    print(f"CREATE FILE AT {dest_filename}")
    Path(DIR_PROCESSED_LOGS / dest_filename).write_text(Path(file_to_copy).read_text())
    return Path(DIR_PROCESSED_LOGS / dest_filename)


def _get_logs_issues_filename(log_file_copy):
    # Return name for issues log file from copy of log file
    log_path = Path(log_file_copy)
    suffix = log_path.suffix
    issues_path = str(log_path).replace(f"{suffix}", "")
    issues_path = f"{issues_path}_issues{suffix}"
    return issues_path


def _write_line_to_file(file_to_write, line):
    # Write lines to specified file
    with open(file_to_write, "a") as file:
        file.writelines(f"{line}\n")
    file.close()


def main():
    """"Main routine to handle all log reading, writing functionality"""
    global FILES_LOGS_PATHS
    _create_logs_dir()
    FILES_LOGS_PATHS = _set_abs_log_file_paths(NAMES_FILES_LOGS)
    _check_logfiles_for_issues(FILES_LOGS_PATHS)


main()
