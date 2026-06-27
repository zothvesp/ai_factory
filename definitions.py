
APP_NAME = "SqlBak"
FULL_BACKUP_CONST = "FULL"
DIFF_BACKUP_CONST = "DIFF"
LOG_BACKUP_CONST = "LOG"
INC_BACKUP_CONST = "INC"
FOLDER_BACKUP_CONST = "FOLDER"
FULL_COPY_BACKUP = "FullCopy"
LOG_TRANS_COPY = "LogTranCopy"
PIN_INTERVAL = 45
DIFF_BACKUP_SUFFIX = "diff"
TRANS_LOG_BACKUP_SUFFIX = "log"
INC_BACKUP_SUFFIX = "inc"
HOUR_IN_MINUTES = 60
SEC_IN_MILLISECOND = 1000
MINUTE_IN_SEC = 60
TIMEOUT = 60
CHUNK_SIZE = 6400
K_BIT = 1024
M_BIT = K_BIT * K_BIT
G_BIT = K_BIT * M_BIT
SCRIPTS_TIMEOUT_DEFAULT = 15 * MINUTE_IN_SEC
MSSQL_LOGIN_TIMEOUT = 30
MAX_BACKUP_SIZE = 25 * G_BIT
MYSQL_CONST = "mysql"
MSSQL_CONST = "mssql"
POSTGRESQL_CONST = "postgresql"
MARIADB_CONST = "mariadb"
POSTGRES_CONST = "postgres"
XTRABACKUP_CONST = "xtrabackup"
MYSQLDUMP_CONST = "mysqldump"
MONGO_CONST = "mongo"
MONGODB_CONST = "mongodb"
AZURESQL_CONST = "azure"
POSTGRES_BACKUP_FORMATS = {'Plain':"Plain", 
 'Tar':"Tar", 
 'Custom':"Custom"}
AVAILABLE_SERVER_TYPES = [
 MYSQL_CONST, POSTGRESQL_CONST, MSSQL_CONST, MARIADB_CONST, POSTGRES_CONST, 
 MONGO_CONST, MONGODB_CONST, AZURESQL_CONST]
COMPRESSION_ENGINE_7Z = "E7Zip"
COMPRESSION_ENGINE_ZIP = "EInternal"
COMPRESSION_LEVEL_DEFAULT = "Normal"
COMPRESSION_PRIORITY_DEFAULT = "Normal"
E7Zip_EXT = ".7z"
ZIP_EXT = ".zip"
ARCHIVES_EXT = [
 E7Zip_EXT, ZIP_EXT]
SQL_EXT = ".sql"
SQL_SCRIPT_TYPE = 1
CMD_SCRIPT_TYPE = 0
DYNAMIC_SETTING_LOGGING_ACTIVATED = "is_logging_activated"
DYNAMIC_SETTING_LOGGING_LEVEL = "level"
DYNAMIC_SETTING_LOGGING_DEBUG_SIZE = "debug-size"
DYNAMIC_SETTING_LOGGING_RM_TEMP_FILES = "rm-temp-files"
DYNAMIC_SETTING_LOGGING_MYSQLBINLOG_ADDITIONAL_ARGUMENTS = "mysqlbinlog-additional-arguments"
DYNAMIC_SETTING_BASE_PERMISSION = "base-permissions"
TCP_CONNECT_TYPE = "tcp/ip"
SYSTEM_DATABASES_MYSQL = [
 MYSQL_CONST, 'information_schema', 'performance_schema', 'phpmyadmin', 'sys']
SYSTEM_DATABASES_POSTGRESQL = ["postgres", "template1", "template0"]
SYSTEM_DATABASES_MSSQL = ["master", "model", "msdb", "tempdb"]
SYSTEM_DATABASES_MONGO = ["admin", "local", "config"]
PREVIOUS_BACKUP_HAS_FAILED = "PREVIOUS_BACKUP_HAS_FAILED"
MSSQL_BACKUP_CHAIN_BROKEN_RAISE_ERROR = "MSSQL_BACKUP_CHAIN_BROKEN_RAISE_ERROR"
MSSQL_BACKUP_CHAIN_BROKEN_RAISE_WARNINIG = "MSSQL_BACKUP_CHAIN_BROKEN_RAISE_WARNINIG"
MSSQL_BACKUP_CHAIN_BROKEN_MAKE_FULL = "MSSQL_BACKUP_CHAIN_BROKEN_MAKE_FULL"
MSSQL_DOUBLE_LOG_SAME_MINUTE = "MSSQL_DOUBLE_LOG_SAME_MINUTE"
MYSQL_DATA_SCHEMA_HAS_CHANGED = "MYSQL_DATA_SCHEMA_HAS_CHANGED"
BACKUP_TYPE_CHANGED = "BACKUP_TYPE_CHANGED"
FULL_AND_FIRST_BACKUP = "FULL_AND_FIRST_BACKUP"
PREVIOUS_BACKUP_DOES_NOT_EXISTS = "PREVIOUS_BACKUP_DOES_NOT_EXISTS"
DOCKER_EXEC = "docker exec {0} sqlbak"
SUDO_SQLBAK = "sudo sqlbak"
PORTS_SCOPE = [1, 65536]
OPERATION_SHORT_CODE_JOB = "b"
OPERATION_SHORT_CODE_RESTORE = "r"
MESSAGE_TYPES_CONSTS = {
 'SAVE_JOB': 1, 
 'DELETE_JOB': 2, 
 'RUN_JOB': 3, 
 'SAVE_DESTINATION': 101, 
 'DELETE_DESTINATION': 102, 
 'CANCEL_JOB': 4, 
 'REQUEST_ENVIRONMENT': 1001, 
 'CHANGE_ACCOUNT_PLAN': 16001, 
 'TEST_DESTINATION': 201, 
 'UPDATE_PROFILE': 1101, 
 'AGENT_CONFIGURATION_CHANGED': 18002, 
 'ACTIVATE_LOGGING': 14001, 
 'DEACTIVATE_LOGGING': 14002, 
 'UPLOAD_LOGS': 14003, 
 'CLEANUP_UPLOAD_LOGS': 14004, 
 'UPLOAD_DATABASE': 14005, 
 'UPGRADE_APP': 1050, 
 'CHECK_TEMP_FOLDER': 202, 
 'RESTORE_BACKUP': 2001, 
 'CANCEL_RESTORE_BACKUP': 2002, 
 'DOWNLOAD_BACKUP': 1501, 
 'DOWNLOAD_FOLDER_BACKUP': 1503, 
 'CANCEL_DOWNLOAD': 1502, 
 'CANCEL_PROCESS': 11001, 
 'CHECK_DOWN_ALERT': 17001, 
 'SQL_SCRIPT_EXEC': 19002, 
 'DELETE_SERVER': 10002, 
 'RESTART_SERVICE': 10001, 
 'GET_FINGERPRINT': 210, 
 'EDIT_SERVER_NAME': 18003, 
 'GET_DBMS_CONNECTION_SETTINGS': 20001, 
 'SAVE_DBMS_CONNECTION_SETTINGS': 20002, 
 'DELETE_DBMS_CONNECTION_SETTINGS': 20003, 
 'TEST_DBMS_CONNECTION_SETTINGS': 20004}
SYNCHRONOUS_MESSAGE_TYPES = [
 MESSAGE_TYPES_CONSTS["RUN_JOB"],
 MESSAGE_TYPES_CONSTS["SAVE_JOB"],
 MESSAGE_TYPES_CONSTS["DELETE_JOB"],
 MESSAGE_TYPES_CONSTS["SAVE_DESTINATION"],
 MESSAGE_TYPES_CONSTS["DELETE_DESTINATION"]]
DESTINATIONS_CONSTS = {
 'UNKNOWN': 0, 
 'FOLDER': 1, 
 'FTP': 2, 
 'AMAZON': 3, 
 'DROPBOX': 4, 
 'GOOGLE': 5, 
 'ONEDRIVE': 6, 
 'BOX': 7, 
 'AZURE': 8, 
 'ONEDRIVE_BUSINESS': 9, 
 'BACKBLAZE': 10, 
 'YANDEX': 11, 
 'AMAZON_S3_COMP': 12}
DESTINATIONS_WITH_ACCESS_TOKEN = [
 DESTINATIONS_CONSTS["ONEDRIVE"],
 DESTINATIONS_CONSTS["ONEDRIVE_BUSINESS"],
 DESTINATIONS_CONSTS["GOOGLE"]]
DESTINATIONS_NAMES = {
 1: '"Folder"', 
 2: '"FTP"', 
 3: '"Amazon S3"', 
 4: '"Dropbox"', 
 5: '"Google Drive"', 
 6: '"One Drive"', 
 7: '"Box"', 
 8: '"Azure Blob"', 
 9: '"One Drive for Business"', 
 10: '"Backblaze B2"', 
 11: '"Yandex Disk"', 
 12: '"Amazon S3 Compatible"'}
REQUEST_PATH_CONSTS = {
 'runApp': '"runApp"', 
 'registerAgent': '"registerAgent"', 
 'updateAgent': '"updateAgent"', 
 'setAgentActivity': '"setAgentActivity"', 
 'saveDBMSConnection': '"saveDBMSConnection"', 
 'updateAgentConnection': '"updateAgentConnection"', 
 'getAgentConnection': '"getAgentConnection"', 
 'testAgentConnection': '"testAgentConnection"', 
 'removeAgentConnection': '"removeAgentConnection"', 
 'listJobs': '"listJobs"', 
 'runJob': '"runJob"', 
 'restoreDB': '"restoreDB"', 
 'showConsoleCommands': '"showConsoleCommands"', 
 'getAppVersion': '"getAppVersion"', 
 'setAppLogs': '"setAppLogs"', 
 'uploadLogs': '"uploadLogs"', 
 'getInfo': '"getInfo"', 
 'updateApp': '"updateApp"', 
 'restartService': '"restartService"', 
 'uploadDb': '"uploadDb"', 
 'stopService': '"stopService"', 
 'configureMysql': '"configureMysql"', 
 'checkReadyToStart': '"checkReadyToStart"', 
 'runJobCollector': '"runJobCollector"', 
 'runSubservice': '"runSubservice"', 
 'interactiveMenu': '"interactiveMenu"'}
SEVERITY_PARAMS = {
 'Debug': 1, 
 'Info': 2, 
 'Warning': 3, 
 'Error': 4}
BACKUP_TYPES = {
 'UNKNOWN': 0, 
 'FULL': 1, 
 'DIFF': 2, 
 'LOG': 3, 
 'FOLDER': 4, 
 'INC': 5, 
 'FULL_COPY_ONLY_BACKUP': 6}
TRIGGER_BACKUP_TYPES = {
 'Full': FULL_BACKUP_CONST, 
 'Diff': DIFF_BACKUP_CONST, 
 'LogTran': LOG_BACKUP_CONST, 
 'FullCopy': FULL_COPY_BACKUP, 
 'LogTranCopy': LOG_TRANS_COPY, 
 'Incremental': INC_BACKUP_CONST}
MSSQL_BACKUP_TYPES = {FULL_BACKUP_CONST: "D", 
 DIFF_BACKUP_CONST: "I", 
 LOG_BACKUP_CONST: "L", 
 INC_BACKUP_CONST: "i"}
BROKEN_BACKUP_BEHAVIOR = {'ERROR':"Error", 
 'WARNING':"Warning", 
 'FULL':"MakeFull"}
MSSQL_BACKUP_COMPRESSION = {'COMPRESS':"Compress", 
 'DO_NOT_COMPRESS':"DontCompress"}
RUN_SCRIPT_TYPES = {'BEFORE_BACKUP':"BEFORE_BACKUP", 
 'AFTER_BACKUP':"AFTER_BACKUP", 
 'MAINTENANCE':"MAINTENANCE"}
JOB_TYPES = {'MAINTENANCE':"Maintenance", 
 'BACKUP':"Backup"}
AGENT_UTILS_PATH = {
 'mysqldump-path': '"/usr/bin/mysqldump"', 
 'mysql-path': '"/usr/bin/mysql"', 
 'mysql-binlog-base-path': '""', 
 'mysql-binlog-index-path': '""', 
 'pgdump-path': '"/usr/bin/pg_dump"', 
 'psql-path': '"/usr/bin/psql"', 
 'sqlcmd-path': '"/opt/mssql-tools/bin/sqlcmd"', 
 'mssql-data': '"/var/opt/mssql/data/"', 
 'xtrabackup-path': '"/usr/bin/xtrabackup"', 
 'mysql-lib': '"/var/lib/mysql/"', 
 'mongo-path': '"/usr/bin/mongo"', 
 'mongodump-path': '"/usr/bin/mongodump"', 
 'mongorestore-path': '"/usr/bin/mongorestore"', 
 'pg_restore-path': '"/usr/bin/pg_restore"', 
 'sqlpackage-path': '"/opt/mssql-tools/sqlpackage/sqlpackage"'}
ALTERNATIVE_AGENT_UTILS_PATH = {"sqlcmd-path": "/opt/mssql-tools18/bin/sqlcmd"}
DBMS_TYPES_CONSTS = {MYSQL_CONST: {'default_port':3306, 
               'connection_types':{'tcp/ip':4, 
                'phpmyadmin':5}, 
               'native_extention':{FULL_BACKUP_CONST: ".sql", 
                INC_BACKUP_CONST: ""}, 
               'client_util':MYSQL_CONST, 
               'default_path':AGENT_UTILS_PATH["mysql-path"], 
               'default_util':"mysql-path"}, 
 
 MARIADB_CONST: {'default_port':3306, 
                 'connection_types':{'tcp/ip':4, 
                  'phpmyadmin':5}, 
                 'native_extention':{FULL_BACKUP_CONST: ".sql", 
                  INC_BACKUP_CONST: ""}, 
                 'client_util':MYSQL_CONST, 
                 'default_path':AGENT_UTILS_PATH["mysql-path"], 
                 'default_util':"mysql-path"}, 
 
 POSTGRESQL_CONST: {'default_port':5432, 
                    'connection_types':{"tcp/ip": 6}, 
                    'native_extention':{'Plain':".sql", 
                     'Tar':".tar", 
                     'Custom':".custom"}, 
                    'client_util':"psql", 
                    'default_path':AGENT_UTILS_PATH["psql-path"], 
                    'default_util':"psql-path"}, 
 
 POSTGRES_CONST: {'default_port':5432, 
                  'connection_types':{"tcp/ip": 6}, 
                  'native_extention':{FULL_BACKUP_CONST: ".sql", 
                   INC_BACKUP_CONST: ""}, 
                  'client_util':"psql", 
                  'default_path':AGENT_UTILS_PATH["psql-path"], 
                  'default_util':"psql-path"}, 
 
 MSSQL_CONST: {'default_port':1433, 
               'connection_types':{"tcp/ip": 1}, 
               'native_extention':{FULL_BACKUP_CONST: ".bak", 
                DIFF_BACKUP_CONST: ".bak", 
                LOG_BACKUP_CONST: ".bak"}, 
               'client_util':"sqlcmd", 
               'default_path':AGENT_UTILS_PATH["sqlcmd-path"], 
               'default_util':"sqlcmd-path"}, 
 
 XTRABACKUP_CONST: {'default_port':3306, 
                    'connection_types':{"tcp/ip": 8}, 
                    'native_extention':{FULL_BACKUP_CONST: "", 
                     INC_BACKUP_CONST: ""}, 
                    'client_util':XTRABACKUP_CONST, 
                    'default_path':AGENT_UTILS_PATH["xtrabackup-path"], 
                    'default_util':"xtrabackup-path"}, 
 
 MONGO_CONST: {'default_port':27017, 
               'connection_types':{"tcp/ip": 9}, 
               'native_extention':{FULL_BACKUP_CONST: ""}, 
               'client_util':MONGO_CONST, 
               'default_path':AGENT_UTILS_PATH["mongo-path"], 
               'default_util':"mongo-path"}, 
 
 MONGODB_CONST: {'default_port':27017, 
                 'connection_types':{"tcp/ip": 9}, 
                 'native_extention':{FULL_BACKUP_CONST: ""}, 
                 'client_util':MONGO_CONST, 
                 'default_path':AGENT_UTILS_PATH["mongo-path"], 
                 'default_util':"mongo-path"}, 
 
 AZURESQL_CONST: {'default_port':1433, 
                  'connection_types':{"tcp/ip": 2}, 
                  'native_extention':{FULL_BACKUP_CONST: ".bacpac"}, 
                  'client_util':AZURESQL_CONST, 
                  'default_path':AGENT_UTILS_PATH["sqlcmd-path"], 
                  'default_util':"sqlcmd-path"}}
LOG_TYPES = {
 'ERROR': '"ERROR"', 
 'INFO': '"INFO"', 
 'DEBUG': '"DEBUG"', 
 'WARNING': '"WARNING"'}
APP_ROOT_DIR = "/opt/sqlbak/"
CONFIG = {'DYNAMIC_SETTINGS_FILE_NAME':"dynamic_settings.json", 
 'DEFAULT_DOWNLOAD_DIR':"Downloads", 
 'DEFAULT_BACKUP_DIR':"backups/", 
 'PATH_TO_APP':APP_ROOT_DIR, 
 'LOCALE':"en", 
 'SECRET_KEY':"#sdfWG21-SDFsd@1", 
 'WEB_API_PATH':"web_api_protocol.txt", 
 'DB_NAME':"sqlbak.db", 
 'APP_NAME':"sqlbak", 
 'DEV_COMMAND':"sqlbak_build.py", 
 'PATH_TO_DIST':"./dist/", 
 'DEFAULT_ROOT_WORK_DIR':"/tmp/sqlbak/", 
 'PATH_TO_LOGS':"logs/", 
 'PATH_TO_COMPRESSED_LOGS':"compressed_logs/", 
 'APP_VERSION':"1.11.4", 
 'MSSQL_BACKUP_DESC':"SqlBakForLinux Backup", 
 'PATH_TO_PACKAGE':APP_ROOT_DIR + "sqlbak.pkg", 
 'PATH_TO_INSTALL_ID':"/dev/sqlbak.pranas.txt", 
 'PATH_TO_FILE_LIST_OUT':APP_ROOT_DIR + "{0}_file_list_output.txt", 
 'PATH_TO_CUSTOM_CONSOLE_COMMANDS':APP_ROOT_DIR + "console_commands.json", 
 'PATH_TO_LOG_BACKUP':"/tmp/log_backup_mysq_{0}.sql"}
UPDATE_APP_SOURCES = {'AUTO':0, 
 'MANUALLY':1}
COMPRESSION_LEVELS = {COMPRESSION_ENGINE_ZIP: {"None": "-0", 
                          "Lowest": "-3", 
                          COMPRESSION_LEVEL_DEFAULT: "-6", 
                          "Highest": "-9"}, 
 
 COMPRESSION_ENGINE_7Z: {"None": "-mx=0", 
                         "Lowest": "-mx=1", 
                         COMPRESSION_LEVEL_DEFAULT: "-mx=5", 
                         "Highest": "-mx=9"}}
COMPRESSION_PRIORITIES = {"Idle": "-10", 
 "BelowNormal": "-5", 
 COMPRESSION_PRIORITY_DEFAULT: "0", 
 "AboveNormal": "5", 
 "High": "10"}
CONSOLE_COLORS = {
 'RED': '"RED"', 
 'GREEN': '"GREEN"', 
 'WHITE': '"WHITE"', 
 'GREY': '"GREY"'}
RESTORE_STATUSES = {
 'CREATED': 0, 
 'DOWNLOADING': 1, 
 'DOWNLOADED': 2, 
 'UNCOMPRESSING': 3, 
 'UNCOMPRESSED': 4, 
 'RESTORING': 5, 
 'RESTORED': 6, 
 'FAILED': 7, 
 'CANCELED': 8}
DOWNLOAD_STATUSES = {
 'CREATED': 0, 
 'DOWNLOADING': 1, 
 'DOWNLOADED': 2, 
 'FAILED': 3}
FTP_PROTOCOLS = {
 'FTP': '"ftp"', 
 'SFTP': '"sftp"', 
 'FTP_IMPLICIT': '"ftp_implicit"', 
 'FTP_EXPLICIT': '"ftp_explicit"'}
PROCESS_TYPES = {
 'BACKUP': 0, 
 'RESTORE_BACKUP': 1, 
 'DOWNLOAD_BACKUP': 2, 
 'DOWNLOAD_FOLDER': 3}
FEATURES = {
 1: '"AESEncryption"', 
 2: '"BackupHistory"', 
 3: '"DownAlerts"', 
 4: '"HealthCheck"', 
 5: '"ExtendedSupport"'}
DESTINATION_FEATURES = {0:"FTP", 
 1:"FTPS", 
 2:"SFTP"}
BACKUP_JOB_MODE = {'MANUAL':1, 
 'SCHEDULE':2, 
 'CLI':3}
EVENTS_ID = {'ERROR':1, 
 'FORCE_UPDATE':2006}
EVENT_TYPES = {
 'UNKNOWN': 0, 
 'ERROR': 1, 
 'WARNING': 2, 
 'INFO': 3, 
 'SUCCESS_AUDIT': 4, 
 'FAILED_AUDIT': 5}
DATE_TIME_FORMATS = [
 '%m/%d/%Y %H:%M:%S.%f', 
 '%m/%d/%Y %H:%M:%S', 
 '%m/%d/%Y %H:%M', 
 '%Y-%m-%d %H:%M:%S.%f', 
 '%Y-%m-%d %H:%M:%S', 
 '%Y%m%d']
KNOWLEDGE_BASE_LINKS = {'MYSQL_NOT_FOUND':{'code':"#[DBMS-MYSQL:100001]", 
  'link':"https://sqlbak.com/blog/mysql-dbms-bin-sh-1-usr-bin-mysql-not-found/"}, 
 'SQLCMD_NOT_FOUND':{'code':"#[DBMS-MSSQL:100000]", 
  'link':"https://sqlbak.com/blog/ms-sql-server-dbms-bin-sh-1-opt-mssql-tools-bin-sqlcmd/"}, 
 'PSQL_NOT_FOUND':{'code':"#[DBMS-MYSQL:100002]", 
  'link':"https://sqlbak.com/blog/postgresql-dbms-bin-sh-1-usr-bin-psql-not-found/"}, 
 'FAILED_MYSQL_INC_SETUP':{'code':"#[DBMS-MYSQL:100003]", 
  'link':"https://sqlbak.com/blog/how-to-enable-binary-log-in-linux/"}, 
 'INC_BACKUP_NOT_SUPPORTED_FOR_REMOTE_MYSQL':{'code':"#[DBMS-MYSQL:100004]", 
  'link':"https://sqlbak.com/blog/about-mysql-server-incremental-backups-in-sqlbak/"}}
LINUX_DISTROS = {'DEB':[
  "debian", "ubuntu", "raspbian", "linuxmint"], 
 'RPM':[
  'rhel', 'centos', 'sles', 'suse', 'fedora', 'ol', 'amzn', 'almalinux']}
MYSQL_DUMP_CHECKSUM_PARAMS = [
 '--no-create-db', 
 '--no-data', 
 '--single-transaction', 
 '--quick', 
 '--routines', 
 '--skip-add-drop-table', 
 '--skip-comments', 
 '--skip-dump-date', 
 '--triggers', 
 '--events', 
 '--compact', 
 '--force', 
 '--no-tablespaces', 
 '--skip-add-locks', 
 '--skip-tz-utc']
MYSQL_BIN_LOG_PARAMS_ON_GALERA = {
 'server-id': 1, 
 'binlog-format': '"ROW"', 
 'log-bin': '"/var/log/mysql/mysql-bin.log"', 
 'log_slave_updates ': 1}
MYSQL_BIN_LOG_PARAMS = {'server-id':1, 
 'binlog-format':"ROW", 
 'log-bin':"/var/log/mysql/mysql-bin.log"}

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/definitions.pyc
