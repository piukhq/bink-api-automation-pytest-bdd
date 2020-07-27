import logging
import json
from faker import Faker

from tests.helpers.test_data_utils import TestDataUtils
import tests.helpers.constants as constants


class FatFaceCard:
    @staticmethod
    def add_membership_card_payload(invalid_data=None):
        if invalid_data:
            value = TestDataUtils.TEST_DATA.fat_face_invalid_data.get(constants.CARD_NUM)
            logging.info("Invalid data is: " + value)
        else:
            value = TestDataUtils.TEST_DATA.fat_face_membership_card1.get(constants.CARD_NUM)

        payload = {
            "account": {"authorise_fields": [{"column": "Rewards number", "value": value}]},
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("fat_face"),
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
                    {"column": "Email", "value": value},
                    {"column": "First name", "value": faker.name()},
                    {"column": "Last name", "value": faker.name()},
                    {"column": "Email Marketing", "value": constants.EMAIL_MARKETING},
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("fat_face"),
        }
        logging.info("The Request for Enrol Journey: \n" + json.dumps(payload, indent=4))
        return payload
