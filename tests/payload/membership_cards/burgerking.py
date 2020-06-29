from tests.api.base import Endpoint


class BKCard:

    @staticmethod
    def add_membership_card_payload():
        payload = {
            "account": {
                "authorise_fields": [
                    {
                        "column": "Rewards number",
                        "value": Endpoint.TEST_DATA.BK_membership_card3.get('card_num')
                    }
                ]
            },
            "membership_plan": Endpoint.TEST_DATA.membership_plan_id.get('BK')

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
