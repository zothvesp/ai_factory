import os, sys
from sqlbak.console_handler import ConsoleHandler
from sqlbak.definitions import CONFIG
from sqlbak.app import App
from sqlbak.logger import log_func
from sqlbak.app_output import APP_OUTPUT

@log_func
def main():
    if len(sys.argv) <= 1:
        sys.argv.append("--menu")
    elif os.geteuid() != 0:
        print("SqlBak must be run with sudo!")
        return
        if sys.argv[1] in ('--start', '--stop'):
            app = App()
            if sys.argv[1] == "--start":
                app.start_app()
        else:
            app.stop_app()
    else:
        console_handler = ConsoleHandler()
        exit_code = console_handler.parse_console_command_with_params(sys.argv)
        if exit_code is not None:
            if exit_code != 0:
                sys.exit(exit_code)

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/run.pyc
