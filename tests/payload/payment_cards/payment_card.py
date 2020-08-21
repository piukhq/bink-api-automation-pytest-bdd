import logging
import json

from tests.helpers.test_data_utils import TestDataUtils
from tests.api.base import Endpoint
import tests.api as api
import tests.helpers.constants as constants


class PaymentCardDetails:
    @staticmethod
    def add_payment_card_payload(test_email):
        payload = {
            "card": {
                "token": test_email.split("@")[0],
                "last_four_digits": TestDataUtils.TEST_DATA.payment_card.get(constants.LAST_FOUR_DIGITS),
                "first_six_digits": TestDataUtils.TEST_DATA.payment_card.get(constants.FIRST_SIX_DIGITS),
                "name_on_card": test_email.split("@")[0],
                "month": TestDataUtils.TEST_DATA.payment_card.get(constants.MONTH),
                "year": TestDataUtils.TEST_DATA.payment_card.get(constants.YEAR),
                "fingerprint": test_email.split("@")[0],
            },
            "account": {
                "consents": [{"latitude": 51.405372, "longitude": -0.678357, "timestamp": 1541720805, "type": 1}]
            }
        }
        logging.info("The Request to add payment card is : \n\n"
                     + Endpoint.BASE_URL + api.ENDPOINT_PAYMENT_CARDS + "\n\n" + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def add_payment_card_payload_encrypted(test_email):
        payload = {
            "account": {
                "consents": [{"timestamp": 1579607418, "type": 1}]
            },
            "card": {
                "fingerprint": test_email.split("@")[0],
                "token": test_email.split("@")[0],
                "hash": TestDataUtils.TEST_DATA.payment_card_encrypted_amex.get(constants.HASH),
                "first_six_digits": TestDataUtils.TEST_DATA.payment_card_encrypted_amex.get(constants.FIRST_SIX_DIGITS),
                "last_four_digits": TestDataUtils.TEST_DATA.payment_card_encrypted_amex.get(constants.LAST_FOUR_DIGITS),
                "month": TestDataUtils.TEST_DATA.payment_card_encrypted_amex.get(constants.MONTH),
                "year": TestDataUtils.TEST_DATA.payment_card_encrypted_amex.get(constants.YEAR),
                "name_on_card": test_email.split("@")[0]
            }
        }
        logging.info("The Request to add encrypted payment card is : \n\n"
                     + Endpoint.BASE_URL + api.ENDPOINT_PAYMENT_CARDS + "\n\n" + json.dumps(payload, indent=4))
        return payload
