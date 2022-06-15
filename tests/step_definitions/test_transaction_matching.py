import uuid
import random
from decimal import Decimal
from datetime import datetime
import pytz
from pytz import timezone

from pytest_bdd import (
    scenarios,
    then,
    when,
    parsers,
)
import csv
import json
import logging
import time
import io
import os
from azure.storage.blob import ContentSettings
from azure.storage.blob import BlobServiceClient
import harvey_nichols_transaction_matching_files
from tests.helpers.database.query_harmonia import QueryHarmonia
from tests.helpers.test_helpers import PaymentCardTestData
import tests.helpers.constants as constants
import tests.step_definitions.test_payment_cards as test_payment_cards
from settings import BLOB_STORAGE_DSN
from tests.helpers.test_transaction_matching_context import TestTransactionMatchingContext
from tests.payload.payment_cards import transaction_matching_payment_file
from tests.requests.transaction_matching_payment_cards import TransactionMatching
from tests.step_definitions import test_membership_cards

scenarios("transactionMatching/")


@when(parsers.parse('I send matching "{payment_card_transaction}" "{mid}" Authorisation'))
def import_payment_file(payment_card_transaction, mid):
    if payment_card_transaction == "master-auth":
        response = TransactionMatching.get_master_auth_csv(mid)
    elif payment_card_transaction == "amex-auth":
        TransactionMatching.get_amex_register_payment_csv()
        response = TransactionMatching.get_amex_auth_csv(mid)
    elif payment_card_transaction == "amex-settlement":
        TransactionMatching.get_amex_register_payment_csv()
        response = TransactionMatching.get_amex_settlement_csv(mid)
    elif payment_card_transaction == "visa-auth":
        response = TransactionMatching.get_visa_auth_csv(mid)
    elif payment_card_transaction == "visa-settlement":
        response = TransactionMatching.get_visa_settlement_file(mid)
    elif payment_card_transaction == "visa-auth-spotting":
        response = TransactionMatching.get_visa_spotting_merchant_auth_file(mid)
    elif payment_card_transaction == "visa-settlement-spotting":
        response = TransactionMatching.get_visa_spotting_merchant_settlement_file(mid)
    elif payment_card_transaction == "visa-refund-spotting":
        response = TransactionMatching.get_visa_spotting_merchant_refund_file(mid)
    elif payment_card_transaction == "visa-auth-spotting_invalid_token":
        response = TransactionMatching.get_visa_spotting_merchant_refund_file_invalid_token(mid)
    elif payment_card_transaction == "master-auth-spotting":
        response = TransactionMatching.get_master_spotting_auth_file(mid)
    else:
        TransactionMatching.get_amex_register_payment_csv()
        response = TransactionMatching.get_amex_auth_csv(mid)

    response_json = response.json()
    logging.info("The response of POST/import Payment File is: \n\n" + json.dumps(response_json, indent=4))
    assert response.status_code == 201 or 200, "Payment file is not successful"
    if payment_card_transaction == "master-settlement":
        merchant_container = "mastercard"
        file_name = (
            transaction_matching_payment_file.TransactionMatchingPaymentFileDetails.get_master_settlement_txt_file(mid)
        )
        bbs = BlobServiceClient.from_connection_string(BLOB_STORAGE_DSN)
        blob_client = bbs.get_blob_client(
            "harmonia-imports/test/mastercard-settlement", merchant_container + f"{file_name.name}"
        )
        with open(file_name.name, "rb") as settlement_file:
            blob_client.upload_blob(settlement_file, content_settings=ContentSettings(content_type="text/plain"))
            logging.info(
                f"{file_name.name} has been uploaded to blob storage with auth_code = "
                f"{TestTransactionMatchingContext.transaction_matching_uuid} and MID = {mid}"
            )
            os.remove(file_name.name)
    elif payment_card_transaction == "master-settlement-spotting":
        merchant_container = "mastercard"
        file_name = transaction_matching_payment_file.\
            TransactionMatchingPaymentFileDetails.get_master_settlement_spotting_txt_file(mid)
        bbs = BlobServiceClient.from_connection_string(BLOB_STORAGE_DSN)
        blob_client = \
            bbs.get_blob_client("harmonia-imports/test/mastercard-settlement", merchant_container + f"{file_name.name}")
        with open(file_name.name, "rb") as settlement_file:
            blob_client.upload_blob(settlement_file, content_settings=ContentSettings(content_type="text/plain"))
            logging.info(
                f"{file_name.name} has been uploaded to blob storage with spend_amount = "
                f"{TestTransactionMatchingContext.spend_amount} and MID = {mid}"
            )
            os.remove(file_name.name)
    elif payment_card_transaction == 'master-refund-spotting':
        merchant_container = 'mastercard'
        file_name = \
            transaction_matching_payment_file.TransactionMatchingPaymentFileDetails.get_master_refund_spotting_txt_file(
                mid)
        bbs = BlobServiceClient.from_connection_string(BLOB_STORAGE_DSN)
        blob_client = \
            bbs.get_blob_client('harmonia-imports/test/mastercard-settlement', merchant_container + f"{file_name.name}")
        with open(file_name.name, "rb") as settlement_file:
            blob_client.upload_blob(settlement_file, content_settings=ContentSettings(content_type="text/plain"))
            logging.info(f'{file_name.name} has been uploaded to blob storage with spend_amount = '
                         f'{-abs(TestTransactionMatchingContext.spend_amount)},'
                         f'auth_code = {TestTransactionMatchingContext.auth_code} and MID = {mid}')
            os.remove(file_name.name)

    if payment_card_transaction == "visa-auth-spotting":
        logging.info("Waiting for transaction to be spotted and exported")
    elif payment_card_transaction == "visa-settlement-spotting":
        logging.info("Waiting for transaction to be spotted and exported")
    elif payment_card_transaction == "visa-refund-spotting":
        logging.info("Waiting for transaction to be spotted and exported")
    elif payment_card_transaction == "visa-auth-spotting_invalid_token":
        logging.info("Waiting for transaction to be spotted and exported")
    elif payment_card_transaction == "master-settlement-spotting":
        logging.info("Waiting for transaction to be spotted and exported")
    elif payment_card_transaction == "master-auth-spotting":
        logging.info("Waiting for transaction to be spotted and exported")
    elif payment_card_transaction == "master-refund-spotting":
        logging.info("Waiting for transaction to be spotted and exported")

    else:
        logging.info("Waiting for the pods To match the transaction....and Export the Files")
    time.sleep(90)
    return response_json


@then(parsers.parse("I verify 1 reward transaction is exported"))
def verify_into_database():
    matched_count = QueryHarmonia.fetch_match_transaction_count(
        TestTransactionMatchingContext.transaction_matching_id,
        (TestTransactionMatchingContext.transaction_matching_amount * 100),
    )
    assert matched_count.count == 1, f"Transaction didnt match and the status is '{matched_count.count}'"
    logging.info(f"The Transaction got matched : '{matched_count.count}'")


@then(parsers.parse("I verify transaction is not matched and not exported"))
def verify_transaction_not_matched():
    matched_count = QueryHarmonia.fetch_match_transaction_count(
        TestTransactionMatchingContext.transaction_matching_id,
        (TestTransactionMatchingContext.transaction_matching_amount * 100),
    )
    assert matched_count.count == 0, f"Transaction didnt match and the status is '{matched_count.count}'"
    logging.info(f" Transaction not matched and the status is not exported: '{matched_count.count}'")


@then(parsers.parse("I verify transaction is spotted and exported"))
def verify_spotted_transaction():
    spotted_transaction_count = QueryHarmonia.fetch_spotted_transaction_count(
        TestTransactionMatchingContext.transaction_id
    )
    assert spotted_transaction_count.count == 1, "Transaction not spotted and the status is not exported"
    logging.info(f"The Transaction got spotted and exported : '{spotted_transaction_count.count}'")


@then(parsers.parse('I verify "{payment_card_transaction}","{mid}" and "{auth_code}" is spotted and exported'))
def verify_spotted_mastercard_transaction(payment_card_transaction, mid, auth_code):
    if payment_card_transaction == "master-auth-spotting":
        t = TestTransactionMatchingContext.created_at
        form = "%Y-%m-%d %H:%M:%S"
        utc_time = datetime.strptime(t, form)
        created_at = utc_time.astimezone(pytz.UTC)
        logging.info(f"Transaction time: '{created_at}'")
        spotted_transaction_count = QueryHarmonia.fetch_mastercard_spotted_transaction_count(
            TestTransactionMatchingContext.spend_amount * 100, created_at)
        assert spotted_transaction_count.count == 1, "Transaction not spotted and the status is not exported"
        logging.info(f"The Transaction got spotted and exported : '{spotted_transaction_count.count}'")

    elif payment_card_transaction == "master-settlement-spotting":
        t = str(TestTransactionMatchingContext.created_at)
        form = '%Y-%m-%dT%H:%M:%S.%f%z'
        utc_time = datetime.strptime(t, form)
        created_at = utc_time.astimezone(pytz.UTC)
        logging.info(f"Transaction time: '{created_at}'")
        spotted_transaction_count = QueryHarmonia.fetch_mastercard_spotted_transaction_count(
            TestTransactionMatchingContext.spend_amount * 100, created_at)
        assert spotted_transaction_count.count == 1, "Transaction not spotted and the status is not exported"
        logging.info(f"The Transaction got spotted and exported : '{spotted_transaction_count.count}'")

    elif payment_card_transaction == "master-refund-spotting":
        t = str(TestTransactionMatchingContext.created_at)
        form = '%Y-%m-%dT%H:%M:%S.%f%z'
        utc_time = datetime.strptime(t, form)
        created_at = utc_time.astimezone(pytz.UTC)
        logging.info(f"Transaction time: '{created_at}'")
        spotted_transaction_count = QueryHarmonia.fetch_mastercard_spotted_transaction_count(
            TestTransactionMatchingContext.spend_amount * 100, created_at)
        assert spotted_transaction_count.count == 1, "Transaction not spotted and the status is not exported"
        logging.info(f"The Transaction got spotted and exported : '{spotted_transaction_count.count}'")

    else:
        spotted_transaction_count = QueryHarmonia.fetch_spotted_transaction_count(
            TestTransactionMatchingContext.transaction_id
        )
        assert spotted_transaction_count.count == 1, "Transaction not spotted and the status is not exported"
        logging.info(f"The Transaction got spotted and exported : '{spotted_transaction_count.count}'")


@then(parsers.parse("I verify transaction is not spotted and exported"))
def verify_transaction_not_spotted():
    spotted_transaction_count = QueryHarmonia.fetch_spotted_transaction_count(
        TestTransactionMatchingContext.transaction_id
    )
    assert spotted_transaction_count.count == 0, "The Transaction got spotted and exported"
    logging.info(f" Transaction not spotted and the status is not exported: '{spotted_transaction_count.count}'")


@when(parsers.parse('I perform POST request to add "{payment_card_provider}" payment card to wallet'))
def add_transaction_paymentCard(payment_card_provider):
    """Function call to get_membership_cards in test_membership_cards"""
    test_payment_cards.add_payment_card(payment_card_provider)


@when("I perform the GET request to verify the payment card has been added successfully to the wallet")
def get_transaction_paymentCard():
    test_payment_cards.verify_payment_card_added()


@when(parsers.parse('I perform POST request to add & auto link "{merchant}" membership card'))
def post_transaction_add_and_link(merchant):
    test_membership_cards.add_and_link_membership_card(merchant)


@then(
    parsers.parse(
        'I perform GET request to verify the "{merchant}" membershipcard is added & linked successfully '
        "in the wallet"
    )
)
def get_transaction_matching_add_and_link(merchant):
    test_membership_cards.verify_add_and_link_membership_card(merchant)


@when(
    parsers.parse(
        'I send merchant Tlog file with "{merchant_container}" '
        '"{payment_card_provider}" "{mid}" "{cardIdentity}" "{scheme}" and send to bink'
    )
)
def import_merchant_file(merchant_container, payment_card_provider, mid, cardIdentity, scheme):
    if merchant_container == "scheme/iceland/":
        buf = io.StringIO()
        merchant_writer = csv.writer(buf, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        merchant_writer.writerow(TestTransactionMatchingContext.iceland_file_header)
        getNewFileDataToImport()
        merchant_writer.writerow(
            [
                PaymentCardTestData.get_data(payment_card_provider).get(constants.FIRST_SIX_DIGITS),
                PaymentCardTestData.get_data(payment_card_provider).get(constants.LAST_FOUR_DIGITS),
                "01/80",
                "3",
                cardIdentity,
                mid,
                TestTransactionMatchingContext.transaction_matching_currentTimeStamp,
                TestTransactionMatchingContext.transaction_matching_amount,
                "GBP",
                ".00",
                "GBP",
                TestTransactionMatchingContext.transaction_matching_id,
                TestTransactionMatchingContext.transaction_matching_uuid,
            ]
        )
        bbs = BlobServiceClient.from_connection_string(BLOB_STORAGE_DSN)
        blob_client = bbs.get_blob_client(
            TestTransactionMatchingContext.container_name,
            merchant_container + f"{TestTransactionMatchingContext.file_name}",
        )
        blob_client.upload_blob(buf.getvalue().encode())

    elif merchant_container == "scheme/harvey-nichols/":
        json_file = json.dumps(
            harvey_nichols_transaction_matching_files.harvey_nichols_merchant_file(
                payment_card_provider=payment_card_provider, mid=mid, scheme=scheme
            )
        )
        file = json.loads(json_file)
        file_name = "harvey-nichols" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".json"
        bbs = BlobServiceClient.from_connection_string(BLOB_STORAGE_DSN)
        blob_client = bbs.get_blob_client(TestTransactionMatchingContext.container_name, merchant_container + file_name)
        blob_client.upload_blob(json.dumps(file, indent=2))
        logging.info(f" This is the Merchant file sent to blob storage  : '{json.dumps(file, indent=2)}'")


def getNewFileDataToImport():
    TestTransactionMatchingContext.transaction_matching_id = uuid.uuid4()
    TestTransactionMatchingContext.transaction_matching_uuid = random.randint(100000, 999999)
    TestTransactionMatchingContext.transaction_matching_amount = int(Decimal(str(random.choice(range(10, 1000)))))
    TestTransactionMatchingContext.transaction_matching_currentTimeStamp = datetime.now(
        timezone("Europe/London")
    ).strftime("%Y-%m-%d %H:%M:%S")
    TestTransactionMatchingContext.transaction_matching_amexTimeStamp = datetime.now(timezone("MST")).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    TestTransactionMatchingContext.file_name = "iceland-bonus-card" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv"
