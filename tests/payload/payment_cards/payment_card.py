import logging
import json
import config
from tests.helpers.test_helpers import PaymentCardTestData

from tests.api.base import Endpoint
import tests.api as api
import tests.helpers.constants as constants

from tests.helpers.vault import channel_vault
from tests.helpers.vault.channel_vault import KeyType
from tests.helpers.test_context import TestContext
from shared_config_storage.credentials.encryption import RSACipher


class PaymentCardDetails:
    FIELDS_TO_ENCRYPT = (
        'first_six_digits',
        'last_four_digits',
        'month',
        'year',
        'hash'
    )

    @staticmethod
    def add_payment_card_payload_encrypted(test_email, card_provider="master"):
        payment_card = PaymentCardDetails.get_card(test_email, card_provider)
        if TestContext.channel_name == config.BINK.channel_name:
            pub_key = channel_vault.get_key(config.BINK.bundle_id, KeyType.PUBLIC_KEY)
        elif TestContext.channel_name == config.BARCLAYS.channel_name:
            pub_key = channel_vault.get_key(config.BARCLAYS.bundle_id, KeyType.PUBLIC_KEY)
        payload = PaymentCardDetails.encrypt(payment_card, pub_key)
        logging.info("The Request to add encrypted payment card is : \n\n"
                     + Endpoint.BASE_URL + api.ENDPOINT_PAYMENT_CARDS + "\n\n" + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def get_card(email, card_provider="master"):
        return {
            "card": {
                "hash": email.split("@")[0],
                "token": email.split("@")[0],
                "last_four_digits": PaymentCardTestData.get_data(card_provider).get(constants.LAST_FOUR_DIGITS),
                "first_six_digits": PaymentCardTestData.get_data(card_provider).get(constants.FIRST_SIX_DIGITS),
                "name_on_card": email.split("@")[0],
                "month": PaymentCardTestData.get_data(card_provider).get(constants.MONTH),
                "year": PaymentCardTestData.get_data(card_provider).get(constants.YEAR),
                "fingerprint": email.split("@")[0],
            },
            "account": {
                "consents": []
            },
        }

    @staticmethod
    def encrypt(payment_card, pub_key):
        for field in PaymentCardDetails.FIELDS_TO_ENCRYPT:
            cred = payment_card['card'].get(field)
            if not cred:
                raise ValueError(f"Missing credential {field}")
            try:
                encrypted_val = RSACipher().encrypt(cred, pub_key=pub_key)
            except Exception as e:
                raise ValueError(f"Value: {cred}") from e
            payment_card['card'][field] = encrypted_val

        return payment_card

    @staticmethod
    def add_payment_card_payload_unencrypted(email, card_provider="master"):
        payload = {
            "card": {
                "hash": email.split("@")[0],
                "token": email.split("@")[0],
                "last_four_digits": PaymentCardTestData.get_data(card_provider).get(constants.LAST_FOUR_DIGITS),
                "first_six_digits": PaymentCardTestData.get_data(card_provider).get(constants.FIRST_SIX_DIGITS),
                "name_on_card": email.split("@")[0],
                "month": PaymentCardTestData.get_data(card_provider).get(constants.MONTH),
                "year": PaymentCardTestData.get_data(card_provider).get(constants.YEAR),
                "fingerprint": email.split("@")[0],
            },
            "account": {
                "consents": [{"latitude": 51.405372, "longitude": -0.678357, "timestamp": 1541720805, "type": 1}]
            }
        }

        logging.info("The Request to add payment card is : \n\n"
                     + Endpoint.BASE_URL + api.ENDPOINT_PAYMENT_CARDS + "\n\n" + json.dumps(payload, indent=4))
        return payload
