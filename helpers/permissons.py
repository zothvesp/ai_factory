
from sqlbak.platform.helper import is_app_run_in_docker_container
from sqlbak.app_output import APP_OUTPUT
from sqlbak.definitions import CONFIG
from sqlbak.local_db import local_db_instanse
from sqlbak.logger import log_error, log_module_method, log_data
from sqlbak.native_command import native_command_instanse
import sqlbak.config.log_settings
from time import sleep
import os

@log_module_method
def create_sqlbak_user_group():
    try:
        native_command_instanse.run_linux_script("groupadd 'sqlbak'")
        for x in ('mysql', 'mssql', 'postgres', 'mongodb'):
            try:
                native_command_instanse.run_linux_script("usermod -a -G sqlbak {0}".format(x))
            except:
                pass

    except:
        pass


@log_module_method
def exist_sqlbak_group():
    try:
        output = native_command_instanse.run_linux_script("cat /etc/group | grep sqlbak")
    except:
        return False

    return "sqlbak" in output and len([x for x in ('mysql', 'mssql', 'postgres', 'mongodb') if x in output]) > 0


@log_module_method
def get_perm_numberParse error at or near `SETUP_FINALLY' instruction at offset 0


@log_module_method
def get_group_nameParse error at or near `SETUP_FINALLY' instruction at offset 0


@log_module_method
def set_group_name(group_name, path):
    native_command_instanse.run_linux_script("chgrp -R --no-dereference --preserve-root {0} '{1}'".format(group_name, path))


@log_module_method
def chmod(perm_number_, path, force=False):
    if force or perm_number_ != get_perm_number(path):
        native_command_instanse.run_linux_script("chmod -R --preserve-root {0} '{1}'".format(perm_number_, path))


@log_module_method
def grant_recursive_access_to_sqlbak_group(path):
    if is_app_run_in_docker_container():
        chmod777path
    else:
        if exist_sqlbak_group():
            set_group_name"sqlbak"path
            chmodsqlbak.config.log_settings.base_permissionspath
        else:
            create_sqlbak_user_group()
            if exist_sqlbak_group():
                set_group_name"sqlbak"path
                chmodsqlbak.config.log_settings.base_permissionspath
            else:
                chmod777path


@log_module_method
def grant_access_x_all_userParse error at or near `LOAD_GLOBAL' instruction at offset 0


@log_module_method
def grant_777_access(path):
    native_command_instanse.run_linux_script("chmod 777 -R --preserve-root '{0}'".format(str(path)))
    sleep(1)


@log_module_method
def reset_access_for_working_dir():
    work_dir = local_db_instanse.get_working_dir()
    try:
        if not os.path.isdir(work_dir):
            os.makedirs(work_dir, mode=509)
        if work_dir.endswith(CONFIG["DEFAULT_DOWNLOAD_DIR"] + "/"):
            grant_access_x_all_user(work_dir[None[:-len(CONFIG["DEFAULT_DOWNLOAD_DIR"] + "/")]])
    except Exception as e:
        try:
            log_errore"Error adding x permissions to parent directory"
        finally:
            e = None
            del e

    else:
        grant_recursive_access_to_sqlbak_group(work_dir)


@log_module_method
def try_set_owner_parent_folder(user, filepath):
    dir = os.path.dirname(filepath)
    if native_command_instanse.try_run_linux_script("chown -R --preserve-root --no-dereference {0} '{1}'".format(user, dir)) == None:
        log_data("Failed set user '{0}' as owner for '{1}'".format(user, dir))


def try_with_full_access_folderParse error at or near `SETUP_FINALLY' instruction at offset 0
