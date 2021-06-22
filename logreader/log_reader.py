#!/usr/bin/env python
"""Read selected log files.
Log files with issues are copied into
    DIR_PROCESSED_LOGS/{log file name}{timestamp}.log
Log files with issues have issues extracted and written to
    DIR_PROCESSED_LOGS/{log file name}{timestamp}_issues.log
"""

# TODO: Add line numbers for issue and copy files
# TODO: Write different logs to different directories in logs
# TODO: Add flags for:
#   -d directory containing log files
#   -f file containing logs
#   -k keywords (list strings?)
#   -o output destination
# TODO: Add docs for flags
import os
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


def _set_abs_log_file_paths(log_files):
    # Return updated list with absolute file paths for log files
    log_files_abs = []
    for i, file in enumerate(log_files):
        if Path(PATH_DIR_LOGS / file).is_file():
            log_files_abs.append(PATH_DIR_LOGS / file)
        else:
            print(f"Log file {file} will not be processed as not found")
    return log_files_abs


def _remove_nonexistent_files(files_logs_paths):
    # Return list without log files which cannot be found
    for log_file in files_logs_paths:
        if not log_file.is_file():
            print(f"Log file {log_file} does not exist. Removing from log "
                  f"reading")
            files_logs_paths.remove(log_file)
    return files_logs_paths


def _iterate_check_each_file(all_logfiles):
    # Routine to call functionality to check all logfiles for issues
    for file in all_logfiles:
        try:
            _check_logs_for_issues(file)
        except PermissionError:
            print(f"You require administrator privileges to access {file}")


def _check_logs_for_issues(file_to_read):
    # Find lines in log file matching issue keywords
    issues_found = {}
    logs_copy_made = False
    regex = re.compile(r"error|failed|warning", re.IGNORECASE)
    with open(file_to_read, "r") as file:
        for i, line in enumerate(file):
            cols = [col.strip() for col in line.split(":") if col]
            for col in cols:
                if regex.search(col) is not None:
                    if not logs_copy_made:
                        logs_copy_file = _write_log_file_copy(file_to_read)
                        logs_issues_file = \
                            _get_logs_issues_filename(logs_copy_file)
                        logs_copy_made = logs_copy_file is not None
                        print(f"\nIssues found in {file_to_read.name}:\n"
                              f"See {logs_copy_file} directory for logs copy\n"
                              f"See {logs_issues_file} directory for issues")
                    if col not in issues_found:
                        issues_found.update({col: 1})
                    else:
                        issues_found[col] += 1
    file.close()
    if issues_found:
        write_log_file_issues(logs_issues_file, issues_found)


def _write_log_file_copy(file_to_copy):
    # Create copy of passed log file
    time_stamp = _get_formatted_timestamp()
    filename = file_to_copy.name.replace(file_to_copy.suffix, "")
    dest_filename = f"{filename}_{time_stamp}{file_to_copy.suffix}"
    Path(DIR_PROCESSED_LOGS / dest_filename) \
        .write_text(Path(file_to_copy).read_text())
    return Path(DIR_PROCESSED_LOGS / dest_filename)


def _get_formatted_timestamp():
    # Return ISO8601-formatted timestamp for filenames
    time_stamp = datetime.now().isoformat()
    time_stamp = time_stamp.replace(":", "")
    return time_stamp[:time_stamp.index(".")]


def _get_logs_issues_filename(log_file_copy):
    # Return name for issues log file from copy of log file
    log_path = Path(log_file_copy)
    suffix = log_path.suffix
    issues_path = str(log_path).replace(f"{suffix}", "")
    issues_path = f"{issues_path}_issues{suffix}"
    return issues_path


def write_log_file_issues(logs_issues_file, issues_found):
    with open(logs_issues_file, "a") as file:
        for issue in issues_found:
            file.writelines(f"ISSUE (appeared {issues_found[issue]} times):\n"
                            f"  {issue}\n\n")
    file.close()


def _delete_logs_dir_if_empty():
    for _, _, files in os.walk(DIR_PROCESSED_LOGS):
        if not files:
            DIR_PROCESSED_LOGS.rmdir()


def main():
    """Routine responsible for handling log copying, issue extraction"""
    global FILES_LOGS_PATHS
    _create_logs_dir()
    FILES_LOGS_PATHS = _set_abs_log_file_paths(NAMES_FILES_LOGS)
    FILES_LOGS_PATHS = _remove_nonexistent_files(FILES_LOGS_PATHS)
    _iterate_check_each_file(FILES_LOGS_PATHS)
    _delete_logs_dir_if_empty()


main()
