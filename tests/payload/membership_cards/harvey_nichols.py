from tests.api.base import Endpoint
import logging


class HarveyNicholsCard:

    @staticmethod
    def add_membership_card_payload(invalid_data=None):
        if invalid_data:
            value = Endpoint.TEST_DATA.harvey_nichols_membership_invalid_card.get('id')
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
    def enrol_membership_scheme():
        payload = {
            "account": {
                "enrol_fields": [
                    {
                        "column": "Email",
                        "value": "test@testbink.com"
                    },
                    {
                        "column": "Password",
                        "value": "Password1"
                    },
                    {
                        "column": "Title",
                        "value": "Mr"
                    },
                    {
                        "column": "First name",
                        "value": "mer_262"
                    },
                    {
                        "column": "Last name",
                        "value": "Bink"
                    },
                    {
                        "column": "Mobile number",
                        "value": "123454567"
                    },

                    {
                        "column": "Consent 1",
                        "value": "true"
                    }

                ]
            },
            "membership_plan": 194
        }
        return payload
