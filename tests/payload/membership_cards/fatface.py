class FFCard:

    @staticmethod
    def add_membership_card_payload():
        payload = {
            "account": {
                "authorise_fields": [
                    {
                        "column": "Rewards number",
                        "value": "FF00000059702811"
                    }
                ]
            },
            "membership_plan": 281
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