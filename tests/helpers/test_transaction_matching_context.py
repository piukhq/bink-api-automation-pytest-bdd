import uuid
import random
from decimal import Decimal
from datetime import datetime
from pytz import timezone


class TestTransactionMatchingContext:
    """ Transaction matching """
    amex_token = ""
    transaction_matching_id = uuid.uuid4()
    transaction_matching_uuid = random.randint(100000, 999999)
    transaction_matching_amount = int(Decimal(str(random.choice(range(10, 1000)))))
    transaction_matching_currentTimeStamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    transaction_matching_amexTimeStamp = datetime.now(timezone('MST')).strftime('%Y-%m-%d %H:%M:%S')
    container_name = "harmonia-imports"
    file_name = "iceland-bonus-card" + datetime.now().strftime('%Y%m%d-%H%M%S') + ".csv"

    iceland_file_header = ['TransactionCardFirst6', 'TransactionCardLast4', 'TransactionCardExpiry',
                           'TransactionCardSchemeId', 'TransactionCardScheme', 'TransactionStore_Id',
                           'TransactionTimestamp', 'TransactionAmountValue', 'TransactionAmountUnit',
                           'TransactionCashbackValue', 'TransactionCashbackUnit', 'TransactionId',
                           'TransactionAuthCode']
