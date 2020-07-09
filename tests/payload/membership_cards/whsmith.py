from tests.api.base import Endpoint


class WHSmithCard:
    @staticmethod
    def add_membership_card_payload():
        payload = {
            "account": {
                "authorise_fields": [
                    {
                        "column": "Reward number",
                        "value": Endpoint.TEST_DATA.whsmith_membership_card1.get('card_num1')

                    }
                ]
            },
            "membership_plan": Endpoint.TEST_DATA.membership_plan_id.get('whsmith')
        }
        return payload

    @staticmethod
    def enrol_membership_scheme():
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
        return payload