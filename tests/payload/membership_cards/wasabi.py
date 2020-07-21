from tests.api.base import Endpoint
import tests.helpers.constants as constants
from faker import Faker
import logging
import json


class WasabiCard:
    @staticmethod
    def add_membership_card_payload(invalid_data=None):
        payload = {
            "account": {
                "add_fields": [
                    {
                        "column": "Bonus card number",
                        "value": Endpoint.TEST_DATA.IL_membership_card2.get('card_num')
                    }
                ],
                "authorise_fields": [
                    {
                        "column": "Last name",
                        "value": Endpoint.TEST_DATA.IL_membership_card2.get('last_name')
                    },
                    {
                        "column": "Postcode",
                        "value": Endpoint.TEST_DATA.IL_membership_card2.get('postcode')
                    }
                ]
            },
            "membership_plan": Endpoint.TEST_DATA.membership_plan_id.get('IL')
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
