import datetime
import logging
import time
from dataclasses import dataclass
import tests.helpers.database.setupdb as db


@dataclass
class MatchedTransactionRecord:
    count: int


@dataclass
class MatchedTransactionRecordDetails:
    provider_slug: str
    transaction_date: datetime.datetime
    spend_amount: int
    loyalty_id: str
    mid: str
    scheme_account_id: int
    status: str
    location_id: str
    merchant_internal_id: str
    payment_card_account_id: int
    auth_code: str
    approval_code: str
    last_four: str
    payment_provider_slug: str
    primary_identifier: str
    export_uid: str
    feed_type: str


class QueryHarmonia:
    @staticmethod
    def fetch_match_transaction_count(transaction_id):
        """Fetch the matched account details using matched_transaction_id and amount"""
        connection = db.connect_harmonia_db()
        matched_transaction_record = MatchedTransactionRecord(0)
        try:
            query = get_matched_query(transaction_id)
            logging.info(query)
            logging.info("Waiting for transaction to get exported in export_transaction table")
            for i in range(1, 60):
                record = db.execute_query_fetch_one(connection, query)
                if record[0] == 0:
                    time.sleep(1)
                    continue
                else:
                    matched_transaction_record = MatchedTransactionRecord(record[0])
                    break
        except Exception:
            raise Exception(f"Transaction with '{transaction_id}' is not exported")
        db.clear_db(connection)
        return matched_transaction_record

    @staticmethod
    def fetch_match_transaction_count_invalid_mid(transaction_id, amount):
        """Fetch the matched account details using matched_transaction_id and amount"""
        connection = db.connect_harmonia_db()
        matched_transaction_record = MatchedTransactionRecord(0)
        try:
            query = get_matched_query_negative_cases(transaction_id, amount)
            logging.info(query)
            logging.info("Waiting for transaction to get exported in export_transaction table")
            for i in range(1, 60):
                record = db.execute_query_fetch_one(connection, query)
                if record[0] == 0:
                    time.sleep(1)
                    continue
                else:
                    matched_transaction_record = MatchedTransactionRecord(record[0])
                    break
        except Exception:
            raise Exception(f"Transaction with '{transaction_id}' is not exported")
        db.clear_db(connection)
        return matched_transaction_record

    @staticmethod
    def fetch_transaction_details(transaction_id):
        """Fetch the matched account details using matched_transaction_id and amount"""
        connection = db.connect_harmonia_db()
        query = get_matched_query_details(transaction_id)
        logging.info(query)
        logging.info("Waiting for Transaction status to change from PENDING to EXPORTED")
        try:
            for i in range(1, 90):
                record = db.execute_query_fetch_one(connection, query)
                if record[6] == "PENDING":
                    time.sleep(1)
                    continue
                else:
                    matched_transaction_details = MatchedTransactionRecordDetails(record[0], record[1], record[2],
                                                                                  record[3],
                                                                                  record[4], record[5],
                                                                                  record[6], record[7], record[8],
                                                                                  record[9],
                                                                                  record[10], record[11],
                                                                                  record[12], record[13], record[14],
                                                                                  record[15], record[16])

                    break
        except Exception:
            raise Exception(f"Transaction with '{transaction_id}' is in PENDING status")
        db.clear_db(connection)
        return matched_transaction_details

    @staticmethod
    def fetch_imported_transaction_count(transaction_id):
        """Fetch the spotted account details using spotted_transaction_id and amount"""
        connection = db.connect_harmonia_db()
        record = db.execute_query_fetch_one(connection, get_imported_transaction(transaction_id))
        if record is None:
            raise Exception(f"'{transaction_id}' is an Invalid transaction_id")
        else:
            imported_transaction_record = MatchedTransactionRecord(record[0])
        db.clear_db(connection)
        return imported_transaction_record


def get_imported_transaction(transaction_id):
    spotted_transaction = (
        "SELECT count(*) from harmonia.public.import_transaction "
        "WHERE transaction_id = '{}'".format(transaction_id)
    )
    logging.info(spotted_transaction)
    return spotted_transaction


def get_matched_query(transaction_id):
    transaction_query_account = (

        "SELECT count(*) FROM harmonia.public.export_transaction WHERE transaction_id='{}' ".format(transaction_id)
    )
    return transaction_query_account


def get_matched_query_negative_cases(transaction_id, amount):
    """For negative tests adding amount along with transaction_id
    as there is a row exists in Harmonia with transaction_id as null """
    transaction_query_account = (
        "SELECT count(*) FROM harmonia.public.export_transaction WHERE transaction_id='{}' "
        "and spend_amount={}".format(transaction_id, amount)
    )
    return transaction_query_account


def get_matched_query_details(transaction_id):
    transaction_details_record = (

        "SELECT provider_slug,transaction_date,spend_amount,loyalty_id,mid,scheme_account_id,status,location_id,"
        "merchant_internal_id,"
        "payment_card_account_id,auth_code, approval_code, last_four, payment_provider_slug, primary_identifier,"
        "export_uid,feed_type"
        " FROM harmonia.public.export_transaction WHERE transaction_id='{}'".format(transaction_id)

    )
    return transaction_details_record
