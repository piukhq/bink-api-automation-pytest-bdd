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
    TestTransactionMatchingContext.spend_amount = random.choice(range(1, 20)) / 100
    TestTransactionMatchingContext.transaction_id = (
        TransactionMatchingPaymentFileDetails.get_random_alphanumeric_string(48)
    )
    TestTransactionMatchingContext.transaction_auth_code = random.randint(100000, 999999)
    TestTransactionMatchingContext.current_time_stamp = datetime.now(timezone("Europe/London")).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


class TransactionMatchingPaymentFileDetails:
    @staticmethod
    def import_master_auth_payment_card(mid):
        import_payment_file = TransactionMatchingPaymentFileDetails.get_mastercard_auth_data(mid)
        return import_payment_file

    @staticmethod
    def import_spotting_master_auth_payment_card(mid):
        import_payment_file = TransactionMatchingPaymentFileDetails.get_mastercard_auth_spotting_data(mid)
        return import_payment_file

    @staticmethod
    def get_mastercard_auth_spotting_data(mid):
        TestTransactionMatchingContext.spend_amount = random.choice(range(1, 20))
        TestTransactionMatchingContext.transaction_id = TransactionMatchingPaymentFileDetails. \
            get_random_alphanumeric_string(48)
        TestTransactionMatchingContext.third_party_id = base64.b64encode(uuid.uuid4().bytes).decode()[:9]
        TestTransactionMatchingContext.transaction_auth_code = random.randint(100000, 999999)
        TestTransactionMatchingContext.created_at = datetime.now(timezone('Europe/London')) \
            .strftime('%Y-%m-%d %H:%M:%S')
        return {
            "amount": TestTransactionMatchingContext.spend_amount / 100,
            "currency_code": "GBP",
            "mid": mid,
            "payment_card_token": PaymentCardTestData.get_data("master").get(constants.TOKEN),
            "third_party_id": TestTransactionMatchingContext.third_party_id,
            "time": TestTransactionMatchingContext.created_at
        }

    @staticmethod
    def get_master_settlement_spotting_txt_file(mid):
        get_data_to_import()
        third_part_id = base64.b64encode(uuid.uuid4().bytes).decode()[:9]
        TestTransactionMatchingContext.created_at = now = pendulum.now()
        mid = mid
        TestTransactionMatchingContext.transaction_matching_id = uuid.uuid4()
        TestTransactionMatchingContext.auth_code = random.randint(100000, 999999)
        TestTransactionMatchingContext.spend_amount = random.choice(range(1, 10))
        payment_card_token = PaymentCardTestData.get_data("master").get(constants.TOKEN)
        amount = (str(TestTransactionMatchingContext.spend_amount).zfill(12))
        lines = [join(
            ("H", 1),
            (now.format("YYYYMMDD"), 8),
            (now.format("hhmmss"), 6),
            (" ", 6),
            ("mastercard-tgx2-settlement.txt", 9),
            ("", 835),

        ), join(
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
            (TestTransactionMatchingContext.auth_code, 6),
            ("", 188),
            (third_part_id, 9),
        ), join(
            ("T", 1),
            (now.format("YYYYMMDD"), 8),
            (now.format("hhmmss"), 6),
            ("", 6),
            ("mastercard-tgx2-settlement.txt", 9),
            ("", 835),
        )]
        file_name = str("-tgx2-settlement" + str(TestTransactionMatchingContext.spend_amount) + ".txt")
        with open(file_name, "a+") as file_name:
            for line in lines:
                (file_name.write(str(line)))
                file_name.write('\n')
        return file_name

    @staticmethod
    def get_master_settlement_txt_file(mid):
        get_data_to_import()
        third_part_id = base64.b64encode(uuid.uuid4().bytes).decode()[:9]
        now = pendulum.now()
        auth_code = TestTransactionMatchingContext.transaction_matching_uuid
        mid = mid
        payment_card_token = PaymentCardTestData.get_data("master").get(constants.TOKEN)
        amount = str(TestTransactionMatchingContext.transaction_matching_amount * 100).zfill(12)
        lines = [
            join(
                ("H", 1),
                (now.format("YYYYMMDD"), 8),
                (now.format("hhmmss"), 6),
                (" ", 6),
                ("mastercard-tgx2-settlement.txt", 9),
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
                (third_part_id, 9),
            ),
            join(
                ("T", 1),
                (now.format("YYYYMMDD"), 8),
                (now.format("hhmmss"), 6),
                (" ", 6),
                ("mastercard-tgx2-settlement.txt", 9),
                ("", 835),
            ),
        ]
        file_name = str("-tgx2-settlement" + str(TestTransactionMatchingContext.transaction_matching_amount) + ".txt")
        with open(file_name, "a+") as file_name:
            for line in lines:
                (file_name.write(str(line)))
                file_name.write("\n")
        return file_name

    @staticmethod
    def get_master_refund_spotting_txt_file(mid):
        TestTransactionMatchingContext.created_at = now = pendulum.now()
        mid = mid
        TestTransactionMatchingContext.transaction_matching_id = uuid.uuid4()
        TestTransactionMatchingContext.auth_code = random.randint(100000, 999999)
        TestTransactionMatchingContext.spend_amount = -(random.choice(range(1, 10)))
        payment_card_token = PaymentCardTestData.get_data("master").get(constants.TOKEN)
        amount = (str(-abs(TestTransactionMatchingContext.spend_amount)).zfill(12))
        lines = [join(
            ("H", 1),
            (now.format("YYYYMMDD"), 8),
            (now.format("hhmmss"), 6),
            (" ", 6),
            ("mastercard-tgx2-settlement.txt", 9),
            ("", 835),

        ), join(
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
            (TestTransactionMatchingContext.auth_code, 6),
            ("", 188),
            ("", 9),
        ), join(
            ("T", 1),
            (now.format("YYYYMMDD"), 8),
            (now.format("hhmmss"), 6),
            ("", 6),
            ("mastercard-tgx2-settlement.txt", 9),
            ("", 835),
        )]
        file_name = str("-tgx2-settlement" + str(TestTransactionMatchingContext.spend_amount) + ".txt")
        with open(file_name, "a+") as file_name:
            for line in lines:
                (file_name.write(str(line)))
                file_name.write('\n')
        return file_name

    @staticmethod
    def get_mastercard_auth_data(mid):
        return {
            "amount": TestTransactionMatchingContext.transaction_matching_amount,
            "currency_code": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.CURRENCY),
            "mid": mid,
            "payment_card_token": PaymentCardTestData.get_data("master").get(constants.TOKEN),
            "third_party_id": base64.b64encode(uuid.uuid4().bytes).decode()[:9],
            "time": TestTransactionMatchingContext.transaction_matching_currentTimeStamp,
        }

    @staticmethod
    def import_amex_auth_payment_card():
        import_amex_register_file = TransactionMatchingPaymentFileDetails.get_amex_auth_regirster_data()
        return import_amex_register_file

    @staticmethod
    def get_amex_auth_regirster_data():
        return {
            "client_id": "8UXGKh7ihjAeqZldlIBqlcnmoljug5ZznluEDLd6z33s9W7ZXP",
            "client_secret": "w9IgmvHABKgvwGgsnAof66hFZQlvxvyiR82PR3ZOcnlHWFdHO9",
        }

    @staticmethod
    def get_amex_auth_data(mid):
        return {
            "approval_code": str(TestTransactionMatchingContext.transaction_matching_auth_code)[-6:],
            "cm_alias": PaymentCardTestData.get_data("amex").get(constants.TOKEN),
            "merchant_number": mid,
            "offer_id": "0",
            "transaction_amount": str(TestTransactionMatchingContext.transaction_matching_amount),
            "transaction_currency": "UKL",
            "transaction_id": str(TestTransactionMatchingContext.transaction_matching_id),
            "transaction_time": TestTransactionMatchingContext.transaction_matching_amexTimeStamp,
        }

    @staticmethod
    def get_amex_auth_spotting_data(mid):
        TestTransactionMatchingContext.approval_code = random.randint(100000, 999999)
        TestTransactionMatchingContext.transaction_id = base64.b64encode(str(uuid.uuid4()).encode()).decode()
        TestTransactionMatchingContext.spend_amount = int(Decimal(str(random.choice(range(10, 1000)))))
        TestTransactionMatchingContext.transaction_matching_amexTimeStamp = datetime.now(timezone("MST")).strftime(
            "%Y-%m-%d %H:%M:%S")
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
        TestTransactionMatchingContext.approval_code = random.randint(100000, 999999)
        TestTransactionMatchingContext.transaction_id = base64.b64encode(str(uuid.uuid4()).encode()).decode()
        TestTransactionMatchingContext.spend_amount = int(Decimal(str(random.choice(range(10, 1000)))))
        TestTransactionMatchingContext.transaction_matching_amexTimeStamp = datetime.now(timezone("MST")).strftime(
            "%Y-%m-%d %H:%M:%S")
        return {
            "approvalCode": str(TestTransactionMatchingContext.approval_code),
            "cardToken": PaymentCardTestData.get_data("amex").get(constants.TOKEN),
            "currencyCode": "840",
            "dpan": PaymentCardTestData.get_data("amex").get(constants.FIRST_SIX_DIGITS)
            + "XXXXX" + PaymentCardTestData.get_data("amex").get(constants.LAST_FOUR_DIGITS),
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
        TestTransactionMatchingContext.approval_code = random.randint(100000, 999999)
        TestTransactionMatchingContext.transaction_id = base64.b64encode(str(uuid.uuid4()).encode()).decode()
        TestTransactionMatchingContext.spend_amount = int(Decimal(str(random.choice(range(10, 1000)))))
        TestTransactionMatchingContext.transaction_matching_amexTimeStamp = datetime.now(timezone("MST")).strftime(
            "%Y-%m-%d %H:%M:%S")
        return {
            "approvalCode": str(TestTransactionMatchingContext.approval_code),
            "cardToken": PaymentCardTestData.get_data("amex").get(constants.TOKEN),
            "currencyCode": "840",
            "dpan": PaymentCardTestData.get_data("amex").get(constants.FIRST_SIX_DIGITS) + "XXXXX"
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
    def get_amex_settlement_data(mid):
        return {
            "approvalCode": str(TestTransactionMatchingContext.transaction_matching_uuid),
            "cardToken": PaymentCardTestData.get_data("amex").get(constants.TOKEN),
            "currencyCode": "840",
            "dpan": PaymentCardTestData.get_data("amex").get(constants.FIRST_SIX_DIGITS) + "XXXXX"
            + PaymentCardTestData.get_data("amex").get(constants.LAST_FOUR_DIGITS),
            "merchantNumber": mid,
            "offerId": "0",
            "partnerId": "AADP0050",
            "recordId": f"{base64.b64encode(str(uuid.uuid4()).encode()).decode()}AADP00400",
            "transactionAmount": str(TestTransactionMatchingContext.transaction_matching_amount),
            "transactionDate": TestTransactionMatchingContext.transaction_matching_currentTimeStamp,
            "transactionId": str(TestTransactionMatchingContext.transaction_matching_id),
        }

    @staticmethod
    def get_random_alphanumeric_string(length):
        letters_and_digits = string.ascii_letters + string.digits
        result_str = "".join((random.choice(letters_and_digits) for i in range(length)))
        return result_str

    @staticmethod
    def get_visa_auth_data(mid):
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
                {"Key": "Transaction.USDAmount",
                 "Value": TestTransactionMatchingContext.transaction_matching_amount / 100
                 },
                {"Key": "Transaction.MerchantLocalPurchaseDate", "Value": str(date.today())},
                {"Key": "Transaction.MerchantGroup.0.Name", "Value": "ICELAND-BONUS-CARD"},
                {"Key": "Transaction.MerchantGroup.0.ExternalId", "Value": "Iceland"},
                {"Key": "Transaction.AuthCode", "Value": TestTransactionMatchingContext.transaction_matching_uuid},
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
    def get_visa_spotting_merchant_auth_data(mid):
        return {
            "CardId": TestTransactionMatchingContext.transaction_id,
            "ExternalUserId": PaymentCardTestData.get_data("visa").get(constants.TOKEN),
            "MessageElementsCollection": [
                {"Key": "Transaction.MerchantCardAcceptorId", "Value": mid},
                {"Key": "Transaction.MerchantAcquirerBin", "Value": "3423432"},
                {"Key": "Transaction.TransactionAmount", "Value": TestTransactionMatchingContext.spend_amount},
                {"Key": "Transaction.VipTransactionId", "Value": TestTransactionMatchingContext.transaction_id},
                {"Key": "Transaction.VisaMerchantName", "Value": ""},
                {"Key": "Transaction.VisaMerchantId", "Value": ""},
                {"Key": "Transaction.VisaStoreName", "Value": ""},
                {"Key": "Transaction.VisaStoreId", "Value": ""},
                {"Key": "Transaction.CurrencyCodeNumeric", "Value": "840"},
                {"Key": "Transaction.BillingCurrencyCode", "Value": "840"},
                {"Key": "Transaction.USDAmount", "Value": TestTransactionMatchingContext.spend_amount},
                {"Key": "Transaction.MerchantLocalPurchaseDate", "Value": str(date.today())},
                {"Key": "Transaction.MerchantGroup.0.Name", "Value": "SPOTTING-MERCHANT"},
                {"Key": "Transaction.MerchantGroup.0.ExternalId", "Value": "Spotting Merchant"},
                {"Key": "Transaction.AuthCode", "Value": TestTransactionMatchingContext.transaction_auth_code},
                {
                    "Key": "Transaction.PanLastFour",
                    "Value": PaymentCardTestData.get_data("visa").get(constants.LAST_FOUR_DIGITS),
                },
                {"Key": "Transaction.MerchantDateTimeGMT", "Value": TestTransactionMatchingContext.current_time_stamp},
                {"Key": "Transaction.BillingAmount", "Value": TestTransactionMatchingContext.spend_amount},
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
    def get_visa_spotting_merchant_settlement_data(mid):
        return {
            "CardId": TestTransactionMatchingContext.transaction_id,
            "ExternalUserId": PaymentCardTestData.get_data("visa").get(constants.TOKEN),
            "MessageElementsCollection": [
                {"Key": "Transaction.MerchantCardAcceptorId", "Value": mid},
                {"Key": "Transaction.MerchantAcquirerBin", "Value": "3423432"},
                {"Key": "Transaction.TransactionAmount", "Value": TestTransactionMatchingContext.spend_amount},
                {"Key": "Transaction.VipTransactionId", "Value": TestTransactionMatchingContext.transaction_id},
                {"Key": "Transaction.VisaMerchantName", "Value": ""},
                {"Key": "Transaction.VisaMerchantId", "Value": ""},
                {"Key": "Transaction.VisaStoreName", "Value": ""},
                {"Key": "Transaction.VisaStoreId", "Value": ""},
                {"Key": "Transaction.CurrencyCodeNumeric", "Value": "840"},
                {"Key": "Transaction.BillingCurrencyCode", "Value": "840"},
                {"Key": "Transaction.USDAmount", "Value": TestTransactionMatchingContext.spend_amount},
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
                {"Key": "Transaction.SettlementAmount", "Value": TestTransactionMatchingContext.spend_amount},
                {"Key": "Transaction.SettlementCurrencyCodeNumeric", "Value": "826"},
                {"Key": "Transaction.SettlementBillingAmount",
                 "Value": TestTransactionMatchingContext.spend_amount},
                {"Key": "Transaction.SettlementBillingCurrency", "Value": "826"},
                {"Key": "Transaction.SettlementUSDAmount", "Value": TestTransactionMatchingContext.spend_amount},
            ],
            "MessageId": str(uuid.uuid4()),
            "MessageName": "AuthMessageTest",
            "UserDefinedFieldsCollection": [{"Key": "TransactionType", "Value": "Settle"}],
            "UserProfileId": str(uuid.uuid4()),
        }

    @staticmethod
    def get_visa_spotting_merchant_refund_data(mid):
        TestTransactionMatchingContext.spend_amount = random.choice(range(1, 20))
        TestTransactionMatchingContext.transaction_id = (
            TransactionMatchingPaymentFileDetails.get_random_alphanumeric_string(48)
        )
        TestTransactionMatchingContext.transaction_auth_code = random.randint(100000, 999999)
        TestTransactionMatchingContext.current_time_stamp = datetime.now(timezone("Europe/London")).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        return {
            "CardId": TestTransactionMatchingContext.transaction_id,
            "ExternalUserId": PaymentCardTestData.get_data("visa").get(constants.TOKEN),
            "MessageElementsCollection": [
                {"Key": "ReturnTransaction.CardAcceptorIdCode", "Value": mid},
                {"Key": "ReturnTransaction.AcquirerBIN", "Value": "3423432"},
                {"Key": "ReturnTransaction.Amount", "Value": TestTransactionMatchingContext.spend_amount / 100},
                {"Key": "ReturnTransaction.VipTransactionId", "Value": TestTransactionMatchingContext.transaction_id},
                {"Key": "ReturnTransaction.SettlementId", "Value": TestTransactionMatchingContext.transaction_id},
                {"Key": "ReturnTransaction.VisaMerchantName", "Value": ""},
                {"Key": "ReturnTransaction.VisaMerchantId", "Value": ""},
                {"Key": "ReturnTransaction.VisaStoreName", "Value": ""},
                {"Key": "ReturnTransaction.VisaStoreId", "Value": ""},
                {"Key": "ReturnTransaction.AcquirerAmount", "Value": TestTransactionMatchingContext.spend_amount / 100},
                {"Key": "ReturnTransaction.AcquirerCurrencyCode", "Value": "840"},
                {"Key": "ReturnTransaction.CurrencyCode", "Value": "840"},
                {"Key": "ReturnTransaction.TransactionUSDAmount", "Value":
                    TestTransactionMatchingContext.spend_amount / 100},
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
        TestTransactionMatchingContext.spend_amount = random.choice(range(1, 20))
        TestTransactionMatchingContext.transaction_id = (
            TransactionMatchingPaymentFileDetails.get_random_alphanumeric_string(48)
        )
        TestTransactionMatchingContext.transaction_auth_code = random.randint(100000, 999999)
        TestTransactionMatchingContext.current_time_stamp = datetime.now(timezone("Europe/London")).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        return {
            "CardId": TestTransactionMatchingContext.transaction_id,
            "ExternalUserId": invalid_token,
            "MessageElementsCollection": [
                {"Key": "Transaction.MerchantCardAcceptorId", "Value": mid},
                {"Key": "Transaction.MerchantAcquirerBin", "Value": "3423432"},
                {"Key": "Transaction.TransactionAmount", "Value": TestTransactionMatchingContext.spend_amount},
                {"Key": "Transaction.VipTransactionId", "Value": TestTransactionMatchingContext.transaction_id},
                {"Key": "Transaction.VisaMerchantName", "Value": ""},
                {"Key": "Transaction.VisaMerchantId", "Value": ""},
                {"Key": "Transaction.VisaStoreName", "Value": ""},
                {"Key": "Transaction.VisaStoreId", "Value": ""},
                {"Key": "Transaction.CurrencyCodeNumeric", "Value": "840"},
                {"Key": "Transaction.BillingCurrencyCode", "Value": "840"},
                {"Key": "Transaction.USDAmount", "Value": TestTransactionMatchingContext.spend_amount},
                {"Key": "Transaction.MerchantLocalPurchaseDate", "Value": str(date.today())},
                {"Key": "Transaction.MerchantGroup.0.Name", "Value": "SPOTTING-MERCHANT"},
                {"Key": "Transaction.MerchantGroup.0.ExternalId", "Value": "Spotting Merchant"},
                {"Key": "Transaction.AuthCode", "Value": TestTransactionMatchingContext.transaction_auth_code},
                {
                    "Key": "Transaction.PanLastFour",
                    "Value": PaymentCardTestData.get_data("visa").get(constants.LAST_FOUR_DIGITS),
                },
                {"Key": "Transaction.MerchantDateTimeGMT", "Value": TestTransactionMatchingContext.current_time_stamp},
                {"Key": "Transaction.BillingAmount", "Value": TestTransactionMatchingContext.spend_amount},
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
    def get_visa_settlement_data(mid):
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
                {"Key": "Transaction.USDAmount", "Value": TestTransactionMatchingContext.transaction_matching_amount
                 },
                {"Key": "Transaction.MerchantLocalPurchaseDate", "Value": str(date.today())},
                {"Key": "Transaction.MerchantGroup.0.Name", "Value": "ICELAND-BONUS-CARD"},
                {"Key": "Transaction.MerchantGroup.0.ExternalId", "Value": "Iceland"},
                {"Key": "Transaction.AuthCode", "Value": TestTransactionMatchingContext.transaction_matching_uuid},
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
