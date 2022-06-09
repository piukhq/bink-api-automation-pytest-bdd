import json
import logging
import time
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
        logging.info("Request body for POST Registeration" + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def consent_user_payload(test_email):
        """Consent for Bink User"""
        payload = {
            "consent": {"email": test_email, "timestamp": int(time.time()), "latitude": 0.0, "longitude": 12.345}
        }
        logging.info("Request body for POST consent" + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def without_consent_user_payload():
        """Consent for Bink User with empty request"""
        payload = {}
        logging.info("Request body for POST without the 'consent' field : " + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def without_consent_key_user_payload():
        """Consent for Bink User without consent field"""
        payload = {
            "email": "pytest_automation_barclays@testbink.com",
            "latitude": 0.0123,
            "longitude": 12.345,
            "timestamp": 1618489226,
        }
        logging.info("Request body for POST without the 'consent' field : " + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def without_mandatory_consent_field():
        """Consent for Bink User without mandatory field"""
        payload = {"longitude": 12.345, "timestamp": 1618489226}
        logging.info("Request body for POST without the 'consent' field : " + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def timestamp_with_quote(test_email):
        payload = {
            "consent": {"email": test_email, "timestamp": str(time.time()), "latitude": 0.0123, "longitude": 12.345}
        }
        logging.info("Request body for POST without the 'consent' field : \n" + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def without_latitude(test_email):
        payload = {"consent": {"email": test_email, "timestamp": int(time.time()), "longitude": 12.345}}
        logging.info("Request body for POST without the latitude field : \n" + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def without_longitude(test_email):
        payload = {"consent": {"email": test_email, "timestamp": int(time.time()), "latitude": 0.0123}}
        logging.info("Request body for POST without the longitude field : \n" + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def longitude_with_alphabet(test_email):
        """Longitude with Alphabet in consent"""
        payload = {
            "consent": {"email": test_email, "latitude": 0.0123, "longitude": "alphabet", "timestamp": int(time.time())}
        }
        logging.info("Request body for POST longitude as alphabet  : \n" + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def bink_login_user_payload(client_id, bundle_id):
        """Login for Bink user"""
        payload = {
            "email": TestDataUtils.TEST_DATA.bink_user_accounts.get(constants.USER_ID),
            "password": TestDataUtils.TEST_DATA.bink_user_accounts.get(constants.PWD),
            "client_id": client_id,
            "bundle_id": bundle_id,
        }
        logging.info("Request body for POST Login" + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def register_bearer_user_payload(email, latitude=0.0123, longitude=12.345):
        """Banking User Subscription to Bink"""
        payload = {
            "consent": {"email": email, "latitude": latitude, "longitude": longitude, "timestamp": int(time.time())}
        }
        logging.info("Request body for POST Service consent" + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def expected_user_consent_json(test_email, timestamp):
        response = {"consent": {"email": test_email, "timestamp": timestamp, "latitude": 0.0123, "longitude": 12.345}}
        return response

    @staticmethod
    def expected_user_consent_with_optional_field(test_email, timestamp):
        response = {
            "consent": {
                "email": test_email,
                "timestamp": timestamp,
            }
        }
        return response

    @staticmethod
    def expected_existing_user_consent_json(timestamp):
        response = {
            "consent": {
                "email": TestDataUtils.TEST_DATA.barclays_user_accounts.get(constants.USER_ID),
                "timestamp": timestamp,
                "latitude": 0.0,
                "longitude": 12.345,
            }
        }
        return response
