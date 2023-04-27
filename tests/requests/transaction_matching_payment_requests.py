import json
import logging
import os

from azure.storage.blob import ContentSettings
from azure.storage.blob import BlobServiceClient
import tests.api as api
from settings import BLOB_STORAGE_DSN
from tests.api.transactionmatching_base import TransactionMatchingEndpoint
from tests.helpers.test_transaction_matching_context import TestTransactionMatchingContext
from tests.api.base import Endpoint
from tests.payload.transaction_matching.transaction_matching_payment_file import TransactionMatchingPaymentFileDetails,\
    get_data_to_import


def import_visa_matching_auth_json(mid):
    """Import Visa Auth Matching Transactions"""
    get_data_to_import()
    url = get_visa_url()
    header = TransactionMatchingEndpoint.request_header_visa()
    payload = TransactionMatchingPaymentFileDetails.get_visa_auth_data(mid)
    response = Endpoint.call(url, header, "POST", payload)
    logging.info(json.dumps(payload, indent=4))
    return response


def import_visa_matching_settlement_json(mid):
    """Import Visa Settlement Matching Transactions"""

    get_data_to_import()
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
    merchant_container = "mastercard"
    file_name = (
        TransactionMatchingPaymentFileDetails.get_master_settlement_txt_file(mid)
    )
    logging.info(file_name)
    f = open(file_name.name, 'r')
    file_contents = f.read()
    logging.info("The MasterCard Settlement Matching file is: \n" + file_contents)
    upload_mastercard_settlement_file_into_blob(file_name, merchant_container, mid)


def upload_mastercard_settlement_file_into_blob(file_name, merchant_container, mid):
    """Upload master card settlement file (.csv) into blob storage"""
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


def get_amex_register_payment_json():
    """Get Amex Tokens for Importing Transactions"""

    get_data_to_import()
    url = get_amex_register_url()
    header = TransactionMatchingEndpoint.request_register_amex()
    payload = TransactionMatchingPaymentFileDetails.import_amex_auth_payment_card()
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


def get_master_spotting_auth_file(mid):
    get_data_to_import()
    url = get_mastrcard_url()
    header = TransactionMatchingEndpoint.request_header_mastercard()
    payload = TransactionMatchingPaymentFileDetails.import_spotting_master_auth_payment_card(mid)
    response = Endpoint.call(url, header, "POST", payload)
    print(json.dumps(payload, indent=4))
    return response


def get_visa_spotting_merchant_auth_file(mid):
    get_data_to_import()
    url = get_visa_url()
    header = TransactionMatchingEndpoint.request_header_visa()
    payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_merchant_auth_data(mid)
    response = Endpoint.call(url, header, "POST", payload)
    print(json.dumps(payload, indent=4))
    return response


def get_visa_spotting_auth_settlement_file(mid):
    get_data_to_import()
    url = get_visa_url()
    header = TransactionMatchingEndpoint.request_header_visa()
    payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_merchant_auth_data(mid)
    response = Endpoint.call(url, header, "POST", payload)
    logging.info((json.dumps(payload, indent=4)))
    print(response)
    url = get_visa_url()
    header = TransactionMatchingEndpoint.request_header_visa()
    payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_merchant_settlement_data(mid)
    response = Endpoint.call(url, header, "POST", payload)
    logging.info((json.dumps(payload, indent=4)))
    print(response)


def get_visa_spotting_merchant_settlement_file(mid):
    get_data_to_import()
    url = get_visa_url()
    header = TransactionMatchingEndpoint.request_header_visa()
    payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_merchant_settlement_data(mid)
    response = Endpoint.call(url, header, "POST", payload)
    print(json.dumps(payload, indent=4))
    return response


def get_visa_spotting_merchant_refund_file(mid):
    get_data_to_import()
    url = get_visa_url()
    header = TransactionMatchingEndpoint.request_header_visa()
    payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_merchant_refund_data(mid)
    response = Endpoint.call(url, header, "POST", payload)
    print(json.dumps(payload, indent=4))
    return response


def get_visa_spotting_merchant_refund_file_invalid_token(mid):
    url = get_visa_url()
    header = TransactionMatchingEndpoint.request_header_visa()
    payload = TransactionMatchingPaymentFileDetails.get_visa_spotting_merchant_auth_data_with_invalid_token(mid)
    response = Endpoint.call(url, header, "POST", payload)
    print(json.dumps(payload, indent=4))
    return response


def get_amex_auth_spotting_file(mid):
    get_amex_register_payment_json()
    url = TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL_ZEPHYRUS + api.ENDPOINT_AMEX_CARD
    headers = TransactionMatchingEndpoint.request_header_amex(TestTransactionMatchingContext.amex_token)
    payload = TransactionMatchingPaymentFileDetails.get_amex_auth_spotting_data(mid)
    logging.info(json.dumps(payload, indent=2))
    response = Endpoint.call(url, headers, "POST", payload)
    return response


def get_amex_settlement_spotting_file(mid):
    get_amex_register_payment_json()
    url = TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL_ZEPHYRUS + api.ENDPOINT_AMEX_SETTLEMENT_CARD
    headers = TransactionMatchingEndpoint.request_header_amex(TestTransactionMatchingContext.amex_token)
    payload = TransactionMatchingPaymentFileDetails.get_amex_settlement_spotting_data(mid)
    logging.info(json.dumps(payload, indent=2))
    response = Endpoint.call(url, headers, "POST", payload)
    return response


def get_amex_refund_spotting_file(mid):
    get_data_to_import()
    url = TransactionMatchingEndpoint.TRANSACTION_MATCHING_BASE_URL_ZEPHYRUS + api.ENDPOINT_AMEX_SETTLEMENT_CARD
    headers = TransactionMatchingEndpoint.request_header_amex(TestTransactionMatchingContext.amex_token)
    payload = TransactionMatchingPaymentFileDetails.get_amex_refund_spotting_data(mid)
    logging.info(json.dumps(payload, indent=2))
    response = Endpoint.call(url, headers, "POST", payload)
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
        case ["amex-auth-streaming", "amex-auth-spotting"]:
            return import_amex_matching_auth_json(mid)

# @staticmethod
# def exported_transaction(transaction_type):
#     """This function will return the exported transactions"""
#
#     match transaction_type:
#         case "visa-auth-spotting":
#             return QueryHarmonia.fetch_spotted_transaction_count(TestTransactionMatchingContext.transaction_id)
#         # case _ : return "default function"