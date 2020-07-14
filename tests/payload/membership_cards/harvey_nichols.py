from tests.api.base import Endpoint
import tests.helpers.constants as constants
import logging
from faker import Faker


class HarveyNicholsCard:

    @staticmethod
    def add_membership_card_payload(invalid_data=None):
        if invalid_data:
            value = Endpoint.TEST_DATA.harvey_nichols_invalid_data.get('id')
            logging.info('Invalid data is: ' + value)
        else:
            value = Endpoint.TEST_DATA.harvey_nichols_membership_card2.get('id')

        payload = {
            "account": {
                "authorise_fields": [
                    {
                        "column": "Email",
                        "value": value
                    },
                    {
                        "column": "Password",
                        "value": Endpoint.TEST_DATA.harvey_nichols_membership_card2.get('password')
                        # "value": RSACipher.encrypt_field("Password01")
                    }
                ]
            }, "membership_plan": Endpoint.TEST_DATA.membership_plan_id.get('harvey_nichols')

        }
        return payload

    @staticmethod
    def enrol_membership_scheme_payload(email, invalid_data=None):
        faker = Faker()

        if invalid_data:
            value = Endpoint.TEST_DATA.harvey_nichols_invalid_data.get('id')
        else:
            value = email
        payload = {
            "account": {
                "enrol_fields": [
                    {
                        "column": "Email",
                        "value": value
                    },
                    {
                        "column": "Password",
                        "value": "Password1"
                    },
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
                        "column": "Mobile number",
                        "value": faker.phone_number()
                    },

                    {
                        "column": "Consent 1",
                        "value": constants.CONSENT
                    }

                ]
            },
            "membership_plan": Endpoint.TEST_DATA.membership_plan_id.get('harvey_nichols')
        }
        return payload
