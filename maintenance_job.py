from sqlbak.definitions import FULL_BACKUP_CONST
from sqlbak.helper import Helper
from sqlbak.logger import log_method
from sqlbak.job import Job
from sqlbak.dbms.dbms import DBMS
from sqlbak.violation import Violation
from sqlbak.helpers.temporary_directory import create_directory

class MaintenanceJob(Job):

    def __init__(self):
        self.helper = Helper()
        Job.__init__(self)

    @log_method
    def handle_maintenance_job(self, job_params):
        is_success_job = False
        try:
            try:
                self.callback(job_params)
                self.get_initial_settings(job_params)
                self.begin_job()
                self.set_job_settings()
                violation = Violation(self.params["UserFullName"])
                violation.check_job_plan_violation(job_params["JobId"])
                create_directory(self.params["PathToBackup"])
                self.run_maintenance_job()
                is_success_job = True
            except Exception as e:
                try:
                    self.catch_job_error(str(e))
                finally:
                    e = None
                    del e

        finally:
            self.send_unsend_backup_logs(self.params["BackupId"], self.params["JobMode"])
            self.end_job()

        return is_success_job

    @log_method
    def run_maintenance_job(self):
        self.params = self.job_log.start_maintenance_job_log(self.params)
        dbms = DBMS(self.params)
        dbms.run_scripts_before_backup()

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/maintenance_job.pyc
