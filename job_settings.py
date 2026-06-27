
import os, re
import xml.etree.ElementTree as Et
from datetime import datetime
from operator import itemgetter
from sqlbak.app_output import APP_OUTPUT
from sqlbak.dbms.dbms import DBMS
from sqlbak.destinations.destination import Destination
from sqlbak.exchange_message.helper import IsIntensiveMode
from sqlbak.exchange_message.remote_server_requests import RemoteServerRequest
from sqlbak.helper import Helper
from sqlbak.job_log import JobLog
from sqlbak.local_db import LocalDB
from sqlbak.logger import log_method
from sqlbak.definitions import COMPRESSION_LEVEL_DEFAULT, COMPRESSION_ENGINE_ZIP, MAX_BACKUP_SIZE, M_BIT, MINUTE_IN_SEC, INC_BACKUP_CONST, FULL_BACKUP_CONST, OPERATION_SHORT_CODE_JOB, POSTGRES_BACKUP_FORMATS, POSTGRESQL_CONST, SEVERITY_PARAMS, COMPRESSION_PRIORITY_DEFAULT, PROCESS_TYPES, DBMS_TYPES_CONSTS, E7Zip_EXT, MARIADB_CONST, HOUR_IN_MINUTES, SQL_SCRIPT_TYPE, CMD_SCRIPT_TYPE, BROKEN_BACKUP_BEHAVIOR, CONFIG, ZIP_EXT, MYSQL_CONST, SCRIPTS_TIMEOUT_DEFAULT, XTRABACKUP_CONST
from sqlbak.helpers.files import get_archive_ext
from sqlbak.helpers.temporary_directory import create_temp_dir

class JobSettings:

    def __init__(self):
        self.local_db = LocalDB()
        self.job_log = JobLog()
        self.remote_request = RemoteServerRequest()
        self.count_job_errors = 0
        self.params = {}
        self.helper = Helper()
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]

    @log_method
    def get_initial_job_settings(self, params):
        try:
            message_id = int(params["MessageId"]) if params["MessageId"] is not None else params["MessageId"]
            job = self.local_db.get_job_by_id(params["JobId"])
            backup = self.local_db.add_backup(params["JobId"], params["JobBackupType"], message_id)
            self.local_db.add_process(os.getpid(), params["JobId"], backup["BackupLastRowId"], PROCESS_TYPES["BACKUP"])
            agent = self.local_db.get_current_agent()
            path_to_temporarry_dir = create_temp_dir(params["JobId"], OPERATION_SHORT_CODE_JOB)
            initial_params = {'AgentKey':agent["AgentKey"], 
             'BackupAt':(datetime.now)(), 
             'PathToBackup':path_to_temporarry_dir, 
             'MessageId':message_id, 
             'JobId':int(params["JobId"]), 
             'JobMode':str(params["JobMode"]), 
             'BackupId':backup["BackupLastRowId"], 
             'BackupKey':backup["BackupKey"], 
             'BackupType':params["JobBackupType"], 
             'JobBackupType':params["JobBackupType"], 
             'JobCredentialsId':job["JobCredentialsId"], 
             'JobInfo':job["JobInfo"], 
             'CountJobErrors':0, 
             'JobName':job["JobName"], 
             'IsConsoleMode':params["IsConsoleMode"], 
             'IsEncryptionEnabled':None, 
             'ObjectBackupResults':[],  'Databases':[],  'Severity':SEVERITY_PARAMS["Info"], 
             'IsSilentMode':not (IsIntensiveMode()), 
             'BackupTypeForTrigger':None, 
             'FreeFolderSpace':(self.helper.get_client_free_space)(path_to_temporarry_dir), 
             'GeneralArchiveSize':0, 
             'GeneralSize':0, 
             'IsMaintenanceJob':params["IsMaintenanceJob"]}
            job_info = Et.fromstring(job["JobInfo"].encode("utf-16"))
            for root in job_info:
                if root.tag == "EmailInfo":
                    email_params = self.set_email_settings(root)
                    initial_params.update(email_params)
                return                 return initial_params

            except Exception as e:
            try:
                self.local_db.delete_process(params["JobId"], PROCESS_TYPES["BACKUP"])
                raise Exception(self.cm["FAILED_SET_JOB_SETTINGS"].format(str(e)))
            finally:
                e = None
                del e

    @log_method
    def get_job_settings(self, params):
        """

        :param params:
        :return:
        """
        self.params = params
        self.set_agent_settings()
        self.set_connection_settings()
        self.set_job_info_settings()
        if not self.params["IsMaintenanceJob"]:
            self.set_destination_settings()
            self.set_job_triggers()
            self.set_backup_settings()
        return self.params

    @log_method
    def set_agent_settings(self):
        """
        A method to get an agent settings
        :return: None
        """
        agent = self.local_db.get_current_agent()
        self.params.update({'UserFullName':agent["AccountName"], 
         'ClientName':agent["AgentName"], 
         'ClientVersion':(str(agent["MajorVersion"]) + "." + str(agent["MinorVersion"]) + ".") + (str(agent["PatchVersion"])), 
         'UtilsPath':agent["UtilsPath"], 
         'AgentId':agent["AgentId"]})

    @log_method
    def set_connection_settings(self):
        """
        A method to get a host connection settings by JobCredentialsId.
        Method may raise an exception if a connection will not be find
        :return: None
        """
        connection = self.local_db.get_connection_by_job_cred_id(self.params["JobCredentialsId"])
        if connection is None:
            raise Exception(self.cm["CONNECTION_NOT_FOUND"].format(self.params["JobCredentialsId"]))
        self.params.update(connection)
        if self.params["BackupUtil"] == XTRABACKUP_CONST:
            self.params["ServerType"] = XTRABACKUP_CONST

    @log_method
    def set_job_info_settings(self):
        """
        A method to parse xml and get job info settings
        :param job: xml
        :return: None
        """
        job_info = Et.fromstring(self.params["JobInfo"].encode("utf-16"))
        self.params.update({'BackupOneAndSend':True if ("LocalStorageMethod" in job_info.attrib) else False, 
         'IsBackupToSubFolders':self.helper.is_text_true(job_info.attrib["IsBackupToSubFolders"]) if ("IsBackupToSubFolders" in job_info.attrib) else False, 
         'JobType':job_info.attrib["JobType"], 
         'FileNameFormat':job_info.attrib["OutputFileNameFormat"] if ("OutputFileNameFormat" in job_info.attrib) else "DateAndTime"})
        for root in job_info:
            if root.tag == "DatabaseBackupInfo":
                self.set_database_settings(root)
            elif root.tag == "FolderBackupInfo":
                self.set_folder_settings(root)
            elif root.tag == "CompressionInfo":
                self.set_compression_settings(root)
                self.set_compression_extension_settings()
            elif root.tag == "JobScripts":
                self.set_job_scripts_settings(root)

    @log_method
    def set_database_settings(self, backup_info):
        """
        A method to parse xml and get a database backup info
        :param backup_info: xml
        :return: None
        """
        for child in backup_info:
            if child.tag == "AllNonSystemDatabases" and child.text:
                self.params["AllNonSystemDatabases"] = self.helper.is_text_true(child.text)
            elif child.tag == "DbTimeout" and child.text:
                self.params["DbTimeout"] = int(child.text)
            elif child.tag == "BackupOptions":
                self.set_azure_settings(child)
                self.set_mysql_settings(child)
                self.set_mssql_settings(child)
                self.set_postgresql_settings(child)
            elif child.tag == "DatabaseBackupConditions":
                self.check_database_backup_conditions(child)
            elif child.tag == "Databases":
                self.params["Databases"] = [ch.text.strip() for ch in child if ch.tag == "Database" if ch.text]
        else:
            if child.tag == "ExcludeDatabases":
                self.params["ED"] = [ch.text for ch in child if ch.tag == "Database" if ch.text]
            if "AllNonSystemDatabases" in self.params:
                if self.params["AllNonSystemDatabases"]:
                    dbms = DBMS(self.params)
                    for d in dbms.get_non_system_databases():
                        if d and d not in self.params["Databases"]:
                            match_found = False
                        for x in self.params["ED"]:
                            if re.search(x, d):
                                match_found = True
                                break
                            if not match_found:
                                self.params["Databases"].append(d)

    @log_method
    def set_azure_settings(self, child):
        self.params.update({"Azure_CreateSnapshot": (self.helper.is_text_true(child.attrib["CreateSnapshot"]) if "CreateSnapshot" in child.attrib else False)})

    @log_method
    def set_mysql_settings(self, child):
        self.params.update({'My_SqlUseTransaction':self.helper.is_text_true(child.attrib["SqlUseTransaction"]) if ("SqlUseTransaction" in child.attrib) else False, 
         'My_LockTables':self.helper.is_text_true(child.attrib["LockTables"]) if ("LockTables" in child.attrib) else True, 
         'My_PasswordInEnv':self.helper.is_text_true(child.attrib["PasswordInEnv"]) if ("PasswordInEnv" in child.attrib) else False, 
         'My_SQLCompatibility':str(child.attrib["SQLCompatibility"]) if ("SQLCompatibility" in child.attrib) else None, 
         'My_SqlColumnStatistics':self.helper.is_text_true(child.attrib["SqlColumnStatistics"]) if ("SqlColumnStatistics" in child.attrib) else None, 
         'My_SQLIncludeComments':self.helper.is_text_true(child.attrib["SQLIncludeComments"]) if ("SQLIncludeComments" in child.attrib) else True, 
         'My_SQLHeaderComment':str(child.attrib["SQLHeaderComment"]) if ("SQLHeaderComment" in child.attrib) else None, 
         'My_ExtraCommandLineParameters':str(child.attrib["ExtraCommandLineParameters"]) if ("ExtraCommandLineParameters" in child.attrib) else None, 
         'My_SqlDropTable':self.helper.is_text_true(child.attrib["SqlDropTable"]) if ("SqlDropTable" in child.attrib) else False, 
         'My_SqlBackQuotes':self.helper.is_text_true(child.attrib["SqlBackQuotes"]) if ("SqlBackQuotes" in child.attrib) else True, 
         'My_SqlProcedureFunction':self.helper.is_text_true(child.attrib["SqlProcedureFunction"]) if ("SqlProcedureFunction" in child.attrib) else False, 
         'My_SqlIfNotExists':self.helper.is_text_true(child.attrib["SqlIfNotExists"]) if ("SqlIfNotExists" in child.attrib) else True, 
         'My_Events':self.helper.is_text_true(child.attrib["Events"]) if ("Events" in child.attrib) else False, 
         'My_NoCreateDatabaseStatement':self.helper.is_text_true(child.attrib["NoCreateDatabaseStatement"]) if ("NoCreateDatabaseStatement" in child.attrib) else True, 
         'My_SqlColumns':self.helper.is_text_true(child.attrib["SqlColumns"]) if ("SqlColumns" in child.attrib) else True, 
         'My_SqlExtended':self.helper.is_text_true(child.attrib["SqlExtended"]) if ("SqlExtended" in child.attrib) else True, 
         'My_SqlIgnore':self.helper.is_text_true(child.attrib["SqlIgnore"]) if ("SqlIgnore" in child.attrib) else False, 
         'My_SqlHexForBlob':self.helper.is_text_true(child.attrib["SqlHexForBlob"]) if ("SqlHexForBlob" in child.attrib) else True, 
         'My_SqlType':self.helper.is_text_true(child.attrib["SqlType"]) if ("SqlType" in child.attrib) else None, 
         'My_MaxAllowedPacket':int(child.attrib["MaxAllowedPacket"]) if ("MaxAllowedPacket" in child.attrib) else 1024, 
         'My_SqlData':self.helper.is_text_true(child.attrib["SqlData"]) if ("SqlData" in child.attrib) else True, 
         'My_SqlStructure':self.helper.is_text_true(child.attrib["SqlStructure"]) if ("SqlStructure" in child.attrib) else True})

    @log_method
    def set_mssql_settings(self, child):
        self.params.update({'BrokenChainBehavior':str(child.attrib["BrokenChainBehavior"]) if ("BrokenChainBehavior" in child.attrib) else (BROKEN_BACKUP_BEHAVIOR["WARNING"]), 
         'MS_NativeBackupCompression':str(child.attrib["NativeBackupCompression"]) if ("NativeBackupCompression" in child.attrib) else None, 
         'MS_IsCopyOnly':self.helper.is_text_true(child.attrib["CopyOnly"]) if ("CopyOnly" in child.attrib) else False, 
         'MS_VerifyAfterBackup':self.helper.is_text_true(child.attrib["VerifyAfterBackup"]) if ("VerifyAfterBackup" in child.attrib) else False, 
         'MS_EnableCheckSum':self.helper.is_text_true(child.attrib["EnableCheckSum"]) if ("EnableCheckSum" in child.attrib) else False})

    @log_method
    def set_postgresql_settings(self, child):
        self.params["PS_PARAMS"] = {'--data-only':self.helper.is_text_true(child.attrib["DataOnly"]) if ("DataOnly" in child.attrib) else False, 
         '--schema-only':self.helper.is_text_true(child.attrib["SchemaOnly"]) if ("SchemaOnly" in child.attrib) else False, 
         '--lock-wait-timeout':int(child.attrib["LockWaitTimeout"]) if ("LockWaitTimeout" in child.attrib) else 30000, 
         '--clean':self.helper.is_text_true(child.attrib["Clean"]) if ("Clean" in child.attrib) else True, 
         '--if-exists':self.helper.is_text_true(child.attrib["IsExists"]) if ("IsExists" in child.attrib) else True, 
         '--create':self.helper.is_text_true(child.attrib["Create"]) if ("Create" in child.attrib) else False, 
         '--oids':self.helper.is_text_true(child.attrib["Oids"]) if ("Oids" in child.attrib) else True, 
         '--no-owner':self.helper.is_text_true(child.attrib["NoOwner"]) if ("NoOwner" in child.attrib) else False, 
         '--no-privileges':self.helper.is_text_true(child.attrib["NoPrivileges"]) if ("NoPrivileges" in child.attrib) else True, 
         '--custom-arguments':str(child.attrib["CustomArgument"]) if ("CustomArgument" in child.attrib) else None, 
         '--format':POSTGRES_BACKUP_FORMATS[child.attrib["PgDumpFileFormat"]] if ("PgDumpFileFormat" in child.attrib) else (POSTGRES_BACKUP_FORMATS["Plain"])}

    @log_method
    def check_database_backup_conditions(self, conditions):
        """

        :param conditions:
        :return:
        """
        for condition in conditions:
            if condition.tag == "DatabaseStateBackupAction":
                self.params.update({'DatabaseState':None, 
                 'BackupCommand':condition.attrib["BackupCommand"] if ("BackupCommand" in condition.attrib) else None})
            for states in condition:
                if states.tag == "DatabaseStates":
                    for state in states:
                        self.params.update({"DatabaseState": (state.text)})

    @log_method
    def set_folder_settings(self, folder_info):
        """
        A method to parse xml and get folder backup info
        :param folder_info: xml
        :return: None
        """
        self.params["IsFolderBackupEnabled"] = self.helper.is_text_true(folder_info.attrib["Enabled"]) if "Enabled" in folder_info.attrib else True
        if self.params["IsFolderBackupEnabled"]:
            for child in folder_info:
                if child.tag == "IncludeMasks":
                    self.params["FolderBackupsIncludeMasks"] = [c.text for c in child]
                elif child.tag == "ExcludeMasks":
                    self.params["FolderBackupsExcludeMasks"] = [c.text for c in child]
                elif child.tag == "Folders":
                    self.params["FolderBackups"] = [{'path':f.attrib["Path"], 
                     'name':f.attrib["Name"],  'file_name':(self.helper.get_backup_file_name)(self.params["FileNameFormat"], f.attrib["Name"], self.params["BackupAt"])} for f in child]
                elif child.tag == "BackupTypes":
                    self.params["FolderBackupTypes"] = [c.attrib["BackupType"] for c in child]

    @log_method
    def set_compression_settings(self, settings):
        self.params.update({'IsCompressionEnabled':True if (self.helper.is_text_true(settings.attrib["IsCompressionEnabled"])) else False, 
         'CompressionLevel':settings.attrib["CompressionLevel"] if ("CompressionLevel" in settings.attrib) else COMPRESSION_LEVEL_DEFAULT, 
         'CompressionMethod':settings.attrib["Method"] if ("Method" in settings.attrib) else "Off", 
         'CompressionPriority':settings.attrib["Priority"] if ("Priority" in settings.attrib) else COMPRESSION_PRIORITY_DEFAULT, 
         'CompressionEngine':settings.attrib["Engine"] if ("Engine" in settings.attrib) else COMPRESSION_ENGINE_ZIP, 
         'CompressionMaxFileSize':int(settings.attrib["MaxFileSize"]) * M_BIT if ("MaxFileSize" in settings.attrib) else MAX_BACKUP_SIZE, 
         'CompressionCommandLineOptions':settings.attrib["CommandLineOptions"] if ("CommandLineOptions" in settings.attrib) else "", 
         'IsEncryptionEnabled':self.helper.is_text_true(settings.attrib["IsEncryptionEnabled"]) if ("IsEncryptionEnabled" in settings.attrib) else False, 
         'CompressionPassword':settings.attrib["Password"], 
         'EncryptionMethod':settings.attrib["EncryptionMethod"], 
         'EncryptionStrength':settings.attrib["EncryptionStrength"] if ("EncryptionStrength" in settings.attrib) else None})

    @log_method
    def set_compression_extension_settings(self):
        backup_extention = get_archive_ext(self.params["CompressionMethod"])
        self.params.update({'CompressedBackupExtension':backup_extention if (self.params["IsCompressionEnabled"]) else None, 
         'CompressedFolderExtension':backup_extention if (self.params["IsCompressionEnabled"]) else ZIP_EXT, 
         'CompressionEngineFolder':self.params["CompressionEngine"] if (self.params["IsCompressionEnabled"]) else COMPRESSION_ENGINE_ZIP})

    @log_method
    def set_email_settings(self, email_info):
        """
        A method to parse xml and get email settings
        :param email_info: xml
        :return:
        """
        params = {}
        params["EmailInfoEnabled"] = True if ("Enabled" in email_info.attrib and self.helper.is_text_true(email_info.attrib["Enabled"])) else False
        for child in email_info:
            if child.tag == "EmailAdvancedSettings":
                params["EmailType"] = child.attrib["EmailType"]
            elif child.tag == "SuccessMail":
                params["SuccessMailAddressTo"] = child.attrib["AddressTo"]
            elif child.tag == "FailureMail":
                params["FailureMailAddressTo"] = child.attrib["AddressTo"]
            elif child.tag == "FailureMailCondition":
                params["FailureMailConditionEnable"] = True if ("Enabled" in child.attrib and self.helper.is_text_true(child.attrib["Enabled"])) else False
                params["FailureMailConditionInterval"] = child.attrib["Interval"] if "Interval" in child.attrib else "00:05:00"
            else:
                if child.tag == "SuccessBackupTypes":
                    params["SuccessBackupTypes"] = [sub_child.attrib["BackupType"] for sub_child in child if sub_child.tag == "BackupType"]
                return params

    @log_method
    def set_job_scripts_settings(self, scripts_info):
        """
        A method to parse xml and get scripts and commands settings
        :param scripts_info: xml
        :return: None
        """
        scripts = []
        for s in scripts_info:
            for entry in s:
                script = [sc.text for sc in entry[0][0] if sc.text]
                scripts.append({'IsSqlScript':entry[0].attrib["ScriptType"] == "Sql", 
                 'IsBeforeBackup':s.tag == "ScriptsBefore", 
                 'Timeout':(self.get_job_scripts_timeout)(entry), 
                 'Script':script})

        else:
            self.params.update({'IsJobScriptEnabled':self.helper.is_text_true(scripts_info.attrib["Enabled"]) if ("Enabled" in scripts_info.attrib) else True, 
             'JobScripts':scripts})

    @log_method
    def get_job_scripts_timeout(self, entry):
        timeout = SCRIPTS_TIMEOUT_DEFAULT
        if "Timeout" in entry.attrib:
            list_time = entry.attrib["Timeout"].split(":")
            timeout = int(list_time[0]) * HOUR_IN_MINUTES * MINUTE_IN_SEC + int(list_time[1]) * MINUTE_IN_SEC + int(list_time[2]) if len(list_time) > 1 else 0
        return timeout

    @log_method
    def set_backup_settings(self):
        """
        A method to get backup settings
        :return: None
        """
        backups = self.get_backups()
        if len(backups) == 0:
            if not self.params["IsFolderBackupEnabled"]:
                raise Exception(self.cm["ABSENT_DATABASES_AND_FOLDERS"])
        self.params["DatabaseBackups"] = backups

    @log_method
    def get_backups(self):
        backups = []
        dbms = DBMS(self.params)
        job = self.local_db.get_job_by_id(self.params["JobId"])
        for database in self.params["Databases"]:
            backup = dbms.get_backup_settings(database, self.params["JobBackupType"])
            last_success_backup = self.get_last_success_backup_data(database)
            if backup["backup_type"] == INC_BACKUP_CONST:
                backup["backup_name"] = self.helper.replace_colon_sign_in_file_name(backup["backup_name"])
            backups.append({'BackupName':backup["backup_name"], 
             'CurrentBackupType':backup["backup_type"], 
             'DatabaseName':str(database), 
             'BackupTypeRaiseType':backup["raise_type"], 
             'BackupTypeRaiseData':backup["raise_data"], 
             'BackupExtension':DBMS_TYPES_CONSTS[self.params["ServerType"]]["native_extention"][self.params["PS_PARAMS"]["--format"]] if (self.params["ServerType"] == POSTGRESQL_CONST) else (DBMS_TYPES_CONSTS[self.params["ServerType"]]["native_extention"][backup["backup_type"]]), 
             'ShouldGetDumpChecksum':(self.search_scheduled_mysql_inc_jobs)(database, backup["backup_type"]), 
             'BackupId':self.params["BackupId"], 
             'PathToPreviousBackup':last_success_backup["PathToBackup"] if (last_success_backup is not None) else None, 
             'PreviousBackupType':last_success_backup["ObjectType"] if (last_success_backup is not None) else None, 
             'BackupWorkingDir':(self.local_db.get_working_dir)(), 
             'BackupJobId':self.params["JobId"], 
             'IsIncBackupEnabled':(self.is_job_scheduled_for_inc)(job["ScheduleInfo"])})
        else:
            return backups

    @log_method
    def get_last_success_backup_data(self, object_name):
        last_success_backup_data = None
        if self.params["ServerType"] == XTRABACKUP_CONST:
            last_success_backup_data = self.local_db.get_last_success_backup_data(self.params["JobId"], object_name)
        return last_success_backup_data

    @log_method
    def set_destination_settings(self):
        destinations = []
        job_destinations = self.local_db.get_job_destinations(self.params["JobId"])
        for d in job_destinations:
            settings = self.get_destination_settings_by_job_id(self.params["JobId"], d["DestinationId"])
            destinations.append(settings)
        else:
            self.params["Destinations"] = sorted(destinations, key=(itemgetter("is_extreme")))

    @log_method
    def get_destination_settings_by_job_id(self, job_id, destination_id):
        """

        :param job_id:
        :param destination_id:
        :return:
        """
        destination = self.local_db.get_destination_and_job_destination(job_id, destination_id)
        d = Destination()
        settings = d.get_destination_settings(destination)
        destination_instance = d.get_destination_instance(settings)
        return {'instance':destination_instance, 
         'settings':settings, 
         'is_extreme':destination["IsExtreme"], 
         'destination_id':destination["DestinationId"]}

    @log_method
    def set_job_triggers(self):
        """

        :return:
        """
        self.params["JobTriggers"] = []
        for trigger in self.local_db.get_job_triggers_by_job_id(self.params["JobId"]):
            trigger_settings = self.get_trigger_settings(trigger["TriggerSettings"])
            self.params["JobTriggers"].append({'DestinationId':trigger_settings["destination_id"], 
             'Databases':trigger_settings["databases"], 
             'BackupTypes':trigger_settings["backup_types"], 
             'TriggerId':trigger["TriggerId"], 
             'JobId':trigger["JobId"], 
             'TriggerTypeId':trigger["TriggerTypeId"], 
             'AgentId':trigger_settings["agent_id"], 
             'JobCredentialsId':trigger_settings["credential_id"], 
             'WaitForComplete':trigger_settings["wait"], 
             'RestoreScripts':trigger_settings["restore_scripts"]})

    @log_method
    def get_trigger_settings(self, trigger):
        trigger_data = Et.fromstring(trigger.encode("utf-16"))
        trigger_params = self.get_trigger_params(trigger_data)
        return {'destination_id':trigger_params["destination_id"], 
         'databases':trigger_params["databases"], 
         'backup_types':trigger_params["backup_types"], 
         'agent_id':trigger_data.attrib["AgentId"], 
         'credential_id':trigger_data.attrib["JobCredentialsId"], 
         'wait':trigger_data.attrib["WaitForComplete"], 
         'restore_scripts':trigger_params["restore_scripts"]}

    @log_method
    def get_trigger_params(self, trigger_data):
        trigger_params = {'destination_id':None, 
         'databases':[],  'backup_types':[],  'restore_scripts':{'ScriptsBefore':[],  'ScriptsAfter':[]}}
        for root in trigger_data:
            if root.tag == "DestitnationId":
                trigger_params["destination_id"] = root.text
            elif root.tag == "Databases":
                trigger_params["databases"] = self.get_databases_for_trigger(root)
            elif root.tag == "BackupTypes":
                trigger_params["backup_types"] = self.get_backup_types_for_trigger(root)
            else:
                if root.tag == "Scripts":
                    trigger_params["restore_scripts"] = self.get_restore_scripts(root)
                return trigger_params

    @log_method
    def get_databases_for_trigger(self, trigger):
        databases = []
        for child in trigger:
            if child.tag == "Database":
                ms_data = self.get_mssql_data_for_trigger(child)
                databases.append({'SourceDb':child.attrib["SourceDatabase"], 
                 'DestinationDb':child.attrib["DestinationDatabase"], 
                 'LocalSqlServerSettings':ms_data})
            return databases

    @log_method
    def get_mssql_data_for_trigger(self, sql_settings):
        ms_data = None
        for option in sql_settings:
            if option.tag == "LocalSqlServerSettings":
                ms_data = {'CheckAfterRestore':self.helper.is_text_true(option.attrib["CheckAfterRestore"]) if ("CheckAfterRestore" in option.attrib) else False,  'VerifyOnly':self.helper.is_text_true(option.attrib["VerifyOnly"]) if ("VerifyOnly" in option.attrib) else False, 
                 'Files':(self.get_mssql_files_for_trigger)(option)}
            return ms_data

    @log_method
    def get_mssql_files_for_trigger(self, mssql_settings):
        mssql_files = []
        for files in mssql_settings:
            if files.tag == "Files":
                for f in files:
                    if f.tag == "File":
                        mssql_files.append({'Type':int(f.attrib["Type"]), 
                         'Name':f.attrib["Name"], 
                         'Path':f.attrib["Path"]})

            return mssql_files

    @log_method
    def get_backup_types_for_trigger(self, trigger):
        backup_types = []
        for child in trigger:
            if child.tag == "BackupType":
                backup_type = self.helper.get_backup_type_for_trigger(child.attrib["BackupType"])
                backup_types.append(backup_type)
            return backup_types

    @log_method
    def get_restore_scripts(self, scripts):
        restore_scripts = {'ScriptsBefore':[],  'ScriptsAfter':[]}
        for script in scripts:
            if script.tag == "ScriptsAfter" or script.tag == "ScriptsBefore":
                for script_after in script:
                    if script_after.tag == "ScriptEntry":
                        timeout = self.get_job_scripts_timeout(script_after)
                    for script_entry in script_after:
                        if script_entry.tag == "CommandScript":
                            script_data = {'ScriptType':SQL_SCRIPT_TYPE if (script_entry.attrib["ScriptType"] == "Sql") else CMD_SCRIPT_TYPE,  'StopOnFailed':True, 
                             'Timeout':timeout, 
                             'Text':[]}
                        for text in script_entry:
                            if text.tag == "Text":
                                for line in text:
                                    if line.tag == "Line":
                                        script_data["Text"].append(line.text)
                                else:
                                    restore_scripts[script.tag].append(script_data)

            return restore_scripts

    @log_method
    def get_job_email_settings(self, job):
        email_settings = {}
        email_info = self.get_email_info(job["JobInfo"])
        email_settings["EmailInfoEnabled"] = True if ("Enabled" in email_info.attrib and self.helper.is_text_true(email_info.attrib["Enabled"])) else False
        for child in email_info:
            if child.tag == "EmailAdvancedSettings":
                email_settings["EmailType"] = child.attrib["EmailType"]
            elif child.tag == "SuccessMail":
                email_settings["SuccessMailAddressTo"] = child.attrib["AddressTo"]
            elif child.tag == "FailureMail":
                email_settings["FailureMailAddressTo"] = child.attrib["AddressTo"]
            elif child.tag == "FailureMailCondition":
                email_settings["FailureMailConditionEnable"] = True if ("Enabled" in child.attrib and self.helper.is_text_true(child.attrib["Enabled"])) else False
                email_settings["FailureMailConditionInterval"] = child.attrib["Interval"]
            else:
                if child.tag == "SuccessBackupTypes":
                    email_settings["SuccessBackupTypes"] = [sub_child.attrib["BackupType"] for sub_child in child if sub_child.tag == "BackupType"]
                return email_settings

    @log_method
    def get_email_info(self, job_info):
        email_info = None
        parsed_job_info = Et.fromstring(job_info.encode("utf-16"))
        for root in parsed_job_info:
            if root.tag == "EmailInfo":
                email_info = root
            if email_info is None:
                raise Exception("Failed to get job email settings")
            return email_info

    @log_method
    def is_database_scheduled_for_mysql_incParse error at or near `LOAD_FAST' instruction at offset 0

    @log_method
    def is_job_scheduled_for_inc(self, job_schedule_info):
        schedule_info = Et.fromstring(job_schedule_info.encode("utf-16"))
        is_inc_enable = False
        for root in schedule_info:
            if root.tag == "IncrementalBackup":
                is_inc_enable = "Enabled" in root.attrib and self.helper.is_text_true(root.attrib["Enabled"])
            return is_inc_enable

    @log_method
    def search_scheduled_mysql_inc_jobs(self, db_name, backup_type):
        is_backup_scheduled_inc = False
        if self.params["ServerType"] in (MYSQL_CONST, MARIADB_CONST):
            if backup_type == FULL_BACKUP_CONST:
                if self.is_database_scheduled_for_mysql_inc(db_name):
                    is_backup_scheduled_inc = True
        return is_backup_scheduled_inc
