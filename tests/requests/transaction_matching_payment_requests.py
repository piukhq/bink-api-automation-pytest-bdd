import json
import logging
import os
import time
from datetime import datetime


import pytz
from azure.storage.blob import ContentSettings
from azure.storage.blob import BlobServiceClient
import tests.api as api
from settings import BLOB_STORAGE_DSN
from tests.api.transactionmatching_base import TransactionMatchingEndpoint
from tests.helpers.database.query_harmonia import QueryHarmonia
from tests.helpers.test_transaction_matching_context import TestTransactionMatchingContext
from tests.api.base import Endpoint
from tests.payload.transaction_matching.transaction_matching_payment_file import (
    TransactionMatchingPaymentFileDetails,
    get_data_to_import,
)
import tests.payload.transaction_matching.transaction_matching_dedupe_payment_file as dedupe_payment_file


def import_visa_matching_auth_json(mid):
    """Import Visa Auth Matching Transactions"""
    url = get_visa_url()
    header = TransactionMatchingEndpoint.request_header_visa()
    payload = TransactionMatchingPaymentFileDetails.get_visa_auth_data(mid)
    response = Endpoint.call(url, header, "POST", payload)
    logging.info(json.dumps(payload, indent=4))
    return response


def import_visa_matching_settlement_json(mid):
    """Import Visa Settlement Matching Transactions"""

    url = get_visa_url()
    header = TransactionMatchingEndpoint.request_header_visa()
    payload = TransactionMatchingPaymentFileDetails.get_visa_settlement_data(mid)
    response = Endpoint.call(url, header, "POST", payload)
    print(json.dumps(payload, indent=4))
    return response


def import_master_matching_auth_json(mid):
    """Import Master Auth Matching Transactions"""

    url = get_mastrcard_url()
    header = TransactionMatchingEndpoint.request_header_mastercard()
    payload = TransactionMatchingPaymentFileDetails.get_mastercard_auth_data(mid)
    response = Endpoint.call(url, header, "POST", payload)
    print(json.dumps(payload, indent=4))
    return response


def import_master_matching_settlement_text(mid):
    """Import Master Settlement Matching Transactions in the text file to Harmonia"""
    file_name = TransactionMatchingPaymentFileDetails.get_master_settlement_txt_file(mid)
    upload_mastercard_settlement_file_into_blob(file_name, mid, "harmonia-imports/test/mastercard-settlement")


def upload_mastercard_settlement_file_into_blob(file_name, mid, path):
    """Pass the path inside the Harmonia import container
     for settlement and refund files to this function"""
    """Print the file content"""
    f = open(file_name.name, "r")
    file_contents = f.read()
    logging.info("The MasterCard Settlement Matching file is: \n" + file_contents)

    """Upload master card settlement file (.csv) into blob storage"""
    merchant_container = "mastercard"
    bbs = BlobServiceClient.from_connection_string(BLOB_STORAGE_DSN)
    blob_client = bbs.get_blob_client(
        path, merchant_container + f"{file_name.name}"
    )
    with open(file_name.name, "rb") as settlement_file:
        blob_client.upload_blob(settlement_file, content_settings=ContentSettings(content_type="text/plain"))
        logging.info(
            f"{file_name.name} has been uploaded to blob storage with spend_amount = "
            f"{TestTransactionMatchingContext.transaction_matching_amount} and MID = {mid}"
        )
        time.sleep(60)
        os.remove(file_name.name)


def get_amex_register_payment_json():
    """Get Amex Tokens for Importing Transactions"""

    url = get_amex_register_url()
    header = TransactionMatchingEndpoint.request_register_amex()
    payload = TransactionMatchingPaymentFileDetails.get_amex_register_token()
    response = Endpoint.call(url, header, "POST", payload)
    TestTransactionMatchingContext.amex_token = response.json().get("api_key")
    Endpoint.call(url, header, "POST", payload)


def import_amex_matching_auth_json(mid):
    """Import Amex Auth Matching Transactions"""
    get_amex_register_payment_json()
    url = TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL_ZEPHYRUS + api.ENDPOINT_AMEX_CARD
    headers = TransactionMatchingEndpoint.request_header_amex(TestTransactionMatchingContext.amex_token)
    payload = TransactionMatchingPaymentFileDetails.get_amex_auth_data(mid)
    logging.info(json.dumps(payload, indent=2))
    response = Endpoint.call(url, headers, "POST", payload)
    return response


def import_amex_matching_settlement_json(mid):
    """Import Amex Settlement Matching Transactions"""
    get_amex_register_payment_json()
    url = TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL_ZEPHYRUS + api.ENDPOINT_AMEX_SETTLEMENT_CARD
    headers = TransactionMatchingEndpoint.request_header_amex(TestTransactionMatchingContext.amex_token)
    payload = TransactionMatchingPaymentFileDetails.get_amex_settlement_data(mid)
    logging.info(json.dumps(payload, indent=2))
    response = Endpoint.call(url, headers, "POST", payload)
    return response


# *************************Spotting Streaming transactions*************************************************


def get_visa_spotting_streaming_auth_json(mid):
    """Import Visa Auth Streaming or Spotting Transactions"""

    url = get_visa_url()
    header = TransactionMatchingEndpoint.request_header_visa()
    payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_merchant_auth_data(mid)
    response = Endpoint.call(url, header, "POST", payload)
    logging.info("Visa Auth Streaming / Spotting json: \n\n" + json.dumps(payload, indent=4))
    return response


def verify_visa_spotting_streaming_auth_json_e2e(mid):
    """Import Visa auth Streaming or Spotting Transactions for E2E testing"""

    url = get_visa_url()
    header = TransactionMatchingEndpoint.request_header_visa()
    payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_merchant_auth_data(mid, "e2e")
    response = Endpoint.call(url, header, "POST", payload)
    logging.info("Visa Auth Streaming / Spotting json: \n\n" + json.dumps(payload, indent=4))
    return response


def get_visa_spotting_streaming_settlement_json(mid):
    """Import Visa Auth Streaming or Spotting Transactions"""
    get_data_to_import()
    url = get_visa_url()
    header = TransactionMatchingEndpoint.request_header_visa()
    payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_settlement_data(mid)
    response = Endpoint.call(url, header, "POST", payload)
    logging.info("Visa Settle Streaming / Spotting json: \n\n" + json.dumps(payload, indent=4))
    return response


def get_visa_spotting_streaming_settlement_json_e2e(mid):
    """Import Visa settelemet Streaming or Spotting Transactions for E2E testing"""

    get_data_to_import()
    url = get_visa_url()
    header = TransactionMatchingEndpoint.request_header_visa()
    payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_settlement_data(mid, "e2e")
    response = Endpoint.call(url, header, "POST", payload)
    logging.info("Visa Settle Streaming / Spotting json: \n\n" + json.dumps(payload, indent=4))
    return response


def get_visa_spotting_streaming_refund_json(mid):
    """Import Visa Refund Streaming or Spotting Transactions"""
    get_data_to_import()
    url = get_visa_url()
    header = TransactionMatchingEndpoint.request_header_visa()
    payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_refund_data(mid)
    response = Endpoint.call(url, header, "POST", payload)
    logging.info("Visa Refund Streaming / Spotting json: \n\n" + json.dumps(payload, indent=4))
    return response


def get_visa_spotting_streaming_refund_json_e2e(mid):
    """Import Visa Refund Streaming or Spotting Transactions for E2E testing"""

    get_data_to_import()
    url = get_visa_url()
    header = TransactionMatchingEndpoint.request_header_visa()
    payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_refund_data(mid, "e2e")
    response = Endpoint.call(url, header, "POST", payload)
    logging.info("Visa Refund Streaming / Spotting json: \n\n" + json.dumps(payload, indent=4))
    return response


def get_master_spotting_streaming_auth_json(mid):
    """Import master Auth Streaming or Spotting Transactions"""

    get_data_to_import()
    url = get_mastrcard_url()
    header = TransactionMatchingEndpoint.request_header_mastercard()
    payload = TransactionMatchingPaymentFileDetails.get_mastercard_auth_spotting_data(mid)
    response = Endpoint.call(url, header, "POST", payload)
    logging.info("Master Auth Streaming / Spotting json: \n\n" + json.dumps(payload, indent=4))
    return response


def import_master_spotting_streaming_settlement_text(mid):
    """Import Master Settlement/Spotting Settlement Transactions in the text file to Harmonia"""
    file_name = TransactionMatchingPaymentFileDetails.get_master_settlement_spotting_txt_file(mid)
    upload_mastercard_settlement_file_into_blob(file_name, mid, "harmonia-imports/test/mastercard-settlement")


def import_master_spotting_streaming_refund_text(mid):
    """Import Master spotting/ streaming refund  Transactions in the text file to Harmonia"""
    file_name = TransactionMatchingPaymentFileDetails.get_master_refund_spotting_txt_file(mid)
    upload_mastercard_settlement_file_into_blob(file_name, mid, "harmonia-imports/test/mastercard-refund")


def import_master_spotting_refund_the_works_text(mid):
    """Import Master spotting refund  Transactions file for merchant the-woks
    Unlike other merchant's master refund payment file, The-works master refund file contain
    transaction_id"""
    file_name = TransactionMatchingPaymentFileDetails.get_master_refund_spotting_txt_file_the_works(mid)
    upload_mastercard_settlement_file_into_blob(file_name, mid, "harmonia-imports/test/mastercard-refund")


def import_amex_spotting_streaming_auth_json(mid):
    """Import Amex Auth spotting / streaming file"""
    get_amex_register_payment_json()
    url = TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL_ZEPHYRUS + api.ENDPOINT_AMEX_CARD
    headers = TransactionMatchingEndpoint.request_header_amex(TestTransactionMatchingContext.amex_token)
    payload = TransactionMatchingPaymentFileDetails.get_amex_auth_spotting_data(mid)
    logging.info("Amex Auth Streaming / Spotting json: \n\n" + json.dumps(payload, indent=4))
    response = Endpoint.call(url, headers, "POST", payload)
    return response


def import_amex_spotting_streaming_settlement_json(mid):
    """Import Amex settlement spotting / streaming file"""
    get_amex_register_payment_json()
    url = TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL_ZEPHYRUS + api.ENDPOINT_AMEX_SETTLEMENT_CARD
    headers = TransactionMatchingEndpoint.request_header_amex(TestTransactionMatchingContext.amex_token)
    payload = TransactionMatchingPaymentFileDetails.get_amex_settlement_spotting_data(mid)
    logging.info("Amex Settle Streaming / Spotting json: \n\n" + json.dumps(payload, indent=4))
    response = Endpoint.call(url, headers, "POST", payload)
    return response


def import_amex_spotting_streaming_refund_json(mid):
    get_amex_register_payment_json()
    url = TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL_ZEPHYRUS + api.ENDPOINT_AMEX_SETTLEMENT_CARD
    headers = TransactionMatchingEndpoint.request_header_amex(TestTransactionMatchingContext.amex_token)
    payload = TransactionMatchingPaymentFileDetails.get_amex_refund_spotting_data(mid)
    logging.info("Amex Refund Streaming / Spotting json: \n\n" + json.dumps(payload, indent=4))
    response = Endpoint.call(url, headers, "POST", payload)
    return response


def get_visa_spotting_merchant_refund_file_invalid_token(mid):
    url = get_visa_url()
    header = TransactionMatchingEndpoint.request_header_visa()
    payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_merchant_auth_data_with_invalid_token(mid)
    response = Endpoint.call(url, header, "POST", payload)
    print(json.dumps(payload, indent=4))
    return response


def get_mastrcard_url():
    return TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL + api.ENDPOINT_MASTER_CARD


def get_amex_register_url():
    return TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL_ZEPHYRUS + api.ENDPOINT_AMEX_CARD_REGISTER


def get_visa_url():
    return TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL_ZEPHYRUS + api.ENDPOINT_VISA_CARD


def import_payment_file_into_harmonia(transaction_type, mid):
    """This function will decide which way( API, Blob storage etc.,) the Payment Transaction needs to be
    imported into Harmonia"""
    TestTransactionMatchingContext.mid = mid
    match transaction_type:
        case "visa-auth-matching":
            return import_visa_matching_auth_json(mid)
        case "visa-settlement-matching":
            return import_visa_matching_settlement_json(mid)
        case "master-auth-matching":
            return import_master_matching_auth_json(mid)
        case "master-settlement-matching":
            return import_master_matching_settlement_text(mid)
        case "amex-auth-matching":
            return import_amex_matching_auth_json(mid)
        case "amex-settlement-matching":
            return import_amex_matching_settlement_json(mid)
        case "visa-auth-streaming" | "visa-auth-spotting":
            return get_visa_spotting_streaming_auth_json(mid)
        case "visa-settlement-streaming" | "visa-settlement-spotting":
            return get_visa_spotting_streaming_settlement_json(mid)
        case "visa-refund-streaming" | "visa-refund-spotting":
            return get_visa_spotting_streaming_refund_json(mid)
        case "master-auth-streaming" | "master-auth-spotting":
            return get_master_spotting_streaming_auth_json(mid)
        case "master-settlement-streaming" | "master-settlement-spotting":
            return import_master_spotting_streaming_settlement_text(mid)
        case "master-refund-streaming" | "master-refund-spotting":
            return import_master_spotting_streaming_refund_text(mid)
        case "amex-auth-streaming" | "amex-auth-spotting":
            return import_amex_spotting_streaming_auth_json(mid)
        case "amex-settlement-streaming" | "amex-settlement-spotting":
            return import_amex_spotting_streaming_settlement_json(mid)
        case "amex-refund-streaming" | "amex-refund-spotting":
            return import_amex_spotting_streaming_refund_json(mid)
        case "visa-auth-spotting-e2e":
            return verify_visa_spotting_streaming_auth_json_e2e(mid)
        case "visa-settlement-spotting-e2e":
            return get_visa_spotting_streaming_settlement_json_e2e(mid)
        case "visa-refund-spotting-e2e":
            return get_visa_spotting_streaming_refund_json_e2e(mid)
        case "master-refund-spotting-the-works":
            return import_master_spotting_refund_the_works_text(mid)


def import_payment_file_with_duplicate_txn(transaction_type, mid):
    """Create a file with a transaction spend_amount and date same as a reflector transaction"""
    TestTransactionMatchingContext.mid = mid
    match transaction_type:
        case "visa-auth-spotting":
            return import_visa_auth_spotting_streaming_dedupe_json(mid)
        case "visa-settle-spotting":
            return import_visa_settle_spotting_streaming_dedupe_json(mid)
    #     case "visa-refund-spotting" | "visa-refund-streaming":
    #         return import_visa_refund_spotting_streaming_dedupe_json(mid)
    #     case "master-settle-spotting" | "master-settle-streaming":
    #         return import_master_settle_spotting_streaming_dedupe_text_file(mid)
    #     case "master-refund-spotting" | "master-refund-streaming":
    #         return import_master_refund_spotting_streaming_dedupe_text_file(mid)
    #     case "amex-settle-spotting" | "amex-settle-streaming":
    #         return import_amex_settle_spotting_streaming_dedupe_json(mid)
    #     case "amex-refund-spotting" | "amex-refund-streaming":
    #         return import_amex_refund_spotting_streaming_dedupe_json(mid)


def import_visa_settle_spotting_streaming_dedupe_json(mid):
    """Import Visa Auth spotting duplicate Transactions"""
    url = get_visa_url()
    header = TransactionMatchingEndpoint.request_header_visa()
    payload = dedupe_payment_file.import_visa_settle_matching_dedupe_json(mid)
    response = Endpoint.call(url, header, "POST", payload)
    logging.info("Visa Auth Spotting-Dedupe json:" + json.dumps(payload, indent=4))
    return response


def import_visa_auth_spotting_streaming_dedupe_json(mid):
    """Import Visa Auth spotting duplicate Transactions"""
    url = get_visa_url()
    header = TransactionMatchingEndpoint.request_header_visa()
    payload = dedupe_payment_file.import_visa_settle_matching_dedupe_json(mid)
    response = Endpoint.call(url, header, "POST", payload)
    logging.info("Visa Auth Spotting-Dedupe json:" + json.dumps(payload, indent=4))
    return response


def verify_exported_transaction(transaction_type):
    """This function will return the exported transactions"""
    match transaction_type:
        case "transaction_matching":
            return verify_matching_transactions()
        case "transaction-streaming" | "transaction-spotting":
            return verify_streaming_spotting_transactions()
        case "transaction-spotting-refund-the-works":
            return verify_the_works_master_spotting_refund_transactions()
        case "transaction-spotting-refund" | "transaction-streaming-refund":
            return verify_streaming_spotting_refund_transactions()


def verify_matching_transactions():
    """Check harmonia and verify exported transactions after Transaction Matching"""
    matched_count = QueryHarmonia.fetch_match_transaction_count(TestTransactionMatchingContext.retailer_transaction_id)
    assert matched_count.count == 1, f"Transaction didnt match and '{matched_count.count}' records exported"
    logging.info(f"No.of Transactions got matched is : '{matched_count.count}'")
    matched_transaction = QueryHarmonia.fetch_transaction_details(
        TestTransactionMatchingContext.retailer_transaction_id
    )
    return matched_transaction


def verify_streaming_spotting_transactions():
    """Check harmonia and verify exported transactions after Transaction Streaming or Spotting"""
    matched_count = QueryHarmonia.fetch_match_transaction_count(TestTransactionMatchingContext.transaction_id)
    assert matched_count.count == 1, "Transaction not spotted and the status is not exported"
    logging.info(f"No. of Transactions got spotted and exported : '{matched_count.count}'")
    matched_transaction = QueryHarmonia.fetch_transaction_details(TestTransactionMatchingContext.transaction_id)
    return matched_transaction


def verify_streaming_spotting_refund_transactions():
    """Check harmonia and verify exported refund transactions after Transaction Streaming or Spotting.
    Query harmonia using created date, amount and mid as transaction_id will be dynamically generated
    for refund transactions"""
    t = str(TestTransactionMatchingContext.created_at)
    form = '%Y-%m-%dT%H:%M:%S.%f%z'
    utc_time = datetime.strptime(t, form)
    created_at = utc_time.astimezone(pytz.UTC)
    matched_count = QueryHarmonia.fetch_match_refund_transaction_count(
            TestTransactionMatchingContext.transaction_matching_amount,
            TestTransactionMatchingContext.mid,
            created_at
    )
    assert matched_count.count == 1, "Transaction not spotted and the status is not exported"
    logging.info(f"No. of Refund Transactions got spotted and exported : '{matched_count.count}'")
    matched_transaction = QueryHarmonia.fetch_refund_transaction_details(
        TestTransactionMatchingContext.transaction_matching_amount,
        TestTransactionMatchingContext.mid,
        created_at
    )
    return matched_transaction


def verify_the_works_master_spotting_refund_transactions():
    """Merchant the works has transaction_id in mastercard refund file,
    which is same as transaction_id in settlement file. So need to fetch harmonia with
     transaction id & refund amount to get the unique record """
    matched_count = QueryHarmonia.fetch_match_transaction_count(
        TestTransactionMatchingContext.transaction_id,
        TestTransactionMatchingContext.transaction_matching_amount
    )
    assert matched_count.count == 1, "Transaction not spotted and the status is not exported"
    logging.info(f"No. of The woks refund Transactions got spotted and exported : '{matched_count.count}'")
    matched_transaction = QueryHarmonia.fetch_transaction_details(
        TestTransactionMatchingContext.transaction_id,
        TestTransactionMatchingContext.transaction_matching_amount
    )
    return matched_transaction


def verify_master_streaming_spotting_e2e_transactions():
    """Check harmonia and verify exported transactions after Transaction Streaming or Spotting"""
    matched_count = QueryHarmonia.fetch_match_transaction_count(TestTransactionMatchingContext.transaction_id)
    assert matched_count.count == 1, "Transaction not spotted and the status is not exported"
    logging.info(f"No. of Transactions got spotted and exported : '{matched_count.count}'")
    matched_transaction = QueryHarmonia.fetch_transaction_details(TestTransactionMatchingContext.transaction_id)
    return matched_transaction


def verify_deduped_transaction():
    """This function will return the exported transactions"""
    matched_count = QueryHarmonia.fetch_match_transaction_count(TestTransactionMatchingContext.transaction_id)
    assert matched_count.count == 1, "Transaction not spotted and the status is not exported"
    logging.info(f"No. of Transactions : '{matched_count.count}'")
    deduped_transaction = QueryHarmonia.fetch_dedupe_transaction_details(TestTransactionMatchingContext.transaction_id)
    return deduped_transaction
