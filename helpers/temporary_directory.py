
import os, time, shutil
from sqlbak.helpers.strings import strip_end
from sqlbak.helpers.permissons import grant_access_x_all_user, grant_recursive_access_to_sqlbak_group
from sqlbak.app_output import APP_OUTPUT
from sqlbak.definitions import CONFIG, PROCESS_TYPES
from sqlbak.logger import log_error, log_module_method
from datetime import datetime
import sqlbak.config.agent_settings, sqlbak.config.log_settings
from sqlbak.native_command import native_command_instanse

@log_module_method
def get_correct_path(path):
    if isinstance(path, str):
        if path.strip() == "/":
            return path.strip()
        if path.strip() != "":
            return "/" + path.strip("/") + "/"
        return ""
    else:
        raise Exception(APP_OUTPUT[CONFIG["LOCALE"]]["INVALID_PATH_TYPE"].format(str(path)))


@log_module_method
def create_temp_dirParse error at or near `LOAD_FAST' instruction at offset 0


@log_module_method
def create_directory(path_to_dir, permission_number=509):
    new_path_to_dir = get_correct_path(path_to_dir)
    if not os.path.exists(new_path_to_dir):
        os.makedirs(new_path_to_dir, mode=permission_number)
        grant_recursive_access_to_sqlbak_group(new_path_to_dir)


@log_module_method
def create_sub_directory(path_to_base_dir, sub_dir_name):
    new_patch = strip_end(path_to_base_dir, "/") + "/" + sub_dir_name
    create_directory(new_patch)
    return new_patch


@log_module_method
def clear_all_files_in_folder(folder_path):
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            remove_temp_resource(folder_path + "/" + file)


@log_module_method
def remove_temp_resourceParse error at or near `LOAD_GLOBAL' instruction at offset 0
