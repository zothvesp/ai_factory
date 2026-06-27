import sys
from getpass import getpass
from sqlbak.exceptions import ConsoleCommandError
from sqlbak.definitions import APP_NAME, CONFIG, CONSOLE_COLORS
from sqlbak.helper import Helper
from sqlbak.logger import log_method, log_only_exception
from sqlbak.local_db import LocalDB
from sqlbak.app_output import APP_OUTPUT

class ConsoleParser:

    def __init__(self):
        self.local_db = LocalDB()
        self.helper = Helper()
        self.parsed_command_and_params = None
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]
        self.commands_pattern = self.helper.get_console_commands()

    @log_only_exception
    def prepare_command_and_params(self, items):
        """
        Method receive array of entered commands
        Then we split a command and params with value for a further processing
        :param items: array of strings
        :return: None
        """
        command = items[1]
        passed_params = items[2[:None]] if len(items) > 2 else []
        self.handle_command_and_params(command, passed_params)

    @log_only_exception
    def handle_command_and_params(self, passed_command, passed_params):
        """
        A method receives a command and params entered in a console line.
        Detect command with the existing commands pattern.
        If a passed command has params then parse and check params in different ways.
        Send request to a server

        :param passed_command: string; a command which entered in console line
        :param passed_params: empty array or array of dicts; params which entered in console line
        :return: None
        """
        has_appropriate_command_sign = False
        for command in self.commands_pattern:
            if passed_command in (command["command"], command["short_command"]):
                has_appropriate_command_sign = True
                parsed_params = None
                if isinstance(passed_params, list):
                    if len(passed_params) > 0:
                        parsed_params = self.parse_params(passed_params)
                if not parsed_params:
                    if len(passed_params) > 0:
                        break
                self.validate_params(command, parsed_params)
                if parsed_params:
                    parsed_params = self.convert_short_params_to_full(command, parsed_params)
                if self.check_required_params(command, False, parsed_params):
                    break
                parsed_params = self.check_optional_params(command, parsed_params)
                if "params" in command:
                    if "conditional" in command["params"]:
                        result = self.check_conditional_params(command["command"], parsed_params)
                        if result is not None:
                            parsed_params = result
                        else:
                            if result is None and len(passed_params) > 0:
                                break
                self.prepare_parsed_command_and_params(command["command"], parsed_params)
                break
        else:
            if not has_appropriate_command_sign:
                self.helper.print_color_text(self.cm["INCORRECT_COMMAND"], CONSOLE_COLORS["RED"])
                sys.exit(0)

    def validate_params(self, command, parsed_params):
        all_params = []
        if "params" in command:
            if parsed_params is not None:
                optional_params = [x["name"] for x in command["params"]["optional"]] if "optional" in command["params"] else []
                required_params = [x["name"] for x in command["params"]["required"]] if "required" in command["params"] else []
                conditional_params = [x["name"] for x in command["params"]["conditional"]] if "conditional" in command["params"] else []
                for long_and_short in optional_params + required_params + conditional_params:
                    for long_parameter_name in long_and_short:
                        all_params += [long_parameter_name] + [long_and_short[long_parameter_name]]
                    else:
                        unknow_parameters = [param for param in parsed_params if param not in all_params]
                        if len(unknow_parameters) > 0:
                            error_message = "{}: unrecognized option '{}' \n".format(APP_NAME, ",".join(unknow_parameters))
                            error_message += "Try 'sudo sqlbak --help --command={}' for more information.".format(command["command"].strip("-"))
                            raise ConsoleCommandError(error_message, 1)

    @log_only_exception
    def check_required_params(self, command, is_command_short, params):
        """
        Detect if the existed command needs required params and print an error if the command needs this and they
        were not passed.
        :param command: dict; a part of the existed command"s dict
        :param is_command_short: bool; True if a passed command is short otherwise False
        :param params: None or a passed param"s dict
        :return: False if the existed command needs required params and they were passed via console line.
        Return True if the existed command needs required params and they were passed via console line.
        """
        if "params" in command:
            if "required" in command["params"]:
                if isinstance(command["params"]["required"], list):
                    if len(command["params"]["required"]) > 0:
                        required_params_str = ""
                        is_required_params_missed = False
                        for param in command["params"]["required"]:
                            full_required_param = list(param["name"])[0]
                            short_required_param = param["name"][full_required_param]
                            required_params_str += ("-" + short_required_param if is_command_short else "--" + full_required_param) + (" value " if is_command_short else "=value ")
                            if params is None or full_required_param not in params:
                                is_required_params_missed = True

                        if is_required_params_missed:
                            self.helper.print_color_text(self.cm["INCORRECT_REQUIRED_PARAMS"].format(sys.argv[0], command["short_command"] if is_command_short else command["command"], required_params_str))
                            return True
        return False

    @log_only_exception
    def check_optional_params(self, command, params):
        """
        Detect if the existed command has optional params.
        If the command has optional params and they were not passed
        then find default values for such params and put them in passed params dict
        :param command: dict; a part of the existed command"s dict
        :param params: None or a passed param"s dict
        :return: None or a passed param"s dict
        """
        if "params" in command:
            if "optional" in command["params"]:
                if isinstance(command["params"]["optional"], list):
                    if len(command["params"]["optional"]) > 0:
                        for param in command["params"]["optional"]:
                            full_optional_param = list(param["name"])[0]
                            if not params is None:
                                if not isinstance(params, dict) or full_optional_param not in params:
                                    if params is not None:
                                        if isinstance(params, dict):
                                            params[full_optional_param] = param["value"]
                                    if params is None:
                                        params = {}
                                    params[full_optional_param] = param["value"]

        return params

    @log_only_exception
    def check_conditional_params(self, command, params):
        """
        There is commands pattern which has conditionally optional params. Params which depends from other params
        and become required if that params take especial values.
        Method detect if a passed command has such conditionally optional params and if it has check value of params
        influence on other params

        :param command: string; a passed command
        :param params: None or a passed param"s dict
        :return: None or a passed param"s dict
        """
        if command == "--add-connection":
            checked_param = "use-ssh"
            if checked_param in params:
                checked_param_value = params[checked_param]
                parsed_checked_param_value = checked_param_value.lower()
                if parsed_checked_param_value in ('yes', 'y'):
                    params[checked_param] = 1
                    ssh_conditional_params = [
                     "ssh-host", "ssh-user", "ssh-password"]
                    for param in ssh_conditional_params:
                        if not param not in params:
                            if params[param].strip() == "":
                                if param != "ssh-password":
                                    self.helper.print_color_text(self.cm["INCORRECT_CONDITIONAL_PARAMS"].format(checked_param, checked_param_value, param), CONSOLE_COLORS["RED"])
                                    return                                     return None
                            if not param not in params:
                                if params[param].strip() == "":
                                    if param == "ssh-password":
                                        password = None
                                        while True:
                                            if password is None:
                                                password = self.handle_entered_text(checked_param)

                                params[param] = password
                                return params
                        else:
                            pass

                params[checked_param] = 0
        else:
            if command == "--update-connection":
                checked_param = "use-ssh"
                if checked_param in params:
                    checked_param_value = params[checked_param]
                    parsed_checked_param_value = None
                    if checked_param_value is not None:
                        if isinstance(checked_param_value, str):
                            parsed_checked_param_value = checked_param_value.lower()
                    if parsed_checked_param_value is not None and parsed_checked_param_value in ('yes',
                                                                                                 'y'):
                        params[checked_param] = 1
                        ssh_conditional_params = [
                         "ssh-host", "ssh-user", "ssh-password"]
                        connection = self.local_db.get_connection_by_id_with_alias_params(params["connection-id"])
                        for param in ssh_conditional_params:
                            if "-" in param:
                                index_sign = param.index("-")
                                parsed_param = param.title()
                                alias_param = parsed_param[None[:index_sign]] + parsed_param[(index_sign + 1)[:None]]
                            else:
                                alias_param = param.title()
                            local_db_param_value = connection[alias_param]
                            if params[param] is None:
                                params[param] = local_db_param_value
                            if param not in params or params[param] is None or params[param] == "None" or params[param].strip() == "":
                                if param != "ssh-password":
                                    self.helper.print_color_text(self.cm["INCORRECT_CONDITIONAL_PARAMS"].format(checked_param, checked_param_value, param), CONSOLE_COLORS["RED"])
                                    return                                     return None
                                if param == "ssh-password" and not params[param] is None or params[param] == "None":
                                    if params[param].strip() == "":
                                        pass
                                    password = None
                                    if password is None:
                                        password = self.handle_entered_text(param)
                            else:
                                params[param] = password
                                return params

                    else:
                        params[checked_param] = 0
            return params

    @log_only_exception
    def handle_entered_text(self, param):
        """
        Method ask enter a param"s value in a console line
        If value entered and it is not empty then return it"s value otherwise print an error and return None
        :param param: string;
        :return: None or a new value (string)
        """
        value = getpass("Enter a {0}: ".format(param))
        if value.strip() == "":
            self.helper.print_color_text(self.cm["EMPTY_PARAM_VALUE"].format(param), CONSOLE_COLORS["RED"])
            return
        return value

    @log_only_exception
    def parse_full_params(self, params):
        """
        Method receives entered by user full params, handle them, check errors and
        if everything is ok send parsed params
        :param params: array of strings; entered by user full params
        :return: False if an error occurred during a parsing or a dictionary with parameters
        """
        params_dict = {}
        error = False
        for param in params:
            index_of_equal_sign = param.find("=")
            if index_of_equal_sign != -1:
                param_name = param[0[:index_of_equal_sign]]
                if len(param_name) >= 3:
                    if "--" == param_name[0[:2]]:
                        param_name = param_name.lstrip("--")
                        param_value = param[index_of_equal_sign[:None]]
                        if len(param_value) > 1:
                            param_value = param_value[1[:None]]
                            if len(param_value) > 0:
                                if param_name in params_dict:
                                    pass
                                else:
                                    params_dict[param_name] = param_value
                            else:
                                error = True
                                break
                        else:
                            error = True
                            break
                    else:
                        error = True
                        break
                else:
                    error = True
                break
            elif param == "--password":
                password = None
                while True:
                    if password is None:
                        password = self.request_user_password()
                        if password:
                            params_dict["password"] = password

            else:
                error = True
                break

        if error:
            self.helper.print_color_text(self.cm["INCORRECT_PARAMS"], CONSOLE_COLORS["RED"])
            return False
        return params_dict

    def parse_params(self, lexems):
        """
        Method receives entered by user params, handle them, check errors and
        if everything is ok send parsed params
        :param params: array of strings; entered by user params
        :return: Exception if an error occurred during a parsing or a dictionary with parameters
        """
        params_dict = {}
        i = 0
        error_mask = "invalid syntax: %s"
        while i < len(lexems):
            lexem = lexems[i]
            if len(lexem) < 2:
                raise Exception(error_mask % lexem)
            elif lexem[0] == "-":
                if lexem[1] == "-":
                    if "=" in lexem:
                        param_name = lexem[2[:None]].split("=")[0]
                        param_value = lexem.split("=")[1]
                        params_dict[param_name] = param_value
                    else:
                        raise Exception(error_mask % lexem)
                else:
                    param_name = lexem[1[:None]]
                    i += 1
                    if not param_name == "p" or i == len(lexems) or lexems[i][0] == "-":
                        password = getpass()
                        params_dict[param_name] = password
                    else:
                        if i >= len(lexems):
                            raise Exception(error_mask % lexem)
                        else:
                            param_value = lexems[i]
                            params_dict[param_name] = param_value
            else:
                raise Exception(error_mask % lexem)
            i += 1

        return params_dict

    @log_method
    def request_user_password(self):
        password = getpass()
        strip_password = password.strip()
        if not strip_password:
            return
        return strip_password

    @log_only_exception
    def parse_short_params(self, params):
        """
        Method receives entered by user short params, handle them, check errors and
        if everything is ok send parsed params
        :param params: array of strings; entered by user short params
        :return: False if an error occurred during a parsing or a dictionary with parameters
        """
        params_dict = {}
        is_error = False
        for i, item in enumerate(params):
            if i % 2 == 0:
                if "-" != item[0]:
                    is_error = True
                    break
                key = item.lstrip("-")
                params_dict[key] = None
            else:
                params_dict[key] = item
            i += 1
        else:
            if "p" in params_dict:
                if params_dict["p"] is None:
                    password = None
                    while password is None:
                        password = self.request_user_password()
                        if password:
                            params_dict["p"] = password

            if is_error:
                self.helper.print_color_text(self.cm["INCORRECT_PARAMS"], CONSOLE_COLORS["RED"])
                return False
            return params_dict

    @log_only_exception
    def convert_short_params_to_full(self, existed_command, params):
        """
        Convert short params to full params
        :param existed_command: a part of the existed commands pattern
        :param params: passed params
        :return: a new param"s dict
        """
        new_params_dict = {}
        if "params" in existed_command:
            for param in existed_command["params"]:
                for existed_param in existed_command["params"][param]:
                    p = existed_param["name"]
                    full_existed_param = list(p)[0]
                    short_existed_param = p[full_existed_param]
                    if short_existed_param in params:
                        value = params[short_existed_param]
                        new_params_dict[full_existed_param] = value
                    elif full_existed_param in params:
                        new_params_dict[full_existed_param] = params[full_existed_param]

        return new_params_dict

    @log_only_exception
    def prepare_parsed_command_and_params(self, command, params):
        """
        Method prepare a request to a local rest server and saves it in the self.rest_request variable
        :param command: string; a passed command
        :param params: passed and parsed params
        :return: None
        """
        for c in self.commands_pattern:
            if c["command"] == command:
                local_rest_settings = c["local_rest_settings"]
                self.parsed_command_and_params = {'is_get_request':local_rest_settings["is_get_method"], 
                 'path':local_rest_settings["url"], 
                 'params':params, 
                 'command':command}
                break

    @log_only_exception
    def get_parsed_command_and_params(self):
        """
        Method returns a prepared request to a local server
        :return: dict request : {"is_get_request": bool, "url": str, "payload": dict or None}
        """
        return self.parsed_command_and_params

    @log_method
    def parse_connection_params(self, current_params, passed_params):
        """
        A method to parse a connection params.

        :param current_params:
        :param passed_params:
        :return: dict with handled a connection params and a sign if params value not equal params in a local db
        """
        is_changed = False
        updated_params = {}
        parsed_passed_params = {}
        for passed_param in passed_params:
            if "-" in passed_param:
                index_sign = passed_param.index("-")
                parsed_param = passed_param.title()
                parsed_passed_params[parsed_param[None[:index_sign]] + parsed_param[(index_sign + 1)[:None]]] = passed_params[passed_param]
            else:
                parsed_passed_params[passed_param.title()] = passed_params[passed_param]
        else:
            if len(parsed_passed_params) > 0:
                for current_param in current_params:
                    current_value = current_params[current_param]
                    if current_param in parsed_passed_params:
                        if parsed_passed_params[current_param] is not None:
                            if str(current_value) != str(parsed_passed_params[current_param]):
                                is_changed = True
                                if current_param == "Password" or current_param == "SshPassword":
                                    password = self.helper.encrypt_string(parsed_passed_params[current_param])
                                    current_value = password if current_value != password else current_value
                                else:
                                    current_value = parsed_passed_params[current_param]
                    updated_params[current_param] = current_value

            return {'updated_params':updated_params, 
             'is_changed':is_changed}

    @log_method
    def show_console_commands(self, params):
        """
        A method to print in the console line all exist console commands or a special command
        :param params:
        :return:
        """
        try:
            if params["command"] == "all":
                full_commands = self.get_len_full_console_commands()
                short_commands = self.get_len_short_console_commands()
                self.print_console_commands(full_commands, short_commands)
            else:
                is_command_true = self.print_specific_console_command(params)
                if not is_command_true:
                    self.helper.print_color_text(self.cm["INCORRECT_COMMAND"], CONSOLE_COLORS["RED"])
        except Exception as e:
            try:
                raise Exception(self.cm["FAILED_SHOW_COMMANDS"].format(str(e)))
            finally:
                e = None
                del e

    @log_method
    def print_specific_console_command(self, params):
        is_command_true = False
        for command in self.commands_pattern:
            if params["command"] in (command["command"], command["short_command"]) or command["command"] == "--" + params["command"] or command["short_command"] == "-" + params["command"]:
                is_command_true = True
                self.print_command_with_params(command)
            return is_command_true

    @log_method
    def get_len_full_console_commands(self):
        full_commands = []
        for command in self.commands_pattern:
            if command["is_public"]:
                full_commands.append(len(command["command"]))
            return full_commands

    @log_method
    def get_len_short_console_commands(self):
        short_commands = []
        for command in self.commands_pattern:
            if command["is_public"]:
                short_commands.append(len(command["short_command"]))
            return short_commands

    @log_method
    def print_console_commands(self, full_commands, short_commands):
        print("Usage:")
        print("  sqlbak <command> [parameters]\n")
        for command in self.commands_pattern:
            if command["is_public"]:
                print("  {0:<{numFull}}{3}{1:<{numShort}}{3}{2}".format((command["command"]), (command["short_command"]), (command["description"]), "     ", numFull=(max(full_commands)), numShort=(max(short_commands))))
        else:
            print(self.cm["HELP_PARTIAL"])

    @log_method
    def print_command_with_params(self, command):
        """
        A method to print a command with it params if params exist
        :param command: string
        :return: None
        """
        is_public = command["is_public"]
        has_params = "params" in command
        if is_public:
            print("Usage:")
            print("  sqlbak {0} <{1}> {2}".format(command["command"], command["short_command"], "[parameters]" if "params" in command else ""))
        if is_public:
            if has_params:
                len_full_args = []
                len_short_args = []
                if "optional" in command["params"]:
                    for optional_param in command["params"]["optional"]:
                        if optional_param["is_public"]:
                            for arg in list(optional_param["name"]):
                                len_full_args = self.get_len_full_params(len_full_args, len(arg) + 2)
                                len_short_args = self.get_len_short_params(len_short_args, len(optional_param["name"][arg]) + 1)

                elif "required" in command["params"]:
                    for required_param in command["params"]["required"]:
                        if required_param["is_public"]:
                            for arg in list(required_param["name"]):
                                len_full_args = self.get_len_full_params(len_full_args, len(arg) + 2)
                                len_short_args = self.get_len_short_params(len_short_args, len(required_param["name"][arg]) + 1)

                elif "required" in command["params"]:
                    print("\nRequired parameters:")
                    for required_param in command["params"]["required"]:
                        if required_param["is_public"]:
                            for arg in list(required_param["name"]):
                                print("  {0:<{numFull}}{3}{1:<{numShort}}{3}{2}".format(("--" + arg), ("-" + required_param["name"][arg]),
                                  (required_param["description"]),
                                  "     ", numFull=(max(len_full_args)),
                                  numShort=(max(len_short_args))))

            else:
                if "optional" in command["params"]:
                    print("\nOptional parameters:")
                    for optional_param in command["params"]["optional"]:
                        if optional_param["is_public"]:
                            for arg in list(optional_param["name"]):
                                print("  {0:<{numFull}}{3}{1:<{numShort}}{3}{2}".format(("--" + arg), ("-" + optional_param["name"][arg]),
                                  (optional_param["description"]),
                                  "     ", numFull=(max(len_full_args)),
                                  numShort=(max(len_short_args))))

                if "conditional" in command["params"]:
                    print("\nConditional parameters:")
                    for optional_param in command["params"]["conditional"]:
                        if optional_param["is_public"]:
                            for arg in list(optional_param["name"]):
                                print("  {0:<{numFull}}{3}{1:<{numShort}}{3}{2}".format(("--" + arg), ("-" + optional_param["name"][arg]),
                                  (optional_param["description"]),
                                  "     ", numFull=(max(len_full_args)),
                                  numShort=(max(len_short_args))))

    @log_method
    def get_len_full_params(self, len_full_args, param):
        len_full_args.append(param)
        return len_full_args

    @log_method
    def get_len_short_params(self, len_short_args, param):
        len_short_args.append(param)
        return len_short_args

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/console_parser.pyc
