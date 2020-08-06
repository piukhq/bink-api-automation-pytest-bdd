import tests.helpers.constants as constants
from tests.helpers.test_data_utils import TestDataUtils


class PaymentCardDetails:
    @staticmethod
    def add_payment_card_payload():
        payload = {
            "card": {
                "token": TestDataUtils.TEST_DATA.payment_card.get(constants.TOKEN),
                "last_four_digits": TestDataUtils.TEST_DATA.payment_card.get(constants.LAST_FOUR_DIGITS),
                "first_six_digits": TestDataUtils.TEST_DATA.payment_card.get(constants.FIRST_SIX_DIGITS),
                "name_on_card": TestDataUtils.TEST_DATA.payment_card.get(constants.NAME_ON_CARD),
                "month": TestDataUtils.TEST_DATA.payment_card.get(constants.MONTH),
                "year": TestDataUtils.TEST_DATA.payment_card.get(constants.YEAR),
                "fingerprint": TestDataUtils.TEST_DATA.payment_card.get(constants.FINGERPRINT),
            },
            "account": {
                "consents": [{"latitude": 51.405372, "longitude": -0.678357, "timestamp": 1541720805, "type": 1}]
            },
        }
        return payload
