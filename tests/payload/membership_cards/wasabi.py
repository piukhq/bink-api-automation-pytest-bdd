from tests.api.base import Endpoint


class WasabiCard:
    @staticmethod
    def add_membership_card_payload(invalid_data=None):
        payload = {
            "account": {
                "add_fields": [
                    {
                        "column": "Bonus card number",
                        "value":  Endpoint.TEST_DATA.IL_membership_card2.get('card_num')
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