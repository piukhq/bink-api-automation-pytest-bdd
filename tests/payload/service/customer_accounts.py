import time
import jwt

import tests.helpers.constants as constants
from tests.helpers.test_data_utils import TestDataUtils


class UserDetails:
    @staticmethod
    def register_user_payload(test_email, client_id, bundle_id):
        """Payload for Bink User"""
        payload = {
            "email": test_email,
            "password": constants.PASSWORD_ENROL,
            "client_id": client_id,
            "bundle_id": bundle_id,
        }
        return payload

    @staticmethod
    def consent_user_payload(test_email):
        """Consent for Bink User"""
        payload = {
            "consent": {
                "email": test_email,
                "timestamp": int(time.time()),
                "latitude": 0.0,
                "longitude": 12.345
            }
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

    # @staticmethod
    # def generate_jwt_token(user_id, property_id, bundle_id, organisation_id, client_secret):
    #     claims = {
    #         "user_id": user_id,
    #         "property_id": property_id,
    #         "bundle_id": bundle_id,
    #         "organisation_id": organisation_id,
    #         "iat": 1581112213
    #     }
    #     token = 'bearer {}'.format(jwt.encode(claims, client_secret, algorithm="HS512").decode("UTF-8"))
    #     return token

    @staticmethod
    def register_bearer_user_payload(email, latitude=0.0, longitude=12.345):
        payload = {
            "consent": {
                "email": email,
                "latitude": latitude,
                "longitude": longitude,
                "timestamp": int(time.time())
            }
        }
        return payload
