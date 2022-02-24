import logging
import json
from faker import Faker
from tests.helpers.test_data_utils import TestDataUtils


class TrenetteCard:
    @staticmethod
    def enrol_membership_scheme_payload(email, env=None, channel=None, invalid_data=None):

        faker = Faker()

        if invalid_data:
            value = TestDataUtils.TEST_DATA.trenette_invalid_data.get("email")
            logging.info("Invalid data is: " + value)
        else:
            value = email

        payload = {
            "account": {
                "enrol_fields": [
                    {"column": "First name", "value": faker.name()},
                    {"column": "Last name", "value": faker.name()},
                    {"column": "Email", "value": value},
                    {"column": "Consent 1", "value": "true"},
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("trenette"),
        }

        logging.info("The Request for Enrol Journey : \n" + json.dumps(payload, indent=4))
        return payload
        # logging.info("The Request for Enrol Journey with " + data_type + " :\n\n"
        #              + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n" + json.dumps(payload, indent=4))
        # return payload
