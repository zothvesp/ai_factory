from sys import maxsize
from sqlalchemy import true
from sqlbak.exchange_message.remote_server_requests import RemoteServerRequest
from sqlbak.definitions import CONFIG, DESTINATIONS_NAMES, FEATURES, DESTINATION_FEATURES
from sqlbak.local_db import LocalDB
from sqlbak.helper import Helper
import xml.etree.ElementTree as Et
from sqlbak.logger import log_method
from sqlbak.app_output import APP_OUTPUT

class Violation:
    database_limit = maxsize

    def __init__(self, account_name):
        self.local_db = LocalDB()
        self.remote_request = RemoteServerRequest()
        self.helper = Helper()
        self.account_name = account_name
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]
        self.error_messages = []

    @log_method
    def check_job_plan_violation(self, job_id):
        try:
            job_plan_violation_data = self.get_job_violation_data(job_id)
            self.local_db.add_job_plan_violation(job_plan_violation_data)
            self.get_messages_from_violation_data(job_plan_violation_data)
        except Exception as e:
            try:
                raise Exception("Your account is temporarily suspended due to an unpaid invoice. Please check your SqlBak account https://sqlbak.com/account/billing for more details. Job execution error: {0}".format(e))
            finally:
                e = None
                del e

        else:
            if len(self.error_messages) > 0:
                raise Exception(self.cm["INVALID_VIOLATION_PLAN"].format(" | ".join(self.error_messages)))

    @log_method
    def get_job_violation_dataParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_method
    def can_backup_database(self, database_index):
        if self.database_limit < database_index:
            raise Exception(self.cm["DATABASE_COUNT_EXCESS"].format(database_index, self.database_limit))

    @log_method
    def get_local_violation_data(self):
        violation_data = self.local_db.get_job_plan_violation_data
        if violation_data is not None:
            return self.helper.decrypt_string(violation_data)

    @log_method
    def get_messages_from_violation_data(self, job_plan_violation_data):
        for root in Et.fromstring(job_plan_violation_data.encode("utf-16")):
            if root.tag == "Plan":
                if self.check_account(root):
                    self.check_count_allowed_servers(root)
                    self.check_count_allowed_databases(root)
                return                 return None
        else:
            for root in Et.fromstring(job_plan_violation_data.encode("utf-16")):
                if root.tag == "Job":
                    for child in root:
                        if child.tag == "Features":
                            self.check_violation_job_features(child)
                        elif child.tag == "Destinations":
                            self.check_violation_job_destinations(child)

    @log_method
    def check_account(self, plan):
        if not plan.attrib["IsAllowed"]:
            name = plan.attrib["Name"] if "Name" in plan.attrib else None
            if name is not None:
                self.error_messages.append(self.cm["INCORRECT_PLAN_WITH_NAME"].format(name, self.account_name))
            else:
                self.error_messages.append(self.cm["INCORRECT_PLAN_WITHOUT_NAME"].format(self.account_name))
            return False
        return True

    @log_method
    def check_count_allowed_servers(self, plan):
        server_limit = plan.attrib["ServerLimit"]
        if len(plan) > 0:
            count = plan[0]
            server_count = count.attrib["ServerCount"]
            if int(server_limit) < int(server_count):
                self.error_messages.append(self.cm["SERVER_COUNT_EXCESS"].format(server_count, server_limit))

    @log_method
    def check_count_allowed_databases(self, plan):
        self.database_limit = int(plan.attrib["DatabaseLimit"])
        count = plan[0]
        database_count = int(count.attrib["DatabaseCount"])
        if self.database_limit < database_count:
            self.error_messages.append(self.cm["DATABASE_COUNT_EXCESS"].format(database_count, self.database_limit))

    @log_method
    def check_violation_job_features(self, features):
        for f in features:
            if self.helper.is_text_true(f.attrib["IsUsed"]):
                self.helper.is_text_true(f.attrib["IsAllowed"]) or self.error_messages.append(self.cm["FEATURE_EXCESS"].format(FEATURES[int(f.attrib["Id"])]))

    @log_method
    def check_violation_job_destinations(self, destinations):
        for d in destinations:
            dest_type = DESTINATIONS_NAMES[int(d.attrib["Type"])]
            is_used = self.helper.is_text_true(d.attrib["IsUsed"])
            is_allowed = self.helper.is_text_true(d.attrib["IsAllowed"])
            if not is_allowed:
                if is_used:
                    dest_name = self.get_destination_name_by_id(d.attrib["Id"], dest_type)
                    self.error_messages.append(self.cm["DESTINATION_NOT_ALLOWED"].format(dest_type, dest_name))
                    self.check_violation_job_destination_features(d, dest_type, dest_name)

    @log_method
    def get_destination_name_by_id(self, id, dest_type):
        destination = self.local_db.get_destination_by_id(id)
        if destination is None:
            self.error_messages.append(self.cm["DESTINATION_IS_ABSENT"].format(dest_type))
            name = ""
        else:
            name = destination["DestinationName"]
        return name

    @log_method
    def check_violation_job_destination_features(self, destination, dest_type, name):
        for features in destination:
            for f in features:
                feature_name = DESTINATION_FEATURES[f.attrib["Id"]]
                is_used = self.helper.is_text_true(f.attrib["IsUsed"])
                is_allowed = self.helper.is_text_true(f.attrib["IsAllowed"])
                if is_used:
                    is_allowed or self.error_messages.append(self.cm["DESTINATION_FEATURE_NOT_ALLOWED"].format(feature_name, dest_type, name))
