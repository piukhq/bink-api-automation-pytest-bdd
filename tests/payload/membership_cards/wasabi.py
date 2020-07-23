import logging
import json
from faker import Faker

from tests.helpers.test_data_utils import TestDataUtils
import tests.helpers.constants as constants


class WasabiCard:
    @staticmethod
    def add_membership_card_payload(invalid_data=None):
        if invalid_data:
            value = TestDataUtils.TEST_DATA.wasabi_invalid_data.get(constants.EMAIL)
            logging.info('Invalid data is: ' + value)
        else:
            value = TestDataUtils.TEST_DATA.wasabi_membership_card1.get(constants.EMAIL)
        payload = {
            "account": {
                "add_fields": [
                    {
                        "column": "Membership card number",
                        "value": TestDataUtils.TEST_DATA.wasabi_membership_card1.get(constants.CARD_NUM)
                    }
                ],
                "authorise_fields": [
                    {
                        "column": "Email",
                        "value": value
                    }
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get('wasabi')
        }
        logging.info('The Request for Add Journey : \n' + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def enrol_membership_scheme_payload(email, invalid_data=None):
        faker = Faker()

        if invalid_data:
            value = Endpoint.TEST_DATA.wasabi_invalid_data.get('email')
            logging.info('Invalid data is: ' + value)
        else:
            value = email
        payload = {
            "account": {
                "enrol_fields": [
                    {
                        "column": "First name",
                        "value": faker.name()
                    },
                    {
                        "column": "Last name",
                        "value": faker.name()
                    },
                    {
                        "column": "Postcode",
                        "value": faker.postcode()
                    },
                    {
                        "column": "Phone number",
                        "value": faker.phone_number()
                    },
                    {
                        "column": "Email",
                        "value": value
                    },
                    {
                        "column": "Consent 1",
                        "value": constants.CONSENT
                    }
                ]

            },
            "membership_plan": Endpoint.TEST_DATA.membership_plan_id.get('wasabi')
        }

        logging.info('The Request for Enrol Journey : \n' + json.dumps(payload, indent=4))
        return payload
