from tests.api.base import Endpoint
import logging


class PaymentCardDetails:

    @staticmethod
    def add_payment_card_payload():
        payload = {
            "card": {
                "token": "auto1093448038331testbinkcom",
                "last_four_digits": "4444",
                "first_six_digits": "555555",
                "name_on_card": "auto1093448038331testbinkcom",
                "month": 1,
                "year": 2044,
                "fingerprint": "auto1093448038331testbinkcom"
            },
            "account": {
                "consents": [
                    {
                        "latitude": 51.405372,
                        "longitude": -0.678357,
                        "timestamp": 1541720805,
                        "type": 1
                    }
                ]
            }
        }
        return payload
