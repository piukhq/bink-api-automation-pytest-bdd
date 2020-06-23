from tests_resources.test_data import testdata_dev
from tests.api.base import Endpoint
import time


class CustomerAccounts:

    @staticmethod
    def register_user_payload(test_email, client_id, bundle_id):
        payload = {
            "email": test_email,
            "password": "Password01",
            "client_id": client_id,
            "bundle_id": bundle_id
        }
        return payload

    @staticmethod
    def consent_user_payload(test_email):
        payload = {
            "email": test_email,
            "timestamp": int(time.time()),
                "latitude": 0.0,
                "longitude": 12.345
        }
        return payload

    @staticmethod
    def login_user_payload(client_id, bundle_id):
        payload = {
            "email": "njames@bink.com",
            "password": "Password@200",
            "client_id": client_id,
            "bundle_id": bundle_id
        }
        return payload
