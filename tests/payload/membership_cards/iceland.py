import logging
import json
from faker import Faker

from tests.api.base import Endpoint
import tests.api as api
from tests.helpers.test_data_utils import TestDataUtils
import tests.helpers.constants as constants


class IcelandCard:
    @staticmethod
    def add_membership_card_payload(invalid_data=None):
        if invalid_data:
            value = TestDataUtils.TEST_DATA.iceland_invalid_data.get(constants.POSTCODE)
            logging.info("Invalid data is: " + value)
            data_type = "Invalid data"
        else:
            value = TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.POSTCODE)
            data_type = "Valid data"

        payload = {
            "account": {
                "add_fields": [
                    {
                        "column": "Bonus card number",
                        "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.CARD_NUM),
                    }
                ],
                "authorise_fields": [
                    {
                        "column": "Last name",
                        "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.LAST_NAME)
                    },
                    {
                        "column": "Postcode",
                        "value": value
                    }
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("iceland"),
        }

        logging.info("The Request for Add Journey with " + data_type + " :\n\n"
                     + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n" + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def enrol_membership_scheme_payload(email, invalid_data=None):
        faker = Faker()

        if invalid_data:
            value = TestDataUtils.TEST_DATA.iceland_invalid_data.get(constants.EMAIL)
            logging.info("Invalid data is: " + value)
            data_type = "Invalid data"
        else:
            value = email
            data_type = "Valid data"

        payload = {
            "account": {
                "enrol_fields": [
                    {"column": "Title", "value": constants.TITLE},
                    {"column": "First name", "value": faker.name()},
                    {"column": "Last name", "value": faker.name()},
                    {"column": "Date of birth", "value": constants.DATE_OF_BIRTH},
                    {"column": "Email", "value": value},
                    {"column": "Phone", "value": faker.phone_number()},
                    {"column": "House name or number", "value": faker.building_number()},
                    {"column": "Street name", "value": faker.street_address()},
                    {"column": "City", "value": faker.city()},
                    {"column": "County", "value": faker.country()},
                    {"column": "Postcode", "value": faker.postcode()},
                    {"column": "Consent 1", "value": constants.CONSENT},
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("iceland"),
        }
        logging.info("The Request for Enrol Journey with " + data_type + " :\n\n"
                     + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n" + json.dumps(payload, indent=4))
        return payload
