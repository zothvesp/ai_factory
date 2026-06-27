from sqlbak.definitions import AGENT_UTILS_PATH, CONFIG, ALTERNATIVE_AGENT_UTILS_PATH
import os

def get_path_to_utils(util_name):
    try:
        if util_name in ALTERNATIVE_AGENT_UTILS_PATH:
            if os.path.exists(ALTERNATIVE_AGENT_UTILS_PATH[util_name]):
                return                 return ALTERNATIVE_AGENT_UTILS_PATH[util_name]
    except:
        pass
    else:
        return AGENT_UTILS_PATH[util_name]


def renew_utils_path(agent_utils):
    for util in AGENT_UTILS_PATH:
        if util not in agent_utils:
            agent_utils = get_path_to_utils(util)


def cross_params_and_default_util_path(params):
    all_custom_utils_path = {'mysqldump-path': None, 
     'mysql-path': None, 
     'mysql-binlog-base-path': None, 
     'mysql-binlog-index-path': None, 
     'pgdump-path': None, 
     'psql-path': None, 
     'sqlcmd-path': None, 
     'mssql-data': None, 
     'xtrabackup-path': None, 
     'mysql-lib': None, 
     'mongo-path': None, 
     'mongodump-path': None, 
     'mongorestore-path': None, 
     'pg_restore-path': None, 
     'sqlpackage-path': None}
    for key in all_custom_utils_path:
        all_custom_utils_path[key] = params[key] if (key in params and params[key] is not None) else (get_path_to_utils(key))
    else:
        return all_custom_utils_path

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/helpers/util_paths.pyc
