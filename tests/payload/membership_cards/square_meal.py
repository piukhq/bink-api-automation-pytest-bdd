import json
import logging

from faker import Faker
from shared_config_storage.credentials.encryption import RSACipher

import config
import tests.api as api
import tests.helpers.constants as constants
from tests.api.base import Endpoint
from tests.helpers.test_context import TestContext
from tests.helpers.test_data_utils import TestDataUtils
from tests.helpers.vault import channel_vault
from tests.helpers.vault.channel_vault import KeyType


class SquareMealCard:
    @staticmethod
    def enrol_membership_scheme_payload(email, env=None, channel=None, invalid_data=None):
        faker = Faker()

        if invalid_data:
            email = TestDataUtils.TEST_DATA.square_meal_invalid_data.get("id")
            # password = TestDataUtils.TEST_DATA.square_meal_invalid_data.get("password")
            password = "invalidauthorization"
            data_type = "Invalid data"
        else:
            email = email
            password = constants.PASSWORD_ENROL
            data_type = "Valid data"

        # if channel == "barclays":
        #     pub_key = channel_vault.get_key(config.BARCLAYS.bundle_id, KeyType.PUBLIC_KEY)
        # else:
        #     pub_key = channel_vault.get_key(config.BINK.bundle_id, KeyType.PUBLIC_KEY)

        payload = {
            "account": {
                "enrol_fields": [
                    {"column": "Email", "value": email},
                    {"column": "Password", "value": password},
                    {"column": "First name", "value": faker.name()},
                    {"column": "Last name", "value": faker.name()},
                    {"column": "Consent 1", "value": "true"},
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("square_meal"),
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
    def add_membership_card_payload(invalid_data=None, txn_matching_testing=None):
        if invalid_data:
            invalid_email = TestDataUtils.TEST_DATA.square_meal_invalid_data.get(constants.ID)
            invalid_password = TestDataUtils.TEST_DATA.square_meal_invalid_data.get(constants.PASSWORD)
            logging.info("Invalid id is: " + invalid_email)
            logging.info("Invalid password is: " + invalid_password)
            data_type = "Invalid data"

            payload = {
                "account": {
                    "authorise_fields": [
                        {"column": "Email", "value": invalid_email},
                        {"column": "Password", "value": invalid_password},
                    ]
                },
                "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("square_meal"),
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
        else:
            valid_email = TestDataUtils.TEST_DATA.square_meal_membership_card.get(constants.ID)
            data_type = "Valid data"

            sensitive_value = TestDataUtils.TEST_DATA.square_meal_membership_card.get(constants.PASSWORD)

        if TestContext.flag_encrypt == "true":
            if TestContext.channel_name == config.BINK.channel_name:
                pub_key = channel_vault.get_key(config.BINK.bundle_id, KeyType.PUBLIC_KEY)
            elif TestContext.channel_name == config.BARCLAYS.channel_name:
                pub_key = channel_vault.get_key(config.BARCLAYS.bundle_id, KeyType.PUBLIC_KEY)

            password = RSACipher().encrypt(sensitive_value, pub_key)

        elif TestContext.flag_encrypt == "false":
            password = sensitive_value

        payload = {
            "account": {
                "authorise_fields": [
                    {"column": "Email", "value": valid_email},
                    {"column": "Password", "value": password},
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("square_meal"),
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
    def add_membership_card_payload_without_field(field):
        faker = Faker()
        email = TestDataUtils.TEST_DATA.square_meal_membership_card.get(constants.ID)
        sensitive_value = TestDataUtils.TEST_DATA.square_meal_membership_card.get(constants.PASSWORD)

        if TestContext.flag_encrypt == "true":
            if TestContext.channel_name == config.BINK.channel_name:
                pub_key = channel_vault.get_key(config.BINK.bundle_id, KeyType.PUBLIC_KEY)
            elif TestContext.channel_name == config.BARCLAYS.channel_name:
                pub_key = channel_vault.get_key(config.BARCLAYS.bundle_id, KeyType.PUBLIC_KEY)

            password = RSACipher().encrypt(sensitive_value, pub_key)

        elif TestContext.flag_encrypt == "false":
            password = sensitive_value

        if field == "account":
            payload = {
                "authorise_fields": [{"column": "Email", "value": email}, {"column": "Password", "value": password}],
                "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("square_meal"),
            }

        elif field == "membership_plan":
            payload = {
                "account": {
                    "authorise_fields": [{"column": "Email", "value": email}, {"column": "Password", "value": password}]
                }
            }

        elif field == "authorise_fields":
            payload = {
                "account": [{"column": "Email", "value": email}, {"column": "Password", "value": password}],
                "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("square_meal"),
            }

        elif field == "enrol_account":
            payload = {
                "enrol_fields": [
                    {"column": "Email", "value": email},
                    {"column": "Password", "value": RSACipher().encrypt(sensitive_value, pub_key)},
                    {"column": "First name", "value": faker.name()},
                    {"column": "Last name", "value": faker.name()},
                    {"column": "Consent 1", "value": "true"},
                ],
                "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("square_meal"),
            }

        elif field == "email":
            payload = {
                "account": {
                    "authorise_fields": [{"column": "Email", "value": ""}, {"column": "Password", "value": password}]
                },
                "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("square_meal"),
            }

        elif field == "email_coloumn_value":
            payload = {
                "account": {
                    "authorise_fields": [{"column": "email", "value": email}, {"column": "Password", "value": password}]
                },
                "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("square_meal"),
            }

        elif field == "password_coloumn_value":
            payload = {
                "account": {
                    "authorise_fields": [{"column": "Email", "value": email}, {"column": "password", "value": password}]
                },
                "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("square_meal"),
            }

        elif field == "token":
            payload = {
                "account": {
                    "authorise_fields": [{"column": "Email", "value": email}, {"column": "Password", "value": password}]
                },
                "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("square_meal"),
            }

        elif field == "email_address":
            payload = {
                "account": {
                    "authorise_fields": [
                        {"column": "Email", "value": "automatione2e.bink.com"},
                        {"column": "Password", "value": password},
                    ]
                },
                "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("square_meal"),
            }
        return payload

    @staticmethod
    def enrol_membership_card_payload(enrol_status, test_email, env, channel):
        sensitive_value = constants.PASSWORD_ENROL
        faker = Faker()
        if channel == "barclays":
            pub_key = channel_vault.get_key(config.BARCLAYS.bundle_id, KeyType.PUBLIC_KEY)
        else:
            pub_key = channel_vault.get_key(config.BINK.bundle_id, KeyType.PUBLIC_KEY)
        if enrol_status == "identical_enrol":
            test_email = TestDataUtils.TEST_DATA.square_meal_membership_card.get("identical_enrol_email")
        payload = {
            "account": {
                "enrol_fields": [
                    {"column": "Email", "value": test_email},
                    {"column": "Password", "value": RSACipher().encrypt(sensitive_value, pub_key)},
                    {"column": "First name", "value": faker.name()},
                    {"column": "Last name", "value": faker.name()},
                    {"column": "Consent 1", "value": "true"},
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("square_meal"),
        }
        logging.info(
            "The Request for Enrol Journey with "
            + " :\n\n"
            + Endpoint.BASE_URL
            + api.ENDPOINT_MEMBERSHIP_CARDS
            + "\n\n"
            + json.dumps(payload, indent=4)
        )
        return payload
