
from tests.api.base import Endpoint
import tests.helpers.constants as constants
from tests.helpers.test_data_utils import TestDataUtils
from faker import Faker
import logging
import json


class IcelandCard:
    @staticmethod
    def add_membership_card_payload(invalid_data=None):
        if invalid_data:
            value = Endpoint.TEST_DATA.iceland_invalid_data.get('invalid_postal_code')
            logging.info('Invalid data is: ' + value)
        else:
            value = Endpoint.TEST_DATA.iceland_membership_card1.get('postcode')
        payload = {
            "account": {
                "add_fields": [
                    {
                        "column": "Bonus card number",
                        "value": Endpoint.TEST_DATA.iceland_membership_card1.get('card_num')
                    }
                ],
                "authorise_fields": [
                    {
                        "column": "Last name",
                        "value": Endpoint.TEST_DATA.iceland_membership_card1.get('last_name')
                        # "value": iceland_membership_card3_last_name

                    },
                    {
                        "column": "Postcode",
                        "value": value
                    }
                ]
            },
            "membership_plan": Endpoint.TEST_DATA.membership_plan_id.get('iceland')
        }
        return payload

    @staticmethod
    def enrol_membership_scheme_payload(email, invalid_data=None):
        faker = Faker()

        if invalid_data:
            value = Endpoint.TEST_DATA.iceland_invalid_data.get('email')
            logging.info('Invalid data is: ' + value)
        else:
            value = email

        payload = {
            "account": {
                "enrol_fields": [
                    {
                        "column": "Title",
                        "value": constants.TITLE
                    },
                    {
                        "column": "First name",
                        "value": faker.name()
                    },
                    {
                        "column": "Last name",
                        "value": faker.name()
                    },
                    {
                        "column": "Date of birth",
                        "value": constants.DOB
                    },
                    {
                        "column": "Email",
                        "value": value
                    },
                    {
                        "column": "Phone",
                        "value": faker.phone_number()
                    },
                    {
                        "column": "House name or number",
                        "value": faker.building_number()
                    },
                    {
                        "column": "Street name",
                        "value": faker.street_address()
                    },
                    {
                        "column": "City",
                        "value": faker.city()
                    },
                    {
                        "column": "County",
                        "value": faker.country()
                    },
                    {
                        "column": "Postcode",
                        "value": faker.postcode()
                    },
                    {
                        "column": "Enrol Consent 1",
                        "value": constants.CONSENT
                    }
                ]
            },
            "membership_plan": Endpoint.TEST_DATA.membership_plan_id.get('iceland')
        }
        logging.info('The Request for Enrol Journey : \n' + json.dumps(payload, indent=4))
        return payload
