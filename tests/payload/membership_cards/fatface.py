from tests.api.base import Endpoint
import logging


class FFCard:

    @staticmethod
    def add_membership_card_payload(invalid_data=None):
        if invalid_data:
            value = Endpoint.TEST_DATA.FF_invalid_card.get('card_num')
            logging.info('Invalid data is: ' + value)
        else:
            value = Endpoint.TEST_DATA.FF_membership_card1.get('card_num')

        payload = {
            "account": {
                "authorise_fields": [
                    {
                        "column": "Rewards number",
                        "value": value
                    }
                ]
            },
            "membership_plan": Endpoint.TEST_DATA.membership_plan_id.get('FF')
        }
        return payload


@staticmethod
def enrol_membership_scheme():
    payload = {
        # "account": {
        #     "enrol_fields": [
        #
        #         {
        #             "column": "First name",
        #             "value": "megan"
        #         },
        #         {
        #             "column": "Last name",
        #             "value": "Bink"
        #         },
        #         {
        #             "column": "Email",
        #             "value": "megan_bink@testbink.com"
        #         },
        #         {
        #             "column": "Postcode",
        #             "value": "SL59FE"
        #         },
        #         {
        #             "column": "Phone",
        #             "value": "07724678390"
        #         }
        #     ]
        # },
        # "membership_plan": 314
    }
    return payload
