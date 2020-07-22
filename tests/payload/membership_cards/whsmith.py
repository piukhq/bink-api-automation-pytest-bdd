from tests.helpers.test_data_utils import TestDataUtils
import tests.helpers.constants as constants
from faker import Faker
import logging
import json


class WHSmithCard:
    @staticmethod
    def add_membership_card_payload():
        payload = {
            "account": {
                "authorise_fields": [
                    {
                        "column": "Reward number",
                        "value": Endpoint.TEST_DATA.whsmith_membership_card1.get(constants.CARD_NUM)

                    }
                ]
            },
            "membership_plan": Endpoint.TEST_DATA.membership_plan_id.get('whsmith')
        }
        logging.info('The Request for Add Journey : \n' + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def enrol_membership_scheme_payload():
        payload = {
            "account": {
                "enrol_fields": [
                    {
                        "column": "Email",
                        "value": "whsmith@testbink.com"
                    },
                    {
                        "column": "Title",
                        "value": "Mr"
                    },
                    {
                        "column": "First name",
                        "value": "Smith"
                    },
                    {
                        "column": "Last name",
                        "value": "Bink"
                    },
                    {
                        "column": "Mobile number",
                        "value": "07726548769"
                    },
                    {
                        "column": "Address line 1",
                        "value": "29"
                    },
                    {
                        "column": "City",
                        "value": "Ascot"
                    },
                    {
                        "column": "Postcode",
                        "value": "SL5 9FE"
                    },
                    {
                        "column": "Consent 1",
                        "value": "true"

                    }
                ]
            },
            "membership_plan": 280
        }
        logging.info('The Request for Enrol Journey : \n' + json.dumps(payload, indent=4))
        return payload
