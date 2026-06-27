import base64, calendar, json, math, multiprocessing, os, shutil, signal, time
from datetime import datetime, timedelta
from typing import IO, Any, Callable, Dict, Iterator, List
import psutil
from pathlib import Path
import platform
from requests.exceptions import HTTPError, ConnectionError
import random, string, uuid
from uuid import UUID
import requests, hashlib, re
from urllib.parse import urlparse
from Crypto.Cipher import AES
from sshtunnel import SSHTunnelForwarder
from sqlbak.platform.helper import is_app_run_in_docker_container
from sqlbak.definitions import CONFIG, PIN_INTERVAL, CONSOLE_COLORS, COMPRESSION_PRIORITIES, BACKUP_TYPES, TIMEOUT, HOUR_IN_MINUTES, MINUTE_IN_SEC, SEC_IN_MILLISECOND
from sqlbak.definitions import TRIGGER_BACKUP_TYPES, DIFF_BACKUP_CONST, DIFF_BACKUP_SUFFIX, K_BIT, CHUNK_SIZE, AVAILABLE_SERVER_TYPES, INC_BACKUP_CONST, INC_BACKUP_SUFFIX
from sqlbak.definitions import LOG_BACKUP_CONST, TRANS_LOG_BACKUP_SUFFIX, DBMS_TYPES_CONSTS, KNOWLEDGE_BASE_LINKS, DATE_TIME_FORMATS, PROCESS_TYPES
from sqlbak.logger import log_method, log_only_exception, log_only_exception_without_raising, log_data, log_error
from sqlbak.console_commands import CONSOLE_COMMANDS
from sqlbak.log_actions import LOG_ACTIONS
from sqlbak.app_output import APP_OUTPUT
from sqlbak.exceptions import DestinationFileDoesNotExist
import sqlbak.config.log_settings

class Helper:

    def __init__(self):
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]

    @log_method
    def run_additional_process(self, target: Callable, *args) -> multiprocessing.Process:
        process = multiprocessing.Process(target=target, args=args)
        process.start()
        return process

    @log_method
    def time_out_exception(self, signum, frame):
        """

        :param signum:
        :param frame:
        :return:.
        """
        raise Exception(self.cm["TIMEOUT"])

    def check_none(self, value, default_value=''):
        if value is None:
            return default_value
        return value

    def get_attempt_pauseParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_only_exception
    def run_method_with_number_attempts_and_timeoutParse error at or near `LOAD_FAST' instruction at offset 0

    def local_time_str_to_UTC_str(self, dateTimeStr):
        return time.strftime"%Y-%m-%d %H:%M:%S"time.gmtimetime.mktimetime.strptimedateTimeStr"%Y-%m-%d %H:%M:%S.%f"

    @log_only_exception
    def get_utc_offset(self):
        offset = (calendar.timegmtime.localtime() - calendar.timegmtime.gmtime()) / 3600.0
        int_part, decimal_part = int(offset), offset - int(offset)
        if offset > 0:
            sign = "+"
        else:
            sign = "-"
            int_part *= -1
        int_part = "0" + str(int_part) if int(int_part) < 10 else int_part
        if decimal_part == 0:
            decimal_part = "00"
        else:
            decimal_part = "30" if decimal_part == 0.5 else "45"
        return str(sign) + "" + str(int_part) + ":" + str(decimal_part)

    @log_only_exception
    def get_timezone_offset_in_millisseconds(self):
        timezone = self.get_utc_offset()
        is_positive = timezone[0[:1]] == "+"
        split_offset = timezone.split":"
        hours_in_millis = HOUR_IN_MINUTES * MINUTE_IN_SEC * SEC_IN_MILLISECOND * int(split_offset[0][1[:None]])
        minutes_in_millis = MINUTE_IN_SEC * SEC_IN_MILLISECOND * int(split_offset[1])
        offset = hours_in_millis + minutes_in_millis
        return {'is_positive':is_positive, 
         'offset':offset}

    @log_method
    def approximate_size(self, size: int) -> str:
        """
        Convert a file size to human-readable form.
        Keyword arguments:
        size -- file size in bytes
        a_kilobyte_is_1024_bytes -- 1024; if False

        :param size:
        :return: string
        """
        suffixes = [
         'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        if size < 0:
            raise Exception(self.cm["INVALID_FILE_SIZE"])
        for suffix in suffixes:
            size /= K_BIT
            if size < K_BIT:
                return "{0:.3f}{1}".formatsizesuffix
        else:
            raise Exception(self.cm["EXTRA_FILE_SIZE"])

    @log_method
    def remove_file_or_dir(self, path_to_files: List[str]) -> None:
        if sqlbak.config.log_settings.rm_temp_files:
            for path in path_to_files:
                if os.path.existspath:
                    try:
                        os.removepath
                    except OSError:
                        shutil.rmtreepath

    @log_method
    def encrypt_string(self, text):
        if text:
            key = CONFIG["SECRET_KEY"]
            cipher = AES.newkey.encode"utf8"AES.MODE_CTR
            ct_bytes = cipher.encrypttext.encode"utf-8"
            nonce = base64.b64encodecipher.nonce.decode"utf-8"
            ct = base64.b64encodect_bytes.decode"utf-8"
            json_input = json.dumps{'nonce':nonce,  'ciphertext':ct}
            return json_input

    @log_method
    def decrypt_string(self, json_input):
        key = CONFIG["SECRET_KEY"]
        b64 = json.loadsjson_input
        nonce = base64.b64decodeb64["nonce"]
        ct = base64.b64decodeb64["ciphertext"]
        cipher = AES.new((key.encode"utf8"), (AES.MODE_CTR), nonce=nonce)
        pt = cipher.decryptct
        return pt.decode"utf-8".strip()

    @log_only_exception
    def get_time_in_milliseconds(self, datetime_text=None):
        get_time_in_milliseconds = None
        if datetime_text is None:
            return int(round(time.time() * 1000))
        for f in DATE_TIME_FORMATS:
            try:
                get_time_in_milliseconds = int(time.mktimedatetime.strptimedatetime_textf.timetuple() * 1000)
                break
            except ValueError:
                pass

        else:
            if get_time_in_milliseconds is not None:
                return get_time_in_milliseconds
            return int(round(time.time() * 1000))

    @log_method
    def get_time_from_milliseconds(self, milesecond_text):
        try:
            x = re.match"\\/Date\\((\\d*)\\)\\/"milesecond_text
            if x is not None:
                groups = x.groups()
                if len(groups) == 1:
                    return                     return datetime(1970, 1, 1) + timedelta(milliseconds=(int(groups[0])))
            raise Exception("Unknow format.")
        except Exception as e:
            try:
                raise Exception("Failed to convert {0} to date: {1}".formatmilesecond_texte)
            finally:
                e = None
                del e

    @log_method
    def get_file_name_for_test(self) -> str:
        time_in_millis = self.get_time_in_milliseconds()
        return "test_file_" + str(time_in_millis) + ".txt"

    @log_method
    def set_ssh_tunnel_connection(self, ssh_host, ssh_user, ssh_password, sql_hostname, sql_port, ssh_port, ssh_local_mapped_port):
        server = SSHTunnelForwarder((ssh_host, int(ssh_port)), ssh_username=ssh_user, ssh_password=ssh_password, remote_bind_address=(sql_hostname, int(sql_port)), local_bind_address=("0.0.0.0", int(ssh_local_mapped_port)))
        if server:
            server.start()
        return server

    @log_method
    def print_color_text(self, text, color=None):
        if color == CONSOLE_COLORS["RED"]:
            c = "0;31m"
        else:
            if color == CONSOLE_COLORS["WHITE"]:
                c = "0m"
            else:
                if color == CONSOLE_COLORS["GREY"]:
                    c = "37m"
                else:
                    c = "92m"
        print("\x1b[" + c + text + "\x1b[0m")

    def print(self, text):
        print(text)

    @log_only_exception
    def get_pin_interval(self):
        from sqlbak.local_db import LocalDB
        local_db = LocalDB()
        params = local_db.get_request_params()
        if params is None:
            return PIN_INTERVAL
        interval = params["RequestInterval"]
        expiration = self.get_date_timeparams["RequestExpiration"]
        return int(int(interval) / 1000 if expiration >= datetime.now() else PIN_INTERVAL)

    @log_only_exception
    def get_date_time(self, datetime_text=None):
        date_time = None
        if datetime_text is None:
            return datetime.now()
        for f in DATE_TIME_FORMATS:
            try:
                date_time = datetime.strptimedatetime_textf
                break
            except ValueError:
                pass

        else:
            if date_time is not None:
                return date_time
            return datetime.now()

    @log_only_exception
    def is_correct_response(self, response):
        try:
            response.raise_for_status()
        except ConnectionError as e:
            try:
                raise ConnectionError(response.json() if "json" in response else str(e))
            finally:
                e = None
                del e

        except HTTPError as e:
            try:
                raise e
            finally:
                e = None
                del e

        except Exception as err:
            try:
                raise Exception(err)
            finally:
                err = None
                del err

    @log_only_exception
    def get_log_action(self, locale, key, params=None):
        if params is not None:
            if len(params) > 0:
                return LOG_ACTIONS[locale][key] % params
        return LOG_ACTIONS[locale][key]

    @log_only_exception
    def is_text_true(self, text):
        return text.lower() == "true"

    @log_method
    def update_dynamic_settings_property(self, setting: str, value: Any) -> None:
        dynamic_settings = self.get_dynamic_settings()
        dynamic_settings[setting] = value
        with open(CONFIG["PATH_TO_APP"] + CONFIG["DYNAMIC_SETTINGS_FILE_NAME"], "w") as f:
            f.writejson.dumpsdynamic_settings

    @log_method
    def save_dynamic_settings(self, file_content: str) -> None:
        file_path = CONFIG["PATH_TO_APP"] + CONFIG["DYNAMIC_SETTINGS_FILE_NAME"]
        with open(file_path, "w") as f:
            f.writefile_content

    @log_method
    def get_dynamic_settingsParse error at or near `LOAD_GLOBAL' instruction at offset 0

    @log_method
    def get_dynamic_settings_value(self, setting: str) -> Any:
        dynamic_settings = self.get_dynamic_settings()
        if setting in dynamic_settings:
            return dynamic_settings[setting]
        return

    @log_method
    def parse_working_dir(self, working_dir_from_site):
        if working_dir_from_site is not None:
            if working_dir_from_site != "":
                new_working_dir_list = [d.strip"/" for d in working_dir_from_site.strip"/".split"/" if d != ""]
                return "/" + "/".joinnew_working_dir_list + "/"
        return CONFIG["DEFAULT_ROOT_WORK_DIR"] + "/"

    @log_method
    def get_host_name(self) -> str:
        system_info = platform.uname()
        return system_info.node

    def get_client_memory_infoParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_method
    def get_user_machine_info_in_xml(self) -> str:
        system_info = platform.uname()
        time_zone = self.get_iana_time_zone()
        distro_info = self.get_distro_info()
        if time_zone == "":
            time_zone = str(time.tzname[time.daylight])
        return '\n        <SystemInfo xmlns="">\n          <OSInfo Time="{0}" TimeZone="{8}" LinuxId="{10}" LinuxIdLike="{11}" LinuxPrettyName="{12}" LinuxVersionId="{13}"></OSInfo>\n          <MemoryInfo>{1}</MemoryInfo>\n          <OperatingSystem>{2}</OperatingSystem>\n          <NodeName>{3}</NodeName>\n          <MachineInfo>{4}</MachineInfo>\n          <KernelVersion>{5}</KernelVersion>\n          <KernelRelease>{6}</KernelRelease>\n          <KernelPlatform>{7}</KernelPlatform>\n          {9}\n        </SystemInfo>\n        '.format(str(datetime.now()), str(self.get_client_memory_info()), system_info.system, system_info.node, system_info.machine, system_info.version, system_info.release, platform.platform(), time_zone, self.detect_if_app_run_in_docker_container_and_return_settings(), distro_info["os"], distro_info["os_like"], distro_info["pretty_name"], distro_info["version"])

    @log_method
    def get_distro_info(self):
        distro_info = {
         'os': '""', 
         'version': '""', 
         'os_like': '""', 
         'pretty_name': '""'}
        if os.path.exists"/etc/os-release":
            with open("/etc/os-release", "r") as f:
                for line in f.readlines():
                    if "=" in line:
                        split_line = line.split"="

                if len(split_line) > 1:
                    param = split_line[0].strip().lower()
                    value = split_line[1].strip().lower().strip'"'
                    if param == "id":
                        distro_info["os"] = value
                    elif param == "version_id":
                        distro_info["version"] = value
                    elif param == "id_like":
                        distro_info["os_like"] = value
                    elif param == "pretty_name":
                        distro_info["pretty_name"] = value
        else:
            if os.path.exists"/etc/lsb-release":
                with open("/etc/lsb-release", "r") as f:
                    for line in f.readlines():
                        split_line = line.split"="
                        param = split_line[0].strip().lower()
                        value = split_line[1].strip().lower()
                        if param == "distrib_id":
                            distro_info["os"] = value
                    else:
                        if param == "distrib_release":
                            distro_info["version"] = value

            else:
                if os.path.exists"/etc/debian_version":
                    with open("/etc/debian_version", "r") as f:
                        distro_info["os"] = "debian"
                        distro_info["version"] = f.read()
                else:
                    if os.path.exists"/etc/SuSe-release":
                        with open("/etc/SuSe-release", "r") as f:
                            distro_info["os"] = "suse"
                            distro_info["version"] = "old"
                    else:
                        if os.path.exists"/etc/redhat-release":
                            with open("/etc/redhat-release", "r") as f:
                                distro_info["os"] = "centos"
                                distro_info["version"] = "old"
                        return distro_info

    @log_method
    def is_app_run_in_docker_container(self):
        return is_app_run_in_docker_container()

    @log_method
    def detect_if_app_run_in_docker_container_and_return_settings(self) -> str:
        settings = ""
        if self.is_app_run_in_docker_container():
            container_id = self.get_host_name()
            settings = '<DockerInfo IsAppRunInDocker="True" ContainerId="{0}"></DockerInfo>'.formatcontainer_id
        return settings

    @log_method
    def get_iana_time_zoneParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_method
    def get_directory_size(self, path_to_directory: str) -> int:
        root_directory = Path(path_to_directory)
        size = sum((f.stat().st_size for f in  if f.is_file()))
        return size

    @log_method
    def get_resource_size(self, path_to_resource: str) -> int:
        if not os.path.existspath_to_resource:
            raise Exception(self.cm["FILE_NOT_EXISTS"].formatpath_to_resource)
        elif os.path.isdirpath_to_resource:
            size = self.get_directory_sizepath_to_resource
        else:
            size = os.path.getsizepath_to_resource
        return size

    @log_method
    def get_files_in_directory(self, directory: str) -> List[str]:
        files_in_directory = os.listdirdirectory
        sorted_files = sorted(files_in_directory)
        return sorted_files

    @log_method
    def get_processes_id_by_name(self, name: str) -> List[int]:
        processes_id = []
        for process in psutil.process_iter():
            process_info = self.get_process_infoprocess
            if process_info:
                id = self.get_process_id(process_info, name, process)
                if id:
                    processes_id.appendid
            return processes_id

    @log_only_exception_without_raising
    def get_process_info(self, process):
        return process.cmdline()

    @log_only_exception_without_raising
    def get_process_id(self, process_info, name, process):
        process_name = " ".joinprocess_info
        if name.lower() in process_name.lower():
            return int(process.pid)
        return

    @log_method
    def stop_process_and_return_is_success(self, pid):
        try:
            process = psutil.Processpid
            process.kill()
            return True
        except:
            except Exception:
            return False

    @log_method
    def set_process_priority(self, priority, pid):
        try:
            p = psutil.Processint(pid)
            p.niceint(COMPRESSION_PRIORITIES[priority])
        except Exception:
            pass

    @log_method
    def get_client_free_spaceParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_method
    def get_params_to_run_server_script(self, command, request, password, port, use_ssh, ssh_host, ssh_user, ssh_pass, host, user, ssh_port, ssh_local_mapped_port):
        password = self.decrypt_stringpassword if password else None
        local_bind_port = port
        server = None
        if bool(use_ssh):
            server = self.set_ssh_tunnel_connection(ssh_host, ssh_user, self.decrypt_stringssh_pass, host, port, ssh_port, ssh_local_mapped_port)
            local_bind_port = server.local_bind_port
            host = "127.0.0.1"
        return (host, user, local_bind_port, password, command, request, use_ssh, server)

    @log_method
    def read_file_by_chunks(self, file_object: IO, chunk_size: int=CHUNK_SIZE) -> Iterator[bytes]:
        while True:
            data = file_object.readchunk_size
            if not data:
                break
            yield data

    @log_method
    def get_backup_type_for_trigger(self, trigger_backup_type: str) -> str:
        if trigger_backup_type not in TRIGGER_BACKUP_TYPES:
            raise Exception(self.cm["FAILED_TRIGGER_BACKUP_TYPE"].formattrigger_backup_type)
        return TRIGGER_BACKUP_TYPES[trigger_backup_type]

    @log_method
    def get_backup_file_name(self, file_format: str, db_name: str, backup_at, backup_type=False) -> str:
        if backup_type == DIFF_BACKUP_CONST:
            suffix = DIFF_BACKUP_SUFFIX
        else:
            if backup_type == LOG_BACKUP_CONST:
                suffix = TRANS_LOG_BACKUP_SUFFIX
            else:
                if backup_type == INC_BACKUP_CONST:
                    suffix = INC_BACKUP_SUFFIX
                else:
                    suffix = ""
        if "Date" == file_format:
            file_name = str(db_name) + str(backup_at.strftime"%Y%m%d") + suffix
        else:
            if "DayOfMonth" == file_format:
                file_name = str(db_name) + str(backup_at.strftime"%d") + suffix
            else:
                if "DayOfWeek" == file_format:
                    file_name = str(db_name) + str(backup_at.strftime"%A") + suffix
                else:
                    if "NameOnly" == file_format:
                        file_name = str(db_name) + suffix
                    else:
                        file_name = str(db_name) + str(backup_at.strftime"%Y%m%d%H%M") + suffix
        return file_name

    @log_method
    def replace_colon_sign_in_file_name(self, file_name: str) -> str:
        return file_name.replace":""_"

    @log_method
    def get_dbms_type_by_name(self, server_type, connection_type):
        if server_type not in DBMS_TYPES_CONSTS:
            raise Exception(self.cm["WRONG_SERVER_TYPE"].formatserver_type", ".joinAVAILABLE_SERVER_TYPES)
        if connection_type not in DBMS_TYPES_CONSTS[server_type]["connection_types"]:
            raise Exception(self.cm["FAILED_GET_DBMS_TYPE_BY_NAME"])
        return DBMS_TYPES_CONSTS[server_type]["connection_types"][connection_type]

    @log_method
    def get_random_name(self, length: int) -> str:
        return "".join(random.choicestring.ascii_lowercase for i in )

    @log_method
    def get_knowledge_base_error(self, error: Any, should_get_code: bool=False) -> str:
        if type(error) == str:
            if "not found" in error:
                if "mysql" in error or "mysqldump" in error:
                    if should_get_code:
                        error = KNOWLEDGE_BASE_LINKS["MYSQL_NOT_FOUND"]["code"] + " " + error
                else:
                    error += "Link to a resource: {0}".formatKNOWLEDGE_BASE_LINKS["MYSQL_NOT_FOUND"]["link"]
            else:
                if "sqlcmd" in error:
                    if should_get_code:
                        error = KNOWLEDGE_BASE_LINKS["SQLCMD_NOT_FOUND"]["code"] + " " + error
                    else:
                        error += "Link to a resource: {0}".formatKNOWLEDGE_BASE_LINKS["SQLCMD_NOT_FOUND"]["link"]
                else:
                    if "pgdump" in error or "psql" in error:
                        if should_get_code:
                            error = KNOWLEDGE_BASE_LINKS["PSQL_NOT_FOUND"]["code"] + " " + error
                        else:
                            error += "Link to a resource: {0}".formatKNOWLEDGE_BASE_LINKS["PSQL_NOT_FOUND"]["link"]
        else:
            if "Error enabling binary logs" in error:
                error = KNOWLEDGE_BASE_LINKS["FAILED_MYSQL_INC_SETUP"]["code"] + " " + error + "Link to a resource: {0}".formatKNOWLEDGE_BASE_LINKS["FAILED_MYSQL_INC_SETUP"]["link"]
            else:
                for x in KNOWLEDGE_BASE_LINKS:
                    if KNOWLEDGE_BASE_LINKS[x]["code"] in error:
                        should_get_code or error += "Link to a resource: {0}".formatKNOWLEDGE_BASE_LINKS[x]["link"]
                    else:
                        return error

    @log_method
    def delete_log_files_older_then_seven_days(self) -> None:
        path_to_logs = CONFIG["PATH_TO_APP"] + CONFIG["PATH_TO_LOGS"]
        log_files = self.get_files_in_directorypath_to_logs
        for p in log_files:
            self.remove_log_filepath_to_logsp

    @log_method
    def remove_log_file(self, path_to_logs: str, file_name: str) -> None:
        file_time = self.get_date_timefile_name.split"."[0]
        last_week = datetime.now() - timedelta(days=7)
        is_file_older_seven_days = file_time < last_week
        if is_file_older_seven_days:
            self.remove_file_or_dir[path_to_logs + file_name]

    @log_only_exception
    def get_uuid(self) -> str:
        return str(uuid.uuid4().hex)

    @log_only_exception
    def get_guid(self) -> str:
        return str(uuid.uuid4())

    @log_method
    def download_package_from_serverParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_method
    def download_file(self, file_name, token):
        from sqlbak.exchange_message.remote_server_requests import RemoteServerRequest
        prefix = RemoteServerRequest().web_api_protocol
        if "https" in prefix:
            url = prefix + ".sqlbak.com/Client/Service/SqlBakUpdate.svc/secure/{0}/{1}".formatfile_nametoken
        else:
            url = prefix + ".sqlbak.com/Client/Service/SqlBakUpdate.svc/{0}/{1}".formatfile_nametoken
        log_data("Download package url: {}".formaturl)
        res = requests.get(url, stream=True)
        self.is_correct_responseres
        return res

    @log_method
    def save_package_data_to_file(self, file_data):
        with open(CONFIG["PATH_TO_PACKAGE"], "wb") as f:
            for chunk in file_data.iter_content(chunk_size=1024):
                if chunk:
                    f.writechunk

    @log_method
    def update_agent_session(self, agent, local_db) -> str:
        if agent["SessionId"] is None:
            agent["SessionId"] = self.get_guid()
            local_db.update_agent_session_idagent["SessionId"]
        return agent["SessionId"]

    @log_only_exception
    def get_time_with_offset(self, current_time):
        offset = self.get_timezone_offset_in_millisseconds()
        if offset is not None:
            if isinstance(offset, dict):
                if offset["is_positive"]:
                    current_time = current_time + offset["offset"]
                else:
                    current_time = current_time - offset["offset"]
        return current_time

    @log_only_exception
    def get_begin_time_with_offset(self, start_time, now, begin_at, time_format):
        if begin_at is not None:
            begin_at_arr = begin_at.split":"
            temp_start_at = now.replace(hour=(int(begin_at_arr[0])), minute=(int(begin_at_arr[1])))
            return self.get_time_in_millisecondstemp_start_at.strftimetime_format
        return start_time

    @log_only_exception
    def get_end_time_with_offset(self, start_time, now, end_at, time_format):
        if end_at is not None:
            end_at_arr = end_at.split":"
            temp_end_at = now.replace(hour=(int(end_at_arr[0])), minute=(int(end_at_arr[1])))
            return self.get_time_in_millisecondstemp_end_at.strftimetime_format
        return start_time

    @log_only_exception
    def get_console_commands_from_file(self):
        custom_commands = None
        if os.path.existsCONFIG["PATH_TO_CUSTOM_CONSOLE_COMMANDS"]:
            with open(CONFIG["PATH_TO_CUSTOM_CONSOLE_COMMANDS"], "r") as f:
                custom_commands = json.loadsf.read()
        return custom_commands

    @log_only_exception
    def get_console_commands(self):
        custom_commands = self.get_console_commands_from_file()
        if custom_commands is not None:
            for custom_command in custom_commands:
                for c in CONSOLE_COMMANDS:
                    if custom_command["command"] == c["command"]:
                        c["description"] = custom_command["description"]
                        c["is_public"] = custom_command["is_public"]

            if "params" in custom_command:
                if "required" in custom_command["params"]:
                    for custom_required in custom_command["params"]["required"]:
                        for required in c["params"]["required"]:
                            if required["name"] == custom_required["name"]:
                                required["description"] = custom_required["description"]
                                required["is_public"] = custom_required["is_public"]

            elif "optional" in custom_command["params"]:
                for custom_optional in custom_command["params"]["optional"]:
                    for optional in c["params"]["optional"]:
                        if optional["name"] == custom_optional["name"]:
                            optional["description"] = custom_optional["description"]
                            optional["is_public"] = custom_optional["is_public"]

            elif "conditional" in custom_command["params"]:
                for custom_conditional in custom_command["params"]["conditional"]:
                    for conditional in c["params"]["conditional"]:
                        if conditional["name"] == custom_conditional["name"]:
                            conditional["description"] = custom_conditional["description"]
                            conditional["is_public"] = custom_conditional["is_public"]

        return CONSOLE_COMMANDS

    @log_method
    def is_path_exists_and_valid(self, path_to: str) -> bool:
        if "\\" in path_to:
            return False
        else:
            return os.path.existspath_to or False
        return True

    @log_method
    def get_checksum_for_file(self, path_to_file: str) -> str:
        checksum = None
        if self.is_path_exists_and_validpath_to_file:
            with open(path_to_file, "rb") as f:
                data = f.read()
                checksum = hashlib.md5data.hexdigest()
        return checksum

    @log_method
    def check_if_previous_backup_was_success(self, database, object_type, local_db, job_id):
        result = local_db.get_object_backup_result(database, job_id, object_type)
        if result is None:
            return
        if int(result["IsSuccess"]):
            return True
        return False

    @log_method
    def get_dbms_name_by_server_typeParse error at or near `LOAD_CONST' instruction at offset 0

    @log_method
    def is_url_valid(self, url: str) -> bool:
        try:
            res = urlparse(url)
            return res.scheme != ""
        except:
            except ValueError:
            return False

    @log_method
    def get_url_path(self, url):
        result = urlparse(url)
        return result.path

    @log_method
    def is_local_host(self, address: str) -> bool:
        return address.lower() == "localhost" or address == "127.0.0.1"

    @log_method
    def get_backup_type_by_object_type(self, object_type):
        backup_type = None
        for b in BACKUP_TYPES:
            if BACKUP_TYPES[b] == object_type:
                backup_type = b
            return backup_type

    @log_method
    def read_file_by_chunks_test(self, file_object, chunk_size=CHUNK_SIZE):
        while True:
            data = file_object.readchunk_size
            if not data:
                break
            yield data


helper_instanse = Helper()
