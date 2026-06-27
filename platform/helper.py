import os
from sqlbak.logger import log_module_method

@log_module_method
def is_app_run_in_docker_container():
    return os.path.exists("/.dockerenv")

