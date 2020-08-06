import tests.api as api
from tests.api.base import Endpoint
from tests.helpers.test_helpers import TestData


class MembershipTransactions(Endpoint):

    @staticmethod
    def get_all_membership_transactions(token):
        url = Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD_TRANSACTIONS
        header = Endpoint.request_header(token)
        response = Endpoint.call(url, header, "GET")
        return response

    @staticmethod
    def get_membership_transactions(token, membership_card_id):
        url = Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD_TRANSACTIONS.format(membership_card_id)
        header = Endpoint.request_header(token)
        response = Endpoint.call(url, header, "GET")
        return response

    @staticmethod
    def get_membership_card_single_transaction_detail(token, transaction_id):
        url = Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD_SINGLE_TRANSACTION.format(transaction_id)
        header = Endpoint.request_header(token)
        response = Endpoint.call(url, header, "GET")
        return response
