import time
from datetime import datetime
from operator import itemgetter
import xml.etree.ElementTree as Et
import os
from calendar import monthrange
from sqlbak.helpers.strings import get_attribute_value
from sqlbak.config.log_settings import reload_log_settings
from sqlbak.helper import Helper
from sqlbak.definitions import CONFIG, FULL_BACKUP_CONST, JOB_TYPES, BACKUP_JOB_MODE, PROCESS_TYPES, MINUTE_IN_SEC, SEC_IN_MILLISECOND, BACKUP_TYPES
from sqlbak.backup_job import BackupJob
from sqlbak.maintenance_job import MaintenanceJob
from sqlbak.local_db import LocalDB
from sqlbak.trace_event import TraceEvent
from sqlbak.exchange_message.remote_server_requests import RemoteServerRequest
from sqlbak.logger import log_data, log_error, log_method, log_only_exception, log_without_raising, log_only_exception_without_raising
from sqlbak.exceptions import JobDoubleRun
from sqlbak.native_command import NativeCommand
from sqlbak.app_output import APP_OUTPUT
from sqlbak.process_managment.helper import set_subservice_title, is_process_running
from sqlbak.exchange_message.remote_server_requests import remoute_server_request_instanse
from sqlbak.exchange_message.throttling import free_error, check_error_throttling, get_error_count

class PlainJob:

    def __init__(self):
        self.native_command = NativeCommand()
        self.local_db = LocalDB()
        self.helper = Helper()
        self.trace_event = TraceEvent()
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]

    @log_only_exception
    def handle_scheduled_jobParse error at or near `SETUP_FINALLY' instruction at offset 0_2

    @log_only_exception
    def should_run(self, current_time, start_at, interval):
        delta = int(current_time) - int(start_at)
        return delta % int(interval) == 0

    @log_only_exception
    def get_schedule_settings(self, schedule_settings, job_id):
        time_format = "%m/%d/%Y %H:%M"
        now = datetime.now
        current_time = self.helper.get_time_in_millisecondsnow.strftimetime_format
        begin_at = self.helper.get_begin_time_with_offset(current_time, now, schedule_settings["begin_at"], time_format)
        end_at = self.helper.get_end_time_with_offset(current_time, now, schedule_settings["end_at"], time_format)
        is_working_day = now.strftime"%A" in schedule_settings["business_days"].split","
        allow_to_run = is_working_day and begin_at <= current_time <= end_at
        return {'current_time':current_time, 
         'start_at':schedule_settings["start_at"], 
         'begin_at':begin_at, 
         'end_at':end_at, 
         'is_working_day':is_working_day, 
         'allow_to_run':allow_to_run}

    @log_method
    def start_job(self, job_id, job_backup_type, job_info):
        backup_type = self.helper.get_backup_type_by_object_typejob_backup_type
        if backup_type is None:
            raise Exception(self.cm["INVALID_BACKUP_TYPE"].formatstr(job_backup_type))
        process = self.helper.run_additional_processself.run_job{'JobId':job_id, 
         'JobBackupType':backup_type, 
         'JobMode':BACKUP_JOB_MODE["SCHEDULE"], 
         'JobInfo':job_info, 
         'MessageId':None, 
         'SendMessage':None, 
         'Message':None, 
         'IsConsoleMode':None}
        process.join0

    def run_jobParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_method
    def handle_job(self, job_params):
        """
        A wrapper method to run a job
        :param job_params: dict
        :return: None;
        """
        if job_params["JobInfo"] is None:
            job_info = self.get_job_infojob_params
        else:
            job_info = job_params["JobInfo"]
        job_type = self.get_job_typejob_info
        job_params["IsMaintenanceJob"] = job_type != JOB_TYPES["BACKUP"]
        self.local_db.update_last_runjob_params["JobId"]
        is_success_job = True
        if job_type == JOB_TYPES["BACKUP"]:
            backup_job = BackupJob()
            is_success_job = backup_job.run_backup_jobjob_params
        else:
            maintenance_job = MaintenanceJob()
            is_success_job = maintenance_job.handle_maintenance_jobjob_params
        return is_success_job

    @log_method
    def get_job_info_by_id(self, job_id):
        job = self.local_db.get_job_by_idjob_id
        if job is None:
            raise Exception(self.cm["INVALID_JOB"].formatjob_id)
        return job["JobInfo"]

    @log_method
    def get_job_info(self, job_params):
        if "JobId" not in job_params:
            raise Exception(self.cm["INVALID_JOB"].formatstr(None))
        return self.get_job_info_by_idjob_params["JobId"]

    @log_only_exception
    def is_job_run_soon(self, schedule_info):
        """

        :param job:
        :return:
        """
        job = self.parse_job_schedule_settingsschedule_info
        now = datetime.now
        time_format = "%m/%d/%Y %H:%M:%S.%f"
        current_time = self.get_current_time_stamp + 3 * SEC_IN_MILLISECOND * MINUTE_IN_SEC
        if "begin_at" in job:
            if job["begin_at"] is not None:
                begin_at = self.helper.get_begin_time_with_offset(current_time, now, job["begin_at"], time_format)
            else:
                begin_at = None
            if "end_at" in job and job["end_at"] is not None:
                end_at = self.helper.get_end_time_with_offset(current_time, now, job["end_at"], time_format)
            else:
                end_at = None
            if "business_days" in job:
                is_working_day = now.strftime"%A" in job["business_days"].split","
                if not is_working_day:
                    return False
        elif begin_at is None or current_time < begin_at:
            return False
        if end_at is None or current_time > end_at:
            return False
        next_start = self.simple_calc_next_start_timejob["schedules"]job["start_at"]
        if next_start - current_time < 5 * SEC_IN_MILLISECOND * MINUTE_IN_SEC:
            return True
        return False

    @log_method
    def get_current_time_stamp(self):
        return self.helper.get_time_in_millisecondsdatetime.now.strftime"%m/%d/%Y %H:%M:%S.%f"

    @log_method
    def simple_calc_next_start_time(self, schedules, start_at):
        try:
            result = None
            current_time = self.get_current_time_stamp
            delta = current_time - start_at
            for x in schedules:
                interval = x["interval"]
                full_cycle = delta // int(interval)
                next_start = int(start_at) + interval * (full_cycle + 1)
                if result is None or result > next_start:
                    result = next_start
                next_start_time = datetime.fromtimestamp(result / 1000.0)
                log_data("NextStart:" + str(next_start_time))
                return                 return result

            except Exception as e:
            try:
                log_error(e, "Can't calculate next start time")
                raise
            finally:
                e = None
                del e

    @log_only_exception
    def get_job_type(self, job_info):
        job_info_params = Et.fromstringjob_info.encode"utf-16"
        job_type = job_info_params.attrib["JobType"] if "JobType" in job_info_params.attrib else None
        if job_type not in (JOB_TYPES["BACKUP"], JOB_TYPES["MAINTENANCE"]):
            raise Exception(self.cm["INCORRECT_JOB_TYPE"].formatstr(job_type))
        return job_type

    @log_only_exception
    def parse_job_schedule_settings(self, schedule_info):
        schedule_settings = self.parse_schedule_xmlschedule_info
        is_scheduled = self.helper.is_text_trueschedule_settings.attrib["Enabled"] if "Enabled" in schedule_settings.attrib else False
        is_month_days_enabled = self.helper.is_text_trueschedule_settings.attrib["MonthDaysEnabled"] if "MonthDaysEnabled" in schedule_settings.attrib else False
        if not is_scheduled:
            return {"is_scheduled": False}
        schedules = []
        business_time = {'end_at':None, 
         'begin_at':None}
        business_days = ""
        month_days = []
        for root in schedule_settings:
            if root.tag == "BusinessDays":
                business_days = self.get_business_daysroot
            if root.tag == "DailyBulinessTime":
                business_time = self.get_business_timerootbusiness_time
            if root.tag == "FullBackup":
                schedules = self.get_full_backup_type_datarootschedules
            if root.tag == "DiffBackup":
                schedules = self.get_diff_backup_type_datarootschedules
            if root.tag == "LogTranBackup":
                schedules = self.get_log_backup_type_datarootschedules
            if root.tag == "IncrementalBackup":
                schedules = self.get_inc_backup_type_datarootschedules
            start_at = self.helper.get_time_in_millisecondsschedule_settings.attrib["StartAt"]
            if "MonthDays" in schedule_settings.attrib:
                month_days = schedule_settings.attrib["MonthDays"].split","
            return {'is_scheduled':is_scheduled, 
             'business_days':business_days, 
             'schedules':schedules, 
             'begin_at':business_time["begin_at"], 
             'end_at':business_time["end_at"], 
             'start_at':(self.helper.get_time_with_offset)start_at, 
             'is_month_days_enabled':is_month_days_enabled, 
             'month_days':month_days}

    @log_only_exception
    def parse_schedule_xml(self, schedule_info):
        return Et.fromstringschedule_info.encode"utf-16"

    @log_only_exception
    def get_business_days(self, root):
        return ",".join[child.attrib["DayOfWeek"] for child in root if child.tag == "BusinessDay"]

    @log_only_exception
    def get_business_time(self, root, business_time):
        for child in root:
            if child.tag == "Interval":
                business_time.update{'begin_at':child.attrib["BeginAt"] if ("BeginAt" in child.attrib) else None, 
                 'end_at':child.attrib["EndAt"] if ("EndAt" in child.attrib) else None}
            return business_time

    @log_only_exception
    def get_full_backup_type_data(self, root, schedules):
        if "Enabled" in root.attrib:
            if self.helper.is_text_trueroot.attrib["Enabled"]:
                interval = int(root.attrib["Interval"]) * MINUTE_IN_SEC * SEC_IN_MILLISECOND
                schedules.append{'type':BACKUP_TYPES["FULL"],  'interval':interval}
        return schedules

    @log_only_exception
    def get_diff_backup_type_data(self, root, schedules):
        if "Enabled" in root.attrib:
            if self.helper.is_text_trueroot.attrib["Enabled"]:
                interval = int(root.attrib["Interval"]) * MINUTE_IN_SEC * SEC_IN_MILLISECOND
                schedules.append{'type':BACKUP_TYPES["DIFF"],  'interval':interval}
        return schedules

    @log_only_exception
    def get_log_backup_type_data(self, root, schedules):
        if "Enabled" in root.attrib:
            if self.helper.is_text_trueroot.attrib["Enabled"]:
                interval = int(root.attrib["Interval"]) * MINUTE_IN_SEC * SEC_IN_MILLISECOND
                schedules.append{'type':BACKUP_TYPES["LOG"],  'interval':interval}
        return schedules

    @log_only_exception
    def get_inc_backup_type_data(self, root, schedules):
        if "Enabled" in root.attrib:
            if self.helper.is_text_trueroot.attrib["Enabled"]:
                interval = int(root.attrib["Interval"]) * MINUTE_IN_SEC * SEC_IN_MILLISECOND
                schedules.append{'type':BACKUP_TYPES["INC"],  'interval':interval}
        return schedules

    @log_without_raising
    def remove_cron_taks(self):
        self.local_db.remove_job_schedules
        self.native_command.remove_all_cron_tasks

    @log_only_exception
    def check_scheduled_jobs(self):
        for job in self.local_db.get_jobs:
            if int(job["IsScheduled"]) == 1:
                if job["CheckAt"] == datetime.now.strftime"%m/%d/%Y %H:%M":
                    pass
                else:
                    self.local_db.update_job_check_datetimejob["JobId"]
                    self.handle_scheduled_jobjob

    @log_method
    def check_month_days(self, month_days):
        now = datetime.now
        is_month_day = False
        if "*" in month_days:
            is_month_day = True
        else:
            for m in month_days:
                days_range = m.split"-"
                if len(days_range) > 1:
                    if self.check_days_rangenowdays_range:
                        is_month_day = True
                        break
                elif m == "L":
                    if now.day == self.get_number_days_in_monthnow:
                        is_month_day = True
                        break
                    elif now.day == int(m):
                        is_month_day = True
                        break
                else:
                    return is_month_day

    @log_method
    def get_number_days_in_month(self, now):
        number_days_in_month = monthrange(now.year, now.month)
        return int(number_days_in_month[1])

    @log_method
    def check_days_range(self, now, days_range):
        is_month_day = False
        first_sign = "L"
        for idx, d in enumerate(days_range):
            if idx == 0:
                first_sign = d
            elif first_sign == "L":
                if now.day == self.get_number_days_in_monthnow - int(d):
                    is_month_day = True
                    break
            else:
                days = list(range(int(first_sign), int(d)))
                days.appendint(d)
                if now.day in days:
                    is_month_day = True
                    break
                else:
                    return is_month_day
