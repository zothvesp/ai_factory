import hashlib, json, sqlite3
from datetime import datetime
import time
from sqlbak.definitions import CONFIG, TIMEOUT, BACKUP_TYPES, DBMS_TYPES_CONSTS, MYSQL_CONST, MARIADB_CONST
from sqlbak.helper import helper_instanse
from sqlbak.logger import log_data, log_method, log_only_exception

class LocalDB:

    def __init__(self):
        self._connection = None
        self._cursor = None
        self.helper = helper_instanse

    @log_only_exception
    def _connect(self):
        """
        create a database connection and a cursor to the SQLite database specified by the db_file
        :return: None
        """
        self._connection = sqlite3.connect(CONFIG["PATH_TO_APP"] + CONFIG["DB_NAME"])
        self._connection.row_factory = self._dict_factory
        self._cursor = self._connection.cursor()

    @log_only_exception
    def close_connection(self):
        if self._cursor:
            self._cursor.close()
        if self._connection:
            self._connection.close()

    def _executeParse error at or near `SETUP_FINALLY' instruction at offset 0

    def _execute_and_return_last_idParse error at or near `SETUP_FINALLY' instruction at offset 0

    def _executescriptParse error at or near `SETUP_FINALLY' instruction at offset 0

    def _fetchallParse error at or near `SETUP_FINALLY' instruction at offset 0

    def _dict_factory(self, cursor, row):
        """
        Method to receive after a query dict, like {table_field: value}
        :param cursor: db cursor
        :param row: row
        :return: result
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        else:
            return d

    @log_method
    def get_current_db_version(self):
        """
        Returns a version of a local database
        :return: db version or False if db version is not indicated
        """
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='DbVersion';"
        result = self._fetchall(sql)
        if len(result) > 0:
            sql = "SELECT Version FROM DbVersion WHERE Id = 1"
            result = self._fetchall(sql)
            if result is not None:
                if len(result) > 0:
                    return result[0]["Version"]
            return
        return

    @log_method
    def update_db_version(self, db_version):
        """
        Method to update a db version
        :param db_version: int
        :return: dict;
        """
        sql = "UPDATE DbVersion SET Version = ? WHERE Id = 1"
        self._executesql(db_version,)

    @log_method
    def create_db_tables_and_update_db_version(self):
        """
        Create new tables in a local db
        :return: None
        """
        tables = [
         {'version':1, 
          'sql':[
           '\n                    DROP TABLE IF EXISTS Agent; \n                    CREATE TABLE Agent(\n                    AgentKey TEXT DEFAULT NULL, \n                    AgentId TEXT DEFAULT NULL, \n                    AgentName TEXT DEFAULT NULL, \n                    AccountName TEXT DEFAULT NULL, \n                    IsActive TINYINT (1) DEFAULT 0,\n                    UtilsPath TEXT DEFAULT "",\n                    MajorVersion INT DEFAULT 1,\n                    MinorVersion INT DEFAULT 0,\n                    PatchVersion INT DEFAULT 0,\n                    WorkingDir TEXT DEFAULT "",\n                    WorkingDirChanged TINYINT (1) DEFAULT 0);\n\n                    DROP TABLE IF EXISTS Connection; \n                    CREATE TABLE Connection (\n                    ConnectionId INTEGER PRIMARY KEY UNIQUE, \n                    ServerType VARCHAR (20) DEFAULT NULL, \n                    ConnectionType VARCHAR (50) DEFAULT NULL, \n                    Host VARCHAR (20) DEFAULT NULL, \n                    Port INT (5) DEFAULT NULL, \n                    User TEXT DEFAULT NULL, \n                    Password TEXT DEFAULT NULL, \n                    UseSsh BOOLEAN NOT NULL DEFAULT False, \n                    SshHost VARCHAR (20) DEFAULT NULL, \n                    SshPort INT (6) DEFAULT NULL, \n                    SshLocalMappedPort INT (6) DEFAULT NULL, \n                    SshUser TEXT DEFAULT NULL, \n                    SshPassword TEXT DEFAULT NULL, \n                    ConnectionName TEXT DEFAULT NULL, \n                    ConnCredentialId INT DEFAULT NULL, \n                    Version INTEGER NOT NULL DEFAULT (1));\n\n                    DROP TABLE IF EXISTS DbVersion; \n                    CREATE TABLE DbVersion (Id INTEGER PRIMARY KEY NOT NULL, \n                    Version INTEGER NOT NULL DEFAULT (1)); \n                    INSERT INTO DbVersion (Id, Version) VALUES (1, 1);\n\n                    DROP TABLE IF EXISTS RequestParameters; \n                    CREATE TABLE RequestParameters (RequestExpiration TEXT, RequestInterval INT);\n\n                    DROP TABLE IF EXISTS JobSchedule;                    \n                    CREATE TABLE [JobSchedule] (\n                    [Id] INTEGER NOT NULL PRIMARY KEY ASC AUTOINCREMENT,\n                    [JobId] INTEGER NOT NULL,\n                    [StartDate] VARCHAR NOT NULL,\n                    [Interval] VARCHAR NOT NULL,\n                    [BackupType] TINYINT NOT NULL DEFAULT 1,\n                    [BusinessDays] VARCHAR NOT NULL DEFAULT "",\n                    [BeginAt] TEXT DEFAULT NULL,\n                    [EndAt] TEXT DEFAULT NULL\n                    );\n\n                    DROP TABLE IF EXISTS Job;\n                    CREATE TABLE Job (\n                    JobId INTEGER NOT NULL PRIMARY KEY,\n                    JobName TEXT DEFAULT NULL,\n                    JobInfo TEXT DEFAULT NULL,\n                    JobVersion INTEGER DEFAULT NULL,\n                    IsScheduled BOOLEAN NOT NULL,\n                    ScheduleInfo TEXT DEFAULT NULL, \n                    LastRunAt DATETIME DEFAULT NULL, \n                    PlanViolations TEXT DEFAULT NULL, \n                    JobCredentialsId INT DEFAULT NULL,\n                    JobGlobalId INT NOT NULL DEFAULT 0,\n                    LastModifiedAt DATETIME DEFAULT NULL, \n                    CreatedAt DATETIME DEFAULT NULL, \n                    Oid VARCHAR(32) DEFAULT NULL,\n                    ServiceVersion TEXT DEFAULT NULL,\n                    MessageId BIGINT);\n\n                    DROP TABLE IF EXISTS JobCredentials;\n                    CREATE TABLE [JobCredentials] (\n                    [JobCredentialsId] INTEGER NOT NULL PRIMARY KEY ASC,\n                    [Name] TEXT NOT NULL,\n                    [Version] INT NOT NULL DEFAULT 0,\n                    [JobCredentials] TEXT DEFAULT NULL,\n                    [SqlConnection] TEXT DEFAULT NULL, \n                    [JobCredentialsGlobalId] INT DEFAULT 0, \n                    [ServerType] INT NOT NULL DEFAULT 0);\n\n                    DROP TABLE IF EXISTS JobTrigger;\n                    CREATE TABLE [JobTrigger] (\n                    [Id] INTEGER NOT NULL PRIMARY KEY ASC,\n                    [TriggerId] INT NOT NULL,\n                    [JobId] INT NOT NULL,\n                    [TriggerTypeId] INT NOT NULL,\n                    [TriggerSettings] TEXT DEFAULT NULL);\n\n                    DROP TABLE IF EXISTS JobDestination;\n                    CREATE TABLE [JobDestination] (\n                    [JobId] INTEGER NOT NULL,\n                    [DestinationId] INTEGER NOT NULL,\n                    [DestinationConfiguration] TEXT DEFAULT NULL, \n                    [Ord] INTEGER DEFAULT 0, \n                    [LastModifiedAt] DATETIME DEFAULT NULL,\n                    PRIMARY KEY ([JobId], [DestinationId]));\n\n                    DROP TABLE IF EXISTS Destination;\n                    CREATE TABLE [Destination] (\n                    [DestinationId] INTEGER NOT NULL PRIMARY KEY,\n                    [DestinationType] INTEGER NOT NULL,\n                    [DestinationName] TEXT DEFAULT NULL,\n                    [DestinationSettings] TEXT DEFAULT NULL,\n                    [AccessInfo] TEXT DEFAULT NULL,\n                    [DestinationVersion] INTEGER DEFAULT NULL, \n                    [DestinationGlobalId] INT NOT NULL DEFAULT 0, \n                    [LastModifiedAt] DATETIME DEFAULT NULL, \n                    [AccessTokenInfo] TEXT DEFAULT NULL,\n                    [Oid] VARCHAR(32) DEFAULT NULL);\n\n                    DROP TABLE IF EXISTS Backup;\n                    CREATE TABLE [Backup] (\n                    [Id] INTEGER NOT NULL PRIMARY KEY ASC AUTOINCREMENT,\n                    [RemoteId] BIGINT,\n                    [JobId] INTEGER NOT NULL,\n                    [BackupType] CHAR(1) NOT NULL,\n                    [IsSuccess] BOOLEAN NOT NULL DEFAULT FALSE,\n                    [Size] BIGINT NOT NULL DEFAULT (0),\n                    [ArchiveSize] BIGINT NOT NULL DEFAULT (0),\n                    [StartTime] DATETIME NOT NULL,\n                    [EndTime] DATETIME DEFAULT NULL,\n                    [MessageId] BIGINT,\n                    [BackupStatus] TINYINT,\n                    [BackupKey] VARCHAR(32),\n                    [IsSent] BOOLEAN NOT NULL DEFAULT FALSE, \n                    [Mode] INT, \n                    [Password] NVARCHAR(512));\n\n                    DROP TABLE IF EXISTS BackupLog;\n                    CREATE TABLE [BackupLog] (\n                    [Id] INTEGER NOT NULL PRIMARY KEY ASC AUTOINCREMENT,\n                    [RemoteId] BIGINT,\n                    [BackupId] INTEGER NOT NULL,\n                    [ActionType] VARCHAR(64) NOT NULL,\n                    [CreatedDate] DATETIME NOT NULL,\n                    [Severity] TINYINT NOT NULL,\n                    [BackupLogKey] VARCHAR(32), \n                    [IsForced] BOOLEAN NOT NULL DEFAULT FALSE, \n                    [Filled] BOOLEAN);\n\n                    DROP TABLE IF EXISTS BackupLogParam;\n                    CREATE TABLE [BackupLogParam] (\n                    [Id] INTEGER NOT NULL PRIMARY KEY ASC AUTOINCREMENT,\n                    [BackupLogId] INTEGER NOT NULL,\n                    [ParamName] VARCHAR(64) NOT NULL,\n                    [ParamValue] TEXT\n                    );\n\n                    DROP TABLE IF EXISTS BackupObject;\n                    CREATE TABLE [BackupObject] (\n                    [Id] INTEGER NOT NULL PRIMARY KEY ASC AUTOINCREMENT,\n                    [RemoteId] BIGINT,\n                    [BackupId] INTEGER NOT NULL,\n                    [DestinationId] INTEGER NOT NULL,\n                    [ObjectType] TINYINT NOT NULL,\n                    [ObjectName] NVARCHAR(512) NOT NULL,\n                    [ObjectNameHash] VARBINARY(64) NOT NULL,\n                    [BackupDate] DATETIME NOT NULL,\n                    [IsSuccess] BOOLEAN NOT NULL,\n                    [Folder] NVARCHAR(512),\n                    [Size] BIGINT NOT NULL,\n                    [ArchiveSize] BIGINT NOT NULL,\n                    [BackupObjectKey] VARCHAR(32)\n                    );\n\n                    DROP TABLE IF EXISTS BackupObjectFile;\n                    CREATE TABLE [BackupObjectFile] (\n                    [Id] INTEGER NOT NULL PRIMARY KEY ASC AUTOINCREMENT,\n                    [BackupObjectId] INTEGER NOT NULL,\n                    [FileName] NVARCHAR(512) NOT NULL,\n                    [Exist] BOOLEAN NOT NULL,\n                    [OutId] VARCHAR(128) DEFAULT NULL);\n\n                    DROP TABLE IF EXISTS BackupObjectResult;\n                    CREATE TABLE [BackupObjectResult] (\n                    [Id] INTEGER NOT NULL PRIMARY KEY ASC AUTOINCREMENT,\n                    [RemoteId] BIGINT,\n                    [BackupId] INTEGER NOT NULL,\n                    [ObjectType] TINYINT NOT NULL,\n                    [ObjectName] NVARCHAR(512) NOT NULL,\n                    [BackupAt] DATETIME NOT NULL,\n                    [IsSuccess] BOOLEAN NOT NULL,\n                    [ObjectStatus] TINYINT NOT NULL,\n                    [BackupObjectResultKey] VARCHAR(32),\n                    [FullObjectName] TEXT NOT NULL\n                    );\n\n                    DROP TABLE IF EXISTS Message;\n                    CREATE TABLE [Message] (\n                    [Id] INTEGER NOT NULL PRIMARY KEY ASC AUTOINCREMENT,\n                    [MessageId] INTEGER NOT NULL,\n                    [CreatedAt] DATETIME NOT NULL,\n                    [EndAt] DATETIME DEFAULT NULL);\n\n                    DROP TABLE IF EXISTS Process;\n                    CREATE TABLE [Process] (\n                    [Id] INTEGER NOT NULL PRIMARY KEY ASC AUTOINCREMENT,\n                    [Pid] INTEGER NOT NULL, \n                    [RunnerId] INT NOT NULL,\n                    [MainRunnerId] INT NOT NULL,\n                    [RunnerType] INT NOT NULL,\n                    [CreatedAt] DATETIME NOT NULL,\n                    [EndAt] DATETIME DEFAULT NULL);\n                    ']},
         {'version':2, 
          'sql':[
           "\n                    DROP TABLE IF EXISTS ObjectBackupResult;\n                    CREATE TABLE [ObjectBackupResult] (\n                    [ObjectBackupResultId] INTEGER NOT NULL PRIMARY KEY,\n                    [JobId] INTEGER NOT NULL,\n                    [ObjectType] INTEGER NOT NULL,\n                    [ObjectName] TEXT NOT NULL,\n                    [BackupType] TEXT NOT NULL,\n                    [BackupId] INTEGER NOT NULL,\n                    [IsSuccess] BOOLEAN NOT NULL,\n                    [BackupAt] DATETIME NOT NULL);\n\n                    DROP TABLE IF EXISTS ObjectDestinationResult;\n                    CREATE TABLE [ObjectDestinationResult] (\n                    [ObjectBackupResultId] INTEGER NOT NULL,\n                    [DestinationId] INTEGER NOT NULL,\n                    [IsSuccess] BOOLEAN NOT NULL,\n                    [BackupAt] DATETIME NOT NULL);\n                    "]},
         {'version':3, 
          'sql':[
           "\n                        DROP TABLE IF EXISTS DBMSState; \n                        CREATE TABLE DBMSState(\n                        ConnectionId INT NOT NULL,\n                        State TINYINT (1) DEFAULT 1,\n                        ChangeState DATETIME);\n\n                        DROP TABLE IF EXISTS JobDestinationData;\n                        CREATE TABLE IF NOT EXISTS [JobDestinationData] (\n                        [Id] INTEGER NOT NULL PRIMARY KEY ASC AUTOINCREMENT,\n                        [JobId] INTEGER NOT NULL,\n                        [DestinationId] INTEGER NOT NULL,\n                        [LastCleanupAt] DATETIME);\n\n                        DROP TABLE IF EXISTS JobPlanViolation; \n                        CREATE TABLE JobPlanViolation(Data TEXT);\n\n                        ALTER TABLE Agent ADD COLUMN DownAlertPingInterval INTEGER DEFAULT 0;\n                    "]},
         {'version':5, 
          'sql':[
           "\n                        ALTER TABLE Agent ADD COLUMN IsAutoUpdateEnabled INTEGER DEFAULT 1;\n                    "]},
         {'version':6, 
          'sql':[
           "\n                        ALTER TABLE Agent ADD COLUMN SessionId TEXT DEFAULT NULL;\n                    "]},
         {'version':1072, 
          'sql':[
           "\n                        ALTER TABLE Agent ADD COLUMN DownloadPackageVersion VARCHAR(255) DEFAULT NULL;\n                    "]},
         {'version':10107, 
          'sql':[
           "\n                        ALTER TABLE Job ADD COLUMN IsChecking TINYINT (1) DEFAULT 0;\n                    "]},
         {'version':10114, 
          'sql':[
           "\n                        ALTER TABLE BackupObjectFile ADD COLUMN FileSize BIGINT NOT NULL DEFAULT 0;\n                    "]},
         {'version':10127, 
          'sql':[
           "\n                        ALTER TABLE Job ADD COLUMN CheckAt DATETIME DEFAULT NULL;\n                    "]},
         {'version':10132, 
          'sql':[
           "\n                        DROP TABLE IF EXISTS BackupNextDbmsType; \n                        CREATE TABLE BackupNextDbmsType(\n                        DbName TEXT DEFAULT NULL,\n                        DbmsType TEXT DEFAULT NULL,\n                        BackupType INT DEFAULT NULL,\n                        ChangeState DATETIME DEFAULT NULL);\n                    ",
           "\n                        DROP TABLE IF EXISTS BackupTypeSettings; \n                        CREATE TABLE BackupTypeSettings(\n                        DbmsType TEXT DEFAULT NULL,\n                        BackupType INT DEFAULT NULL,\n                        Settings TEXT DEFAULT NULL);\n                    "]},
         {'version':10135, 
          'sql':[
           "\n                        ALTER TABLE ObjectBackupResult ADD COLUMN DbmsType TEXT DEFAULT NULL;\n                    ",
           "\n                        DROP TABLE IF EXISTS BackupChecksum; \n                        CREATE TABLE BackupChecksum(\n                        JobId INT DEFAULT NULL,\n                        DbName TEXT DEFAULT NULL,\n                        BackupChecksum TEXT DEFAULT NULL,\n                        SavedAt DATETIME DEFAULT NULL);\n                    "]},
         {'version':10144, 
          'sql':[
           "\n                        ALTER TABLE Connection ADD COLUMN BackupUtil TEXT DEFAULT NULL;\n                    ",
           "\n                        ALTER TABLE ObjectBackupResult ADD COLUMN PathToBackup TEXT DEFAULT NULL;\n                    "]},
         {'version':10163, 
          'sql':[
           "\n                        ALTER TABLE JobTrigger ADD COLUMN Ord INT DEFAULT 0;\n                    "]},
         {'version':10174, 
          'sql':[
           "\n                        ALTER TABLE Connection ADD COLUMN Database DEFAULT NULL;\n                    "]},
         {'version':10175, 
          'sql':[
           "\n                       DROP TABLE IF EXISTS DestinationAccessTokens;\n\n                       CREATE TABLE [DestinationAccessTokens] (\n                                    [DestinationId] INTEGER NOT NULL PRIMARY KEY,\n                                    [AccessToken] TEXT NOT NULL, \n                                    [ExpiresAt] DATETIME NULL);\n                   "]},
         {'version':10179, 
          'sql':[
           "\n                       DROP TABLE IF EXISTS MySQLBinLogObject;\n\n                       CREATE TABLE [MySQLBinLogObject] (\n                                    [JobId] INTEGER NOT NULL,\n                                    [BackupId] INTEGER NOT NULL,\n                                    [BinlogIndexFile] TEXT NOT NULL,\n                                    [LastSavedBinlog] TEXT NOT NULL);\n                   "]}]
        current_version = self.get_current_db_version()
        db_version = 10179
        for table in tables:
            db_version = int(table["version"])
            if current_version is None or db_version > current_version:
                for sql in table["sql"]:
                    self._executescript(sql)

        else:
            self.update_db_version(db_version)

    @log_method
    def get_last_backuped_binlog(self, binlog_index_path, job_id):
        sql = "select * from MySQLBinLogObject where JobId = ? and BinlogIndexFile = ? "
        return self._fetchallsql(job_id, binlog_index_path)

    @log_method
    def reset_backuped_binlog(self, binlog_index_path):
        sql = "DELETE FROM MySQLBinLogObject WHERE BinlogIndexFile = ?"
        return self._execute_and_return_last_idsql(binlog_index_path,)

    @log_method
    def save_backuped_binlog(self, binlog_index_path, job_id, binlog_name, backup_id):
        if self.get_last_backuped_binlogbinlog_index_pathjob_id:
            sql = "update MySQLBinLogObject set LastSavedBinlog = ?, BackupId = ? where JobId = ? and BinlogIndexFile = ? "
        else:
            sql = "insert into MySQLBinLogObject (LastSavedBinlog,BackupId, JobId, BinlogIndexFile) VALUES (?,?,?,?) "
        return self._execute_and_return_last_idsql(str(binlog_name), int(backup_id), int(job_id), str(binlog_index_path))

    @log_method
    def remove_all_database_data(self):
        sql = "\n            SELECT \n                name\n            FROM \n                sqlite_master \n            WHERE \n                type ='table' AND \n                name NOT LIKE 'sqlite_%';\n        "
        tables = self._fetchall(sql)
        for table in [x["name"] for x in tables]:
            if table not in ('DbVersion', ):
                log_data("Delete table " + table)
                self._execute("DELETE FROM {0}".format(table))

    @log_method
    def add_connection(self, server_type, connection_type, host, port, user, password, use_ssh, ssh_host, ssh_port, ssh_local_mapped_port, ssh_user, ssh_password, connection_name, credential_id, backup_util, database):
        """
        Method adds new connection to DB with several params
        :param server_type:
        :param connection_type:
        :param host:
        :param port:
        :param user:
        :param password:
        :param use_ssh:
        :param ssh_host:
        :param ssh_port:
        :param ssh_local_mapped_port:
        :param ssh_user:
        :param ssh_password:
        :param connection_name:
        :param credential_id:
        :return: Last inserted row id
        """
        encrypted_password = self.helper.encrypt_string(password) if password is not None else None
        encrypted_ssh_password = self.helper.encrypt_string(ssh_password) if ssh_password is not None else None
        sql = "INSERT INTO Connection (ServerType, ConnectionType, Host, Port, User, Password, UseSsh, SshHost,\n                 SshPort, SshLocalMappedPort, SshUser, SshPassword, ConnectionName, ConnCredentialId, BackupUtil, Database)\n                 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        return self._execute_and_return_last_idsql(server_type, connection_type, host, port, user, encrypted_password,
         bool(use_ssh), ssh_host, ssh_port, ssh_local_mapped_port, ssh_user,
         encrypted_ssh_password, str(connection_name), credential_id, backup_util, database)

    @log_method
    def get_connections_by_server_type(self, server_type=None):
        """
        Method to get client"s connections by server type
        :param server_type: str
        :return: rows
        """
        if server_type and server_type != "all":
            sql = "SELECT * FROM Connection WHERE ServerType = ?"
            result = self._fetchallsql(server_type,)
        else:
            sql = "SELECT * FROM Connection"
            result = self._fetchall(sql)
        if result is not None:
            if len(result) > 0:
                return result

    @log_method
    def get_connection_by_id(self, connection_id):
        """
        Returns a connection corresponding with connection_id
        :param connection_id: int;
        :return: connection
        """
        sql = "SELECT * FROM Connection WHERE ConnectionId = ?"
        result = self._fetchallsql(connection_id,)
        if result is not None:
            if len(result) > 0:
                return result[0]

    @log_method
    def get_connection_by_id_with_alias_params(self, connection_id):
        """
        Returns a connection corresponding with connection_id
        :param connection_id: int;
        :return: connection
        """
        sql = "SELECT * FROM Connection WHERE ConnectionId = ?"
        result = self._fetchallsql(connection_id,)
        if result is not None:
            if len(result) > 0:
                return result[0]

    @log_method
    def update_connection_param(self, connection_id, param_name, param_value):
        """
        Method to update a connection param
        :param connection_id: int;
        :param param_name: str;
        :param param_value: str;
        :return: None
        """
        sql = "UPDATE Connection SET {0} = ? WHERE ConnectionId = ?".format(param_name)
        self._executesql(param_value, connection_id)

    @log_method
    def update_connection_params(self, connection_id, params):
        """
        Method to update a multiple connection"s params
        :param connection_id: int;
        :param params: array of params
        :return: None
        """
        for p in params:
            self.update_connection_param(connection_id, p, params[p])

    @log_method
    def get_connection_by_server_type_and_connection_name(self, server_type, connection_name):
        """
        Returns a connection corresponding with server_type and connection_name
        :param server_type: string;
        :param connection_name: string;
        :return: connection if it found or empty list
        """
        sql = "SELECT * FROM Connection WHERE ConnectionName = ? and ServerType = ?"
        result = self._fetchallsql(connection_name, server_type)
        if result is not None:
            if len(result) > 0:
                return result[0]

    @log_method
    def delete_connection_by_id(self, connection_id):
        """
        Method to delete a connection
        :param connection_id: int;
        :return: None
        """
        sql = "DELETE FROM Connection WHERE ConnectionId = ?"
        self._executesql(connection_id,)

    @log_method
    def add_new_agent(self, agent, utils_path, client_version, session_id):
        """
        Method to add a new client
        :param agent: dict
        :param utils_path: dict
        :param client_version: dict
        :return: a last inserted row id
        """
        utils_path = json.dumps(utils_path)
        working_dir = self.helper.parse_working_dir(agent["Profile"]["WorkingDir"])
        sql = "INSERT INTO Agent (AgentKey, AgentId, AgentName, AccountName, IsActive, UtilsPath,\n                 MajorVersion, MinorVersion, PatchVersion, WorkingDir, SessionId) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
        self._executesql(agent["AgentKey"], agent["AgentId"], agent["AgentName"], agent["AccountName"],
         agent["IsActive"], utils_path, client_version["major_version"],
         client_version["minor_version"], client_version["patch_version"], working_dir, session_id)

    @log_method
    def update_agent(self, agent_key, agent_id, agent_name, account_name, is_active, working_dir, session_id):
        """
        Method to update a client"s info
        :param agent_key:
        :param agent_id:
        :param agent_name:
        :param account_name:
        :param is_active:
        :param working_dir:
        :return: None
        """
        parsed_working_dir = self.helper.parse_working_dir(working_dir)
        is_working_dir_changed = 1 if self.is_working_dir_changed(parsed_working_dir) else 0
        sql = "UPDATE Agent SET AgentKey = ?, AgentId = ?, AgentName = ?, AccountName = ?, IsActive = ?,\n                 WorkingDir = ?, WorkingDirChanged = ?, SessionId = ? "
        self._executesql(agent_key, agent_id, agent_name, account_name, is_active, parsed_working_dir,
         is_working_dir_changed, session_id)

    @log_only_exception
    def get_current_agent(self):
        """
        Method to get a current client
        :return: client or none
        """
        sql = "SELECT * FROM Agent"
        result = self._fetchall(sql)
        if result is not None:
            if len(result) > 0:
                return result[0]

    @log_method
    def update_agent_activity(self, agent_key, is_active):
        """
        Method to update a client"s activity
        :param agent_key: str;
        :param is_active: bool
        :return: None
        """
        sql = "UPDATE Agent SET IsActive = ? WHERE AgentKey = ?"
        self._executesql(is_active, agent_key)

    @log_method
    def update_agent_name(self, agent_key, computer_name):
        """
        Method to update a client"s name
        :param agent_key:
        :param computer_name:
        :return: None
        """
        sql = "UPDATE Agent SET AgentName = ? WHERE AgentKey = ?"
        self._executesql(computer_name, agent_key)

    @log_method
    def update_agent_utils_path(self, agent_key, utils_path):
        """
        Method to update a client"s name
        :param agent_key:
        :param agent_settings:
        :return: None
        """
        utils = json.dumps(utils_path)
        sql = "UPDATE Agent SET UtilsPath = ? WHERE AgentKey = ?"
        self._executesql(utils, agent_key)

    @log_only_exception
    def get_request_params(self):
        """
        Method to get request params
        :return: array
        """
        sql = "SELECT * FROM RequestParameters"
        result = self._fetchall(sql)
        if result is not None:
            if len(result) > 0:
                return result[0]

    @log_only_exception
    def remove_request_params(self):
        """

        :return:
        """
        sql = "DELETE FROM RequestParameters"
        self._execute(sql)

    @log_only_exception
    def save_request_params(self, expiration, interval):
        """
        Method to update request params
        :param expiration:
        :param interval:
        :return: None
        """
        if self.get_request_params() is None:
            sql = "INSERT INTO RequestParameters (RequestExpiration, RequestInterval) VALUES (?,?)"
        else:
            sql = "UPDATE RequestParameters SET RequestExpiration = ?, RequestInterval = ?"
        self._executesql(expiration, interval)

    @log_method
    def is_job_exist(self, job_id):
        """
        A method to check if a job with job_id already exists
        :param job_id: int
        :return: True or False
        """
        sql = "SELECT * FROM Job WHERE JobId = ?"
        result = self._fetchallsql(job_id,)
        if result is not None:
            if len(result) > 0:
                return True
        return False

    @log_method
    def add_job(self, message):
        """
        Method to add a job
        :param message: dict
        :return: None
        """
        if self.is_job_exist(message["JobId"]):
            sql = "UPDATE Job SET JobName=?, JobInfo=?, JobVersion=?, IsScheduled=?, ScheduleInfo=?, \n                     JobCredentialsId=?, CreatedAt=?, MessageId = ? WHERE JobId=?"
        else:
            sql = "INSERT INTO Job (JobName, JobInfo, JobVersion, IsScheduled, ScheduleInfo, \n                     JobCredentialsId, CreatedAt, MessageId, JobId) VALUES (?,?,?,?,?,?,?,?,?)"
        self._executesql(message["JobName"] if "JobName" in message else None,
         message["JobInfo"] if "JobInfo" in message else None,
         message["JobVersion"] if "JobVersion" in message else None,
         message["IsScheduled"] if "IsScheduled" in message else False,
         message["ScheduleInfo"] if "ScheduleInfo" in message else None,
         message["JobCredentialsId"] if "JobCredentialsId" in message else None,
         datetime.now(),
         message["MessageId"] if "MessageId" in message else None,
         message["JobId"])

    @log_method
    def add_trigger(self, trigger):
        """

        :param trigger:
        :return:
        """
        if self.is_trigger_existsint(trigger["JobId"])int(trigger["TriggerId"]):
            sql = "UPDATE JobTrigger SET TriggerTypeId = ?, TriggerSettings = ?, Ord=? WHERE JobId = ? AND TriggerId = ? "
            self._executesql(int(trigger["TriggerTypeId"]), str(trigger["TriggerSettings"]), int(trigger["Ord"]),
             int(trigger["JobId"]), int(trigger["TriggerId"]))
        else:
            sql = "INSERT INTO JobTrigger (TriggerId, JobId, TriggerTypeId, TriggerSettings,Ord) VALUES (?,?,?,?,?)"
            self._executesql(int(trigger["TriggerId"]), int(trigger["JobId"]),
             int(trigger["TriggerTypeId"]), str(trigger["TriggerSettings"]), int(trigger["Ord"]))

    @log_method
    def is_trigger_exists(self, job_id, trigger_id):
        """

        :param job_id:
        :param trigger_id:
        :return:
        """
        sql = "SELECT * FROM JobTrigger WHERE JobId = ? AND TriggerId = ?"
        res = self._fetchallsql(job_id, trigger_id)
        return len(res) > 0

    @log_method
    def get_job_triggers_by_job_id(self, job_id):
        """

        :param job_id:
        :return:
        """
        sql = "SELECT * FROM JobTrigger WHERE JobId =? ORDER BY Ord"
        return self._fetchallsql(job_id,)

    @log_method
    def add_destination(self, destination):
        """
        Method to add destination
        :param destination: dict
        :return: None
        """
        if self.get_destination_by_id(int(destination["DestinationId"])) is None:
            sql = "INSERT INTO Destination (DestinationName, DestinationType, DestinationSettings,\n                     AccessInfo, DestinationId) VALUES (?,?,?,?,?)"
        else:
            sql = "UPDATE Destination SET DestinationName =?, DestinationType=?, DestinationSettings=?,\n                     AccessInfo=? WHERE DestinationId=?"
        self._executesql(destination["DestinationName"], int(destination["DestinationType"]),
         destination["DestinationSettings"], destination["AccessInfo"],
         int(destination["DestinationId"]))

    @log_method
    def add_job_destination(self, job_id, destination_id, configuration, ordi):
        """
        Method to add a job destination
        :param job_id:
        :param destination_id:
        :param configuration:
        :param ordi:
        :return: None
        """
        if self.get_job_destination_by_job_and_destination_idint(job_id)int(destination_id) is None:
            sql = "\n                INSERT INTO JobDestination (DestinationConfiguration, Ord, LastModifiedAt, JobId, DestinationId)\n                VALUES (?,?,?,?,?)\n            "
        else:
            sql = "\n                UPDATE JobDestination SET DestinationConfiguration=?, Ord=?, LastModifiedAt =?\n                WHERE JobId =? AND DestinationId =?\n            "
        self._executesql(configuration, int(ordi), datetime.now(), int(job_id), int(destination_id))

    @log_method
    def get_job_destination_by_job_and_destination_id(self, job_id, destination_id):
        """

        :param job_id:
        :param destination_id:
        :return:
        """
        sql = "SELECT * FROM JobDestination WHERE JobId =? AND DestinationId = ?"
        result = self._fetchallsql(job_id, destination_id)
        if result is not None:
            if len(result) > 0:
                return result[0]

    @log_method
    def get_destination_and_job_destination(self, job_id, destination_id):
        """

        :param job_id:
        :param destination_id:
        :return:
        """
        sql = "SELECT * FROM Destination d\n                 INNER JOIN JobDestination jd ON jd.DestinationId = d.DestinationId\n                 WHERE jd.JobId = ? AND d.DestinationId = ?"
        result = self._fetchallsql(int(job_id), int(destination_id))
        if result is not None:
            if len(result) > 0:
                return result[0]

    @log_method
    def get_job_destinations(self, job_id):
        """
        Method to get a job destination
        :param job_id: int
        :return: job destination or none
        """
        sql = "SELECT * FROM Destination d\n                 INNER JOIN JobDestination jd ON jd.DestinationId = d.DestinationId\n                 WHERE jd.JobId = ?"
        result = self._fetchallsql(int(job_id),)
        if result is not None:
            if len(result) > 0:
                return result
        return []

    @log_method
    def get_destinations_id(self, job_id):
        """

        :param job_id:
        :return:
        """
        sql = "SELECT d.DestinationId FROM Destination d\n                 INNER JOIN JobDestination jd ON jd.DestinationId = d.DestinationId\n                 WHERE jd.JobId = ?"
        results = self._fetchallsql(job_id,)
        destinations = []
        if results is not None:
            if len(results) > 0:
                for r in results:
                    destinations.append(r["DestinationId"])

        return destinations

    @log_only_exception
    def get_destination_by_id(self, destination_id):
        """
        Method to get a destination by destination id
        :param destination_id: int
        :return: destination or none
        """
        sql = "SELECT * FROM Destination WHERE DestinationId = ?"
        result = self._fetchallsql(int(destination_id),)
        if result is not None:
            if len(result) > 0:
                return result[0]

    @log_method
    def get_job_by_id(self, job_id):
        """
        Method to get a job by job id
        :param job_id: int
        :return: job or none
        """
        sql = "SELECT * FROM Job WHERE JobId = ?"
        result = self._fetchallsql(int(job_id),)
        if result is not None:
            if len(result) > 0:
                return result[0]

    @log_method
    def get_jobs_by_credentials_id(self, job_cred_id):
        """

        :param job_cred_id:
        :return:
        """
        sql = "SELECT * FROM Job WHERE JobCredentialsId = ?"
        result = self._fetchallsql(int(job_cred_id),)
        if result is not None:
            if len(result) > 0:
                return result

    @log_method
    def save_job_credential(self, job_cred_id, name, server_type):
        """
        Method to add a new jobCredential
        :param job_cred_id: int;
        :param name: str;
        :param server_type: int;
        :return: None
        """
        sql = "INSERT OR REPLACE INTO JobCredentials (JobCredentialsId, Name, ServerType) VALUES (?,?,?)"
        self._executesql(int(job_cred_id), str(name), int(server_type))

    @log_method
    def get_connection_by_job_cred_id(self, job_cred_id):
        """
        Method to get a job credentials by job credentials id
        :param job_cred_id: int;
        :return:
        """
        sql = "SELECT * FROM Connection WHERE ConnCredentialId = ?"
        result = self._fetchallsql(job_cred_id,)
        if result is not None:
            if len(result) > 0:
                return result[0]

    @log_method
    def get_list_of_jobs(self):
        """
        Method to get all the existing jobs
        :return: array of jobs
        """
        sql = "SELECT * FROM Job"
        result = self._fetchall(sql)
        if result is not None:
            if len(result) > 0:
                return result

    @log_method
    def delete_jobs(self):
        """

        :return:
        """
        sql = "DELETE FROM Job"
        self._execute(sql)

    @log_method
    def delete_destinations(self):
        """

        :return:
        """
        sql = "DELETE FROM Destination"
        self._execute(sql)

    @log_method
    def delete_connections(self):
        """

        :return:
        """
        sql = "DELETE FROM Connection"
        self._execute(sql)

    @log_method
    def delete_job_credentials(self):
        """

        :return:
        """
        sql = "DELETE FROM JobCredentials"
        self._execute(sql)

    @log_method
    def delete_job_destinations(self):
        sql = "DELETE FROM JobDestination"
        self._execute(sql)

    @log_method
    def delete_job_schedules(self):
        sql = "DELETE FROM JobSchedule"
        self._execute(sql)

    @log_method
    def delete_destination_by_id(self, destination_id):
        """

        :param destination_id:
        :return:
        """
        sql = "DELETE FROM Destination WHERE DestinationId = ?"
        self._executesql(destination_id,)

    @log_method
    def get_job_destinations_by_destination_id(self, destiantion_id):
        """

        :param destiantion_id:
        :return:
        """
        sql = "SELECT * FROM JobDestination WHERE DestinationId = ?"
        return self._fetchallsql(destiantion_id,)

    @log_method
    def delete_job_destination_by_destination_id_and_job_id(self, destination_id, job_id):
        """

        :param destination_id:
        :return:
        """
        sql = "DELETE FROM JobDestination WHERE DestinationId = ? AND JobId=?"
        self._executesql(destination_id, job_id)

    @log_method
    def remove_destination_and_job_destination(self, job_id):
        """

        :param job_id:
        :return:
        """
        sql = "SELECT * FROM JobDestination WHERE JobId = ?"
        for j in self._fetchallsql(job_id,):
            sql = "DELETE FROM JobDestination WHERE JobId = ?"
            self._executesql(job_id,)
            if len(self.get_job_destinations_by_destination_id(j["DestinationId"])) == 0:
                self.delete_destination_by_id(j["DestinationId"])

    @log_method
    def delete_all_client_records(self):
        """

        :return:
        """
        self.delete_jobs()
        self.delete_destinations()
        self.delete_connections()
        self.delete_job_credentials()
        self.delete_job_schedules()
        self.delete_job_destinations()
        self.delete_object_results()

    @log_method
    def add_backup(self, job_id, backup_type, message_id):
        """

        :param job_id:
        :param backup_type:
        :param message_id:
        :return:
        """
        uud = self.helper.get_uuid()
        date_time = datetime.strftimedatetime.now()"%Y-%m-%d %H:%M:%S.%f"
        sql = "\n            INSERT INTO Backup (JobId, BackupType, StartTime, BackupKey, BackupStatus, MessageId) Values(?,?,?,?,?,?)\n        "
        last_row_id = self._execute_and_return_last_idsql(job_id, backup_type, date_time, uud, 1, message_id)
        return {'BackupLastRowId':last_row_id,  'BackupKey':uud}

    @log_only_exception
    def add_backup_log(self, backup_id, action_type, severity, uud):
        """

        :param backup_id:
        :param action_type:
        :param severity:
        :param uud:
        :return:
        """
        date_time = datetime.strftimedatetime.now()"%Y-%m-%d %H:%M:%S.%f"
        sql = "INSERT INTO BackupLog(BackupId, ActionType, CreatedDate, Severity, IsForced, BackupLogKey)\n                 Values(?,?,?,?,?,?)"
        return self._execute_and_return_last_idsql(backup_id, action_type, date_time, severity, False, str(uud))

    @log_only_exception
    def add_backup_log_params(self, backup_log_id, params):
        """

        :param backup_log_id:
        :param params:
        :return:
        """
        log_params = []
        for param in params:
            sql = "INSERT INTO BackupLogParam(BackupLogId, ParamName, ParamValue) Values(?,?,?)"
            self._executesql(backup_log_id, param, params[param])
            log_params.append({'ParamName':str(param), 
             'ParamValue':str(params[param])})
        else:
            return log_params

    @log_method
    def get_backup_object_by_backup_id(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        sql = "SELECT * FROM BackupObject WHERE BackupId = ?"
        return self._fetchallsql(backup_id,)

    @log_method
    def is_backup_object_file_exist(self, backup_name):
        """

        :param backup_name:
        :return:
        """
        sql = "SELECT * FROM BackupObjectFile WHERE FileName = ?"
        result = self._fetchallsql(backup_name,)
        if result is not None:
            if len(result) > 0:
                return True
        return False

    @log_method
    def add_backup_object(self, params, backup, destination, is_success):
        """

        :param params:
        :param backup:
        :param destination:
        :return:
        """
        uud = self.helper.get_uuid()
        hash_object = hashlib.sha256(str(backup["object_name"]).encode("utf-8"))
        hex_dig = hash_object.hexdigest()
        date_time = datetime.strftimedatetime.now()"%Y-%m-%d %H:%M:%S.%f"
        sql = "INSERT INTO BackupObject (RemoteId, BackupId, DestinationId, ObjectType, ObjectName, ObjectNameHash,\n                 BackupDate, IsSuccess, Folder, Size, ArchiveSize, BackupObjectKey) Values(?,?,?,?,?,?,?,?,?,?,?,?)"
        backup_remote_id = int(params["BackupRemoteId"]) if params["BackupRemoteId"] is not None else None
        last_row_id = self._execute_and_return_last_idsql(backup_remote_id,
         int(params["BackupId"]), int(destination["destination_id"]),
         backup["object_type"], str(backup["object_name"]), hex_dig,
         date_time, is_success, destination["settings"]["DestinationPath"],
         int(backup["size"]), int(backup["archive_size"]), str(uud))
        return {'BackupObjectId':last_row_id,  'BackupObjectKey':str(uud)}

    @log_method
    def add_backup_object_result(self, params):
        """

        :param params:
        :return:
        """
        sql = "INSERT INTO BackupObjectResult (RemoteId, BackupId, ObjectType, ObjectName,\n                 BackupAt, IsSuccess, ObjectStatus, BackupObjectResultKey, FullObjectName) Values(?,?,?,?,?,?,?,?,?)"
        backup_remote_id = int(params["BackupRemoteId"]) if params["BackupRemoteId"] is not None else None
        self._executesql(backup_remote_id, int(params["BackupId"]), params["ObjectType"],
         params["ObjectName"], params["BackupAt"], params["IsSuccess"],
         params["Status"], params["BackupObjectResultKey"], params["FullObjectName"])

    @log_method
    def add_backup_object_file(self, backup_object_id, file_name, is_exist, file_size, outId):
        """

        :param params: dict
        :return:
        """
        sql = "INSERT INTO BackupObjectFile (BackupObjectId, FileName, Exist, FileSize, OutId) Values(?,?,?,?,?)"
        self._executesql(int(backup_object_id), file_name, is_exist, file_size, outId)

    @log_method
    def update_backup_remote_id(self, backup_id, remote_id):
        """

        :param backup_id:
        :param remote_id:
        :return:
        """
        sql = "UPDATE Backup SET RemoteId = ? WHERE Id = ? "
        self._executesql(int(remote_id), int(backup_id))

    @log_method
    def get_backup_by_id(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        sql = "\n            SELECT b.Id, b.JobId, b.BackupType, b.IsSuccess, b.Size, b.ArchiveSize, b.StartTime,\n            b.EndTime, b.BackupStatus, b.BackupKey, b.Mode, j.JobCredentialsId, b.MessageId, j.JobInfo, b.RemoteId\n            FROM Backup b \n            LEFT JOIN Job j ON j.JobId = b.JobId\n            WHERE b.Id = ?\n            ORDER BY b.Id DESC\n        "
        res = self._fetchallsql(int(backup_id),)
        if res is not None:
            if len(res) > 0:
                return res[0]

    @log_method
    def get_backup_and_job_by_backup_remote_id(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        sql = "SELECT * FROM Backup b INNER JOIN Job j ON j.JobId = b.JobId WHERE b.RemoteId = ?"
        res = self._fetchallsql(int(backup_id),)
        if res is not None:
            if len(res) > 0:
                return res[0]

    @log_method
    def get_backup_logs(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        sql = "SELECT bl.* FROM BackupLog bl INNER JOIN Backup b ON b.Id = bl.BackupId WHERE bl.BackupId = ? AND bl.RemoteId IS NULL ORDER BY bl.Id ASC LIMIT 0, 64"
        return self._fetchallsql(int(backup_id),)

    @log_only_exception
    def get_backup_log_params(self, backup_log_id):
        """

        :param backup_log_id:
        :return:
        """
        sql = "SELECT * FROM BackupLogParam WHERE BackupLogId = ? ORDER BY Id ASC"
        return self._fetchallsql(int(backup_log_id),)

    @log_method
    def get_backup_objects(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        sql = "SELECT * FROM BackupObject  WHERE BackupId = ? ORDER BY Id ASC"
        return self._fetchallsql(int(backup_id),)

    @log_method
    def get_backup_object_results(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        sql = "SELECT * FROM BackupObjectResult  WHERE BackupId = ? ORDER BY Id ASC"
        return self._fetchallsql(int(backup_id),)

    @log_only_exception
    def get_backup_object_files(self, backup_object_id):
        """

        :param backup_object_id:
        :return:
        """
        sql = "SELECT * FROM BackupObjectFile WHERE BackupObjectId = ? ORDER BY Id ASC"
        return self._fetchallsql(int(backup_object_id),)

    @log_method
    def delete_backup_by_id(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        sql_backup_log = "SELECT * FROM BackupLog WHERE BackupId = ?"
        sql_backup_object = "SELECT * FROM BackupObject WHERE BackupId = ?"
        sql_backup_result = "SELECT * FROM BackupObjectResult WHERE BackupId = ?"
        if len(self._fetchallsql_backup_log(backup_id,)) == 0:
            if len(self._fetchallsql_backup_object(backup_id,)) == 0:
                if len(self._fetchallsql_backup_result(backup_id,)) == 0:
                    sql = "DELETE FROM Backup WHERE Id = ? AND RemoteId IS NOT NULL"
                    self._executesql(backup_id,)

    @log_method
    def delete_backup_by_id_forced(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        sql_backup_log = "SELECT * FROM BackupLog WHERE BackupId = ?"
        sql_backup_object = "SELECT * FROM BackupObject WHERE BackupId = ?"
        sql_backup_result = "SELECT * FROM BackupObjectResult WHERE BackupId = ?"
        if len(self._fetchallsql_backup_log(backup_id,)) == 0:
            if len(self._fetchallsql_backup_object(backup_id,)) == 0:
                if len(self._fetchallsql_backup_result(backup_id,)) == 0:
                    sql = "DELETE FROM Backup WHERE Id = ?"
                    self._executesql(backup_id,)

    @log_method
    def delete_backup_log_and_param_by_backup_id(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        sql = "SELECT Id FROM BackupLog WHERE BackupId = ? AND RemoteId IS NOT NULL"
        for r in self._fetchallsql(backup_id,):
            self.delete_backup_log_param(int(r["Id"]))
            if len(self.get_backup_log_params(int(r["Id"]))) == 0:
                sql = "DELETE FROM BackupLog WHERE BackupId = ? AND RemoteId IS NOT NULL"
                self._executesql(backup_id,)

    @log_method
    def delete_backup_log_and_param_by_backup_id_forced(self, backup_id, except_backup_action=None):
        """

        :param backup_id:
        :return:
        """
        sql = "SELECT * FROM BackupLog WHERE BackupId = ?"
        for backup_log in self._fetchallsql(backup_id,):
            if except_backup_action is None or backup_log["ActionType"] not in except_backup_action:
                backup_log_id = int(backup_log["Id"])
                self.delete_backup_log_param(backup_log_id)
                if len(self.get_backup_log_params(backup_log_id)) == 0:
                    sql = "DELETE FROM BackupLog WHERE Id = ?"
                    self._executesql(backup_log["Id"],)

    @log_only_exception
    def delete_backup_log_param(self, backup_log_id):
        """

        :param backup_log_id:
        :return:
        """
        sql = "DELETE FROM BackupLogParam WHERE BackupLogId = ?"
        self._executesql(backup_log_id,)

    @log_method
    def delete_backup_object_by_backup_id(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        sql = "SELECT Id FROM BackupObject WHERE BackupId = ? AND RemoteId IS NOT NULL"
        for r in self._fetchallsql(backup_id,):
            self.delete_backup_object_file(int(r["Id"]))
            if len(self.get_backup_object_files(int(r["Id"]))) == 0:
                sql = "DELETE FROM BackupObject WHERE BackupId = ? AND RemoteId IS NOT NULL"
                self._executesql(backup_id,)

    @log_method
    def delete_backup_object_by_backup_id_forced(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        sql = "SELECT * FROM BackupObject WHERE BackupId = ?"
        for backup_object in self._fetchallsql(backup_id,):
            self.delete_backup_object_file_forced(int(backup_object["Id"]))
            if len(self.get_backup_object_files(int(backup_object["Id"]))) == 0:
                sql = "DELETE FROM BackupObject WHERE BackupId = ?"
                self._executesql(backup_id,)
                self.delete_backup_object_result_by_backup_id_forced(backup_id)

    @log_method
    def delete_backup_object_file_forced(self, backup_object_id):
        """

        :param backup_object_id:
        :return:
        """
        sql = "DELETE FROM BackupObjectFile WHERE BackupObjectId = ?"
        self._executesql(backup_object_id,)

    @log_only_exception
    def delete_backup_object_file(self, backup_object_id):
        """

        :param backup_object_id:
        :return:
        """
        sql = "DELETE FROM BackupObjectFile WHERE BackupObjectId = ? AND OutId IS NOT NULL"
        self._executesql(backup_object_id,)

    @log_method
    def delete_backup_object_result_by_backup_id_forced(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        sql = "DELETE FROM BackupObjectResult WHERE BackupId =?"
        self._executesql(backup_id,)

    @log_method
    def delete_backup_object_result_by_backup_id(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        sql = "DELETE FROM BackupObjectResult WHERE BackupId =? AND RemoteId IS NOT NULL"
        self._executesql(backup_id,)

    @log_method
    def clean_backup_logs(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        self.delete_backup_log_and_param_by_backup_id(backup_id)
        self.delete_backup_object_by_backup_id(backup_id)
        self.delete_backup_object_result_by_backup_id(backup_id)
        self.delete_backup_by_id(backup_id)

    @log_method
    def clean_backup_logs_forced(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        self.delete_backup_log_and_param_by_backup_id_forced(backup_id)
        self.delete_backup_object_by_backup_id_forced(backup_id)
        self.delete_backup_by_id_forced(backup_id)

    @log_method
    def delete_job(self, job_id):
        """

        :param job_id:
        :return:
        """
        self.delete_backup_by_job_id(job_id)
        sql = "DELETE FROM Job WHERE JobId = ?"
        self._executesql(job_id,)

    @log_method
    def delete_backup_by_job_id(self, job_id):
        """

        :param job_id:
        :return:
        """
        for backup in self.get_backups_by_job_id(job_id):
            self.delete_backup_logs_and_param_by_backup_id_with_job(backup["Id"])
            self.delete_backup_object_by_backup_id_with_job(backup["Id"])
            self.delete_backup_by_backup_id_with_job(backup["Id"])

    @log_method
    def delete_backup_logs_and_param_by_backup_id_with_job(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        sql = "SELECT Id FROM BackupLog WHERE BackupId = ?"
        for r in self._fetchallsql(backup_id,):
            self.delete_backup_log_param(int(r["Id"]))
        else:
            sql = "DELETE FROM BackupLog WHERE BackupId = ?"
            self._executesql(backup_id,)

    @log_method
    def delete_backup_object_by_backup_id_with_job(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        sql = "SELECT Id FROM BackupObject WHERE BackupId = ?"
        for r in self._fetchallsql(backup_id,):
            self.delete_backup_object_file_forced(int(r["Id"]))
        else:
            sql = "DELETE FROM BackupObject WHERE BackupId = ?"
            self._executesql(backup_id,)
            sql = "DELETE FROM BackupObjectResult WHERE BackupId =?"
            self._executesql(backup_id,)

    @log_method
    def delete_backup_by_backup_id_with_job(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        sql = "DELETE FROM Backup WHERE Id = ?"
        self._executesql(backup_id,)

    @log_method
    def get_backups_by_job_id(self, job_id):
        """

        :param job_id:
        :return:
        """
        sql = "SELECT * FROM Backup WHERE JobId = ?"
        return self._fetchallsql(int(job_id),)

    @log_method
    def delete_job_credential_by_id(self, job_credentials_id):
        """

        :param job_credentials_id:
        :return:
        """
        sql = "DELETE FROM JobCredentials WHERE JobCredentialsId = ?"
        self._executesql(job_credentials_id,)

    @log_method
    def update_backup_object_result_remote_id(self, remote_id, key):
        """

        :param remote_id:
        :param key:
        :return:
        """
        sql = "UPDATE BackupObjectResult SET RemoteId = ? WHERE BackupObjectResultKey = ? "
        self._executesql(int(remote_id), str(key))

    @log_method
    def update_backup_object_remote_id_by_key(self, remote_id, key):
        """

        :param remote_id:
        :param key:
        :return:
        """
        sql = "UPDATE BackupObject SET RemoteId = ? WHERE BackupObjectKey = ? "
        self._executesql(int(remote_id), str(key))

    @log_only_exception
    def update_backup_log_remote_id(self, backup_log_key, remote_id):
        """

        :param backup_log_key:
        :param remote_id:
        :return:
        """
        sql = "UPDATE BackupLog SET RemoteId = ?, IsForced = ? WHERE Id = ? "
        self._executesql(int(remote_id), True, str(backup_log_key))

    @log_only_exception
    def update_backup_log_remote_id_by_key(self, remote_id, key):
        """

        :param remote_id:
        :param key:
        :return:
        """
        sql = "UPDATE BackupLog SET RemoteId = ?, IsForced = ? WHERE BackupLogKey = ? "
        self._executesql(int(remote_id), True, str(key))

    @log_method
    def update_backup_remote_id_by_key(self, remote_id, key):
        """

        :param remote_id:
        :param key:
        :return:
        """
        sql = "UPDATE Backup SET RemoteId = ? WHERE BackupKey = ? "
        self._executesql(int(remote_id), str(key))

    @log_method
    def mark_backup_as_sent(self, backup_key):
        """

        :param backup_key:
        :return:
        """
        sql = "UPDATE Backup SET IsSent = ? WHERE BackupKey = ? "
        self._executesql(True, str(backup_key))

    @log_method
    def add_message(self, message_id):
        """

        :param message_id:
        :return:
        """
        sql = "INSERT INTO Message (MessageId, CreatedAt) VALUES (?,?)"
        self._executesql(message_id, datetime.now())

    @log_only_exception
    def does_message_exists(self, message_id):
        """

        :param message_id:
        :return:
        """
        sql = "SELECT * FROM Message WHERE MessageId = ?"
        res = self._fetchallsql(message_id,)
        if len(res) > 0:
            return True
        return False

    @log_method
    def get_last_full_backup(self, job_id, db_name):
        """

        :param job_id:
        :param db_name:
        :return:
        """
        sql = "SELECT bf.FileName, bo.Id FROM Job j\n                 INNER JOIN Backup b ON b.JobId = j.JobId\n                 INNER JOIN BackupObject bo ON bo.BackupId = b.Id\n                 INNER JOIN BackupObjectFile bf ON bo.Id = bf.BackupObjectId\n                 WHERE j.JobId = ? AND bo.ObjectType=1 AND bo.ObjectName= ?\n                 ORDER BY bf.Id DESC LIMIT 1"
        res = self._fetchallsql(job_id, db_name)
        if res is not None:
            if len(res) > 0:
                return res[0]

    @log_method
    def get_last_incremental_backups(self, last_full_backup_id):
        """

        :param last_full_backup_id:
        :return:
        """
        sql = "SELECT bf.FileName FROM BackupObject bo\n                 INNER JOIN BackupObjectFile bf ON bf.BackupObjectId = bo.Id\n                 WHERE bo.ObjectType = 2 AND bo.Id >= ? ORDER BY bo.Id ASC"
        res = self._fetchallsql(last_full_backup_id,)
        if res is not None:
            if len(res) > 0:
                return res

    @log_method
    def remove_job_schedules(self):
        """

        :return:
        """
        sql = "DELETE FROM JobSchedule"
        self._execute(sql)

    @log_only_exception
    def get_scheduled_jobs_by_schedule_id(self, schedule_id):
        """

        :param schedule_id: int
        :return:
        """
        sql = " \n        SELECT js.BusinessDays as BusinessDays, js.StartDate as StartDate, js.Interval as Interval, js.BackupType,\n        js.Id as Id, js.JobId as JobId, j.MessageId as MessageId, js.BeginAt, js.EndAt\n        FROM JobSchedule js         \n        INNER JOIN Job j ON j.JobId = js.JobId\n        WHERE js.Id = ? "
        res = self._fetchallsql(int(schedule_id),)
        if len(res) > 0:
            return res[0]
        return []

    @log_only_exception
    def get_scheduled_grouped_jobs(self):
        """

        :return:
        """
        jobs = []
        sql = "SELECT group_concat(Id) as schedule_ids, JobId as job_id \n                 FROM JobSchedule GROUP BY JobId ORDER BY BackupType ASC"
        for r in self._fetchall(sql):
            schedules = []
            for schedule_id in r["schedule_ids"].split(","):
                schedules.append(self.get_scheduled_jobs_by_schedule_id(schedule_id))
            else:
                jobs.append({"schedules": schedules})

        else:
            return jobs

    @log_method
    def update_job_start_date_schedule(self, start_date, job_id, backup_type):
        """

        :param start_date:
        :param job_id:
        :param backup_type:
        :return:
        """
        sql = "UPDATE JobSchedule SET StartDate = ? WHERE JobId = ? AND BackupType=?"
        self._executesql(start_date, job_id, backup_type)

    @log_method
    def update_agent_version(self):
        app_version = CONFIG["APP_VERSION"].split(".")
        sql = "UPDATE Agent SET MajorVersion = ?, MinorVersion = ?, PatchVersion = ?"
        self._executesql(app_version[0], app_version[1], app_version[2])

    @log_method
    def end_backup(self, backup_id, is_success):
        """

        :param backup_id:
        :param is_success:
        :return:
        """
        sql = "UPDATE Backup SET IsSuccess = ?, EndTime = ?, IsSent = ? WHERE Id = ? "
        self._executesql(bool(is_success), datetime.strftimedatetime.now()"%Y-%m-%d %H:%M:%S.%f", True, int(backup_id))

    @log_method
    def update_backup_end_time(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        sql = "UPDATE Backup SET EndTime = ? WHERE Id = ?"
        self._executesql(datetime.strftimedatetime.now()"%Y-%m-%d %H:%M:%S.%f", int(backup_id))

    @log_method
    def update_backup_size(self, backup_id, backup_size):
        """

        :param backup_id:
        :param backup_size:
        :return:
        """
        sql = " UPDATE Backup SET Size = ? WHERE Id = ? "
        self._executesql(int(backup_size), int(backup_id))

    @log_method
    def update_backup_archive_size(self, backup_id, backup_archive_size):
        """

        :param backup_id:
        :param backup_archive_size:
        :return:
        """
        sql = " UPDATE Backup SET ArchiveSize = ? WHERE Id = ? "
        self._executesql(int(backup_archive_size), int(backup_id))

    @log_method
    def are_there_unsent_logs_for_backup_with_id(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        sql = "SELECT * FROM BackupLog WHERE IsForced=0 AND BackupId = ?"
        res = self._fetchallsql(int(backup_id),)
        if res is not None:
            if len(res) > 0:
                return True
        return False

    @log_only_exception
    def get_unfinished_backup_job(self):
        sql = "SELECT * FROM Backup WHERE EndTime IS NULL"
        res = self._fetchall(sql)
        if res is not None:
            if len(res) > 0:
                return res
        return []

    @log_method
    def get_working_dir(self):
        """

        :return:
        """
        sql = "SELECT WorkingDir FROM Agent "
        res = self._fetchall(sql)
        if len(res) > 0:
            return res[0]["WorkingDir"]
        return CONFIG["DEFAULT_ROOT_WORK_DIR"]

    @log_method
    def exec_script(self, sql):
        """

        :param sql: str
        :return:
        """
        self._execute(sql)

    @log_only_exception
    def get_backup_object_files_by_backup_object_id(self, backup_object_id):
        """

        :param backup_object_id:
        :return:
        """
        sql = "SELECT * FROM BackupObjectFile WHERE BackupObjectId = ?"
        res = self._fetchallsql(int(backup_object_id),)
        if res is not None:
            if len(res) > 0:
                return res

    @log_method
    def end_message(self, message_id):
        """

        :param message_id:
        :return:
        """
        sql = "UPDATE Message SET EndAt=? WHERE MessageId = ?"
        self._executesql(datetime.now().strftime("%m/%d/%Y %H:%M"), int(message_id))

    @log_method
    def add_process(self, pid, runner_id, main_runner_id, runner_type):
        """

        :param pid:
        :param runner_id:
        :param runner_type:
        :return:
        """
        res = self.get_processrunner_idrunner_type
        is_process_exist = res is not None and len(res) > 0
        if is_process_exist:
            self.delete_processrunner_idrunner_type
        sql = "INSERT INTO Process (Pid, RunnerId, MainRunnerId, RunnerType, CreatedAt) VALUES (?,?,?,?,?)"
        self._executesql(int(pid), int(runner_id), int(main_runner_id), int(runner_type), datetime.now())

    @log_method
    def delete_process_by_pid(self, pid):
        sql = "DELETE FROM Process WHERE Pid = ?"
        self._executesql(int(pid),)

    @log_method
    def delete_process(self, runner_id, runner_type):
        """

        :param runner_id:
        :param runner_type:
        :return:
        """
        sql = "DELETE FROM Process WHERE RunnerId = ? AND RunnerType = ?"
        self._executesql(int(runner_id), int(runner_type))

    @log_method
    def delete_process_by_main_id(self, main_runner_id, runner_type):
        """

        :param runner_id:
        :param runner_type:
        :return:
        """
        sql = "DELETE FROM Process WHERE MainRunnerId = ? AND RunnerType = ?"
        self._executesql(int(main_runner_id), int(runner_type))

    @log_method
    def get_all_process(self):
        sql = "SELECT * FROM Process"
        return self._fetchall(sql)

    @log_only_exception
    def get_process(self, runner_id, runner_type):
        """

        :param runner_id:
        :param runner_type:
        :return:
        """
        sql = "SELECT * FROM Process WHERE RunnerId = ? AND RunnerType = ?"
        return self._fetchallsql(int(runner_id), int(runner_type))

    @log_only_exception
    def get_process_by_main_id(self, main_runner_id, runner_type):
        """

        :param main_runner_id:
        :param runner_type:
        :return:
        """
        sql = "SELECT * FROM Process WHERE MainRunnerId = ? AND RunnerType = ?"
        return self._fetchallsql(int(main_runner_id), int(runner_type))

    @log_method
    def get_processes_by_type(self, runner_type):
        """

        :param runner_type:
        :return:
        """
        sql = "SELECT * FROM Process WHERE RunnerType = ?"
        return self._fetchallsql(int(runner_type),)

    @log_method
    def update_process(self, pid, runner_id, main_runner_id):
        sql = "UPDATE Process SET MainRunnerId = ? WHERE RunnerId = ? AND Pid = ?"
        self._executesql(int(main_runner_id), int(runner_id), int(pid))

    @log_method
    def is_working_dir_changed(self, new_value):
        """

        :param new_value:
        :return:
        """
        old_value = self.get_working_dir()
        return old_value.strip() != new_value.strip()

    @log_method
    def remove_job_trigger(self, job_id):
        """

        """
        sql = "DELETE FROM JobTrigger WHERE JobId = ?"
        self._executesql(int(job_id),)

    @log_method
    def add_object_backup_result(self, object_name, is_success, job_id, backup_type, object_type, backup_id, backup_at, dbms_type):
        sql = "INSERT INTO ObjectBackupResult (JobId, ObjectType, ObjectName, BackupType, BackupId, IsSuccess, BackupAt, DbmsType) VALUES (?,?,?,?,?,?,?,?)"
        return self._execute_and_return_last_idsql(job_id, object_type, object_name, backup_type, backup_id, is_success, backup_at, dbms_type)

    @log_method
    def add_object_destination_result(self, object_result_id, destination_id, is_success):
        sql = "INSERT INTO ObjectDestinationResult (ObjectBackupResultId, DestinationId, IsSuccess, BackupAt) VALUES (?,?,?,?)"
        self._executesql(object_result_id, destination_id, is_success, datetime.now())

    @log_only_exception
    def get_object_backup_result(self, object_name, job_id, object_type):
        sql = "SELECT * FROM ObjectBackupResult WHERE JobId = ? AND ObjectType =? AND ObjectName = ?"
        res = self._fetchallsql(job_id, object_type, object_name)
        if res is not None:
            if len(res) > 0:
                return res[0]

    @log_only_exception
    def get_object_destination_result(self, object_result_id, destination_id):
        sql = "SELECT * FROM ObjectDestinationResult WHERE ObjectBackupResultId = ? AND DestinationId = ?"
        res = self._fetchallsql(object_result_id, destination_id)
        if res is not None:
            if len(res) > 0:
                return res[0]

    @log_method
    def reset_object_backup_result(self, object_backup_id, is_success):
        sql = "UPDATE ObjectBackupResult SET IsSuccess = ? WHERE ObjectBackupResultId = ?"
        self._executesql(is_success, object_backup_id)

    @log_method
    def update_object_backup_result(self, object_backup_id, is_success, backup_at, dbms_type, backup_id):
        sql = "UPDATE ObjectBackupResult SET IsSuccess = ?, BackupAt=?, DbmsType=?, BackupId=? WHERE ObjectBackupResultId = ?"
        self._executesql(is_success, backup_at, dbms_type, backup_id, object_backup_id)

    @log_only_exception
    def reset_object_destination_result(self, object_result_id, destination_id, is_success):
        sql = "UPDATE ObjectDestinationResult SET IsSuccess = ? WHERE ObjectBackupResultId = ? AND DestinationId = ?"
        self._executesql(is_success, object_result_id, destination_id)

    @log_method
    def remove_objects_backup_result_for_job(self, job_id):
        for o in self.object_backups_by_job_id(job_id):
            sql = "DELETE FROM ObjectDestinationResult WHERE ObjectBackupResultId = ?"
            self._executesql(int(o["ObjectBackupResultId"]),)
        else:
            sql = "DELETE FROM ObjectBackupResult WHERE JobId = ?"
            self._executesql(int(job_id),)

    @log_method
    def get_last_backup_type_for_job_id(self, job_id):
        sql = "SELECT * FROM ObjectBackupResult WHERE JobId = ? AND ObjectType <> ? ORDER BY BackupAt DESC LIMIT 1"
        res = self._fetchallsql(job_id, int(BACKUP_TYPES["FOLDER"]))
        if res is not None:
            if len(res) > 0:
                return int(res[0]["ObjectType"])

    @log_method
    def object_backups_by_job_id(self, job_id):
        sql = "SELECT * FROM ObjectBackupResult WHERE JobId = ? "
        return self._fetchallsql(job_id,)

    def get_last_backup_object(self, job_id, object_name=None):
        if object_name is None:
            sql = "SELECT * FROM ObjectBackupResult WHERE JobId = ? order by BackupId DESC LIMIT 1"
            result = self._fetchallsql(job_id,)
        else:
            sql = "SELECT * FROM ObjectBackupResult WHERE JobId = ? and ObjectName = ? order by BackupId DESC LIMIT 1"
            result = self._fetchallsql(job_id, object_name)
        if len(result) > 0:
            return result[0]

    @log_method
    def set_all_backup_types_success_for_job_id(self, db_name, job_id):
        sql = "UPDATE ObjectBackupResult SET IsSuccess = 1, BackupAt=? WHERE ObjectName = ? AND JobId = ?"
        self._executesql(datetime.now(), db_name, job_id)

    @log_method
    def get_time_of_last_log_backup_for_a_job(self, job_id, db_name):
        sql = "SELECT BackupAt FROM ObjectBackupResult WHERE JobId = ? AND ObjectName = ? AND BackupType = 'l' \n                ORDER BY BackupAt DESC LIMIT 1"
        res = self._fetchallsql(job_id, db_name)
        if res is not None:
            if len(res) > 0:
                return res[0]["BackupAt"]

    @log_method
    def get_last_success_backup_data(self, job_id, object_name):
        sql = "SELECT * FROM ObjectBackupResult WHERE JobId=? AND IsSuccess = 1 AND ObjectName=? ORDER BY BackupAt DESC LIMIT 1"
        res = self._fetchallsql(int(job_id), object_name)
        if res is not None:
            if len(res) > 0:
                return res[0]

    @log_method
    def save_current_backup_data(self, job_id, path_to_backup, object_type, object_name, backup_type, dbms_type, backup_id):
        res = self.get_object_backup_result(object_name, job_id, object_type)
        if res is None:
            backup_at = datetime.now()
            sql = "INSERT INTO ObjectBackupResult (JobId, ObjectType, ObjectName, BackupType, BackupId, IsSuccess, BackupAt, DbmsType, PathToBackup) VALUES (?,?,?,?,?,?,?,?,?)"
            self._executesql(job_id, object_type, object_name, backup_type, backup_id, 1, backup_at, dbms_type, path_to_backup)
        else:
            sql = "UPDATE ObjectBackupResult SET PathToBackup=? WHERE JobId=? AND ObjectType=? AND ObjectName=?"
            self._executesql(path_to_backup, int(job_id), object_type, object_name)

    @log_only_exception
    def get_down_alert_interval(self):
        sql = "SELECT DownAlertPingInterval FROM Agent"
        res = self._fetchall(sql)
        if res is not None:
            if len(res) > 0:
                return int(res[0]["DownAlertPingInterval"])
        return 0

    @log_method
    def update_down_alert_interval(self, interval):
        """

        :param interval: int
        :return:
        """
        sql = "UPDATE Agent SET DownAlertPingInterval = ?"
        self._executesql(interval,)

    @log_only_exception
    def get_dbms_connections(self):
        sql = "SELECT * FROM Connection c INNER JOIN Job j ON j.JobCredentialsId = c.ConnCredentialId"
        return self._fetchall(sql)

    @log_method
    def get_dbms_connection_state(self, connection_id):
        """

        :param connection_id:
        :return:
        """
        sql = "SELECT d.State, d.ChangeState, c.ServerType, c.ConnectionType FROM DBMSState d \n                 INNER JOIN Connection c ON c.ConnectionId = d.ConnectionId WHERE c.ConnectionId = ? "
        res = self._fetchallsql(connection_id,)
        if res is not None:
            if len(res) > 0:
                return res[0]

    @log_method
    def update_dbms_connection_state(self, connection_id, state, state_change_date_time):
        """

        :param connection_id:
        :param state:
        :param state_change_date_time:
        :return:
        """
        sql = "UPDATE DBMSState SET State = ?, ChangeState = ? WHERE ConnectionId = ?"
        self._executesql(state, state_change_date_time, connection_id)

    @log_method
    def add_dbms_connection_state(self, connection_id, state, state_change_date_time):
        """

        :param connection_id:
        :param state:
        :param state_change_date_time:
        :return:
        """
        sql = "INSERT INTO DBMSState (ConnectionId, State, ChangeState) VALUES (?,?,?)"
        self._executesql(connection_id, state, state_change_date_time)

    @log_method
    def delete_dbms_connection_state_by_connection_id(self, connection_id):
        """

        :param connection_id:
        :return:
        """
        sql = "DELETE FROM DBMSState WHERE ConnectionId = ?"
        self._executesql(connection_id,)

    @log_only_exception
    def get_last_backup_cleanup_time(self, job_id, destination_id):
        """

        :param job_id:
        :param destination_id:
        :return:
        """
        sql = "SELECT * FROM JobDestinationData WHERE JobId = ? AND DestinationId = ?"
        res = self._fetchallsql(job_id, destination_id)
        if res is not None:
            if len(res) > 0:
                return res[0]

    @log_method
    def delete_job_destination_data(self, job_id, destination_id):
        """

        :param job_id:
        :param destination_id:
        :return:
        """
        sql = "DELETE FROM JobDestinationData WHERE WHERE JobId = ? AND DestinationId = ?"
        self._executesql(job_id, destination_id)

    @log_method
    def add_job_destination_data(self, job_id, destination_id):
        """

        :param job_id:
        :param destination_id:
        :return:
        """
        if self.get_last_backup_cleanup_timejob_iddestination_id is None:
            sql = "INSERT INTO JobDestinationData (LastCleanupAt, JobId, DestinationId) VALUES (?,?,?)"
        else:
            sql = "UPDATE JobDestinationData SET LastCleanupAt = ? WHERE JobId = ? AND DestinationId = ?"
        self._executesql(datetime.now(), job_id, destination_id)

    @log_method
    def add_job_plan_violation(self, job_plan_violation_data):
        if self.get_job_plan_violation_data() is None:
            sql = "INSERT INTO JobPlanViolation (Data) VALUES (?)"
        else:
            sql = "UPDATE JobPlanViolation SET Data = ?"
        encrypted_data = self.helper.encrypt_string(job_plan_violation_data)
        self._executesql(encrypted_data,)

    @log_method
    def get_job_plan_violation_data(self):
        sql = "SELECT * FROM JobPlanViolation"
        res = self._fetchall(sql)
        if res is not None:
            if len(res) > 0:
                return res[0]["Data"]

    @log_method
    def get_backup_object_id(self, destination_id, object_name, backup_id):
        """

        :param destination_id:
        :param object_name:
        :return:
        """
        sql = "SELECT * FROM BackupObject WHERE DestinationId = ? AND ObjectName = ? AND BackupId=?"
        res = self._fetchallsql(destination_id, object_name, backup_id)
        if res is not None:
            if len(res) > 0:
                return res[0]["RemoteId"]

    @log_method
    def delete_object_results(self):
        """

        :return:
        """
        sql = "DELETE FROM ObjectDestinationResult"
        self._fetchall(sql)
        sql = "DELETE FROM ObjectBackupResult"
        self._execute(sql)

    @log_method
    def update_backup(self, backup_id, is_backup_success):
        sql = "UPDATE Backup SET IsSuccess = ? WHERE Id =?"
        self._executesql(is_backup_success, backup_id)

    @log_method
    def get_job_by_backup_remote_id(self, backup_id):
        sql = "SELECT j.* FROM Backup b INNER JOIN Job j ON j.JobId = b.JobId WHERE b.RemoteId=?"
        res = self._fetchallsql(backup_id,)
        if res is not None:
            if len(res) > 0:
                return res[0]

    @log_method
    def is_auto_update_enabled(self):
        sql = "SELECT * FROM Agent"
        res = self._fetchall(sql)
        if res is not None:
            if len(res) > 0:
                return int(res[0]["IsAutoUpdateEnabled"]) == 1
        return False

    @log_method
    def set_agent_deleted(self):
        sql = "UPDATE Agent SET AgentKey=NULL, AgentId=NULL, IsActive=0"
        self._execute(sql)

    @log_method
    def get_download_package_version(self):
        sql = "SELECT * FROM Agent"
        res = self._fetchall(sql)
        if res is not None and len(res) > 0:
            if res[0]["DownloadPackageVersion"] is None:
                return
            return json.loads(res[0]["DownloadPackageVersion"])["version"]
        else:
            return
        if res is not None:
            if len(res) > 0:
                return json.loads(res[0]["DownloadPackageVersion"])["version"]

    @log_method
    def add_downloaded_package_version(self, package_version):
        sql = "UPDATE Agent SET DownloadPackageVersion=?"
        self._executesql(package_version,)

    @log_method
    def update_agent_session_id(self, session_id):
        sql = "UPDATE Agent SET SessionId=?"
        self._executesql(session_id,)

    @log_method
    def get_scheduled_jobs(self):
        sql = "SELECT JobId FROM JobSchedule GROUP BY JobId"
        return self._fetchall(sql)

    @log_only_exception
    def get_jobs(self):
        sql = "SELECT * FROM Job"
        return self._fetchall(sql)

    @log_method
    def update_last_run(self, job_id):
        now = datetime.now()
        sql = "UPDATE Job SET LastRunAt=? WHERE JobId=?"
        self._executesql(now.strftime("%m/%d/%Y %H:%M"), job_id)

    @log_method
    def get_messages(self):
        sql = "SELECT * FROM Message"
        res = self._fetchall(sql)
        if res is not None:
            if len(res) > 0:
                return res

    @log_method
    def remove_message(self, message_id):
        sql = "DELETE FROM Message WHERE MessageId=?"
        self._executesql(int(message_id),)

    @log_only_exception
    def update_job_check_datetime(self, job_id):
        now = datetime.now()
        sql = "UPDATE Job SET CheckAt=? WHERE JobId=?"
        self._executesql(now.strftime("%m/%d/%Y %H:%M"), job_id)

    @log_method
    def get_next_backup_type(self, db_name, dbms_type):
        sql = "SELECT * FROM BackupNextDbmsType WHERE DbName=? AND DbmsType=?"
        res = self._fetchallsql(str(db_name), str(dbms_type))
        if res is not None:
            if len(res) > 0:
                return res[0]["BackupType"]

    @log_method
    def remove_next_backup_type(self, db_name, dbms_type):
        sql = "DELETE FROM BackupNextDbmsType WHERE DbName=? AND DbmsType=?"
        self._executesql(str(db_name), str(dbms_type))

    @log_method
    def set_backup_type_settings(self, dbms_type, backup_type, settings):
        backup_type_settings = self.get_backup_type_settingsdbms_typebackup_type
        if backup_type_settings is None:
            sql = "INSERT INTO BackupTypeSettings (Settings, DbmsType, BackupType) VALUES (?,?,?)"
            self._executesql(str(settings), str(dbms_type), int(backup_type))
        else:
            sql = "UPDATE BackupTypeSettings SET Settings=? WHERE DbmsType=? AND BackupType=?"
            self._executesql(str(settings), str(dbms_type), int(backup_type))

    @log_method
    def get_backup_type_settings(self, dbms_type, backup_type):
        sql = "SELECT * FROM BackupTypeSettings WHERE BackupType=? AND DbmsType=?"
        res = self._fetchallsql(int(backup_type), str(dbms_type))
        if res is not None:
            if len(res) > 0:
                return res[0]["Settings"]

    @log_method
    def get_datetime_last_backup_for_database_by_backup_type(self, object_name, backup_type, object_type):
        sql = "SELECT * FROM ObjectBackupResult WHERE ObjectType =? AND ObjectName = ? AND BackupType = ? ORDER BY BackupAt DESC LIMIT 1"
        res = self._fetchallsql(object_type, object_name, backup_type)
        if res is not None:
            if len(res) > 0:
                return res[0]["BackupAt"]

    @log_method
    def get_checksum_for_dump_file(self, db_name, job_id):
        sql = "SELECT * FROM BackupChecksum WHERE JobId =? AND DbName = ?"
        res = self._fetchallsql(int(job_id), db_name)
        if res is not None:
            if len(res) > 0:
                return res[0]["BackupChecksum"]

    def exist_checksum_for_dump_file(self, db_name, job_id):
        sql = "SELECT * FROM BackupChecksum WHERE JobId =? AND DbName = ?"
        res = self._fetchallsql(int(job_id), db_name)
        return res is not None and len(res) > 0

    @log_method
    def save_checksum_for_dump_file(self, dump_checksum, db_name, job_id):
        x = self.exist_checksum_for_dump_filedb_namejob_id
        if x:
            sql = "UPDATE BackupChecksum SET BackupChecksum=?, SavedAt=? WHERE JobId=? AND DbName=?"
            self._executesql(dump_checksum, datetime.now(), int(job_id), db_name)
        else:
            sql = "INSERT INTO BackupChecksum (BackupChecksum, DbName, JobId, SavedAt) VALUES (?,?,?,?)"
            self._executesql(dump_checksum, db_name, int(job_id), datetime.now())

    @log_method
    def remove_test_dumps_checksum(self, job_id):
        sql = "DELETE FROM BackupChecksum WHERE JobId=?"
        self._executesql(int(job_id),)

    @log_method
    def get_scheduled_job_for_mysql(self):
        sql = "\n            SELECT j.JobInfo, j.ScheduleInfo FROM Job j\n            INNER JOIN JobCredentials jc on jc.JobCredentialsId = j.JobCredentialsId\n            WHERE j.IsScheduled=1 AND jc.ServerType=?\n        "
        return self._fetchallsql(int(DBMS_TYPES_CONSTS[MYSQL_CONST]["connection_types"]["tcp/ip"]),)

    @log_method
    def get_token(self, destioantion_id):
        sql = "SELECT * FROM DestinationAccessTokens WHERE DestinationId =?"
        res = self._fetchallsql(int(destioantion_id),)
        if res is not None:
            if len(res) > 0:
                return res[0]

    @log_method
    def save_token(self, destination_id, access_token, expire_at):
        sql = "INSERT OR REPLACE INTO DestinationAccessTokens (DestinationId, AccessToken, ExpiresAt) VALUES (?,?,?)"
        self._executesql(destination_id, access_token, expire_at)


local_db_instanse = LocalDB()
