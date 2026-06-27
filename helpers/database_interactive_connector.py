
import json, os, paramiko, sqlbak.config.agent_settings
from sqlbak.connection import Connection
from sqlbak.local_db import local_db_instanse
from sqlbak.definitions import CONFIG, DYNAMIC_SETTING_LOGGING_ACTIVATED, DYNAMIC_SETTING_LOGGING_LEVEL, DYNAMIC_SETTING_LOGGING_RM_TEMP_FILES, DYNAMIC_SETTING_LOGGING_MYSQLBINLOG_ADDITIONAL_ARGUMENTS
from sqlbak.exchange_message.remote_server_requests import remoute_server_request_instanse
from sqlbak.helper import helper_instanse
from sqlbak.helpers.app_registration import unregister_app
import getpass
__GLOBAL_EXIT = "global exit"
__RETURN_BACK = "return back"
__SSH_HOST_IS_NOT_SQL_HOST_MESSAGE = "SQL host is not the SSH host. It's usually the localhost or an address relative to the server where the SSH connection is established."

def print_error_message(text):
    print()
    print(f"\x1b[91m{text}\x1b[0m")
    print()


def print_success_message(text):
    print()
    print(f"\x1b[92m{text}\x1b[0m")
    print()


def print_choice_item(number, text, focus_item=False):
    number = str(number).ljust(2)
    if focus_item:
        print(f"\x1b[97m{number}\x1b[0m" + " " + f"\x1b[97m{text}\x1b[0m")
    else:
        print(f"\x1b[37m{number}\x1b[0m" + " " + f"\x1b[37m{text}\x1b[0m")


def print_info_message(text):
    print()
    print(f"\x1b[96m{text}\x1b[0m")
    print()


def print_property_state(name, value):
    print(f"\x1b[90m{name}\x1b[0m" + ": " + f"\x1b[90m{value}\x1b[0m")


def print_master_message(text):
    print()
    print(f"\x1b[93m{text}\x1b[0m")


def print_line():
    print("\n--------------------------------------------------\n")


def try_again_menu(master_message):
    print_master_message(master_message)
    return get_user_input("Try again? ", default_value=True)


def check_ssh_connectionParse error at or near `SETUP_FINALLY' instruction at offset 0


def ssh_connector(local_maped_port, db_type, default_values={}):
    if default_values.get("ssh-host", None) is not None:
        ssh_host = get_user_input("SSH Host", default_value=(default_values.get("ssh-host")))
    else:
        ssh_host = get_user_input("SSH Host", sample=("{}.remoute.com".format(db_type)))
    ssh_port = get_user_input("SSH Port", default_value=(default_values.get("ssh-paort", 22)))
    ssh_local_mapped_port = get_user_input("SSH Local Mapped Port", default_value=(default_values.get("ssh-local-mapped-port", local_maped_port)))
    ssh_user = get_user_input("SSH User", default_value=(default_values.get("ssh-user", "root")))
    ssh_password = get_user_input("SSH Password", shadow_input=True)
    if check_ssh_connection(ssh_host, ssh_port, ssh_user, ssh_password):
        print_success_message("SSH connection established")
        return         return {'use-ssh': True, 
         'ssh-host': ssh_host, 
         'ssh-port': ssh_port, 
         'ssh-local-mapped-port': ssh_local_mapped_port, 
         'ssh-user': ssh_user, 
         'ssh-password': ssh_password}
    print_error_message("SSH connection failed")
    return


def get_empty_ssh_connection(port):
    return {
     'use-ssh': False, 
     'ssh-host': '""', 
     'ssh-port': 22, 
     'ssh-local-mapped-port': port, 
     'ssh-user': '""', 
     'ssh-password': '""'}


def empty_connection_data(db_type):
    return {'db-type':db_type, 
     'connection-type':"tcp/ip"}


def get_user_inputParse error at or near `LOAD_FAST' instruction at offset 0


def console_menuParse error at or near `LOAD_GLOBAL' instruction at offset 0


def get_util_patths():
    agent = local_db_instanse.get_current_agent
    current_utils_path = json.loads(agent["UtilsPath"])
    return current_utils_path


def check_util_path(util_name, install_command_debian, install_command_redhat):
    util_path = get_util_patths()[util_name]
    if not os.path.exists(util_path):
        print_error_message("{} is not found".format(util_path) + "\n" + "Please try to install the client with the following command.")
        if os.path.exists("/etc/debian_version"):
            print(install_command_debian)
        else:
            if os.path.exists("/etc/redhat-release"):
                print(install_command_redhat)
        print()
        return False
    return True


def update_utils_path(util_name, path):
    agent = local_db_instanse.get_current_agent
    if os.path.exists(path):
        print_success_message("{} is found".format(path))
        current_utils_path = json.loads(agent["UtilsPath"])
        current_utils_path[util_name] = path
        local_db_instanse.update_agent_utils_path(agent["AgentKey"], json.dumps(current_utils_path))
        print_success_message("{} updated".format(util_name))
    else:
        print_error_message("{} is not found".format(path))


def try_connectionParse error at or near `SETUP_FINALLY' instruction at offset 0


def postgresql_connectorParse error at or near `LOAD_GLOBAL' instruction at offset 0


def mysql_connectorParse error at or near `LOAD_GLOBAL' instruction at offset 0


def sql_server_connectorParse error at or near `LOAD_GLOBAL' instruction at offset 0


def mongo_connectorParse error at or near `LOAD_GLOBAL' instruction at offset 0


def update_connections():
    connection_handler = Connection()
    print_master_message("Here are your current connections:")
    print_line()
    if connection_handler.get_connections_by_dbms_type("all"):
        print_line()
        print_master_message("Please enter the connection ID you want to update: ")
        connection_id = get_user_input("Connection ID", type_of_value=int)
        connection_data = connection_handler.get_connection_data_by_id(connection_id)
        if connection_data == None:
            print_error_message("Connection with ID {} not found".format(connection_id))
        else:
            connection_params = connection_handler.extract_connection_params(connection_data)
            if connection_params["db-type"] == "postgresql":
                result = postgresql_connectorconnection_paramsconnection_id
            else:
                if connection_params["db-type"] == "mongo":
                    result = mongo_connectorconnection_paramsconnection_id
                else:
                    if connection_params["db-type"] == "mssql":
                        result = sql_server_connectorconnection_paramsconnection_id
                    else:
                        if connection_params["db-type"] == "mysql":
                            result = mysql_connectorconnection_paramsconnection_id
                        else:
                            raise Exception("Unsupported database type")
            if result == __RETURN_BACK:
                return __RETURN_BACK
            return __GLOBAL_EXIT
    else:
        return __RETURN_BACK


def delete_connection():
    connection_handler = Connection()
    print_master_message("Here are your current connections:")
    print_line()
    if connection_handler.get_connections_by_dbms_type("all"):
        print_line()
        connection_id = get_user_input("Please enter the connection ID you want to delete: ", type_of_value=int)
        try:
            if connection_handler.get_jobs_by_connection_id(int(connection_id)) != None:
                print_error_message("Connection is used in a backup job. If you delete this connection, the backup job will be broken.")
                user_choice = get_user_input("Do you want to continue?", type_of_value=bool)
                if user_choice:
                    connection_handler.remove_agent_connection({"connection-id": (int(connection_id))}, should_print=False, force=True)
                    print_success_message(f"Connection with ID {connection_id} has been removed.")
                else:
                    print_master_message("Returning back.")
            else:
                connection_handler.remove_agent_connection({"connection-id": (int(connection_id))})
                print_success_message(f"Connection with ID {connection_id} has been removed.")
        except KeyError:
            print_error_message("Connection with given ID does not exist.")

    else:
        return __RETURN_BACK


def add_database_menu():
    console_menu"Please note that your database credentials are stored securely on our server.\n"[
     (
      "MySQL", mysql_connector, True),
     (
      "PostgreSQL", postgresql_connector, True),
     (
      "SQL Server", sql_server_connector, False),
     (
      "Mongo", mongo_connector, False)]


def connection_menu(first_menu=False):
    console_menu"Please choose what you want to do:"[
     (
      "Add connection", add_database_menu, True),
     (
      "Delete connection", delete_connection, False),
     (
      "Update connection", update_connections, False)]


def print_agent_info():
    try:
        print_master_message("Backup Agent Information:")
        agent = local_db_instanse.get_current_agent
        request_result = remoute_server_request_instanse.get_agent_status(agent["AgentKey"])
        if not request_result["IsSuccess"]:
            print_error_message(f'Unable to retrieve agent status from sqlbak.com: {request_result["ErrorMessage"]}')
            is_agent_activated = "unknown"
        else:
            is_agent_activated = "activated" if request_result["Data"]["IsActive"] else "deactivated"
        app_version = CONFIG["APP_VERSION"]
        print_info_message(f'Dashboard Name: {agent["AgentName"]}\n' + f"Application Version: {app_version} \n" + f'Account Name: {agent["AccountName"]}\n' + f"Status: {is_agent_activated}")
        jobs = local_db_instanse.get_jobs
        scheduled_jobs_count = len([job for job in jobs if int(job["IsScheduled"]) == 1])
        print_info_message(f"Jobs Count: {len(jobs)} ({scheduled_jobs_count} scheduled)")
        print_info_message(f"DBMS Connections Count: {len(local_db_instanse.get_dbms_connections)}")
    except Exception as e:
        try:
            print_error_message(f"An error occurred: {e}")
        finally:
            e = None
            del e


def change_logging_state():
    if helper_instanse.get_dynamic_settings_value(DYNAMIC_SETTING_LOGGING_ACTIVATED):
        user_choise = get_user_input("Do you want to disable logging? ", type_of_value=bool)
        if user_choise:
            helper_instanse.update_dynamic_settings_property(DYNAMIC_SETTING_LOGGING_ACTIVATED, False)
            print_success_message("Logging disabled")
    else:
        user_choise = get_user_input("Do you want to enable logging? ", type_of_value=bool)
        if user_choise:
            helper_instanse.update_dynamic_settings_property(DYNAMIC_SETTING_LOGGING_ACTIVATED, True)
            print_master_message("Logging enabled")
    return __RETURN_BACK


def change_logging_level():
    if not helper_instanse.get_dynamic_settings_value(DYNAMIC_SETTING_LOGGING_ACTIVATED):
        print_master_message("To change the logging level, logging must be enabled first.")
        change_logging_state()
    else:
        return helper_instanse.get_dynamic_settings_value(DYNAMIC_SETTING_LOGGING_ACTIVATED) or __RETURN_BACK

    def update_dynamic_logging_level(level):
        helper_instanse.update_dynamic_settings_property(DYNAMIC_SETTING_LOGGING_LEVEL, level)
        print_success_message(f"Logging level set to {level}")

    return console_menu"Choose the logging level that will determine the amount of information recorded in the logs:"[
     (
      "Errors Only (small size)", (lambda: update_dynamic_logging_level("ERROR")), False),
     (
      "Debug Mode (standard size)", (lambda: update_dynamic_logging_level("DEBUG")), True),
     (
      "Info Mode (large size)", (lambda: update_dynamic_logging_level("INFO")), False)]


def advanced_log_settings_menu():
    print_info_message("Logging assists developers in debugging. Typically, SqlBak developers may request app logs from you.\nHowever, please note that continuous logging may slow down the application and consume significant disk space.")
    print_master_message("Current debug settings:")
    print_property_state"Logging Status"helper_instanse.get_dynamic_settings_value(DYNAMIC_SETTING_LOGGING_ACTIVATED)
    print_property_state"Logging Level"helper_instanse.get_dynamic_settings_value(DYNAMIC_SETTING_LOGGING_LEVEL)
    return console_menu"Modify debug settings below:"[
     (
      "Toggle Logging", change_logging_state, True),
     (
      "Set Logging Level", change_logging_level, False)]


def change_remove_temp_files_setting():
    print_master_message("Turning off this setting may help you to debug the application. \n However, please note that disabling this setting may lead to disk space overflow.")
    if helper_instanse.get_dynamic_settings_value(DYNAMIC_SETTING_LOGGING_RM_TEMP_FILES):
        user_choice = get_user_input("Do you want to disable 'Remove temporary files' setting? ", type_of_value=bool)
        if user_choice:
            helper_instanse.update_dynamic_settings_property(DYNAMIC_SETTING_LOGGING_RM_TEMP_FILES, False)
    else:
        user_choice = get_user_input("Do you want to enable 'Remove temporary files' setting? ", type_of_value=bool)
        if user_choice:
            helper_instanse.update_dynamic_settings_property(DYNAMIC_SETTING_LOGGING_RM_TEMP_FILES, True)
    return __RETURN_BACK


def change_additional_arguments_for_mysqlbinlog_setting():
    print_master_message("Additional arguments for mysqlbinlog allow you to analyze binary logs. \nFor example, you can set '-vv' to include decoded SQL instructions in backup files.")
    additional_arguments = get_user_input"Enter additional arguments for mysqlbinlog (e.g., '-vv'):"str
    helper_instanse.update_dynamic_settings_property(DYNAMIC_SETTING_LOGGING_MYSQLBINLOG_ADDITIONAL_ARGUMENTS, additional_arguments)
    return __RETURN_BACK


def debug_settings_menu():

    def menu_info():
        print_master_message("Current debug settings:")
        print_property_state"Remove temporary files"helper_instanse.get_dynamic_settings_value(DYNAMIC_SETTING_LOGGING_RM_TEMP_FILES)
        print_property_state"Additional arguments for mysqlbinlog"helper_instanse.get_dynamic_settings_value(DYNAMIC_SETTING_LOGGING_MYSQLBINLOG_ADDITIONAL_ARGUMENTS)
        print()

    return console_menumenu_info[
     (
      "Change 'Remove temporary files' setting", change_remove_temp_files_setting, True),
     (
      "Change 'Additional arguments for mysqlbinlog' setting", (lambda: helper_instanse.update_dynamic_settings_property(DYNAMIC_SETTING_LOGGING_MYSQLBINLOG_ADDITIONAL_ARGUMENTS, get_user_input"Enter additional arguments for mysqlbinlog:"str)), False)]


def change_dbms_utils_path_menu():
    print_master_message("DBMS Utils paths are used to execute SQL commands and perform backup operations on the database server.\nCurrent DBMS Utils paths:")
    utils_path = get_util_patths()
    max_key_length = max((len(key) for key in ))
    column_width = max26(max_key_length + 1)
    menu_items = []
    for key, value in utils_path.items:
        display_key = key.ljust(column_width)
        menu_items.append((f"{display_key}: {value}", (lambda k=key, v=value: update_utils_pathkget_user_input(f"New path for {k}:", default_value=v)), False))
    else:
        return console_menu"Select a DBMS Utils path to modify:"menu_items


def agent_configuration_menu():
    return console_menu"Here you can modify agent configuration."[
     (
      "Debug settings", advanced_log_settings_menu, True),
     (
      "Advanced log settings", debug_settings_menu, False),
     (
      "DBMS Utils path", change_dbms_utils_path_menu, False)]


def deactive_agent():
    print_master_message("If you deactivate the agent, all backup jobs will be deleted.")
    result = get_user_input("Are you sure you want to deactivate the agent?", type_of_value=bool)
    if result:
        unregister_app()
        print_success_message("Agent deactivated")
        sqlbak.config.agent_settings.reload_global_config
    return __GLOBAL_EXIT


def main_menuParse error at or near `SETUP_FINALLY' instruction at offset 0


if __name__ == "__main__":
    main_menu()
