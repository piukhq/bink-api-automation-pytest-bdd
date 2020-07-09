from tests.api.base import Endpoint
from tests.helper.test_data_utils import TestDataUtils
import logging


class BurgerKingCard:
    @staticmethod
    def add_membership_card_payload(invalid_data=None):
        if invalid_data:
            # value = TestDataUtils.burger_king_membership_invalid_card_number
            value = Endpoint.TEST_DATA.burger_king_membership_invalid_card_number.get('card_num')
            logging.info('Invalid data is: ' + value)
        else:
            value = TestDataUtils.get_burger_king_card_num1()
        payload = {
                "account": {
                    "authorise_fields": [
                        {
                            "column": "Rewards number",
                            "value": value
                        }
                    ]
                },
                "membership_plan": Endpoint.TEST_DATA.membership_plan_id.get('burger_king')

            }
        return payload

    @staticmethod
    def enrol_membership_scheme():
        payload = {
            "account": {
                "enrol_fields": [

                    {
                        "column": "First name",
                        "value": "megan"
                    },
                    {
                        "column": "Last name",
                        "value": "Bink"
                    },
                    {
                        "column": "Email",
                        "value": "megan_bink@testbink.com"
                    },
                    {
                        "column": "Postcode",
                        "value": "SL59FE"
                    },
                    {
                        "column": "Phone",
                        "value": "07724678390"
                    }
                ]
            },
            "membership_plan": 314
        }
        return payload
