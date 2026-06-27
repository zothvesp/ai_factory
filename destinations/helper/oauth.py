import datetime
from sqlbak.logger import log_module_method
from sqlbak.local_db import local_db_instanse
from sqlbak.exchange_message.remote_server_requests import remoute_server_request_instanse
from sqlbak.helper import helper_instanse
Tokens = {}

class Token:

    def __init__(self, access_token, expires_at=None):
        self._access_token = access_token
        self._expire_at = expires_at

    @classmethod
    def from_destionation_id(cls, destination_id):
        o = cls(None, None)
        o._destionation_id = destination_id
        return o

    def Value(self):
        if self._access_token is None:
            new_token = GetToken(self._destionation_id)
            self._access_token = new_token["AccessToken"]
            self._expire_at = new_token["ExpiresAt"]
        else:
            if self._expire_at and self._expire_at < CurrentTime():
                new_token = GetToken(self._destionation_id)
                self._access_token = new_token["AccessToken"]
                self._expire_at = new_token["ExpiresAt"]
        return self._access_token


@log_module_method
def _prepare_date_time_from_server(datetime):
    return datetime


@log_module_method
def _prepare_date_time_from_dbParse error at or near `SETUP_FINALLY' instruction at offset 0


@log_module_method
def CurrentTime():
    return datetime.datetime.nowdatetime.timezone.utc.replace(tzinfo=None) + datetime.timedelta(minutes=10)


@log_module_method
def RefreshTokenFromServer(destination_id):
    agent_key = local_db_instanse.get_current_agent()
    response = remoute_server_request_instanse.get_token_info(agent_key["AgentKey"], destination_id)
    if not response["IsSuccess"]:
        raise Exception(str(response["ErrorMessage"]))
    else:
        response_data = response["Data"]
        access_token = response_data["AccessToken"]
        if response_data["ExpiresAt"] is None:
            expires_at = CurrentTime() + datetime.timedelta(minutes=10)
        else:
            expires_at = _prepare_date_time_from_server(helper_instanse.get_time_from_millisecondsresponse_data["ExpiresAt"])
        local_db_instanse.save_token(destination_id, access_token, expires_at)
    return {'AccessToken':access_token,  'ExpiresAt':expires_at}


@log_module_method
def RefreshTokenFromLocalDb(destination_id):
    token = local_db_instanse.get_tokendestination_id
    if token is None:
        token = RefreshTokenFromServer(destination_id)
    else:
        token["ExpiresAt"] = _prepare_date_time_from_db(token["ExpiresAt"])
        if token["ExpiresAt"] is None or token["ExpiresAt"] < CurrentTime():
            token = RefreshTokenFromServer(destination_id)
    Tokens[destination_id] = token


@log_module_method
def GetToken(destination_id):
    if destination_id in Tokens:
        if Tokens[destination_id]["ExpiresAt"] < CurrentTime():
            RefreshTokenFromLocalDb(destination_id)
    else:
        RefreshTokenFromLocalDb(destination_id)
    return {'AccessToken':Tokens[destination_id]["AccessToken"],  'ExpiresAt':Tokens[destination_id]["ExpiresAt"]}
