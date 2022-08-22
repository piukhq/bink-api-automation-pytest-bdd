import logging
import json
from faker import Faker
import tests.api as api
import tests.helpers.constants as constants
from tests.api.base import Endpoint
from tests.helpers.test_data_utils import TestDataUtils
from tests.helpers.test_context import TestContext


class ViatorCard:
    @staticmethod
    def enrol_membership_scheme_payload(email, env=None, channel=None, invalid_data=None):
        fake = Faker(locale="en_GB")
        if invalid_data:
            value = TestDataUtils.TEST_DATA.viator_invalid_data.get("email")
            logging.info("Invalid data is: " + value)
        else:
            value = email
        payload = {
            "account": {
                "enrol_fields": [
                    {"column": "First name", "value": fake.name()},
                    {"column": "Last name", "value": fake.name()},
                    {"column": "Date of birth", "value": constants.DATE_OF_BIRTH},
                    {"column": "Email", "value": value},
                    {"column": "Consent 1", "value": "true"},
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("viator"),
        }
        logging.info("The Request for Enrol Journey : \n" + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def add_membership_card_payload(invalid_data=None):
        if invalid_data:
            value = TestDataUtils.TEST_DATA.viator_invalid_data.get(constants.EMAIL)
            logging.info("Invalid data is: " + value)
            data_type = "Invalid data"
        else:
            value = TestDataUtils.TEST_DATA.viator_membership_card.get(constants.EMAIL)
            data_type = "Valid data"
        payload = {
            "account": {
                "add_fields": [
                    {
                        "column": "Membership card number",
                        "value": TestDataUtils.TEST_DATA.viator_membership_card.get(constants.CARD_NUM),
                    }
                ],
                "authorise_fields": [{"column": "Email", "value": value}],
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("viator"),
        }
        logging.info(
            "The Request for Add Journey with "
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
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("viator"),
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

    @staticmethod
    def add_membership_card_payload_without_field(field):
        value = TestDataUtils.TEST_DATA.viator_membership_card.get(constants.EMAIL)
        faker = Faker()
        if field == "account":
            payload = {
                "add_fields": [
                    {
                        "column": "Membership card number",
                        "value": TestDataUtils.TEST_DATA.viator_membership_card.get(constants.CARD_NUM),
                    }
                ],
                "authorise_fields": [{"column": "Email", "value": value}],
                "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("viator"),
            }

        elif field == "membership_plan":
            payload = {
                "account": {
                    "add_fields": [
                        {
                            "column": "Membership card number",
                            "value": TestDataUtils.TEST_DATA.viator_membership_card.get(constants.CARD_NUM),
                        }
                    ],
                    "authorise_fields": [{"column": "Email", "value": value}],
                }
            }

        elif field == "email":
            payload = {
                "account": {
                    "add_fields": [
                        {
                            "column": "Membership card number",
                            "value": TestDataUtils.TEST_DATA.viator_membership_card.get(constants.CARD_NUM),
                        }
                    ],
                    "authorise_fields": [{"column": "email", "value": value}],
                },
                "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("viator"),
            }

        elif field == "Membershipcard_number":
            payload = {
                "account": {
                    "add_fields": [
                        {
                            "column": "Membershipcard_number",
                            "value": TestDataUtils.TEST_DATA.viator_membership_card.get(constants.CARD_NUM),
                        }
                    ],
                    "authorise_fields": [{"column": "Email", "value": value}],
                },
                "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("viator"),
            }

        elif field == "enrol_account":
            payload = {
                "enrol_fields": [
                    {"column": "First name", "value": faker.name()},
                    {"column": "Last name", "value": faker.name()},
                    {"column": "Date of birth", "value": constants.DATE_OF_BIRTH},
                    {"column": "Email", "value": value},
                    {"column": "Consent 1", "value": "true"},
                ],
                "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("viator"),
            }

        elif field == "token":
            payload = {
                "account": {
                    "add_fields": [
                        {
                            "column": "Membership card number",
                            "value": TestDataUtils.TEST_DATA.viator_membership_card.get(constants.CARD_NUM),
                        }
                    ],
                    "authorise_fields": [{"column": "Email", "value": value}],
                },
                "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("viator"),
            }
        return payload
