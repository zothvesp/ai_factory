
import os, re
import sqlbak.helpers.strings as strings
from sqlbak.definitions import ARCHIVES_EXT, E7Zip_EXT, ZIP_EXT
from sqlbak.native_command import native_command_instanse
from sqlbak.logger import log_method

def is_windows_path(path):
    return re.match("^[a-zA-Z]:\\\\", path) is not None


@log_method
def is_archiveParse error at or near `LOAD_CONST' instruction at offset 0


@log_method
def get_ext(file_name):
    return file_name.split"."[-1]


@log_method
def get_archive_ext(compression_method):
    if compression_method == "M7Zip" or compression_method == "E7Zip":
        return E7Zip_EXT
    return ZIP_EXT


@log_method
def decompress(input_archive_files, output_directory, password):
    ext = get_ext(input_archive_files[0])
    if len(input_archive_files) > 1:
        x = sorted(input_archive_files)
        x = " ".joinx
        tmp_path = output_directory + "/unsplit." + ext
        native_command_instanse.run_linux_script"cat {0} > {1}".format(x, tmp_path)
        for for_delete_file in input_archive_files:
            os.removefor_delete_file
        else:
            archive_patch = tmp_path

    else:
        archive_patch = input_archive_files[0]
    files = os.listdiroutput_directory
    if native_command_instanse.check_installed_util"7z" or ext == "7z":
        native_command_instanse.decompress_by_7zip(archive_patch, output_directory, password)
    else:
        if ext == "zip":
            native_command_instanse.decompress_by_unzip(archive_patch, output_directory, password)
    files = list(set(os.listdiroutput_directory) - set(files))
    return [output_directory + "/" + x for x in files]


@log_method
def compres_folder_zip(source_path, destintaiton_acrchive_path, level, password, is_encrypted):
    password_parameter = '-P "{0}"'.formatpassword if is_encrypted else ""
    command = "zip {0} -r {1}  -q {2} {3}".format(password_parameter, level, destintaiton_acrchive_path, source_path)
    native_command_instanse.run_linux_script_with_password(command, [] if strings.is_emptypassword else [password])


@log_method
def compress_folder_7z(source_path, destintaiton_acrchive_path, level, password, is_encrypted, additional_parameters):
    password_parameter = '-p"{0}"'.formatpassword if is_encrypted else ""
    command = "7z a {0} {1} {2} {3} {4}".format(password_parameter, level, additional_parameters, destintaiton_acrchive_path, source_path)
    native_command_instanse.run_linux_script_with_password(command, [] if strings.is_emptypassword else [password])


@log_method
def split_file(source_file, destination_prefix, max_file_size):
    destination_directory, destination_file_prefix = os.path.splitdestination_prefix
    exit_files_in_destionation_directory = os.listdirdestination_directory
    cmd = "split -d -b {0} {1} {2}".format(max_file_size, source_file, destination_prefix)
    native_command_instanse.run_linux_scriptcmd
    new_files = list(set(os.listdirdestination_directory) - set(exit_files_in_destionation_directory))
    result = [os.path.join(destination_directory, x) for x in new_files]
    result.sort()
    return result


@log_method
def get_files_patch_recursive(base_dir):
    return sum([x[2] for x in os.walkbase_dir], [])
