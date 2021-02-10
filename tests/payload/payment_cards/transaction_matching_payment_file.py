import logging
import json
import uuid
import base64

from tests.helpers.test_data_utils import TestDataUtils
from tests.helpers.test_helpers import PaymentCardTestData
from tests.api.base import Endpoint
import tests.api as api
import tests.helpers.constants as constants
from tests.helpers.test_transaction_matching_context import TestTransactionMatchingContext


class TransactionMatchingPaymentFileDetails:

    @staticmethod
    def import_master_auth_payment_card(mid):
        import_payment_file = TransactionMatchingPaymentFileDetails.get_mastercard_auth_data(mid)
        logging.info("The Request to import payment card is : \n\n"
                     + Endpoint.BASE_URL + api.ENDPOINT_MASTER_CARD + "\n\n" +
                     json.dumps(import_payment_file, indent=4))
        return import_payment_file

    @staticmethod
    def get_mastercard_auth_data(mid):
        return {
            "amount": TestTransactionMatchingContext.transaction_matching_amount,
            "currency_code": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.CURRENCY),
            "mid": mid,
            "payment_card_token": PaymentCardTestData.get_data("master").get(constants.TOKEN),
            "third_party_id": base64.b64encode(uuid.uuid4().bytes).decode()[:9],
            "time": TestTransactionMatchingContext.transaction_matching_currentTimeStamp
        }

    @staticmethod
    def import_amex_auth_payment_card():
        import_amex_register_file = TransactionMatchingPaymentFileDetails.get_amex_auth_regirster_data()
        logging.info("The Request to Register Amex Auth payment card is : \n\n"
                     + Endpoint.BASE_URL + api.ENDPOINT_AMEX_CARD_REGISTER + "\n\n" +
                     json.dumps(import_amex_register_file, indent=4))
        return import_amex_register_file

    @staticmethod
    def get_amex_auth_regirster_data():
        return {
                "client_id": "8UXGKh7ihjAeqZldlIBqlcnmoljug5ZznluEDLd6z33s9W7ZXP",
                "client_secret": "w9IgmvHABKgvwGgsnAof66hFZQlvxvyiR82PR3ZOcnlHWFdHO9"
            }

    @staticmethod
    def get_amex_auth_data(mid):
        return {
                "approval_code": str(TestTransactionMatchingContext.transaction_matching_uuid),
                "cm_alias": PaymentCardTestData.get_data("amex").get(constants.TOKEN),
                "merchant_number": mid,
                "offer_id": "0",
                "transaction_amount": str(TestTransactionMatchingContext.transaction_matching_amount),
                "transaction_currency": "UKL",
                "transaction_id": str(TestTransactionMatchingContext.transaction_matching_id),
                "transaction_time": TestTransactionMatchingContext.transaction_matching_amexTimeStamp
        }
