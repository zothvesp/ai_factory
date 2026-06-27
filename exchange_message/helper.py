from sqlbak.trace_event import TraceEvent
from sqlbak.local_db import LocalDB
from sqlbak.helper import Helper
from sqlbak.logger import log_error, log_module_method
from datetime import datetime, timedelta
localDb = LocalDB()
helper = Helper()
AGENT_QUIET_MODE = "Quiet"
AGENT_INTENSIVE_MODE = "Intensive"

@log_module_method
def GetAgentModeParse error at or near `SETUP_FINALLY' instruction at offset 0


@log_module_method
def IsIntensiveMode():
    return GetAgentMode() == AGENT_INTENSIVE_MODE


@log_module_method
def remove_old_messages(only_ended=True):
    try:
        now = datetime.now
        messages = localDb.get_messages
        if messages is not None:
            for message in messages:
                if not only_ended:
                    localDb.remove_messagemessage["MessageId"]
                elif message["EndAt"] is not None:
                    end_at = helper.get_date_timemessage["EndAt"]
                    if end_at + timedelta(days=1) < now:
                        localDb.remove_messagemessage["MessageId"]

    except Exception as e:
        try:
            error_message = "Error deleting old messages: '{}'"
            TraceEvent().trace_client_errorerror_message.formatstr(e)
        finally:
            e = None
            del e
