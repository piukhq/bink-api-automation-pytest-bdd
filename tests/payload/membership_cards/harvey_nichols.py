from tests.api.base import Endpoint


class HNCard:

    @staticmethod
    def add_membership_card_payload():
        payload = {
            "account": {
                "authorise_fields": [
                    {
                        "column": "Email",
                        "value": Endpoint.TEST_DATA.HN_membership_card1.get('id')
                    },
                    {
                        "column": "Password",
                        "value": Endpoint.TEST_DATA.HN_membership_card1.get('password')
                        # "value": RSACipher.encrypt_field("Password01")
                    }
                ]
            }, "membership_plan": Endpoint.TEST_DATA.membership_plan_id.get('HN')

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
