from tests.api.base import Endpoint
import logging


class IcelandCard:
    @staticmethod
    def add_membership_card_payload(invalid_data=None):
        if invalid_data:
            value = Endpoint.TEST_DATA.iceland_invalid_card.get('invalid_postal_code')
            logging.info('Invalid data is: ' + value)
        else:
            value = Endpoint.TEST_DATA.iceland_membership_card2.get('postcode')
        payload = {
            "account": {
                "add_fields": [
                    {
                        "column": "Bonus card number",
                        "value": Endpoint.TEST_DATA.iceland_membership_card2.get('card_num')
                    }
                ],
                "authorise_fields": [
                    {
                        "column": "Last name",
                        "value": Endpoint.TEST_DATA.iceland_membership_card2.get('last_name')
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
