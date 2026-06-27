from sqlbak.trace_event import trace_app_error
from sqlbak.local_db import LocalDB
from setproctitle import setproctitle
from sqlbak.logger import log_data, log_error, log_method, log_module_method_debug, logger_handler, log_module_method
from sqlbak.definitions import APP_NAME, SEVERITY_PARAMS
from sqlbak.definitions import PROCESS_TYPES, BACKUP_JOB_MODE
import psutil, time, os
from sqlbak.app_output import APP_OUTPUT
SUBSERIVICE_TITLE_PREFIX = APP_NAME + "-"
SUBSERIVICE_TITLE_POSTFIX = "-service"

def make_subservice_title(subtask_name):
    return SUBSERIVICE_TITLE_PREFIX + subtask_name + SUBSERIVICE_TITLE_POSTFIX


def is_subservice_service_process_title(process_title):
    return process_title and process_title.startswith(SUBSERIVICE_TITLE_PREFIX) and process_title.endswith(SUBSERIVICE_TITLE_POSTFIX)


@log_module_method_debug
def set_subservice_title(sub_service_name):
    try:
        setproctitle(make_subservice_title(sub_service_name))
    except Exception as e:
        try:
            logger_handler.log_error(set_subservice_title, e)
        finally:
            e = None
            del e


@log_module_method_debug
def is_exist_service_subprocess(pid):
    return psutil.pid_exists(pid) and is_subservice_service_process_title(psutil.Process(pid).name())


@log_module_method
def cleanup_lost_backup_logs(jobHandler):
    """
    A method to get lost backup logs
    :return:
    """
    agent = jobHandler.local_db.get_current_agent()
    if agent is None:
        return
    for backup in jobHandler.local_db.get_unfinished_backup_job():
        if not is_process_with_main_id_running(backup["Id"], jobHandler.local_db):
            if backup["RemoteId"] is not None:
                if not (is_process_with_main_id_running(backup["RemoteId"], jobHandler.local_db) or is_process_with_main_id_running(backup["JobId"], jobHandler.local_db)):
                    try:
                        if time.time() - time.mktime(time.strptime(backup["StartTime"], "%Y-%m-%d %H:%M:%S.%f")) > 82800:
                            trace_app_error('Incomplete backup detected with invalid pid. BackupId:"{}", BackupRemouteId:"{}", Process: "{}"'.format(backup["Id"], backup["RemoteId"], jobHandler.local_db.get_all_process()))
                            job_info = jobHandler.local_db.get_job_by_id(backup["JobId"])
                            if job_info is not None:
                                backup_settings = jobHandler.get_backup_settings(backup, agent["AgentKey"])
                                jobHandler.job_log.send_error_log_local({'BackupRemoteId':backup["RemoteId"], 
                                 'BackupId':backup["Id"], 
                                 'Severity':SEVERITY_PARAMS["Error"], 
                                 'IsConsoleMode':False, 
                                 'IsSilentMode':True}, jobHandler.cm["INTERRUPTED_JOB"])
                                jobHandler.send_unsend_backup_logs(backup_settings["BackupId"], backup_settings["JobMode"])
                                jobHandler.end_job(backup_settings)
                            time.sleep(15)
                    except Exception as e:
                        try:
                            jobHandler.trace_event.failed_run_logs_collector('Failed to handle unsent backup logs - "{0}"'.format(str(e)))
                            time.sleep(300)
                        finally:
                            e = None
                            del e


@log_module_method
def is_process_running(item_id, local_db):
    is_run = False
    for process in local_db.get_process(item_id, PROCESS_TYPES["BACKUP"]):
        if is_process_running_now(process["Pid"]):
            is_run = True
            break
        return is_run


@log_module_method
def is_process_running_nowParse error at or near `SETUP_FINALLY' instruction at offset 0


@log_module_method
def is_process_with_main_id_running(item_id, local_db):
    try:
        is_run = False
        for process in local_db.get_process_by_main_id(item_id, PROCESS_TYPES["BACKUP"]):
            if is_process_running_now(process["Pid"]):
                is_run = True
                break
            return             return is_run

    except Exception as e:
        try:
            logger_handler.log_error(is_process_with_main_id_running, e)
        finally:
            e = None
            del e


def delete_all_stopped_process(local_db):
    for process in local_db.get_all_process():
        if not is_process_running_now(process["Pid"]):
            local_db.delete_process_by_pid(process["Pid"])


@log_module_method
def get_env_for_invoke_system_commandParse error at or near `SETUP_FINALLY' instruction at offset 0
