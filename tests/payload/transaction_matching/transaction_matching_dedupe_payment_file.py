import string
import uuid
import random

from tests.helpers import constants
from tests.helpers.test_helpers import PaymentCardTestData
from tests.helpers.test_transaction_matching_context import TestTransactionMatchingContext


def import_visa_settle_matching_dedupe_json(mid):
    """create json for  Transaction spotting-dedupe Visa Auth"""
    TestTransactionMatchingContext.transaction_id = get_random_alphanumeric_string(48)
    return {
        "CardId": get_random_alphanumeric_string(48),
        "ExternalUserId": PaymentCardTestData.get_data("visa").get(constants.TOKEN),
        "MessageElementsCollection": [
            {"Key": "Transaction.MerchantCardAcceptorId", "Value": mid},
            {"Key": "Transaction.MerchantAcquirerBin", "Value": "3423432"},
            {
                "Key": "Transaction.TransactionAmount",
                "Value": "5.00",
            },
            {
                "Key": "Transaction.VipTransactionId",
                "Value": TestTransactionMatchingContext.transaction_id,
            },
            {"Key": "Transaction.VisaMerchantName", "Value": ""},
            {"Key": "Transaction.VisaMerchantId", "Value": ""},
            {"Key": "Transaction.VisaStoreName", "Value": ""},
            {"Key": "Transaction.VisaStoreId", "Value": ""},
            {"Key": "Transaction.CurrencyCodeNumeric", "Value": "840"},
            {"Key": "Transaction.BillingCurrencyCode", "Value": "840"},
            {"Key": "Transaction.USDAmount", "Value": "5.00"},
            {"Key": "Transaction.MerchantLocalPurchaseDate", "Value": "2023-06-19"},
            {"Key": "Transaction.MerchantGroup.0.Name", "Value": "SPOTTING-MERCHANT"},
            {"Key": "Transaction.MerchantGroup.0.ExternalId", "Value": "Spotting Merchant"},
            {"Key": "Transaction.AuthCode", "Value": random.randint(100000, 999999)},
            {
                "Key": "Transaction.PanLastFour",
                "Value": PaymentCardTestData.get_data("visa").get(constants.LAST_FOUR_DIGITS),
            },
            {
                "Key": "Transaction.MerchantDateTimeGMT",
                "Value": "2023-06-19 14:37:16",
            },
            {"Key": "Transaction.BillingAmount", "Value": ""},
            {"Key": "Transaction.TimeStampYYMMDD", "Value": "0001-01-01T00:00:00"},
            {
                "Key": "Transaction.SettlementDate",
                "Value": "2023-06-19 06:08:40",
            },
            {
                "Key": "Transaction.SettlementAmount",
                "Value": "5.00",
            },
            {"Key": "Transaction.SettlementCurrencyCodeNumeric", "Value": "826"},
            {
                "Key": "Transaction.SettlementBillingAmount",
                "Value": "5.00",
            },
            {"Key": "Transaction.SettlementBillingCurrency", "Value": "826"},
            {
                "Key": "Transaction.SettlementUSDAmount",
                "Value": "5.00",
            },
        ],
        "MessageId": str(uuid.uuid4()),
        "MessageName": "AuthMessageTest",
        "UserDefinedFieldsCollection": [{"Key": "TransactionType", "Value": "Settle"}],
        "UserProfileId": str(uuid.uuid4()),
    }


# Supporting functions
@staticmethod
def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = "".join((random.choice(letters_and_digits) for i in range(length)))
    return result_str
