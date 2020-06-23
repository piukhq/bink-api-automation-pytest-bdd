class CoopCard:
    @staticmethod
    def add_membership_card_payload():
        payload = {
            "account": {
                "add_fields": [
                    {
                        "column": "Membership card number",
                        "value": "633174912301122335"
                    }
                ],
                "authorise_fields": [
                    {
                        "column": "Date of birth",
                        "value": "01/01/2000"
                    },
                    {
                        "column": "Postcode",
                        "value": "qa1 1qa"
                    }
                ]
            },
            "membership_plan": 242
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