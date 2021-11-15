import random
import uuid
from datetime import datetime
from decimal import Decimal

from pytz import timezone

from tests.helpers import constants
from tests.helpers.test_helpers import PaymentCardTestData
from tests.helpers.test_transaction_matching_context import TestTransactionMatchingContext


def harvey_nichols_merchant_file(payment_card_provider, mid, scheme):
    TestTransactionMatchingContext.transaction_matching_id = str(uuid.uuid4())
    TestTransactionMatchingContext.transaction_matching_auth_code = str(random.randint(10000000, 99999999))
    TestTransactionMatchingContext.transaction_matching_amount = int(Decimal(str(random.choice(range(10, 1000)))))
    TestTransactionMatchingContext.transaction_matching_currentTimeStamp = datetime.now(
        timezone("Europe/London")
    ).strftime("%Y-%m-%d %H:%M:%S")
    TestTransactionMatchingContext.transaction_matching_amexTimeStamp = datetime.now(timezone("MST")).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    if scheme == "MASTERCARD":

        data = {
            "transactions": [
                {
                    "alt_id": "",
                    "amount": {"unit": "GBP", "value": TestTransactionMatchingContext.transaction_matching_amount},
                    "auth_code": TestTransactionMatchingContext.transaction_matching_auth_code,
                    "card": {
                        "expiry": "12",
                        "first_6": PaymentCardTestData.get_data(payment_card_provider).get(constants.FIRST_SIX_DIGITS),
                        "last_4": PaymentCardTestData.get_data(payment_card_provider).get(constants.LAST_FOUR_DIGITS),
                        "scheme": scheme,
                    },
                    "id": str(TestTransactionMatchingContext.transaction_matching_id),
                    "store_id": mid,
                    "timestamp": (datetime.now().strftime("%Y-%m-%dT" "%H:%M:%S")),
                }
            ]
        }
        return data
    elif scheme == "AMEX":
        TestTransactionMatchingContext.transaction_matching_id = str(uuid.uuid4())
        TestTransactionMatchingContext.transaction_matching_auth_code = str(random.randint(10000000, 99999999))
        TestTransactionMatchingContext.transaction_matching_amount = int(Decimal(str(random.choice(range(10, 1000)))))
        TestTransactionMatchingContext.transaction_matching_currentTimeStamp = datetime.now(
            timezone("Europe/London")
        ).strftime("%Y-%m-%d %H:%M:%S")
        TestTransactionMatchingContext.transaction_matching_amexTimeStamp = datetime.now(timezone("MST")).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        return {
            "transactions": [
                {
                    "alt_id": "",
                    "amount": {"unit": "GBP", "value": TestTransactionMatchingContext.transaction_matching_amount},
                    "auth_code": TestTransactionMatchingContext.transaction_matching_auth_code,
                    "card": {
                        "expiry": "12",
                        "first_6": PaymentCardTestData.get_data(payment_card_provider).get(constants.FIRST_SIX_DIGITS),
                        "last_4": PaymentCardTestData.get_data(payment_card_provider).get(constants.LAST_FOUR_DIGITS),
                        "scheme": scheme,
                    },
                    "id": str(TestTransactionMatchingContext.transaction_matching_id),
                    "store_id": mid,
                    "timestamp": (datetime.now().strftime("%Y-%m-%dT" "%H:%M:%S")),
                }
            ]
        }
