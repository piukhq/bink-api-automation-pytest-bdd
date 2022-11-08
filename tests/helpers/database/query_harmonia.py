import logging
from dataclasses import dataclass
import tests.helpers.database.setupdb as db


@dataclass
class MatchedTransactionRecord:
    count: int


class QueryHarmonia:
    @staticmethod
    def fetch_match_transaction_count(transaction_id, amount):
        """Fetch the matched account details using matched_transaction_id and amount"""
        connection = db.connect_harmonia_db()
        record = db.execute_query_fetch_one(connection, get_matched_query(transaction_id, amount))
        if record is None:
            raise Exception(f"'{transaction_id}' is an Invalid transaction_id")
        else:
            matched_transaction_record = MatchedTransactionRecord(record[0])
        db.clear_db(connection)
        return matched_transaction_record

    @staticmethod
    def fetch_spotted_transaction_count(transaction_id):
        """Fetch the spotted account details using spotted_transaction_id and amount"""
        connection = db.connect_harmonia_db()
        record = db.execute_query_fetch_one(connection, get_spotted_transaction(transaction_id))
        if record is None:
            raise Exception(f"'{transaction_id}' is an Invalid transaction_id")
        else:
            spotted_transaction_record = MatchedTransactionRecord(record[0])
        db.clear_db(connection)
        return spotted_transaction_record

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

    @staticmethod
    def fetch_mastercard_spotted_transaction_count(spend_amount, created_at):
        """Fetch the spotted account details using spotted_transaction_id and amount """
        connection = db.connect_harmonia_db()
        record = db.execute_query_fetch_one(connection, get_mastercard_spotted_transaction(spend_amount, created_at))
        if record is None:
            raise Exception(f"'{spend_amount}' is an Invalid spend_amount")
        else:
            spotted_transaction_record = MatchedTransactionRecord(record[0])
        db.clear_db(connection)
        return spotted_transaction_record

    @staticmethod
    def fetch_auth_mastercard_spotted_transaction_count(spend_amount, transaction_id):
        """Fetch the spotted account details using spotted_transaction_id and amount """
        connection = db.connect_harmonia_db()
        record = db.execute_query_fetch_one(connection,
                                            get_auth_mastercard_spotted_transaction(spend_amount, transaction_id))
        if record is None:
            raise Exception(f"'{spend_amount}' is an Invalid spend_amount")
        else:
            spotted_transaction_record = MatchedTransactionRecord(record[0])
        db.clear_db(connection)
        return spotted_transaction_record

    @staticmethod
    def fetch_mastercard_spotted_settlement_transaction_count(spend_amount, mid, auth_code):
        """Fetch the spotted account details using spotted_transaction_id and amount """
        connection = db.connect_harmonia_db()
        record = db.execute_query_fetch_one(connection,
                                            get_mastercard_spotted_settlement_transaction(spend_amount, mid, auth_code))
        if record is None:
            raise Exception(f"'{spend_amount}' is an Invalid spend_amount")
        else:
            spotted_transaction_record = MatchedTransactionRecord(record[0])
        db.clear_db(connection)
        return spotted_transaction_record


def get_mastercard_spotted_transaction(spend_amount, created_at):
    spotted_transaction = "SELECT count(*) from harmonia.public.export_transaction " \
                          "WHERE spend_amount = '{}'" \
                          "and status = 'EXPORTED'"\
                          "and created_at >= '{}'".format(spend_amount, created_at)
    logging.info(spotted_transaction)
    return spotted_transaction


def get_auth_mastercard_spotted_transaction(spend_amount, transaction_id):
    spotted_transaction = "SELECT count(*) from harmonia.public.export_transaction " \
                          "WHERE spend_amount = '{}'" \
                          "and status = 'EXPORTED'" \
                          "and transaction_id LIKE '{}%'".format(spend_amount, transaction_id)
    logging.info(spotted_transaction)
    return spotted_transaction


def get_mastercard_spotted_settlement_transaction(spend_amount, mid, auth_code):
    spotted_transaction = "SELECT count(*) from harmonia.public.export_transaction " \
                          "WHERE spend_amount = '{}'" \
                          "and status = 'EXPORTED'" \
                          "and mid = '{}'" \
                          "and auth_code = '{}'".format(spend_amount, mid, auth_code)
    logging.info(spotted_transaction)
    return spotted_transaction


def get_imported_transaction(transaction_id):
    spotted_transaction = (
        "SELECT count(*) from harmonia.public.import_transaction "
        "WHERE transaction_id = '{}'".format(transaction_id)
    )
    logging.info(spotted_transaction)
    return spotted_transaction


def get_spotted_transaction(transaction_id):
    spotted_transaction = (
        "SELECT count(*) from harmonia.public.export_transaction "
        "WHERE transaction_id = '{}'"
        "and status = 'EXPORTED'".format(transaction_id)
    )
    logging.info(spotted_transaction)
    return spotted_transaction


def get_matched_query(transaction_id, amount):
    transaction_query_account = (
        "SELECT count(*) FROM harmonia.public.matched_transaction WHERE transaction_id='{}' "
        "and spend_amount={}".format(transaction_id, amount)
    )
    logging.info(transaction_query_account)
    return transaction_query_account
