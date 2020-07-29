from tests.helpers.test_data_utils import TestDataUtils
import time


class UserDetails:
    @staticmethod
    def register_user_payload(test_email, client_id, bundle_id):
        payload = {"email": test_email, "password": "Password01", "client_id": client_id, "bundle_id": bundle_id}
        return payload

    @staticmethod
    def consent_user_payload(test_email):
        payload = {"email": test_email, "timestamp": int(time.time()), "latitude": 0.0, "longitude": 12.345}
        return payload

    @staticmethod
    def login_user_payload(client_id, bundle_id):
        payload = {
            "email": TestDataUtils.TEST_DATA.user_accounts.get("bink_uid"),
            "password": TestDataUtils.TEST_DATA.user_accounts.get("bink_pwd"),
            "client_id": client_id,
            "bundle_id": bundle_id,
        }
        return payload
