import logging
import json
from faker import Faker

from tests.api.base import Endpoint
import tests.api as api
from tests.helpers.test_data_utils import TestDataUtils
import tests.helpers.constants as constants
from tests.helpers.test_context import TestContext


class TheWorksCard:

    @staticmethod
    def enrol_membership_scheme_payload(email, env=None, channel=None, invalid_data=None):
        faker = Faker()
        if not invalid_data:
            last_name = faker.name()
        else:
            if invalid_data == "account_already_exists":
                last_name = TestDataUtils.TEST_DATA.the_works_invalid_data.get(constants.JOIN_ACCOUNT_ALREADY_EXISTS)
            elif invalid_data == "join_failed":
                last_name = TestDataUtils.TEST_DATA.the_works_invalid_data.get(constants.JOIN_FAILED)
            elif invalid_data == "join_http_failed":
                last_name = TestDataUtils.TEST_DATA.the_works_invalid_data.get(constants.JOIN_HTTP_FAILED)

        data_type = "Invalid data"
        payload = {
            "account": {
                "enrol_fields": [
                    {"column": "First name", "value": faker.name()},
                    {"column": "Last name", "value": last_name},
                    {"column": "Email", "value": email},
                    {"column": "Consent 1", "value": constants.CONSENT},
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("the_works"),
        }
        logging.info(
            "The Request for Enrol Journey with "
            + data_type
            + " :\n\n"
            + Endpoint.BASE_URL
            + api.ENDPOINT_MEMBERSHIP_CARDS
            + "\n\n"
            + json.dumps(payload, indent=4)
        )

        return payload

    @staticmethod
    def enrol_delete_add_membership_card_payload(email=None):
        payload = {
            "account": {
                "add_fields": [
                    {
                        "column": "Membership card number",
                        "value": TestContext.card_number,
                    }
                ],
                "authorise_fields": [{"column": "Email", "value": email}],
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("the_works"),
        }
        logging.info(
            "The Request for Add Journey with "
            + TestContext.card_number
            + " :\n\n"
            + Endpoint.BASE_URL
            + api.ENDPOINT_MEMBERSHIP_CARDS
            + "\n\n"
            + json.dumps(payload, indent=4)
        )
        return payload
