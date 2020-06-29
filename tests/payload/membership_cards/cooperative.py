from tests.api.base import Endpoint


class CoopCard:
    @staticmethod
    def add_membership_card_payload():
        payload = {
            "account": {
                "add_fields": [
                    {
                        "column": "Membership card number",
                        "value": Endpoint.TEST_DATA.CooP_membership_card1.get('card_num')
                    }
                ],
                "authorise_fields": [
                    {
                        "column": "Date of birth",
                        "value": Endpoint.TEST_DATA.CooP_membership_card1.get('dob')
                    },
                    {
                        "column": "Postcode",
                        "value": Endpoint.TEST_DATA.CooP_membership_card1.get('postcode')
                    }
                ]
            },
            "membership_plan": Endpoint.TEST_DATA.membership_plan_id.get('CooP')
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
            "membership_plan": 314
        }
        return payload
