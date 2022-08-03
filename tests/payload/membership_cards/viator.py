import logging
import json
from faker import Faker
from tests.helpers.test_data_utils import TestDataUtils


class ViatorCard:
    @staticmethod
    def enrol_membership_scheme_payload(email, env=None, channel=None, invalid_data=None):
        fake = Faker(locale="en_GB")
        if invalid_data:
            value = TestDataUtils.TEST_DATA.asos_invalid_data.get("email")
            logging.info("Invalid data is: " + value)
        else:
            value = email
        payload = {
            "account": {
                "enrol_fields": [
                    {"column": "First name", "value": fake.name()},
                    {"column": "Last name", "value": fake.name()},
                    {"column": "Email", "value": value},
                    {"column": "Consent 1", "value": "true"},
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("viator"),
        }
        logging.info("The Request for Enrol Journey : \n" + json.dumps(payload, indent=4))
        return payload
