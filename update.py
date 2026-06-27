import json, os, base64
from datetime import datetime
from sqlbak.helper import Helper
from sqlbak.local_db import LocalDB
from sqlbak.native_command import NativeCommand
from sqlbak.trace_event import TraceEvent
from sqlbak.exchange_message.remote_server_requests import RemoteServerRequest
from sqlbak.plain_job import PlainJob
from sqlbak.definitions import CONFIG, LINUX_DISTROS, PIN_INTERVAL, PROCESS_TYPES, UPDATE_APP_SOURCES, SEC_IN_MILLISECOND, MINUTE_IN_SEC
from sqlbak.logger import log_error, log_method
from sqlbak.exceptions import UpdateIsActual, UpdateIsNotPossibleNow, AutoUpdateIsDisabled
from sqlbak.app_output import APP_OUTPUT
from sqlbak.process_managment.helper import is_process_running_now
from sqlbak.helpers.permissons import grant_777_access

class UpdateApp:

    def __init__(self):
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]
        self.helper = Helper()
        self.local_db = LocalDB()
        self.trace_event = TraceEvent()
        self.native_command = NativeCommand()
        self.remote_request = RemoteServerRequest()
        self.plain_job = PlainJob()

    @log_method
    def update_packageParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_method
    def get_app_version_from_server(self, agent_key, update_mode):
        res = self.remote_request.check_update_statusagent_keyupdate_mode
        if not res["IsSuccess"]:
            raise Exception(self.cm["FAILED_GET_UPDATE_STATUS"].formatstr(res["ErrorMessage"]))
        if update_mode == UPDATE_APP_SOURCES["AUTO"]:
            if not res["Data"]["AutoUpdateEnabled"]:
                raise AutoUpdateIsDisabled
        return res["Data"]["MaxVersion"]

    @log_method
    def is_first_version_less_then_second_version(self, first, second):
        """

        :param first:
        :param second:
        :return:
        """
        if int(first["MajorVersion"]) < int(second["MajorVersion"]):
            return True
            if int(first["MajorVersion"]) == int(second["MajorVersion"]):
                if int(first["MinorVersion"]) < int(second["MinorVersion"]):
                    return True
        elif int(first["MajorVersion"]) == int(second["MajorVersion"]):
            if int(first["MinorVersion"]) == int(second["MinorVersion"]) and int(first["PatchVersion"]) < int(second["PatchVersion"]):
                return True
        return False

    @log_method
    def get_distro_os(self):
        res = self.native_command.get_distro_os_and_version
        if not res["IsSuccess"]:
            raise Exception(res["ErrorMessage"])
        distro_os = res["Data"]["os"].lower
        if distro_os not in LINUX_DISTROS["DEB"]:
            if distro_os not in LINUX_DISTROS["RPM"]:
                raise Exception(self.cm["UNSUPPORTED_DISTRO"].formatdistro_os)
        return distro_os

    @log_method
    def download_package_version_from_server(self, agent_key, mode, distro_os, version_from_server):
        token = self.get_token_to_download_packageagent_keymode
        download_package_version = self.local_db.get_download_package_version
        if download_package_version is None:
            self.download_package_from_serverdistro_ostoken
        else:
            if not self.is_first_version_less_or_equals_second_versionversion_from_serverdownload_package_version:
                self.download_package_from_serverdistro_ostoken
            else:
                if not os.path.existsCONFIG["PATH_TO_PACKAGE"]:
                    self.download_package_from_serverdistro_ostoken

    @log_method
    def get_token_to_download_package(self, agent_key, mode):
        return base64.b64encode"{0}|Pranas.NET|{1}".formatagent_keymode.encode"utf-8".decode"utf-8"

    @log_method
    def download_package_from_server(self, distro_os, token):
        if distro_os in LINUX_DISTROS["DEB"]:
            self.download_deb_package_by_tokentoken
        else:
            if distro_os in LINUX_DISTROS["RPM"]:
                self.download_rpm_package_by_tokentoken
            else:
                raise Exception(self.cm["UNSUPPORTED_DISTRO"].formatdistro_os)

    @log_method
    def download_deb_package_by_token(self, token):
        arch = self.native_command.get_debian_arch
        if arch == "amd64":
            res = self.helper.download_package_from_server"sqlbak.deb"token
        else:
            try:
                res = self.helper.download_package_from_server"sqlbak_{}.deb".formatarchtoken
            except Exception as e:
                try:
                    log_error(e, "Can't download pacjage for architecture: {}".formatarch)
                    res = self.helper.download_package_from_server"sqlbak_{}.deb".formatarchtoken
                finally:
                    e = None
                    del e

            else:
                if not res["IsSuccess"]:
                    raise Exception(res["ErrorMessage"])

    @log_method
    def download_rpm_package_by_token(self, token):
        res = self.helper.download_package_from_server"sqlbak.rpm"token
        if not res["IsSuccess"]:
            raise Exception(res["ErrorMessage"])

    @log_method
    def install_download_package(self, distro_os, server_params, version_from_server, mode):
        if not os.path.existsCONFIG["PATH_TO_PACKAGE"]:
            raise Exception(self.cm["ABSENT_DOWNLOAD_PACKAGE"])
        else:
            self.local_db.add_downloaded_package_versionjson.dumps{"version": version_from_server}
            if mode == UPDATE_APP_SOURCES["AUTO"]:
                if not self.check_if_app_can_be_updatedserver_params:
                    raise UpdateIsNotPossibleNow
            else:
                grant_777_access(CONFIG["PATH_TO_PACKAGE"])
                if distro_os in LINUX_DISTROS["DEB"]:
                    self.install_deb_package
                else:
                    if distro_os in LINUX_DISTROS["RPM"]:
                        self.install_rpm_package
                    else:
                        raise Exception(self.cm["UNSUPPORTED_DISTRO"].formatdistro_os)

    @log_method
    def install_deb_package(self):
        self.native_command.install_deb_package

    @log_method
    def install_rpm_package(self):
        self.helper.remove_file_or_dir["/bin/sqlbak"]
        self.native_command.install_rpm_package

    @log_method
    def restart_service(self, mode):
        self.trace_event.trace_restart_servicemode
        self.native_command.restart_sqlbak_service

    @log_method
    def check_if_app_can_be_updated(self, server_params):
        """

        :param server_params:
        :return:
        """
        should_wait_jobs_end = False
        should_check_active_mode = False
        if server_params is not None:
            should_wait_jobs_end = bool(server_params["WaitForJobs"])
            should_check_active_mode = bool(server_params["WaitForSilentMode"])
        are_jobs_run_soon = self.are_there_jobs_run_soon
        is_not_active_mode = not should_check_active_mode or self.helper.get_pin_interval == PIN_INTERVAL
        no_running_jobs = not should_wait_jobs_end or not self.are_there_running_jobs
        return is_not_active_mode and not are_jobs_run_soon and no_running_jobs

    @log_method
    def are_there_jobs_run_soon(self):
        are_there_jobs_run_soon = False
        for job in self.local_db.get_jobs:
            if self.plain_job.is_job_run_soonjob["ScheduleInfo"]:
                are_there_jobs_run_soon = True
            return are_there_jobs_run_soon

    @log_method
    def are_there_running_jobs(self):
        """

        :return:
        """
        is_job_run = False
        for p in self.local_db.get_processes_by_typePROCESS_TYPES["BACKUP"]:
            if is_process_running_now(p["Pid"]):
                is_job_run = True
                break
            return is_job_run

    @log_method
    def is_first_version_less_or_equals_second_version(self, first, second):
        """

        :param first:
        :param second:
        :return:
        """
        if self.is_first_version_less_then_second_versionfirstsecond:
            return True
        if int(first["MajorVersion"]) == int(second["MajorVersion"]):
            if int(first["MinorVersion"]) == int(second["MinorVersion"]):
                if int(first["PatchVersion"]) == int(second["PatchVersion"]):
                    return True
        return False

    @log_method
    def stop_service(self):
        self.native_command.stop_sqlbak_service
