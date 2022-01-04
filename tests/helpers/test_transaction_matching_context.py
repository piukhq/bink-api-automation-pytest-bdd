import random
from decimal import Decimal


class TestTransactionMatchingContext:
    """ Transaction matching """
    amex_token = ""
    transaction_matching_id = ""
    transaction_matching_uuid = ""
    transaction_matching_auth_code = ""
    transaction_matching_amount = ""
    transaction_matching_currentTimeStamp = ""
    transaction_matching_amexTimeStamp = ""
    container_name = "harmonia-imports"
    file_name = ""
    transaction_id = ""
    spend_amount = int(Decimal(str(random.choice(range(10, 1000)))))
    transaction_auth_code = random.randint(100000, 999999)

    iceland_file_header = ['TransactionCardFirst6', 'TransactionCardLast4', 'TransactionCardExpiry',
                           'TransactionCardSchemeId', 'TransactionCardScheme', 'TransactionStore_Id',
                           'TransactionTimestamp', 'TransactionAmountValue', 'TransactionAmountUnit',
                           'TransactionCashbackValue', 'TransactionCashbackUnit', 'TransactionId',
                           'TransactionAuthCode']
