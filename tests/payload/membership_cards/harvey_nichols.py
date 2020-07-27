import logging
import json
from faker import Faker

from tests.helpers.test_data_utils import TestDataUtils
import tests.helpers.constants as constants


class HarveyNicholsCard:
    @staticmethod
    def add_membership_card_payload(invalid_data=None):
        if invalid_data:
            value = TestDataUtils.TEST_DATA.harvey_nichols_invalid_data.get(constants.ID)
            logging.info("Invalid data is: " + value)
        else:
            value = TestDataUtils.TEST_DATA.harvey_nichols_membership_card1.get(constants.ID)

        payload = {
            "account": {
                "authorise_fields": [
                    {"column": "Email", "value": value},
                    {
                        "column": "Password",
                        "value": TestDataUtils.TEST_DATA.harvey_nichols_membership_card2.get(constants.PASSWORD)
                        # "value": RSACipher.encrypt_field("Password01")
                    },
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("harvey_nichols"),
        }
        logging.info("The Request for Add Journey : \n" + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def enrol_membership_scheme_payload(email, invalid_data=None):
        faker = Faker()

        if invalid_data:
            value = TestDataUtils.TEST_DATA.coop_invalid_data.get("email")
            logging.info("Invalid data is: " + value)
        else:
            value = email
        payload = {
            "account": {
                "enrol_fields": [
                    {"column": "Title", "value": constants.TITLE},
                    {"column": "First name", "value": faker.name()},
                    {"column": "Last name", "value": faker.name()},
                    {"column": "Email", "value": value},
                    {"column": "Password", "value": constants.PASSWORD},
                    {"column": "Mobile number", "value": faker.phone_number()},
                    {"column": "Consent 1", "value": constants.CONSENT},
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("harvey_nichols"),
        }
        logging.info("The Request for Enrol Journey : \n" + json.dumps(payload, indent=4))
        return payload
