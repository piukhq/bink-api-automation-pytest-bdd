import tests.api as api
import json
import jsonpath
import time
import logging
from tests.payload.payment_cards.payment_card import PaymentCardDetails
from tests.api.base import Endpoint


class PaymentCards(Endpoint):
    @staticmethod
    def add_payment_card(token):
        url = PaymentCards.get_url()
        header = Endpoint.request_header(token)
        payload = PaymentCardDetails.add_payment_card_payload()
        return Endpoint.call(url, header, "POST", payload)

    @staticmethod
    def get_payment_card(token, payment_card_id):
        url = PaymentCards.get_url(payment_card_id)
        header = Endpoint.request_header(token)
        response = Endpoint.call(url, header, "GET")
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
