#!/usr/bin/env python
"""Read selected log files, writing copy and found issues in ./logs if issues
found. See the first example for default (no flags) behaviour.

Files to parse, directories for files, and issues to look for can be set by
passing flags (-f, -d, -k respectively).

Examples:
    `python3 log_reader.py` checks boot.log, messages, auth.log, daemon.log,
    kern.log in /var/log for mentions of "error", "failed", "warning",
    case-insensitive

    `python3 log_reader.py -f boot.log -k error` checks boot.log in /var/log for
    mentions of "error", case-insensitive

    `python3 log_reader.py -d /example -f boot.log,test.log -k error,warning`
    checks boot.log and test.log in /example for mentions of "error" and
    "warning", case-insensitive
"""

import argparse
import os
from pathlib import Path
from datetime import datetime
import re

# Global constants: general
NONE = "NONE"
DIR_DEST = Path("./logs")


# Global variables: based on flags
DIR_SOURCE = Path(NONE)
DIR_SOURCE_NONE = Path(NONE)
DIR_SOURCE_ARG = DIR_SOURCE_NONE
DIR_SOURCE_DEFAULT = Path('/var/log')
NAMES_FILES_TO_PARSE = []
NAMES_FILES_TO_PARSE_ARG = NONE
ISSUES_ARG = NONE
ISSUES_ARG_DEFAULT = r"error|failed|warning"
ISSUES_REGEX = re.compile(ISSUES_ARG_DEFAULT, re.IGNORECASE)

# Global variables: general
NAMES_FILES_TO_PARSE_DEFAULT = ["boot.log", "messages", "auth.log",
                                "daemon.log", "kern.log"]
FILES_LOGS_PATHS = []
SUFFIXES_ACCEPTED = [".log", ".txt"]

"""Setup"""


def get_flag_arguments():
    global DIR_SOURCE_ARG
    global NAMES_FILES_TO_PARSE_ARG
    global ISSUES_ARG

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str,
                        help="directory in which to parse all files found")
    parser.add_argument("-f", "--files", type=str,
                        help="files in directory to parse for log issues, "
                             "comma-separated")
    parser.add_argument("-k", "--keyword", type=str,
                        help="issue keywords to find in files to parse, "
                             "comma-separated")
    args = parser.parse_args()
    if args.directory:
        DIR_SOURCE_ARG = Path(args.directory)
    if args.files:
        NAMES_FILES_TO_PARSE_ARG = args.files
    if args.keyword:
        ISSUES_ARG = args.keyword


def _set_source_dir():
    # Set source log directory based on whether flag provided
    global DIR_SOURCE
    global DIR_SOURCE_DEFAULT

    if DIR_SOURCE_ARG is not DIR_SOURCE_NONE:
        # Set source directory based on user input flag
        DIR_SOURCE = Path(DIR_SOURCE_ARG)
    else:
        # Set source directory as default
        DIR_SOURCE = DIR_SOURCE_DEFAULT


def _set_issue_keywords():
    # Set issues keyword regex based on whether flag provided
    global ISSUES_ARG
    global ISSUES_REGEX
    global NONE

    # Replace default issue keywords of logs with user selected
    if ISSUES_ARG is not NONE:
        issues_keywords_list = get_list_from_comma_separated_string(ISSUES_ARG)
        issues_keywords_list = [keyword for keyword in issues_keywords_list
                                if keyword]
        issues_keywords = r"|".join(issues_keywords_list)
        ISSUES_REGEX = re.compile(issues_keywords, re.IGNORECASE)


def _set_files_to_parse():
    # Set files to parse based on whether file, dir, flags provided
    global NAMES_FILES_TO_PARSE
    global NAMES_FILES_TO_PARSE_ARG
    global NONE

    if NAMES_FILES_TO_PARSE_ARG is not NONE:
        files_list = \
            get_list_from_comma_separated_string(NAMES_FILES_TO_PARSE_ARG)
        NAMES_FILES_TO_PARSE = files_list
    elif DIR_SOURCE_ARG is not NONE:
        set_files_from_user_dir()
    else:
        NAMES_FILES_TO_PARSE = NAMES_FILES_TO_PARSE_DEFAULT


def set_files_from_user_dir():
    # Get all files to parse from directory from user input flag
    global DIR_SOURCE
    global NAMES_FILES_TO_PARSE
    global SUFFIXES_ACCEPTED

    path_source = Path(DIR_SOURCE).glob('*/')

    for file in path_source:
        if file.is_file() and file.suffix in SUFFIXES_ACCEPTED and \
                NAMES_FILES_TO_PARSE_ARG is NONE:
            NAMES_FILES_TO_PARSE.append(file.name)


def _create_dest_dir(dir_path):
    # Create sibling dir to store processed log files if it doesn't exist
    if not dir_path.is_dir():
        Path(dir_path).mkdir(parents=True, exist_ok=True)


def _set_abs_log_file_paths(names_log_files):
    # Return updated list with absolute file paths for log files
    log_files_abs = []
    for i, file in enumerate(names_log_files):
        if Path(DIR_SOURCE / file).is_file():
            log_files_abs.append(DIR_SOURCE / file)
        else:
            print(f"Log file {DIR_SOURCE}/{file} will not be processed as "
                  f"not found")
    return log_files_abs


def _remove_nonexistent_files(files_logs_paths):
    # Return list without log files which cannot be found
    for log_file in files_logs_paths:
        if not log_file.is_file():
            print(f"Log file {log_file} not found. Removing from log "
                  f"reading")
            files_logs_paths.remove(log_file)
    return files_logs_paths


def _iterate_check_each_file(all_logfiles, regex):
    # Routine to call functionality to check all logfiles for issues
    for file in all_logfiles:
        try:
            _get_log_issues(file, regex)
        except PermissionError:
            print(f"You require administrator privileges to access {file}")


"""Find issues, create parsed log files"""


def _get_log_issues(file_to_read, regex):
    # Find lines in log file matching issue keywords

    # Collect entire line of log message with issue
    issues_found = {}
    # Collect only issue keyword
    issues_found_keyword = {}
    logs_copy_made = False
    print(f"Start read: {file_to_read}")
    with open(file_to_read, "r") as file:
        for i, line in enumerate(file):
            cols = [col.strip() for col in line.split(":") if col]
            for col in cols:
                if regex.search(col) is not None:
                    # Create copy of log file
                    if not logs_copy_made:
                        logs_copy_file = _write_log_file_copy(file_to_read)
                        logs_issues_file = \
                            _get_logs_issues_filename(logs_copy_file)
                        logs_issues_keyword_file = \
                            _get_logs_issues_keywords_filename(logs_copy_file)
                        logs_copy_made = logs_copy_file is not None
                        print(f"\nIssues found in {file_to_read.name}:\n"
                              f"See {logs_copy_file} directory for logs copy\n"
                              f"See {logs_issues_file} directory for issues")
                    # If issue not processed before, add
                    if col not in issues_found:
                        issues_found.update({col: 1})
                        issues_found_keyword.update({regex.findall(col)[0]: 1})
                    # Increment count of issues processed
                    else:
                        issues_found[col] += 1
                        issues_found_keyword[regex.findall(col)[0]] += 1
    file.close()
    if issues_found:
        write_log_file_issues(logs_issues_file, _sort_issues(issues_found))
        write_log_file_issues_short(logs_issues_keyword_file,
                                    _sort_issues(issues_found_keyword))


def _write_log_file_copy(file_to_copy):
    # Create copy of passed log file
    time_stamp = _get_formatted_timestamp()
    filename = file_to_copy.name.replace(file_to_copy.suffix, "")
    dest_filename = f"{filename}_{time_stamp}{file_to_copy.suffix}"
    Path(DIR_DEST / dest_filename) \
        .write_text(Path(file_to_copy).read_text())
    return Path(DIR_DEST / dest_filename)


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


def _get_logs_issues_keywords_filename(log_file_copy):
    # Return name for issues keyword log file from copy of log file
    log_path = Path(log_file_copy)
    suffix = log_path.suffix
    issues_path = str(log_path).replace(f"{suffix}", "")
    issues_path = f"{issues_path}_issues_keywords{suffix}"
    return issues_path


def write_log_file_issues(logs_issues_file, issues_found):
    with open(logs_issues_file, "a") as file:
        for issue in issues_found:
            file.writelines(f"ISSUE (appeared {issues_found[issue]} times):\n"
                            f"  {issue}\n\n")
    file.close()


def write_log_file_issues_short(logs_issues_file, issues_found):
    with open(logs_issues_file, "a") as file:
        for issue in issues_found:
            file.writelines(f"ISSUE (appeared {issues_found[issue]} times):\n"
                            f"  {issue}\n\n")
    file.close()


def _delete_dir_if_empty(dir_dest):
    for _, _, files in os.walk(dir_dest):
        if not files:
            dir_dest.rmdir()


"""Helpers"""


def get_list_from_comma_separated_string(string):
    words = string.split(",")
    return [word for word in words]


def _sort_issues(issues_dict):
    return {key: value for key, value in sorted(
        issues_dict.items(), key=lambda item: item[1], reverse=True)}


"""Entry point"""


def main():
    """Routine responsible for handling log copying, issue extraction"""
    global DIR_DEST
    global FILES_LOGS_PATHS
    global NAMES_FILES_TO_PARSE
    global ISSUES_REGEX

    get_flag_arguments()
    _set_source_dir()
    _set_issue_keywords()
    _set_files_to_parse()
    _create_dest_dir(DIR_DEST)
    FILES_LOGS_PATHS = _set_abs_log_file_paths(NAMES_FILES_TO_PARSE)
    FILES_LOGS_PATHS = _remove_nonexistent_files(FILES_LOGS_PATHS)
    _iterate_check_each_file(FILES_LOGS_PATHS, ISSUES_REGEX)
    _delete_dir_if_empty(DIR_DEST)


main()
