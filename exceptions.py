


class UpdateIsNotPossibleNow(Exception):

    def __init__(self, value=''):
        return


class UpdateIsActual(Exception):

    def __init__(self, value=''):
        return


class AutoUpdateIsDisabled(Exception):

    def __init__(self, value=''):
        return


class JobDoubleRun(Exception):

    def __init__(self, value=''):
        return


class UnregisterAgent(Exception):

    def __init__(self, value=''):
        self.value = value


class DestinationFileDoesNotExist(Exception):

    def __init__(self, value=''):
        return


class ConsoleCommandError(Exception):

    def __init__(self, value='', exit_code=0):
        self.value = value
        self.exit_code = exit_code

    def __str__(self):
        return self.value


class JobError(Exception):

    def __init__(self, innerException=''):
        self.innerException = innerException

    def _get_error_suffix(self):
        return "JOB"

    def _get_know_errors(self):
        return [
         {'errorSubstring':"Unknown table 'COLUMN_STATISTICS'", 
          'errorCode':1001}]

    def _make_error_code_string(self, errorCode):
        return "[{suffix}:{code}]".format(suffix=(self._get_error_suffix()), code=errorCode)

    def _get_knowleadge_base_error_code(self, error):
        know_error_list = [x["errorCode"] for x in self._get_know_errors() if x["errorSubstring"] in error]
        if len(know_error_list) == 1:
            return self._make_error_code_string(know_error_list[0])
        return

    def _get_error_message_with_code(self, error_code, error_message):
        return "{code} {message}".format(code=error_code, message=error_message)

    def __str__(self):
        error_message_str = str(self.innerException)
        error_code = self._get_knowleadge_base_error_code(error_message_str)
        if error_code is None:
            return error_message_str
        return self._get_error_message_with_code(error_code, error_message_str)


class MySQLDumpError(JobError):

    def __init__(self, innerException):
        self.innerException = innerException

    def _get_error_suffix(self):
        return "MYSQLDUMP"

    def _get_know_errors(self):
        return [
         {'errorSubstring':"Unknown table 'COLUMN_STATISTICS'", 
          'errorCode':1001},
         {'errorSubstring':"Can't connect to local MySQL server through socket", 
          'errorCode':1002},
         {'errorSubstring':'to database \'information_schema\'" when using LOCK TABLES', 
          'errorCode':1003}]


class FolderBackupError(JobError):

    def __init__(self, innerException):
        self.innerException = innerException

    def _get_error_suffix(self):
        return "F-BAC"

    def _get_know_errors(self):
        return [
         {'errorSubstring':"doesn't exist", 
          'errorCode':1001}]


class CompressError(JobError):

    def __init__(self, innerException):
        self.innerException = innerException

    def _get_error_suffix(self):
        return "COMPRESS"

    def _get_know_errors(self):
        return [
         {'errorSubstring':"/bin/sh: zip: command not found", 
          'errorCode':1001}]

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/exceptions.pyc
