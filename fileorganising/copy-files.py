#!/usr/bin/env python
import argparse
import os
import shutil
from pathlib import Path

EXTENSION_TO_COPY = ""
RECURSIVE = False
FORCE_COPY = False
DIRECTORY_SOURCE = ""
DIRECTORY_DESTINATION = os.path.expanduser("~/copy-files")

"""Setup"""


def _get_flag_arguments():
    global EXTENSION_TO_COPY
    global FORCE_COPY
    global RECURSIVE
    global DIRECTORY_DESTINATION

    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("destination", type=str,
                        help="(default: ~/copy-files)")
    parser.add_argument("-e", "--extension", type=str, required=True,
                        help="file extension/type to copy (required)")
    parser.add_argument("-f", "--force", type=bool, required=False,
                        help="copy all files, overwriting identical-size "
                             "files (default: False)")
    parser.add_argument("-r", "--recursive", type=bool, required=False,
                        help="copy all files in specified directory tree "
                             "(default: False)")

    args = parser.parse_args()
    if args.source:
        DIRECTORY_SOURCE = args.source
    if args.destination:
        DIRECTORY_DESTINATION = args.destination
    if args.extension:
        EXTENSION_TO_COPY = args.extension
    if args.force:
        FORCE_COPY = args.force
    if args.recursive:
        RECURSIVE = args.recursive


"""Copy functionality"""


def _handle_copy():
    if RECURSIVE:
        _copy_filetype_recursive(Path(DIRECTORY_SOURCE), Path(DIRECTORY_DESTINATION),
                                 EXTENSION_TO_COPY)
    else:
        _copy_filetype(Path(DIRECTORY_SOURCE), Path(DIRECTORY_DESTINATION),
                       EXTENSION_TO_COPY)


def _copy_filetype(dir_source, dir_destination, filetype):
    glob = f"*{filetype}"
    os.makedirs(dir_destination, exist_ok=True)

    for file in dir_source.glob(glob):
        if Path(file).suffix == filetype:
            if _is_dest_copied_file_different(Path(dir_source), dir_destination,
                                              file):
                shutil.copy(Path(dir_source) / Path(file),
                            Path(dir_destination))


def _copy_filetype_recursive(dir_source, dir_destination, filetype):
    os.makedirs(dir_destination, exist_ok=True)

    for directory, sub_directories, files in os.walk(dir_source):
        for file in files:
            if Path(file).suffix == filetype:
                if _is_dest_copied_file_different(Path(directory),
                                                  dir_destination, file):
                    shutil.copy((Path(directory) / Path(file)),
                                Path(dir_destination))


"""Helpers"""


def _is_dest_copied_file_different(dir_source, dir_destination, file):
    if (Path(dir_destination) / Path(file)).is_file():
        return os.path.getsize(Path(dir_destination) / Path(file)) != \
               os.path.getsize(Path(dir_source) / Path(file))
    return True


def main():
    _get_flag_arguments()
    _handle_copy()


main()
