import json
import requests
import config


class TransactionMatching_Endpoint:
    BASE_URL = ""

    @staticmethod
    def set_environment(env):
        TransactionMatching_Endpoint.BASE_URL = getattr(config, env.upper()).base_url

    @staticmethod
    def request_header_mastercard():
        header = {
            "Content-Type": "application/json",
            "Authorization": "token F616CE5C88744DD52DB628FAD8B3D"
        }
        return header

    @staticmethod
    def request_register_amex():
        header = {
            "Content-Type": "application/json",
            "Cookie": "sessionid=ir8ojeq2hssh0cjoihofyitctpt46dk7"
        }
        return header

    @staticmethod
    def request_header_amex(auth_token):
        header = {
            "Content-Type": "application/json",
            "Cookie": "sessionid=ir8ojeq2hssh0cjoihofyitctpt46dk7",
            "Authorization": "token " + auth_token
        }
        return header

    @staticmethod
    def call(url, headers, method="GET", body=None):
        return requests.request(method, url, headers=headers, data=json.dumps(body))
