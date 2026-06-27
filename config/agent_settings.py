import datetime, uuid
from sqlbak.exceptions import UnregisterAgent
from sqlbak.definitions import PIN_INTERVAL
from sqlbak.logger import log_error, log_module_method
from sqlbak.local_db import local_db_instanse
__agent_key = None
__is_active = True
working_directory = None
agent_id = None
pin_interval = PIN_INTERVAL
request_expiration = datetime.datetime.now()
session_id = str(uuid.uuid4())
utils_path = None

def is_registred_agent():
    global __agent_key
    return __agent_key is not None


def is_active():
    global __is_active
    return __agent_key is not None and __is_active


def get_agent_key():
    if __agent_key is None:
        raise UnregisterAgent()
    else:
        return __agent_key


def reload_global_config():
    global __agent_key
    global __is_active
    global agent_id
    global pin_interval
    global request_expiration
    global session_id
    global utils_path
    global working_directory
    try:
        agent = local_db_instanse.get_current_agent()
        __agent_key = agent["AgentKey"]
        working_directory = agent["WorkingDir"]
        agent_id = agent["AgentId"]
        __is_active = agent["IsActive"]
        session_id = agent["SessionId"]
        utils_path = agent["UtilsPath"]
    except Exception as e:
        try:
            log_error(e, "Failed to reload job settings")
            is_active = True
        finally:
            e = None
            del e

    try:
        request_params = local_db_instanse.get_request_params()
        if request_params:
            try:
                request_expiration = datetime.datetime.strptime(request_params["RequestExpiration"], "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                request_expiration = datetime.datetime.now()
            else:
                pin_interval = int(int(request_params["RequestInterval"]) / 1000 if request_expiration >= datetime.datetime.now() else PIN_INTERVAL)
        else:
            pin_interval = PIN_INTERVAL
            request_expiration = datetime.datetime.now()
    except Exception as e:
        try:
            log_error(e, "Failed to reload request_params")
            pin_interval = PIN_INTERVAL
            request_expiration = datetime.datetime.now()
        finally:
            e = None
            del e


reload_global_config()

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/config/agent_settings.pyc
