import random
import string
import uuid
import base64
from decimal import Decimal
from pytz import timezone
from tests.helpers.test_data_utils import TestDataUtils
from tests.helpers.test_helpers import PaymentCardTestData
import tests.helpers.constants as constants
from tests.helpers.test_transaction_matching_context import TestTransactionMatchingContext
from datetime import date
from datetime import datetime
import pendulum
import typing as t

WidthField = t.Tuple[t.Any, int]


def join(*args: WidthField) -> str:
    return "".join(str(value).ljust(length) for value, length in args)


def get_data_to_import():
    TestTransactionMatchingContext.transaction_matching_amount = random.choice(range(1, 20)) / 100
    TestTransactionMatchingContext.transaction_id = (
        TransactionMatchingPaymentFileDetails.get_random_alphanumeric_string(48)
    )
    TestTransactionMatchingContext.settlement_id = TestTransactionMatchingContext.transaction_id
    TestTransactionMatchingContext.transaction_auth_code = random.randint(100000, 999999)
    TestTransactionMatchingContext.current_time_stamp = datetime.now(timezone("Europe/London")).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


class TransactionMatchingPaymentFileDetails:
    # *************************Matching transactions*************************************************
    """Global variables for saving the transaction_id
    and amount for e2e transactions"""
    transaction_id = ""
    spend_amount = ""

    @staticmethod
    def get_visa_auth_data(mid):
        """create json for  Transaction Matching Visa Auth"""
        return {
            "CardId": TransactionMatchingPaymentFileDetails.get_random_alphanumeric_string(48),
            "ExternalUserId": PaymentCardTestData.get_data("visa").get(constants.TOKEN),
            "MessageElementsCollection": [
                {"Key": "Transaction.MerchantCardAcceptorId", "Value": mid},
                {"Key": "Transaction.MerchantAcquirerBin", "Value": "3423432"},
                {
                    "Key": "Transaction.TransactionAmount",
                    "Value": TestTransactionMatchingContext.transaction_matching_amount,
                },
                {
                    "Key": "Transaction.VipTransactionId",
                    "Value": TransactionMatchingPaymentFileDetails.get_random_alphanumeric_string(48),
                },
                {"Key": "Transaction.VisaMerchantName", "Value": ""},
                {"Key": "Transaction.VisaMerchantId", "Value": ""},
                {"Key": "Transaction.VisaStoreName", "Value": ""},
                {"Key": "Transaction.VisaStoreId", "Value": ""},
                {"Key": "Transaction.CurrencyCodeNumeric", "Value": "840"},
                {"Key": "Transaction.BillingCurrencyCode", "Value": "840"},
                {
                    "Key": "Transaction.USDAmount",
                    "Value": TestTransactionMatchingContext.transaction_matching_amount / 100,
                },
                {"Key": "Transaction.MerchantLocalPurchaseDate", "Value": str(date.today())},
                {"Key": "Transaction.MerchantGroup.0.Name", "Value": "ICELAND-BONUS-CARD"},
                {"Key": "Transaction.MerchantGroup.0.ExternalId", "Value": "Iceland"},
                {"Key": "Transaction.AuthCode", "Value": TestTransactionMatchingContext.transaction_matching_auth_code},
                {
                    "Key": "Transaction.PanLastFour",
                    "Value": PaymentCardTestData.get_data("visa").get(constants.LAST_FOUR_DIGITS),
                },
                {
                    "Key": "Transaction.MerchantDateTimeGMT",
                    "Value": TestTransactionMatchingContext.transaction_matching_currentTimeStamp,
                },
                {
                    "Key": "Transaction.BillingAmount",
                    "Value": TestTransactionMatchingContext.transaction_matching_amount,
                },
                {
                    "Key": "Transaction.TimeStampYYMMDD",
                    "Value": TestTransactionMatchingContext.transaction_matching_currentTimeStamp,
                },
                {"Key": "Transaction.SettlementDate", "Value": ""},
                {"Key": "Transaction.SettlementAmount", "Value": "0"},
                {"Key": "Transaction.SettlementCurrencyCodeNumeric", "Value": "0"},
                {"Key": "Transaction.SettlementBillingAmount", "Value": "0"},
                {"Key": "Transaction.SettlementBillingCurrency", "Value": ""},
                {"Key": "Transaction.SettlementUSDAmount", "Value": "0"},
            ],
            "MessageId": str(uuid.uuid4()),
            "MessageName": "AuthMessageTest",
            "UserDefinedFieldsCollection": [{"Key": "TransactionType", "Value": "Auth"}],
            "UserProfileId": str(uuid.uuid4()),
        }

    @staticmethod
    def get_visa_settlement_data(mid):
        """create json for  Transaction Matching Visa Settlement"""

        return {
            "CardId": TransactionMatchingPaymentFileDetails.get_random_alphanumeric_string(48),
            "ExternalUserId": PaymentCardTestData.get_data("visa").get(constants.TOKEN),
            "MessageElementsCollection": [
                {"Key": "Transaction.MerchantCardAcceptorId", "Value": mid},
                {"Key": "Transaction.MerchantAcquirerBin", "Value": "3423432"},
                {
                    "Key": "Transaction.TransactionAmount",
                    "Value": TestTransactionMatchingContext.transaction_matching_amount,
                },
                {
                    "Key": "Transaction.VipTransactionId",
                    "Value": TransactionMatchingPaymentFileDetails.get_random_alphanumeric_string(48),
                },
                {"Key": "Transaction.VisaMerchantName", "Value": ""},
                {"Key": "Transaction.VisaMerchantId", "Value": ""},
                {"Key": "Transaction.VisaStoreName", "Value": ""},
                {"Key": "Transaction.VisaStoreId", "Value": ""},
                {"Key": "Transaction.CurrencyCodeNumeric", "Value": "840"},
                {"Key": "Transaction.BillingCurrencyCode", "Value": "840"},
                {"Key": "Transaction.USDAmount", "Value": TestTransactionMatchingContext.transaction_matching_amount},
                {"Key": "Transaction.MerchantLocalPurchaseDate", "Value": str(date.today())},
                {"Key": "Transaction.MerchantGroup.0.Name", "Value": "ICELAND-BONUS-CARD"},
                {"Key": "Transaction.MerchantGroup.0.ExternalId", "Value": "Iceland"},
                {"Key": "Transaction.AuthCode", "Value": TestTransactionMatchingContext.transaction_matching_auth_code},
                {
                    "Key": "Transaction.PanLastFour",
                    "Value": PaymentCardTestData.get_data("visa").get(constants.LAST_FOUR_DIGITS),
                },
                {
                    "Key": "Transaction.MerchantDateTimeGMT",
                    "Value": TestTransactionMatchingContext.transaction_matching_currentTimeStamp,
                },
                {"Key": "Transaction.BillingAmount", "Value": ""},
                {"Key": "Transaction.TimeStampYYMMDD", "Value": "0001-01-01T00:00:00"},
                {
                    "Key": "Transaction.SettlementDate",
                    "Value": TestTransactionMatchingContext.transaction_matching_currentTimeStamp,
                },
                {
                    "Key": "Transaction.SettlementAmount",
                    "Value": TestTransactionMatchingContext.transaction_matching_amount,
                },
                {"Key": "Transaction.SettlementCurrencyCodeNumeric", "Value": "826"},
                {
                    "Key": "Transaction.SettlementBillingAmount",
                    "Value": TestTransactionMatchingContext.transaction_matching_amount,
                },
                {"Key": "Transaction.SettlementBillingCurrency", "Value": "826"},
                {
                    "Key": "Transaction.SettlementUSDAmount",
                    "Value": TestTransactionMatchingContext.transaction_matching_amount,
                },
            ],
            "MessageId": str(uuid.uuid4()),
            "MessageName": "AuthMessageTest",
            "UserDefinedFieldsCollection": [{"Key": "TransactionType", "Value": "Settle"}],
            "UserProfileId": str(uuid.uuid4()),
        }

    @staticmethod
    def get_mastercard_auth_data(mid):
        """Create Mastercard Auth json for Transaction Matching"""
        return {
            "amount": TestTransactionMatchingContext.transaction_matching_amount,
            "currency_code": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.CURRENCY),
            "mid": mid,
            "payment_card_token": PaymentCardTestData.get_data("master").get(constants.TOKEN),
            "third_party_id": base64.b64encode(uuid.uuid4().bytes).decode()[:9],
            "time": TestTransactionMatchingContext.transaction_matching_currentTimeStamp,
        }

    @staticmethod
    def get_master_settlement_txt_file(mid):
        """Create Mastercard Settlement Text file for Transaction Matching"""
        payment_card_token = PaymentCardTestData.get_data("master").get(constants.TOKEN)
        amount = str(TestTransactionMatchingContext.transaction_matching_amount * 100).zfill(12)
        third_part_id = base64.b64encode(uuid.uuid4().bytes).decode()[:9]
        file_name = "mastercard-tgx2-settlement.txt"
        return create_mastercard_settle_text_file(
            payment_card_token,
            mid,
            amount,
            TestTransactionMatchingContext.transaction_matching_auth_code,
            file_name,
            third_part_id,
        )

    @staticmethod
    def get_amex_register_token():
        import_amex_register_file = TransactionMatchingPaymentFileDetails.get_amex_register_data()
        return import_amex_register_file

    @staticmethod
    def get_amex_register_data():
        return {
            "client_id": "8UXGKh7ihjAeqZldlIBqlcnmoljug5ZznluEDLd6z33s9W7ZXP",
            "client_secret": "w9IgmvHABKgvwGgsnAof66hFZQlvxvyiR82PR3ZOcnlHWFdHO9",
        }

    @staticmethod
    def get_amex_auth_data(mid):
        return {
            "approval_code": str(random.randint(100000, 999999))[-6:],
            "cm_alias": PaymentCardTestData.get_data("amex").get(constants.TOKEN),
            "merchant_number": mid,
            "offer_id": "0",
            "transaction_amount": str(TestTransactionMatchingContext.transaction_matching_amount),
            "transaction_currency": "UKL",
            "transaction_id": str(TransactionMatchingPaymentFileDetails.get_random_alphanumeric_string(48)),
            "transaction_time": datetime.now(timezone("MST")).strftime("%Y-%m-%d %H:%M:%S"),
        }

    @staticmethod
    def get_amex_settlement_data(mid):
        return {
            "approvalCode": str(random.randint(100000, 999999))[-6:],
            "cardToken": PaymentCardTestData.get_data("amex").get(constants.TOKEN),
            "currencyCode": "840",
            "dpan": PaymentCardTestData.get_data("amex").get(constants.FIRST_SIX_DIGITS)
            + "XXXXX"
            + PaymentCardTestData.get_data("amex").get(constants.LAST_FOUR_DIGITS),
            "merchantNumber": mid,
            "offerId": "0",
            "partnerId": "AADP0050",
            "recordId": f"{base64.b64encode(str(uuid.uuid4()).encode()).decode()}AADP00400",
            "transactionAmount": str(TestTransactionMatchingContext.transaction_matching_amount),
            "transactionDate": TestTransactionMatchingContext.transaction_matching_currentTimeStamp,
            "transactionId": str(TransactionMatchingPaymentFileDetails.get_random_alphanumeric_string(48)),
        }

    # *************************Streaming spotting transactions*************************************************
    @staticmethod
    def get_visa_spotting_merchant_auth_data(mid, e2e=None):
        get_data_to_import()
        if e2e:
            TransactionMatchingPaymentFileDetails.transaction_id = TestTransactionMatchingContext.transaction_id
            TransactionMatchingPaymentFileDetails.spend_amount = (
                TestTransactionMatchingContext.transaction_matching_amount
            )
        return {
            "CardId": TestTransactionMatchingContext.transaction_id,
            "ExternalUserId": PaymentCardTestData.get_data("visa").get(constants.TOKEN),
            "MessageElementsCollection": [
                {"Key": "Transaction.MerchantCardAcceptorId", "Value": mid},
                {"Key": "Transaction.MerchantAcquirerBin", "Value": "3423432"},
                {
                    "Key": "Transaction.TransactionAmount",
                    "Value": TestTransactionMatchingContext.transaction_matching_amount,
                },
                {"Key": "Transaction.VipTransactionId", "Value": TestTransactionMatchingContext.transaction_id},
                {"Key": "Transaction.VisaMerchantName", "Value": ""},
                {"Key": "Transaction.VisaMerchantId", "Value": ""},
                {"Key": "Transaction.VisaStoreName", "Value": ""},
                {"Key": "Transaction.VisaStoreId", "Value": ""},
                {"Key": "Transaction.CurrencyCodeNumeric", "Value": "840"},
                {"Key": "Transaction.BillingCurrencyCode", "Value": "840"},
                {"Key": "Transaction.USDAmount", "Value": TestTransactionMatchingContext.transaction_matching_amount},
                {"Key": "Transaction.MerchantLocalPurchaseDate", "Value": str(date.today())},
                {"Key": "Transaction.MerchantGroup.0.Name", "Value": "SPOTTING-MERCHANT"},
                {"Key": "Transaction.MerchantGroup.0.ExternalId", "Value": "Spotting Merchant"},
                {"Key": "Transaction.AuthCode", "Value": TestTransactionMatchingContext.transaction_auth_code},
                {
                    "Key": "Transaction.PanLastFour",
                    "Value": PaymentCardTestData.get_data("visa").get(constants.LAST_FOUR_DIGITS),
                },
                {"Key": "Transaction.MerchantDateTimeGMT", "Value": TestTransactionMatchingContext.current_time_stamp},
                {
                    "Key": "Transaction.BillingAmount",
                    "Value": TestTransactionMatchingContext.transaction_matching_amount,
                },
                {"Key": "Transaction.TimeStampYYMMDD", "Value": TestTransactionMatchingContext.current_time_stamp},
                {"Key": "Transaction.SettlementDate", "Value": ""},
                {"Key": "Transaction.SettlementAmount", "Value": "0"},
                {"Key": "Transaction.SettlementCurrencyCodeNumeric", "Value": "0"},
                {"Key": "Transaction.SettlementBillingAmount", "Value": "0"},
                {"Key": "Transaction.SettlementBillingCurrency", "Value": ""},
                {"Key": "Transaction.SettlementUSDAmount", "Value": "0"},
            ],
            "MessageId": str(uuid.uuid4()),
            "MessageName": "AuthMessageTest",
            "UserDefinedFieldsCollection": [{"Key": "TransactionType", "Value": "Auth"}],
            "UserProfileId": str(uuid.uuid4()),
        }

    @staticmethod
    def get_visa_spotting_settlement_data(mid, e2e=None):
        get_data_to_import()
        if not e2e:
            transaction_id = TestTransactionMatchingContext.transaction_id
            spend_amount = TestTransactionMatchingContext.transaction_matching_amount
        else:
            transaction_id = TransactionMatchingPaymentFileDetails.transaction_id
            spend_amount = TransactionMatchingPaymentFileDetails.spend_amount
            """After visa e2e payment tests(auth &settle), Setting the transaction_id back to
             TestTransactionMatchingContext.transaction_id for DB check """
            TestTransactionMatchingContext.transaction_id = transaction_id

        return {
            "CardId": transaction_id,
            "ExternalUserId": PaymentCardTestData.get_data("visa").get(constants.TOKEN),
            "MessageElementsCollection": [
                {"Key": "Transaction.MerchantCardAcceptorId", "Value": mid},
                {"Key": "Transaction.MerchantAcquirerBin", "Value": "3423432"},
                {
                    "Key": "Transaction.TransactionAmount",
                    "Value": spend_amount,
                },
                {"Key": "Transaction.VipTransactionId", "Value": transaction_id},
                {"Key": "Transaction.VisaMerchantName", "Value": ""},
                {"Key": "Transaction.VisaMerchantId", "Value": ""},
                {"Key": "Transaction.VisaStoreName", "Value": ""},
                {"Key": "Transaction.VisaStoreId", "Value": ""},
                {"Key": "Transaction.CurrencyCodeNumeric", "Value": "840"},
                {"Key": "Transaction.BillingCurrencyCode", "Value": "840"},
                {"Key": "Transaction.USDAmount", "Value": spend_amount},
                {"Key": "Transaction.MerchantLocalPurchaseDate", "Value": str(date.today())},
                {"Key": "Transaction.MerchantGroup.0.Name", "Value": "SPOTTING-MERCHANT"},
                {"Key": "Transaction.MerchantGroup.0.ExternalId", "Value": "Spotting Merchant"},
                {"Key": "Transaction.AuthCode", "Value": TestTransactionMatchingContext.transaction_auth_code},
                {
                    "Key": "Transaction.PanLastFour",
                    "Value": PaymentCardTestData.get_data("visa").get(constants.LAST_FOUR_DIGITS),
                },
                {"Key": "Transaction.MerchantDateTimeGMT", "Value": TestTransactionMatchingContext.current_time_stamp},
                {"Key": "Transaction.BillingAmount", "Value": ""},
                {"Key": "Transaction.TimeStampYYMMDD", "Value": "0001-01-01T00:00:00"},
                {"Key": "Transaction.SettlementDate", "Value": TestTransactionMatchingContext.current_time_stamp},
                {
                    "Key": "Transaction.SettlementAmount",
                    "Value": spend_amount,
                },
                {"Key": "Transaction.SettlementCurrencyCodeNumeric", "Value": "826"},
                {
                    "Key": "Transaction.SettlementBillingAmount",
                    "Value": spend_amount,
                },
                {"Key": "Transaction.SettlementBillingCurrency", "Value": "826"},
                {
                    "Key": "Transaction.SettlementUSDAmount",
                    "Value": spend_amount,
                },
            ],
            "MessageId": str(uuid.uuid4()),
            "MessageName": "AuthMessageTest",
            "UserDefinedFieldsCollection": [{"Key": "TransactionType", "Value": "Settle"}],
            "UserProfileId": str(uuid.uuid4()),
        }

    @staticmethod
    def get_visa_spotting_refund_data(mid, e2e=None):
        get_data_to_import()

        if e2e:
            spend_amount = TransactionMatchingPaymentFileDetails.spend_amount
            TestTransactionMatchingContext.settlement_id = TransactionMatchingPaymentFileDetails.transaction_id

        else:
            spend_amount = TestTransactionMatchingContext.transaction_matching_amount

        return {
            "CardId": TestTransactionMatchingContext.transaction_id,
            "ExternalUserId": PaymentCardTestData.get_data("visa").get(constants.TOKEN),
            "MessageElementsCollection": [
                {"Key": "ReturnTransaction.CardAcceptorIdCode", "Value": mid},
                {"Key": "ReturnTransaction.AcquirerBIN", "Value": "3423432"},
                {
                    "Key": "ReturnTransaction.Amount",
                    "Value": spend_amount,
                },
                {"Key": "ReturnTransaction.VipTransactionId", "Value": TestTransactionMatchingContext.transaction_id},
                {"Key": "ReturnTransaction.SettlementId", "Value": TestTransactionMatchingContext.settlement_id},
                {"Key": "ReturnTransaction.VisaMerchantName", "Value": ""},
                {"Key": "ReturnTransaction.VisaMerchantId", "Value": ""},
                {"Key": "ReturnTransaction.VisaStoreName", "Value": ""},
                {"Key": "ReturnTransaction.VisaStoreId", "Value": ""},
                {
                    "Key": "ReturnTransaction.AcquirerAmount",
                    "Value": spend_amount,
                },
                {"Key": "ReturnTransaction.AcquirerCurrencyCode", "Value": "840"},
                {"Key": "ReturnTransaction.CurrencyCode", "Value": "840"},
                {
                    "Key": "ReturnTransaction.TransactionUSDAmount",
                    "Value": spend_amount,
                },
                {"Key": "ReturnTransaction.DateTime", "Value": "1/19/2022 1:2:48 PM"},
                {"Key": "ReturnTransaction.MerchantGroup.0.Name", "Value": "SPOTTING-MERCHANT"},
                {"Key": "ReturnTransaction.MerchantGroupName.0.ExternalId", "Value": "Spotting Merchant"},
                {"Key": "ReturnTransaction.AuthCode", "Value": TestTransactionMatchingContext.transaction_auth_code},
            ],
            "MessageId": str(uuid.uuid4()),
            "MessageName": "AuthMessageTest",
            "UserDefinedFieldsCollection": [{"Key": "TransactionType", "Value": "return"}],
            "UserProfileId": str(uuid.uuid4()),
        }

    @staticmethod
    def get_visa_spotting_merchant_auth_data_with_invalid_token(mid):
        invalid_token = "5657775"
        get_data_to_import()

        return {
            "CardId": TestTransactionMatchingContext.transaction_id,
            "ExternalUserId": invalid_token,
            "MessageElementsCollection": [
                {"Key": "Transaction.MerchantCardAcceptorId", "Value": mid},
                {"Key": "Transaction.MerchantAcquirerBin", "Value": "3423432"},
                {
                    "Key": "Transaction.TransactionAmount",
                    "Value": TestTransactionMatchingContext.transaction_matching_amount,
                },
                {"Key": "Transaction.VipTransactionId", "Value": TestTransactionMatchingContext.transaction_id},
                {"Key": "Transaction.VisaMerchantName", "Value": ""},
                {"Key": "Transaction.VisaMerchantId", "Value": ""},
                {"Key": "Transaction.VisaStoreName", "Value": ""},
                {"Key": "Transaction.VisaStoreId", "Value": ""},
                {"Key": "Transaction.CurrencyCodeNumeric", "Value": "840"},
                {"Key": "Transaction.BillingCurrencyCode", "Value": "840"},
                {"Key": "Transaction.USDAmount", "Value": TestTransactionMatchingContext.transaction_matching_amount},
                {"Key": "Transaction.MerchantLocalPurchaseDate", "Value": str(date.today())},
                {"Key": "Transaction.MerchantGroup.0.Name", "Value": "SPOTTING-MERCHANT"},
                {"Key": "Transaction.MerchantGroup.0.ExternalId", "Value": "Spotting Merchant"},
                {"Key": "Transaction.AuthCode", "Value": TestTransactionMatchingContext.transaction_auth_code},
                {
                    "Key": "Transaction.PanLastFour",
                    "Value": PaymentCardTestData.get_data("visa").get(constants.LAST_FOUR_DIGITS),
                },
                {"Key": "Transaction.MerchantDateTimeGMT", "Value": TestTransactionMatchingContext.current_time_stamp},
                {
                    "Key": "Transaction.BillingAmount",
                    "Value": TestTransactionMatchingContext.transaction_matching_amount,
                },
                {"Key": "Transaction.TimeStampYYMMDD", "Value": TestTransactionMatchingContext.current_time_stamp},
                {"Key": "Transaction.SettlementDate", "Value": ""},
                {"Key": "Transaction.SettlementAmount", "Value": "0"},
                {"Key": "Transaction.SettlementCurrencyCodeNumeric", "Value": "0"},
                {"Key": "Transaction.SettlementBillingAmount", "Value": "0"},
                {"Key": "Transaction.SettlementBillingCurrency", "Value": ""},
                {"Key": "Transaction.SettlementUSDAmount", "Value": "0"},
            ],
            "MessageId": str(uuid.uuid4()),
            "MessageName": "AuthMessageTest",
            "UserDefinedFieldsCollection": [{"Key": "TransactionType", "Value": "Auth"}],
            "UserProfileId": str(uuid.uuid4()),
        }

    @staticmethod
    def get_mastercard_auth_spotting_data(mid):
        get_data_to_import()
        now = pendulum.now()
        third_party_id = base64.b64encode(uuid.uuid4().bytes).decode()[:9]
        TestTransactionMatchingContext.transaction_id = third_party_id + "_" + now.format("YYYYMMDD")

        return {
            "amount": random.choice(range(1, 20)) / 100,
            "currency_code": "GBP",
            "mid": mid,
            "payment_card_token": PaymentCardTestData.get_data("master").get(constants.TOKEN),
            "third_party_id": third_party_id,
            "time": TestTransactionMatchingContext.current_time_stamp,
        }

    @staticmethod
    def get_master_settlement_spotting_txt_file(mid):
        """Pass below data to create master_settlement_spotting_txt_file"""
        payment_card_token = PaymentCardTestData.get_data("master").get(constants.TOKEN)
        TestTransactionMatchingContext.transaction_matching_amount = random.choice(range(1, 10))
        amount = str(TestTransactionMatchingContext.transaction_matching_amount).zfill(12)
        auth_code = random.randint(100000, 999999)
        third_party_id = base64.b64encode(uuid.uuid4().bytes).decode()[:9]
        """Saving third_party_id to reuse it in refund file
        for the_works master_card e2e tests"""
        TestTransactionMatchingContext.third_party_id = third_party_id
        TestTransactionMatchingContext.transaction_id = third_party_id + "_" + pendulum.now().format("YYYYMMDD")
        file_name = "mastercard-tgx2-settlement.txt"
        return create_mastercard_settle_text_file(payment_card_token, mid, amount, auth_code, file_name, third_party_id)

    @staticmethod
    def get_master_refund_spotting_txt_file(mid):
        """Master card refund file do not have Third_party,
        so can not reuse general function to create mastercard text files"""

        TestTransactionMatchingContext.created_at = now = pendulum.now()
        mid = mid
        TestTransactionMatchingContext.transaction_matching_id = uuid.uuid4()
        TestTransactionMatchingContext.auth_code = random.randint(100000, 999999)
        payment_card_token = PaymentCardTestData.get_data("master").get(constants.TOKEN)
        amount = str(-abs(TestTransactionMatchingContext.transaction_matching_amount)).zfill(12)
        TestTransactionMatchingContext.transaction_matching_amount = str(
            -abs(TestTransactionMatchingContext.transaction_matching_amount)
        )
        lines = [
            join(
                ("H", 1),
                (now.format("YYYYMMDD"), 8),
                (now.format("hhmmss"), 6),
                (" ", 6),
                ("mastercard-tgx2-refund.txt", 9),
                ("", 835),
            ),
            join(
                ("D", 1),
                ("", 20),
                (payment_card_token, 30),
                ("", 51),
                (pendulum.instance(datetime.now()).in_tz("Europe/London").format("YYYYMMDD"), 8),
                # above format is one hr ahead of current time
                # when tests run between 11pm and 12am next day's date is passing in the file
                # to avoid this below time zone format can be used
                # (pendulum.instance(datetime.now()).in_tz("GMT").format("YYYYMMDD"), 8),
                ("", 341),
                (mid, 15),
                ("", 52),
                ((amount[:12]), 12),
                ("", 33),
                (pendulum.instance(datetime.now()).in_tz("Europe/London").format("HHmm"), 4),
                (TestTransactionMatchingContext.auth_code, 6),
                ("", 188),
                ("", 9),
            ),
            join(
                ("T", 1),
                (now.format("YYYYMMDD"), 8),
                (now.format("hhmmss"), 6),
                ("", 6),
                ("mastercard-tgx2-settlement.txt", 9),
                ("", 835),
            ),
        ]
        file_name = str("-tgx2-refund" + str(TestTransactionMatchingContext.spend_amount) + ".txt")
        with open(file_name, "a+") as file_name:
            for line in lines:
                (file_name.write(str(line)))
                file_name.write("\n")
        return file_name

    @staticmethod
    def get_master_refund_spotting_txt_file_the_works(mid):
        """Pass below data to create master_refund_spotting_txt_file.
        Unlike other merchant's master refund payment file for The-works master refund file contain
        transaction_id of the corresponding settlement file"""
        payment_card_token = PaymentCardTestData.get_data("master").get(constants.TOKEN)
        amount = str(-abs(TestTransactionMatchingContext.transaction_matching_amount)).zfill(12)
        auth_code = random.randint(100000, 999999)
        third_party_id = TestTransactionMatchingContext.third_party_id
        TestTransactionMatchingContext.transaction_matching_amount = str(
            -abs(TestTransactionMatchingContext.transaction_matching_amount)
        )
        file_name = "mastercard-tgx2-refund.txt"
        return create_mastercard_settle_text_file(payment_card_token, mid, amount, auth_code, file_name, third_party_id)

    @staticmethod
    def get_amex_auth_spotting_data(mid):
        TestTransactionMatchingContext.approval_code = random.randint(100000, 999999)
        TestTransactionMatchingContext.transaction_id = base64.b64encode(str(uuid.uuid4()).encode()).decode()
        TestTransactionMatchingContext.spend_amount = int(Decimal(str(random.choice(range(10, 1000)))))
        TestTransactionMatchingContext.transaction_matching_amexTimeStamp = datetime.now(timezone("MST")).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        return {
            "approval_code": str(TestTransactionMatchingContext.approval_code),
            "cm_alias": PaymentCardTestData.get_data("amex").get(constants.TOKEN),
            "merchant_number": mid,
            "offer_id": "0",
            "transaction_amount": str(TestTransactionMatchingContext.spend_amount),
            "transaction_currency": "UKL",
            "transaction_id": str(TestTransactionMatchingContext.transaction_id),
            "transaction_time": TestTransactionMatchingContext.transaction_matching_amexTimeStamp,
        }

    @staticmethod
    def get_amex_settlement_spotting_data(mid):
        """For Amex E2E spotting tests approval code, amount should be same in
        auth, settle & refund files"""
        TestTransactionMatchingContext.approval_code = random.randint(100000, 999999)
        TestTransactionMatchingContext.spend_amount = int(Decimal(str(random.choice(range(10, 1000)))))

        TestTransactionMatchingContext.transaction_id = base64.b64encode(str(uuid.uuid4()).encode()).decode()
        TestTransactionMatchingContext.transaction_matching_amexTimeStamp = datetime.now(timezone("MST")).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        return {
            "approvalCode": str(TestTransactionMatchingContext.approval_code),
            "cardToken": PaymentCardTestData.get_data("amex").get(constants.TOKEN),
            "currencyCode": "840",
            "dpan": PaymentCardTestData.get_data("amex").get(constants.FIRST_SIX_DIGITS)
            + "XXXXX"
            + PaymentCardTestData.get_data("amex").get(constants.LAST_FOUR_DIGITS),
            "merchantNumber": mid,
            "offerId": "0",
            "partnerId": "AADP0050",
            "recordId": f"{TestTransactionMatchingContext.transaction_id}AADP00400",
            "transactionAmount": str(TestTransactionMatchingContext.spend_amount),
            "transactionDate": TestTransactionMatchingContext.transaction_matching_amexTimeStamp,
            "transactionId": str(TestTransactionMatchingContext.transaction_id),
        }

    @staticmethod
    def get_amex_refund_spotting_data(mid):
        get_data_to_import()
        """For Amex E2E spotting tests approval code, spend_amount should be same in
               auth, settle & refund files"""
        if not TestTransactionMatchingContext.approval_code:
            TestTransactionMatchingContext.approval_code = random.randint(100000, 999999)
        if not TestTransactionMatchingContext.spend_amount:
            TestTransactionMatchingContext.spend_amount = int(Decimal(str(random.choice(range(10, 1000)))))

        TestTransactionMatchingContext.transaction_id = base64.b64encode(str(uuid.uuid4()).encode()).decode()
        TestTransactionMatchingContext.transaction_matching_amexTimeStamp = datetime.now(timezone("MST")).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        return {
            "approvalCode": str(TestTransactionMatchingContext.approval_code),
            "cardToken": PaymentCardTestData.get_data("amex").get(constants.TOKEN),
            "currencyCode": "840",
            "dpan": PaymentCardTestData.get_data("amex").get(constants.FIRST_SIX_DIGITS)
            + "XXXXX"
            + PaymentCardTestData.get_data("amex").get(constants.LAST_FOUR_DIGITS),
            "merchantNumber": mid,
            "offerId": "0",
            "partnerId": "AADP0050",
            "recordId": f"{TestTransactionMatchingContext.transaction_id}AADP00400",
            "transactionAmount": str(-TestTransactionMatchingContext.spend_amount),
            "transactionDate": "2022-08-14 04:37:57",
            "transactionId": str(TestTransactionMatchingContext.transaction_id),
        }

    @staticmethod
    def get_random_alphanumeric_string(length):
        letters_and_digits = string.ascii_letters + string.digits
        result_str = "".join((random.choice(letters_and_digits) for i in range(length)))
        return result_str


def create_mastercard_settle_text_file(payment_card_token, mid, amount, auth_code, file_name, third_party_id):
    now = pendulum.now()
    lines = [
        join(
            ("H", 1),
            (now.format("YYYYMMDD"), 8),
            (now.format("hhmmss"), 6),
            (" ", 6),
            (file_name, 9),
            ("", 835),
        ),
        join(
            ("D", 1),
            ("", 20),
            (payment_card_token, 30),
            ("", 51),
            (pendulum.instance(datetime.now()).in_tz("Europe/London").format("YYYYMMDD"), 8),
            ("", 341),
            (mid, 15),
            ("", 52),
            ((amount[:12]), 12),
            ("", 33),
            (pendulum.instance(datetime.now()).in_tz("Europe/London").format("HHmm"), 4),
            (auth_code, 6),
            ("", 188),
            (third_party_id, 9),
        ),
        join(
            ("T", 1),
            (now.format("YYYYMMDD"), 8),
            (now.format("hhmmss"), 6),
            (" ", 6),
            (file_name, 9),
            ("", 835),
        ),
    ]

    file_name = str("-tgx2-settlement" + str(TestTransactionMatchingContext.transaction_matching_amount) + ".txt")
    with open(file_name, "a+") as file_name:
        for line in lines:
            (file_name.write(str(line)))
            file_name.write("\n")
    return file_name
