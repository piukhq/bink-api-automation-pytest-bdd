import time

import tests.helpers.constants as constants
from tests.helpers.test_data_utils import TestDataUtils


class UserDetails:
    @staticmethod
    def register_user_payload(test_email, client_id, bundle_id):
        payload = {
            "email": test_email,
            "password": constants.PASSWORD_ENROL,
            "client_id": client_id,
            "bundle_id": bundle_id,
        }
        print('payload', payload)
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
    def bink_login_user_payload(client_id, bundle_id):
        payload = {
            "email": TestDataUtils.TEST_DATA.bink_user_accounts.get(constants.USER_ID),
            "password": TestDataUtils.TEST_DATA.bink_user_accounts.get(constants.PWD),
            "client_id": client_id,
            "bundle_id": bundle_id,
        }
        return payload

    @staticmethod
    def barclays_login_user_payload(client_id, bundle_id):
        payload = {
            "email": TestDataUtils.TEST_DATA.barclays_user_accounts.get(constants.USER_ID),
            "password": TestDataUtils.TEST_DATA.barclays_user_accounts.get(constants.PWD),
            "client_id": client_id,
            "bundle_id": bundle_id,
        }
        return payload
