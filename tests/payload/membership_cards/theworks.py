import logging
import json
from faker import Faker

from tests.api.base import Endpoint
import tests.api as api
from tests.helpers.test_data_utils import TestDataUtils
import tests.helpers.constants as constants


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
    def add_ghost_membership_card_payload():

        """This payload will add Ghost Card and results and scheme account in failed state
        which later can be updated with enrol credentials during PATCH/membership_card/{id}"""
        payload = {
            "account": {
                "add_fields": [
                    {
                        "column": "card_number",
                        "value": TestDataUtils.TEST_DATA.the_works_ghost_membership_card.get(constants.CARD_NUM),
                    }
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("the_works"),
        }

        logging.info(
            "The Request to Register The Works  Ghost Journey with  :\n\n"
            + Endpoint.BASE_URL
            + api.ENDPOINT_MEMBERSHIP_CARDS
            + "\n\n"
            + json.dumps(payload, indent=4)
        )
        return payload

    @staticmethod
    def update_ghost_membership_scheme_payload(email, scheme_account_id, env, channel=None, enrol_cred_type=None):
        """This payload will PATCH Ghost Card with valid / invalid enrol credentials"""
        faker = Faker()
        if enrol_cred_type == "account_already_exists":
            last_name = TestDataUtils.TEST_DATA.the_works_invalid_data.get(constants.JOIN_ACCOUNT_ALREADY_EXISTS)
        elif enrol_cred_type == "card_num_exists":
            last_name = TestDataUtils.TEST_DATA.the_works_invalid_data.get(constants.CARD_NUM_EXISTS)
        elif enrol_cred_type == "join_failed":
            last_name = TestDataUtils.TEST_DATA.the_works_invalid_data.get(constants.JOIN_FAILED)
        elif enrol_cred_type == "join_http_failed":
            last_name = TestDataUtils.TEST_DATA.the_works_invalid_data.get(constants.JOIN_HTTP_FAILED)
        else:
            last_name = faker.name()
        payload = {
            "account": {
                "registration_fields": [
                    {"column": "First name", "value": faker.name()},
                    {"column": "Last name", "value": last_name},
                    {"column": "Email", "value": email},
                    {"column": "Consent 1", "value": constants.CONSENT},
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("the_works"),
        }
        logging.info(
            "The Request for Register Ghost Journey with  :\n\n"
            + Endpoint.BASE_URL
            + api.ENDPOINT_MEMBERSHIP_CARD.format(scheme_account_id)
            + "\n\n"
            + json.dumps(payload, indent=4)
        )
        return payload
