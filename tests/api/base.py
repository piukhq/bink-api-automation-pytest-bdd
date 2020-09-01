import json
import requests
import config


class Endpoint:
    BASE_URL = ""
    DJANGO_URL = ""

    @staticmethod
    def set_environment(env):
        if env == "dev":
            Endpoint.BASE_URL = config.DEV.base_url
            Endpoint.DJANGO_URL = config.DEV.django_url

        elif env == "staging":
            Endpoint.BASE_URL = config.STAGING.base_url
            Endpoint.DJANGO_URL = config.STAGING.django_url

        elif env == "prod":
            Endpoint.BASE_URL = config.PROD.base_url

    @staticmethod
    def request_header(token=None, version='1.2'):
        # def request_header(token=None, version="1.1"):
        if version:
            accept = "application/json;v={}".format(version)
        else:
            accept = "application/json"

        headers = {
            "Accept": accept,
            "Content-Type": "application/json",
        }

        if token:
            if "bearer" in token:
                headers["Authorization"] = token
            else:
                headers["Authorization"] = "token " + token

        return headers

    @staticmethod
    def call(url, headers, method="GET", body=None):
        return requests.request(method, url, headers=headers, data=json.dumps(body))
