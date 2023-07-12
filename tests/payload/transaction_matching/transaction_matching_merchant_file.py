import csv
import random
import uuid
from datetime import datetime
from decimal import Decimal

from pytz import timezone

from tests.helpers import constants
from tests.helpers.test_helpers import PaymentCardTestData
from tests.helpers.test_transaction_matching_context import TestTransactionMatchingContext


def create_iceland_merchant_file_csv(output, payment_card_provider, mid, card_identity):
    """This function creates Iceland Merchant CSV File"""
    merchant_writer = csv.writer(output, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    merchant_writer.writerow(TestTransactionMatchingContext.iceland_file_header)
    get_new_filedata_import("iceland_retailer_file")
    merchant_writer.writerow(
        [
            PaymentCardTestData.get_data(payment_card_provider).get(constants.FIRST_SIX_DIGITS),
            PaymentCardTestData.get_data(payment_card_provider).get(constants.LAST_FOUR_DIGITS),
            "01/80",
            "3",
            card_identity,
            mid,
            TestTransactionMatchingContext.transaction_matching_currentTimeStamp,
            TestTransactionMatchingContext.transaction_matching_amount,
            "GBP",
            ".00",
            "GBP",
            TestTransactionMatchingContext.retailer_transaction_id,
            TestTransactionMatchingContext.transaction_matching_auth_code,
        ]
    )


def get_new_filedata_import(file_name):
    TestTransactionMatchingContext.retailer_transaction_id = uuid.uuid4()
    TestTransactionMatchingContext.transaction_matching_auth_code = random.randint(100000, 999999)
    TestTransactionMatchingContext.transaction_matching_amount = int(Decimal(str(random.choice(range(10, 1000)))))
    TestTransactionMatchingContext.transaction_matching_currentTimeStamp = datetime.now(
        timezone("Europe/London")
    ).strftime("%Y-%m-%d %H:%M:%S")
    TestTransactionMatchingContext.file_name = file_name + datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv"


def create_itsu_merchant_file_csv(output, payment_card_provider, card_identity, retailer_location_id):
    """This function creates Iceland Merchant CSV File"""
    merchant_writer = csv.writer(output, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    merchant_writer.writerow(TestTransactionMatchingContext.itsu_file_header)
    get_new_filedata_import("itsu_retailer_file")
    merchant_writer.writerow(
        [
            TestTransactionMatchingContext.retailer_transaction_id,
            card_identity,
            # first six should be blank
            "",
            PaymentCardTestData.get_data(payment_card_provider).get(constants.LAST_FOUR_DIGITS),
            TestTransactionMatchingContext.transaction_matching_amount,
            "GBP",
            TestTransactionMatchingContext.transaction_matching_auth_code,
            TestTransactionMatchingContext.transaction_matching_currentTimeStamp,
            # mid should be blank
            "",
            retailer_location_id,
            # transaction data should be blank
            "",
            # customer id should be blank
            "",
        ]
    )
