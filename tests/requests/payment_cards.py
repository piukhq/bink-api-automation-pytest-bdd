import time

import tests.api as api
import tests.helpers.constants as constants
from tests.payload.payment_cards.payment_card import PaymentCardDetails
from tests.api.base import Endpoint
from tests.helpers.test_context import TestContext
from tests.helpers.test_helpers import PaymentCardTestData


class PaymentCards(Endpoint):
    @staticmethod
    def add_payment_card(token, card_provider):
        url = PaymentCards.get_url()
        header = Endpoint.request_header(token)
        # payload = PaymentCardDetails.add_payment_card_payload_unencrypted(card_provider)
        payload = PaymentCardDetails.add_payment_card_payload_encrypted(card_provider)
        return Endpoint.call(url, header, "POST", payload)

    @staticmethod
    def get_payment_card(token, payment_card_id):
        for i in range(1, 30):
            url = PaymentCards.get_url(payment_card_id)
            header = Endpoint.request_header(token)
            response = Endpoint.call(url, header, "GET")
            response_json = response.json()
            if not response_json["status"] == PaymentCardTestData.get_data().get(constants.PAYMENT_CARD_STATUS):
                time.sleep(1)
            else:
                break

        return response

    @staticmethod
    def get_payment_cards(token):
        for i in range(1, 30):
            url = PaymentCards.get_url()
            header = Endpoint.request_header(token)
            response = Endpoint.call(url, header, "GET")
            response_json = response.json()
            if not response_json[0]["status"] == PaymentCardTestData.get_data().get(constants.PAYMENT_CARD_STATUS):
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
    def delete_payment_card_with_hash(token):
        """Delete Payment card by hash value
        This is a feature for API v1.2
        And the url should contain 'hash-'
        And the hash value shouldn't contain any special chars"""
        hash_val = TestContext.payment_card_hash
        url = Endpoint.BASE_URL + api.ENDPOINT_PAYMENT_CARD.format("hash-"+hash_val)
        header = Endpoint.request_header(token)
        response = Endpoint.call(url, header, "DELETE")
        return response

    @staticmethod
    def patch_mcard_pcard(token, membership_card_id, payment_card_id):

        url = Endpoint.BASE_URL + api.ENDPOINT_PATCH_MEMBERSHIP_PAYMENT.format(membership_card_id,
                                                                               payment_card_id)
        header = Endpoint.request_header(token)
        response = Endpoint.call(url, header, "PATCH")
        return response

    @staticmethod
    def patch_pcard_mcard(token, payment_card_id, membership_card_id):

        url = Endpoint.BASE_URL + api.ENDPOINT_PATCH_PAYMENT_MEMBERSHIP.format(payment_card_id,
                                                                               membership_card_id)
        header = Endpoint.request_header(token)
        response = Endpoint.call(url, header, "PATCH")
        return response

    @staticmethod
    def delete_mcard_pcard(token, membership_card_id, payment_card_id):

        url = Endpoint.BASE_URL + api.ENDPOINT_PATCH_MEMBERSHIP_PAYMENT.format(membership_card_id,
                                                                               payment_card_id)
        header = Endpoint.request_header(token)
        response = Endpoint.call(url, header, "DELETE")
        return response

    @staticmethod
    def delete_pcard_mcard(token, payment_card_id, membership_card_id):

        url = Endpoint.BASE_URL + api.ENDPOINT_PATCH_PAYMENT_MEMBERSHIP.format(payment_card_id,
                                                                               membership_card_id)
        header = Endpoint.request_header(token)
        response = Endpoint.call(url, header, "DELETE")
        return response

    @staticmethod
    def get_url(payment_card_id=None):
        if payment_card_id is None:
            return Endpoint.BASE_URL + api.ENDPOINT_PAYMENT_CARDS
        else:
            return Endpoint.BASE_URL + api.ENDPOINT_PAYMENT_CARD.format(payment_card_id)
