import json
import logging

import tests.api as api
from tests.api.transactionmatching_base import TransactionMatchingEndpoint
from tests.helpers.test_transaction_matching_context import TestTransactionMatchingContext
from tests.api.base import Endpoint
from tests.payload.payment_cards.transaction_matching_payment_file import (
    TransactionMatchingPaymentFileDetails,
    get_data_to_import,
)


class TransactionMatching(Endpoint):
    @staticmethod
    def get_master_auth_csv(mid):
        url = TransactionMatching.get_mastrcard_url()
        header = TransactionMatchingEndpoint.request_header_mastercard()
        payload = TransactionMatchingPaymentFileDetails.import_master_auth_payment_card(mid)
        response = Endpoint.call(url, header, "POST", payload)
        return response

    @staticmethod
    def get_master_spotting_auth_file(mid):
        get_data_to_import()
        url = TransactionMatching.get_mastrcard_url()
        header = TransactionMatchingEndpoint.request_header_mastercard()
        payload = TransactionMatchingPaymentFileDetails.import_spotting_master_auth_payment_card(mid)
        response = Endpoint.call(url, header, "POST", payload)
        print(json.dumps(payload, indent=4))
        return response

    @staticmethod
    def get_visa_auth_csv(mid):
        get_data_to_import()
        url = TransactionMatching.get_visa_url()
        header = TransactionMatchingEndpoint.request_header_visa()
        payload = TransactionMatchingPaymentFileDetails.get_visa_auth_data(mid)
        response = Endpoint.call(url, header, "POST", payload)
        logging.info(json.dumps(payload, indent=4))
        return response

    @staticmethod
    def get_visa_settlement_file(mid):
        get_data_to_import()
        url = TransactionMatching.get_visa_url()
        header = TransactionMatchingEndpoint.request_header_visa()
        payload = TransactionMatchingPaymentFileDetails.get_visa_settlement_data(mid)
        response = Endpoint.call(url, header, "POST", payload)
        print(json.dumps(payload, indent=4))
        return response

    @staticmethod
    def get_visa_spotting_merchant_auth_file(mid):
        get_data_to_import()
        url = TransactionMatching.get_visa_url()
        header = TransactionMatchingEndpoint.request_header_visa()
        payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_merchant_auth_data(mid)
        response = Endpoint.call(url, header, "POST", payload)
        print(json.dumps(payload, indent=4))
        return response

    @staticmethod
    def get_visa_spotting_auth_settlement_file(mid):
        get_data_to_import()
        url = TransactionMatching.get_visa_url()
        header = TransactionMatchingEndpoint.request_header_visa()
        payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_merchant_auth_data(mid)
        response = Endpoint.call(url, header, "POST", payload)
        logging.info((json.dumps(payload, indent=4)))
        print(response)
        url = TransactionMatching.get_visa_url()
        header = TransactionMatchingEndpoint.request_header_visa()
        payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_merchant_settlement_data(mid)
        response = Endpoint.call(url, header, "POST", payload)
        logging.info((json.dumps(payload, indent=4)))
        print(response)

    @staticmethod
    def get_visa_spotting_merchant_settlement_file(mid):
        get_data_to_import()
        url = TransactionMatching.get_visa_url()
        header = TransactionMatchingEndpoint.request_header_visa()
        payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_merchant_settlement_data(mid)
        response = Endpoint.call(url, header, "POST", payload)
        print(json.dumps(payload, indent=4))
        return response

    @staticmethod
    def get_visa_spotting_merchant_refund_file(mid):
        get_data_to_import()
        url = TransactionMatching.get_visa_url()
        header = TransactionMatchingEndpoint.request_header_visa()
        payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_merchant_refund_data(mid)
        response = Endpoint.call(url, header, "POST", payload)
        print(json.dumps(payload, indent=4))
        return response

    @staticmethod
    def get_visa_spotting_merchant_refund_file_invalid_token(mid):
        url = TransactionMatching.get_visa_url()
        header = TransactionMatchingEndpoint.request_header_visa()
        payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_merchant_auth_data_with_invalid_token(mid)
        response = Endpoint.call(url, header, "POST", payload)
        print(json.dumps(payload, indent=4))
        return response

    @staticmethod
    def get_amex_register_payment_csv():
        get_data_to_import()
        url = TransactionMatching.get_amex_register_url()
        header = TransactionMatchingEndpoint.request_register_amex()
        payload = TransactionMatchingPaymentFileDetails.import_amex_auth_payment_card()
        response = Endpoint.call(url, header, "POST", payload)
        TestTransactionMatchingContext.amex_token = response.json().get("api_key")
        Endpoint.call(url, header, "POST", payload)

    @staticmethod
    def get_amex_auth_csv(mid):
        url = TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL_ZEPHYRUS + api.ENDPOINT_AMEX_CARD
        headers = TransactionMatchingEndpoint.request_header_amex(TestTransactionMatchingContext.amex_token)
        payload = TransactionMatchingPaymentFileDetails.get_amex_auth_data(mid)
        logging.info(json.dumps(payload, indent=2))
        response = Endpoint.call(url, headers, "POST", payload)
        return response

    @staticmethod
    def get_amex_auth_spotting_file(mid):
        get_data_to_import()
        url = TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL_ZEPHYRUS + api.ENDPOINT_AMEX_CARD
        headers = TransactionMatchingEndpoint.request_header_amex(TestTransactionMatchingContext.amex_token)
        payload = TransactionMatchingPaymentFileDetails.get_amex_auth_spotting_data(mid)
        logging.info(json.dumps(payload, indent=2))
        response = Endpoint.call(url, headers, "POST", payload)
        return response

    @staticmethod
    def get_amex_settlement_csv(mid):
        url = TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL_ZEPHYRUS + api.ENDPOINT_AMEX_SETTLEMENT_CARD
        headers = TransactionMatchingEndpoint.request_header_amex(TestTransactionMatchingContext.amex_token)
        payload = TransactionMatchingPaymentFileDetails.get_amex_settlement_data(mid)
        logging.info(json.dumps(payload, indent=2))
        response = Endpoint.call(url, headers, "POST", payload)
        return response

    @staticmethod
    def get_amex_settlement_spotting_file(mid):
        get_data_to_import()
        url = TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL_ZEPHYRUS + api.ENDPOINT_AMEX_SETTLEMENT_CARD
        headers = TransactionMatchingEndpoint.request_header_amex(TestTransactionMatchingContext.amex_token)
        payload = TransactionMatchingPaymentFileDetails.get_amex_settlement_spotting_data(mid)
        logging.info(json.dumps(payload, indent=2))
        response = Endpoint.call(url, headers, "POST", payload)
        return response

    @staticmethod
    def get_amex_refund_spotting_file(mid):
        get_data_to_import()
        url = TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL_ZEPHYRUS + api.ENDPOINT_AMEX_SETTLEMENT_CARD
        headers = TransactionMatchingEndpoint.request_header_amex(TestTransactionMatchingContext.amex_token)
        payload = TransactionMatchingPaymentFileDetails.get_amex_refund_spotting_data(mid)
        logging.info(json.dumps(payload, indent=2))
        response = Endpoint.call(url, headers, "POST", payload)
        return response

    @staticmethod
    def get_mastrcard_url():
        return TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL + api.ENDPOINT_MASTER_CARD

    @staticmethod
    def get_amex_register_url():
        return TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL_ZEPHYRUS + api.ENDPOINT_AMEX_CARD_REGISTER

    @staticmethod
    def get_visa_url():
        return TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL_ZEPHYRUS + api.ENDPOINT_VISA_CARD
