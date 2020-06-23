class IcelandCard:
    @staticmethod
    def add_membership_card_payload():
        payload = {
            "account": {
                "add_fields": [
                    {
                        "column": "Bonus card number",
                        "value": "5555555555555555555"
                    }
                ],
                "authorise_fields": [
                    {
                        "column": "Last name",
                        "value": "five"
                    },
                    {
                        "column": "Postcode",
                        "value": "rg5 5aa"
                    }
                ]
            },
            "membership_plan": 105
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