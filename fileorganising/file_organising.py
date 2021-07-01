#!/usr/bin/env python
"""Scratch files for organising files
    - Basic commands: shutil.copy(path_source, path_dest)
    - Copy file: shutil.copy(path_source, path_dest)
    - Copy directory: shutil.copytree(path_source, path_dest)
    - Delete file: os.unlink({path})
    - Delete empty directory: os.rmdir({path})
    - Delete directory: shutil.rmtree({path})

"""

import os
from pathlib import Path
import shutil
import zipfile


def _walk_example(path):
    for directory, sub_directories, files in os.walk(path):
        print(f"Current walked dir: {directory}")
        for sub_directory in sub_directories:
            print(f"    Sub-directory: {sub_directory}")
        for file in files:
            print(f"    File: {file}")


"""Copy examples"""


def _copy_examples():
    path_cwd = Path("./")
    # Files examples
    shutil.copy(path_cwd / "test-file.txt", path_cwd / "test-file-bu.txt")
    shutil.copy(path_cwd / "test-file.txt", path_cwd / "test-dir")
    # Directory examples
    shutil.copytree(path_cwd / "test-dir", path_cwd / "test-dir-bu")


def _copy_filetype_example():
    # _copy_filetype(Path("./"), Path("../copy-test-dir"), ".txt")
    _copy_filetype_recursive(Path("./"), Path("../copy-test-dir"), ".txt")


def _copy_filetype(dir_source, dir_destination, filetype):
    glob = f"*{filetype}"
    os.makedirs(dir_destination, exist_ok=True)

    for file in dir_source.glob(glob):
        print(
            f"Copy file {file} from source path {Path(dir_source) / Path(file)} to dest path {Path(dir_destination)}")
        if Path(file).suffix == filetype:
            if not _is_dest_copied_file_the_same(Path(dir_source),
                                                 dir_destination, file):
                shutil.copy(Path(dir_source) / Path(file),
                            Path(dir_destination))


def _copy_filetype_recursive(dir_source, dir_destination, filetype):
    os.makedirs(dir_destination, exist_ok=True)

    for directory, sub_directories, files in os.walk(dir_source):
        for file in files:
            if Path(file).suffix == filetype:
                if not _is_dest_copied_file_the_same(Path(directory),
                                                     dir_destination, file):
                    shutil.copy((Path(directory) / Path(file)),
                                Path(dir_destination))


def _is_dest_copied_file_the_same(dir_source, dir_destination, file):
    if (Path(dir_destination) / Path(file)).is_file():
        if os.path.getsize(Path(dir_destination) / Path(file)) != \
                os.path.getsize(Path(dir_source) / Path(file)):
            print(f"Files the same for {file}, don't copy")
            return True

    print(f"Files different for {file}, copy")
    return False


"""Zip examples"""


def _zip_examples():
    name_file = "test-file.txt"
    name_file_additional = "test-file2.txt"
    name_archive = "test-file.zip"
    path_current_directory = Path("./")
    # Create, read archive containing test-file.txt
    _zip_archive(
        Path(path_current_directory / name_file),
        Path(path_current_directory / name_archive))
    _zip_read(Path(path_current_directory / name_archive),
              name_file)
    _zip_extract(path_current_directory / name_archive)
    # Create, read archive containing added test-file2.txt
    _zip_archive_add(
        Path(path_current_directory / name_file_additional),
        Path(path_current_directory / name_archive))
    _zip_extract(path_current_directory / name_archive)


def _zip_archive(path_file_to_zip, path_zip):
    zip_to_make = zipfile.ZipFile(path_zip, "w")

    zip_to_make.write(path_file_to_zip, compress_type=zipfile.ZIP_DEFLATED)
    zip_to_make.close()


def _zip_archive_add(path_file_to_zip, path_zip):
    zip_to_update = zipfile.ZipFile(path_zip, "w")

    zip_to_update.write(path_file_to_zip, compress_type=zipfile.ZIP_DEFLATED)
    zip_to_update.close()


def _zip_read(path_zip, name_file):
    zip_to_read = zipfile.ZipFile(path_zip, "r")
    print(f"zip file contains: {zip_to_read.namelist()}")

    file_info = zip_to_read.getinfo(name_file)
    compression_ration = round(file_info.file_size / file_info.compress_size, 2)
    print(f"{file_info.filename} compression ratio is {compression_ration}\n"
          f"Original size: {file_info.file_size}, compressed size: "
          f"{file_info.compress_size}")
    zip_to_read.close()
    pass


def _zip_extract(path):
    zip_to_extract = zipfile.ZipFile(path, "r")

    zip_to_extract.extractall(zip_to_extract.filename + "_unzipped")
    zip_to_extract.close()


def main():
    # _copy_examples()
    # _walk_example(Path("./"))
    # _zip_examples()
    _copy_filetype_example()


main()
