#!/usr/bin/env python
"""Backup files specified in "backups" file to a specified directory or a
default directory (the user's Documents/my-backups).
"""

import os
import pwd
import subprocess
import sys

BACKUP_DESTINATION = ""
ITEMS_TO_BACKUP = "./backups"


"""Backup destination setup."""


def _select_backup_dir():
    # Return user-specified backup directory or default if none provided.
    if len(sys.argv) > 1:
        return _replace_rel_with_abs_path(sys.argv[1])
    return f"/home/{_get_system_username()}/Documents/my-backups"


def _get_system_username():
    # Return current system's username.
    return pwd.getpwuid(os.getuid())[0]


def _get_backup_dir(destination):
    # Return backup directory - and create if it doesn't exist.
    if not os.path.isdir(os.path.abspath(destination)):
        os.makedirs(os.path.abspath(destination))
    return f"{destination}/"


"""Setup file containing files, directories to back up."""


def _add_lines_to_list():
    # Add each line in file as item to list
    try:
        with open(ITEMS_TO_BACKUP) as files:
            lines = [line.rstrip('\n') for line in files]
            return lines
    except FileNotFoundError:
        print(f"File: {ITEMS_TO_BACKUP} not found in this directory.\nPlease "
              f" create this file and specify in it the items you want to back "
              f"up.")
        sys.exit(1)


def _update_paths(to_backup):
    # Replace any relative paths for home (~/) with absolute paths.
    for i, item in enumerate(to_backup):
        to_backup[i] = _replace_rel_with_abs_path(item)
    return to_backup


""""Backup functionality."""


def _file_or_dir_exists(path):
    # Returns whether the specified file or directory exists or not
    if os.path.isdir(os.path.abspath(path)) or \
            os.path.isfile(os.path.abspath(path)):
        return True
    return False


def _copy_items(items, destination):
    # Main routine for backing up all files, directories in items
    for source in items:
        if os.path.isfile(source):
            subprocess.run(f"cp -r {source} {destination}", shell=True)
            if _source_destination_files_different(
                    source, f"{destination}"):
                subprocess.run(f"cp -r {source} {destination}", shell=True)
        else:
            dir_name = source.split("/")[-1]
            substring_path = destination.split(BACKUP_DESTINATION)
            if _must_append_dir_name_to_path(substring_path, destination):
                dir_destination = f"{destination}{dir_name}"
            else:
                dir_destination = destination
            if not os.path.isdir(dir_destination):
                subprocess.run(f"cp -r {source} {dir_destination}", shell=True)
            else:
                walk_dir(source, dir_destination)


def _source_destination_files_different(source_file, destination_file):
    # Compare if file/directory does not exist or if files are different sizes
    if not _file_or_dir_exists(destination_file):
        return True
    return os.path.getsize(source_file) != os.path.getsize(destination_file) \
           and not os.path.isdir(destination_file)


def _must_append_dir_name_to_path(substring_path, destination):
    # Identify directories only in the root BACKUP_DESTINATION directory
    return not (substring_path[-1] in destination and substring_path[-1]
                is not "")


def walk_dir(source, destination):
    # Call to copy files, directories, in current directory
    for parent_dir, sub_dirs, files in os.walk(source):
        for child_file in files:
            if parent_dir[len(source):].count(os.sep) < 1:
                to_copy_files = [f"{parent_dir}/{child_file}"]
                _copy_items(to_copy_files, f"{destination}/{child_file}")
        for sub_dir in sub_dirs:
            dest_dir = f"{destination}/{sub_dir}"
            source_dir = [f"{parent_dir}/{sub_dir}"]
            _copy_items(source_dir, dest_dir)


"""Helpers."""


def _replace_rel_with_abs_path(path):
    # Replace relative paths for home (~/) with absolute paths.
    return path.replace("~/", f"/home/{_get_system_username()}/")


"""Main routine."""


def backup():
    """Copies to_backup at paths in "to_backup" to user-specified directory or
    default if none provided.
    """
    global BACKUP_DESTINATION
    BACKUP_DESTINATION = _get_backup_dir(_select_backup_dir())
    items_to_backup_list = _add_lines_to_list()
    to_backup = _update_paths(items_to_backup_list)
    _copy_items(to_backup, BACKUP_DESTINATION)


backup()
