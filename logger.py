import logging, logging.config, os
from datetime import datetime
from functools import wraps
import inspect
from re import DEBUG
import psutil, sys, traceback, sqlbak.config.log_settings
from sqlbak.definitions import CONFIG, DYNAMIC_SETTING_LOGGING_ACTIVATED, DYNAMIC_SETTING_LOGGING_LEVEL, DYNAMIC_SETTING_LOGGING_DEBUG_SIZE

class logger_handler:
    path_to_log_file = ""
    _logger_handler__logger = None

    def get_path_to_log_file():
        path_to_app = "/" + CONFIG["PATH_TO_APP"].strip("/") + "/" if CONFIG["PATH_TO_APP"].strip() != "" else ""
        path_to_logs = path_to_app + CONFIG["PATH_TO_LOGS"]
        now = datetime.now()
        return path_to_logs + str(now.strftime("%Y%m%d")) + ".log"

    def get_log_config(logging_level, path_to_file):
        return {'version':1, 
         'handlers':{"fileHandler": {'class':"logging.FileHandler", 
                          'formatter':"myFormatter", 
                          'filename':path_to_file}}, 
         'loggers':{"root": {'handlers':[
                    "fileHandler"], 
                   'level':logging_level}}, 
         'formatters':{"myFormatter": {"format": "%(levelname)s|%(asctime)s|%(message)s"}}}

    def get_logging_level():
        level = None
        try:
            level = logging.getLevelName(sqlbak.config.log_settings.log_level) if sqlbak.config.log_settings.log_level is not None else None
            level = logging.INFO if (level is None and sqlbak.config.log_settings.is_active) else level
        except Exception as e:
            try:
                logger_handler.save_extra_error(e)
            finally:
                e = None
                del e

        else:
            level = logging.WARNING if level is None else level
            return level

    def save_extra_error(error):
        try:
            path_to_log_file = logger_handler.get_path_to_log_file()
            with open(path_to_log_file, "a+") as f:
                f.write(str(error) + "\n")
        except Exception as e:
            try:
                print(str(e))
            finally:
                e = None
                del e

    def get_logger():
        current_path_to_log_file = logger_handler.get_path_to_log_file()
        if logger_handler.path_to_log_file != current_path_to_log_file or logger_handler._logger_handler__logger is None:
            logger_handler.path_to_log_file = logger_handler.get_path_to_log_file()
            config = logger_handler.get_log_config(logger_handler.get_logging_level(), logger_handler.path_to_log_file)
            logging.config.dictConfig(config)
            logger_handler._logger_handler__logger = logging.getLogger("root")
            logger_handler._logger_handler__logger.debug_size = sqlbak.config.log_settings.log_line_size
        return logger_handler._logger_handler__logger

    def log_method_enter(func, args):
        try:
            if sqlbak.config.log_settings.is_active:
                l = logger_handler.get_logger()
                if l.level <= logging.INFO:
                    caller = inspect.stack()[2]
                    caller_name = caller.filename.split("/")[-1]
                    caller_line_no = caller.lineno
                    pid = psutil.Process().pid
                    if l.level == logging.DEBUG:
                        l.debug("{0:4}|{1:25}|{2:4}|{3:45}|ENTER|{4}".format(pid, caller_name, caller_line_no, func.__qualname__, str(args)[None[:l.debug_size]]))
                    else:
                        if l.level == logging.INFO:
                            l.info("{0:4}|{1:25}|{2:4}|{3:45}|ENTER".format(pid, caller_name, caller_line_no, func.__qualname__))
        except Exception as e:
            try:
                logger_handler.save_extra_error(e)
            finally:
                e = None
                del e

    def log_method_exit(func, return_value):
        try:
            if sqlbak.config.log_settings.is_active:
                l = logger_handler.get_logger()
                if l.level <= logging.INFO:
                    caller = inspect.stack()[2]
                    caller_name = caller.filename.split("/")[-1]
                    caller_line_no = caller.lineno
                    pid = psutil.Process().pid
                    if l.level == logging.DEBUG:
                        l.debug("{0:4}|{1:25}|{2:4}|{3:45}|EXIT |{4}".format(pid, caller_name, caller_line_no, func.__qualname__, str(return_value)[None[:l.debug_size]]))
                    else:
                        if l.level == logging.INFO:
                            l.info("{0:4}|{1:25}|{2:4}|{3:45}|EXIT ".format(pid, caller_name, caller_line_no, func.__qualname__))
        except Exception as e:
            try:
                logger_handler.save_extra_error(e)
            finally:
                e = None
                del e

    def log_method_data(data):
        try:
            if sqlbak.config.log_settings.is_active:
                l = logger_handler.get_logger()
                if l.level <= logging.INFO:
                    caller = inspect.stack()[2]
                    caller_name = caller.filename.split("/")[-1]
                    func = caller.function
                    caller_line_no = caller.lineno
                    pid = psutil.Process().pid
                    l.info("{0:4}|{1:25}|{2:4}|{3:45}|INFO |{4}".format(pid, caller_name, caller_line_no, func, data))
        except Exception as e:
            try:
                logger_handler.save_extra_error(e)
            finally:
                e = None
                del e

    def get_trace_errorParse error at or near `SETUP_FINALLY' instruction at offset 0

    def log_error(func, error):
        try:
            if sqlbak.config.log_settings.is_active:
                l = logger_handler.get_logger()
                if l.level <= logging.ERROR:
                    caller = inspect.stack()[2]
                    caller_name = caller.filename.split("/")[-1]
                    caller_line_no = caller.lineno
                    pid = psutil.Process().pid
                    trace_error = logger_handler.get_trace_error()
                    l.error("{0:4}|{1:25}|{2:4}|{3:45}|ERROR|{4}|\n{5}".format(pid, caller_name, caller_line_no, func.__qualname__, str(error), trace_error))
        except Exception as e:
            try:
                logger_handler.save_extra_error(e)
            finally:
                e = None
                del e


def log_module_method(f):
    if sqlbak.config.log_settings.is_active:

        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                logger_handler.log_method_enter(f, args)
                result = f(*args, **kwargs)
                logger_handler.log_method_exit(f, result)
                return                 return result
                    except Exception as e:
                try:
                    logger_handler.log_error(f, e)
                    raise e
                finally:
                    e = None
                    del e

        return decorated
    return f


def log_module_method_debug(f):
    if not sqlbak.config.log_settings.is_active or logger_handler.get_logging_level() <= logging.DEBUG:
        return f

    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            logger_handler.log_method_enter(f, args)
            result = f(*args, **kwargs)
            logger_handler.log_method_exit(f, result)
            return             return result
            except Exception as e:
            try:
                logger_handler.log_error(f, e)
                raise e
            finally:
                e = None
                del e

    return decorated


def log_method(f):
    if sqlbak.config.log_settings.is_active:

        @wraps(f)
        def decorated(this, *args, **kwargs):
            try:
                logger_handler.log_method_enter(f, args)
                result = f(this, *args, **kwargs)
                logger_handler.log_method_exit(f, result)
                return                 return result
                    except Exception as e:
                try:
                    logger_handler.log_error(f, e)
                    raise e
                finally:
                    e = None
                    del e

        return decorated
    return f


def log_func(f):
    if sqlbak.config.log_settings.is_active:

        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                logger_handler.log_method_enter(f, args)
                result = f(*args, **kwargs)
                logger_handler.log_method_exit(f, args)
                return                 return result
                    except Exception as e:
                try:
                    logger_handler.log_error(f, e)
                    raise e
                finally:
                    e = None
                    del e

        return decorated
    return f


def log_only_exception(f):
    if sqlbak.config.log_settings.is_active:

        @wraps(f)
        def decorated(this, *args, **kwargs):
            try:
                return                 return f(this, *args, **kwargs)
                    except Exception as e:
                try:
                    logger_handler.log_error(f, e)
                    raise e
                finally:
                    e = None
                    del e

        return decorated
    return f


def log_without_raising(f):

    @wraps(f)
    def decorated(this, *args, **kwargs):
        try:
            logger_handler.log_method_enter(f, args)
            result = f(this, *args, **kwargs)
            logger_handler.log_method_exit(f, result)
            return             return result
            except Exception as e:
            try:
                logger_handler.log_error(f, e)
            finally:
                e = None
                del e

    return decorated


def log_only_exception_without_raising(f):

    @wraps(f)
    def decorated(this, *args, **kwargs):
        try:
            return             return f(this, *args, **kwargs)
            except Exception as e:
            try:
                logger_handler.log_error(f, e)
            finally:
                e = None
                del e

    return decorated


def log_data(data):
    try:
        logger_handler.log_method_data(data)
    except Exception as e:
        try:
            logger_handler.save_extra_error(str(e))
        finally:
            e = None
            del e


def log_error(exception, message):
    if sqlbak.config.log_settings.is_active:
        try:
            logger_handler.log_method_data(message)
            logger_handler.log_method_data(str(exception))
        except Exception as e:
            try:
                logger_handler.save_extra_error(str(e))
            finally:
                e = None
                del e
