from sqlbak.helpers.util_paths import cross_params_and_default_util_path
from sqlbak.local_db import local_db_instanse
from sqlbak.definitions import AGENT_UTILS_PATH, CONFIG, ALTERNATIVE_AGENT_UTILS_PATH
from sqlbak.helper import helper_instanse
from sqlbak.exchange_message.remote_server_requests import remoute_server_request_instanse
from sqlbak.trace_event import trace_event_instanse
from sqlbak.app_output import APP_OUTPUT

def register_new_agent_on_the_sqlbak_server(secret_key, computer_name, utils_path, app_version, session_id):
    res = remoute_server_request_instanse.register_agent(secret_key, computer_name, utils_path, app_version, session_id)
    if not res["IsSuccess"]:
        raise Exception(APP_OUTPUT[CONFIG["LOCALE"]]["FAILED_REG_CLIENT"].format(str(res["ErrorMessage"])))
    return res["Data"]


def register_app(agent_key, agent_name):
    utils_path = cross_params_and_default_util_path({})
    session_id = helper_instanse.get_uuid()
    app_version = CONFIG["APP_VERSION"].split(".")
    app_version = {'major_version':app_version[0], 
     'minor_version':app_version[1], 
     'patch_version':app_version[2]}
    agent = register_new_agent_on_the_sqlbak_server(agent_key, agent_name, utils_path, app_version, session_id)
    local_db_instanse.update_down_alert_interval(agent["Profile"]["Plan"]["CheckTimeout"])
    local_db_instanse.add_new_agent(agent, utils_path, app_version, session_id)
    trace_event_instanse.trace_register_app()


def unregister_app():
    try:
        agent = local_db_instanse.get_current_agent()
        if agent is None:
            raise Exception(APP_OUTPUT[CONFIG["LOCALE"]]["UNREGISTERED_COMP"])
        res = remoute_server_request_instanse.set_agent_activity(agent["AgentKey"], False)
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))
        local_db_instanse.update_agent_activity(agent["AgentKey"], 0)
        local_db_instanse.remove_all_database_data()
    except Exception as e:
        try:
            raise Exception(APP_OUTPUT[CONFIG["LOCALE"]]["FAILED_DEACTIVATE_CLIENT"].format(str(e)))
        finally:
            e = None
            del e

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/helpers/app_registration.pyc
