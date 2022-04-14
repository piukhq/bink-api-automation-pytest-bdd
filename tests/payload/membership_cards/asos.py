import logging
import json
from faker import Faker
import tests.api as api
import tests.helpers.constants as constants
from tests.api.base import Endpoint
from tests.helpers.test_data_utils import TestDataUtils


class AsosCard:
    @staticmethod
    def add_membership_card_payload(invalid_data=None):
        if invalid_data:
            value = TestDataUtils.TEST_DATA.asos_invalid_data.get(constants.EMAIL)
            logging.info("Invalid data is: " + value)
            data_type = "Invalid data"
        else:
            value = TestDataUtils.TEST_DATA.asos_membership_card.get(constants.EMAIL)
            data_type = "Valid data"
        payload = {
            "account": {
                "add_fields": [
                    {
                        "column": "Membership card number",
                        "value": TestDataUtils.TEST_DATA.asos_membership_card.get(constants.CARD_NUM),
                    }
                ],
                "authorise_fields": [{"column": "Email", "value": value}],
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("asos"),
        }
        logging.info("The Request for Add Journey with " + data_type + " :\n\n"
                     + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n" + json.dumps(payload, indent=4))
        return payload

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
                    {"column": "Postcode", "value": fake.postcode()},
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("asos"),
        }
        logging.info("The Request for Enrol Journey : \n" + json.dumps(payload, indent=4))
        return payload
