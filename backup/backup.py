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


def _select_backup_dir():
    # Return user-specified backup directory or default if none provided.
    if len(sys.argv) > 1:
        return _replace_rel_with_abs_path(sys.argv[1])
    return f"/home/{_get_system_username()}/Documents/my-backups"


def _replace_rel_with_abs_path(path):
    # Replace relative paths for home (~/) with absolute paths.
    return path.replace("~/", f"/home/{_get_system_username()}/")


def _get_backup_dir(destination):
    # Return backup directory - and create if it doesn't exist.
    if not os.path.isdir(os.path.abspath(destination)):
        os.makedirs(os.path.abspath(destination))
    return f"{destination}/"


def _get_system_username():
    # Return current system's username.
    return pwd.getpwuid(os.getuid())[0]


def _update_paths(to_backup):
    # Replace any relative paths for home (~/) with absolute paths.
    for i, item in enumerate(to_backup):
        to_backup[i] = _replace_rel_with_abs_path(item)
    return to_backup


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


def file_or_dir_exists(path):
    # Returns whether the specified file or directory exists or not
    if os.path.isdir(os.path.abspath(path)) or \
            os.path.isfile(os.path.abspath(path)):
        return True
    return False


def copy_sources(sources, destination):
    print(f"Being asked to think about copying {sources}")
    for source in sources:
        if os.path.isfile(source):
            subprocess.run(f"cp -r {source} {destination}", shell=True)
            if source_destination_files_different(
                    source, f"{destination}"):
                print(f"YES I SHOULD")
                subprocess.run(f"cp -r {source} {destination}", shell=True)
        else:
            print(f"Considering dir {source}")
            print(f"Considering dest {destination}")
            dir_name = source.split("/")[-1]
            # If dest dir doesn't contain same substring as root dir/.../dir_name
            substring_path = destination.split(BACKUP_DESTINATION)
            if must_append_dir_name_to_path(substring_path, destination):
                dir_destination = f"{destination}{dir_name}"
            else:
                dir_destination = destination
            print(f"SO I want to copy {source} to {dir_destination}")
            if not os.path.isdir(dir_destination):
                subprocess.run(f"cp -r {source} {dir_destination}", shell=True)
            else:
                walk_dir(source, dir_destination)


def source_destination_files_different(source_file, destination_file):
    if not file_or_dir_exists(destination_file):
        return True
    return os.path.getsize(source_file) != os.path.getsize(destination_file) \
           and not os.path.isdir(destination_file)


def must_append_dir_name_to_path(substring_path, destination):
    return not (substring_path[-1] in destination and substring_path[-1]
    is not "")


def walk_dir(source, destination):
    print(f"Walking source {source} directory")
    print(f"Walking destination {destination} directory")
    for parent_dir, sub_dirs, files in os.walk(source):
        for child_file in files:
            if parent_dir[len(source):].count(os.sep) < 1:
                to_copy_files = [f"{parent_dir}/{child_file}"]
                print(f"I want to think about copying {child_file} ")
                copy_sources(to_copy_files, f"{destination}/{child_file}")
        for sub_dir in sub_dirs:
            dest_dir = f"{destination}/{sub_dir}"
            source_dir = [f"{parent_dir}/{sub_dir}"]
            print(
                f"I should now think about copying {source_dir} to {dest_dir}")
            copy_sources(source_dir, dest_dir)


def backup():
    """Copies to_backup at paths in "to_backup" to user-specified directory or
    default if none provided.
    """
    global BACKUP_DESTINATION
    BACKUP_DESTINATION = _get_backup_dir(_select_backup_dir())
    items_to_backup_list = _add_lines_to_list()
    to_backup = _update_paths(items_to_backup_list)
    copy_sources(to_backup, BACKUP_DESTINATION)


backup()
