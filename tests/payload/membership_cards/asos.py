import logging
import json
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
