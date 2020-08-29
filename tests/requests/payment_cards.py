import time
import config
import tests.api as api
import tests.helpers.constants as constants

from tests.payload.payment_cards.payment_card import PaymentCardDetails
from tests.api.base import Endpoint
from tests.helpers.test_data_utils import TestDataUtils
from tests.helpers.test_helpers import PaymentCardTestData






class PaymentCards(Endpoint):
    @staticmethod
    def add_payment_card(token, test_email):
        url = PaymentCards.get_url()
        header = Endpoint.request_header(token)
        # payload = PaymentCardDetails.add_payment_card_payload(test_email)
        payload = PaymentCardDetails.add_payment_card_payload_encrypted(test_email)
        return Endpoint.call(url, header, "POST", payload)

    @staticmethod
    def get_payment_card(token, payment_card_id):
        for i in range(1, 30):
            url = PaymentCards.get_url(payment_card_id)
            header = Endpoint.request_header(token)
            response = Endpoint.call(url, header, "GET")
            response_json = response.json()
            if not response_json["status"] == PaymentCardTestData.get_data().get(constants.PAYMENT_CARD_STATUS):
                   # TestDataUtils.TEST_DATA.payment_card.get(constants.PAYMENT_CARD_STATUS):
                time.sleep(1)
            else:
                break

        return response

    @staticmethod
    def delete_payment_card(token, payment_card_id):
        url = PaymentCards.get_url(payment_card_id)
        header = Endpoint.request_header(token)
        response = Endpoint.call(url, header, "DELETE")
        return response

    @staticmethod
    def get_url(payment_card_id=None):
        if payment_card_id is None:
            return Endpoint.BASE_URL + api.ENDPOINT_PAYMENT_CARDS
        else:
            return Endpoint.BASE_URL + api.ENDPOINT_PAYMENT_CARD.format(payment_card_id)
