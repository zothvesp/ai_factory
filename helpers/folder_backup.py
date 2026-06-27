
import os
from sqlbak.helpers.temporary_directory import create_sub_directory
from sqlbak.definitions import COMPRESSION_ENGINE_ZIP, COMPRESSION_ENGINE_7Z
from sqlbak.helpers.files import compres_folder_zip, compress_folder_7z, get_archive_ext, get_files_patch_recursive
from sqlbak.logger import log_module_method

@log_module_method
def backup_folder(path_to_folder, backup_folder, backup_object_name, compression_engine, compression_level, commpression_password, is_encryption_enabled, cli_7z_options, idx):
    backup_file_name = get_backup_file_name(backup_folder, backup_object_name, get_archive_ext(compression_engine))
    archive_sub_folder = create_sub_directory(backup_folder, str(idx))
    path_to_compressed_backup = os.path.join(archive_sub_folder, backup_file_name)
    if not os.path.exists(path_to_folder):
        raise Exception("Directory does not exist: {0}".format(path_to_folder))
    elif compression_engine == COMPRESSION_ENGINE_ZIP:
        compres_folder_zip(path_to_folder, path_to_compressed_backup, compression_level, commpression_password, is_encryption_enabled)
    else:
        if compression_engine == COMPRESSION_ENGINE_7Z:
            compress_folder_7z(path_to_folder, path_to_compressed_backup, compression_level, commpression_password, is_encryption_enabled, cli_7z_options)
    return (
     archive_sub_folder, backup_file_name)


@log_module_method
def get_backup_file_nameParse error at or near `LOAD_STR' instruction at offset 0
