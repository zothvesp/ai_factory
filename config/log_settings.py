import json
from sqlbak.definitions import CONFIG, DYNAMIC_SETTING_LOGGING_RM_TEMP_FILES, DYNAMIC_SETTING_LOGGING_MYSQLBINLOG_ADDITIONAL_ARGUMENTS, DYNAMIC_SETTING_LOGGING_ACTIVATED, DYNAMIC_SETTING_LOGGING_LEVEL, DYNAMIC_SETTING_LOGGING_DEBUG_SIZE, DYNAMIC_SETTING_BASE_PERMISSION
is_active = False
log_level = "DEBUG"
log_line_size = 120
base_permissions = 775
rm_temp_files = True
mysqlbinlog_additional_arguments = "AUTO"

def reload_log_settings():
    global base_permissions
    global is_active
    global log_level
    global log_line_size
    global mysqlbinlog_additional_arguments
    global rm_temp_files
    try:
        with open(CONFIG["PATH_TO_APP"] + CONFIG["DYNAMIC_SETTINGS_FILE_NAME"], "r") as f:
            __json_content = json.loads(f.read())
            is_active = str(__json_content[DYNAMIC_SETTING_LOGGING_ACTIVATED]) == "True" or str(__json_content[DYNAMIC_SETTING_LOGGING_ACTIVATED]) == "true" if DYNAMIC_SETTING_LOGGING_ACTIVATED in __json_content else False
            log_level = __json_content[DYNAMIC_SETTING_LOGGING_LEVEL] if DYNAMIC_SETTING_LOGGING_LEVEL in __json_content else None
            log_line_size = int(__json_content[DYNAMIC_SETTING_LOGGING_DEBUG_SIZE]) if DYNAMIC_SETTING_LOGGING_DEBUG_SIZE in __json_content else 120
            base_permissions = int(__json_content[DYNAMIC_SETTING_BASE_PERMISSION]) if DYNAMIC_SETTING_BASE_PERMISSION in __json_content else 775
            rm_temp_files = not (DYNAMIC_SETTING_LOGGING_RM_TEMP_FILES in __json_content and __json_content[DYNAMIC_SETTING_LOGGING_RM_TEMP_FILES] == "False")
            mysqlbinlog_additional_arguments = __json_content[DYNAMIC_SETTING_LOGGING_MYSQLBINLOG_ADDITIONAL_ARGUMENTS] if DYNAMIC_SETTING_LOGGING_MYSQLBINLOG_ADDITIONAL_ARGUMENTS in __json_content else ""
    except:
        is_active = False
        log_level = "DEBUG"
        log_line_size = 120
        base_permissions = 775


reload_log_settings()

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/config/log_settings.pyc
