import io
import logging

from azure.storage.blob import BlobServiceClient

from settings import BLOB_STORAGE_DSN
from tests.helpers.test_transaction_matching_context import TestTransactionMatchingContext
from tests.payload.transaction_matching.transaction_matching_merchant_file import create_iceland_merchant_file_csv


def upload_retailer_file_into_blob(merchant_container, payment_card_provider, mid, card_identity):
    """StringIO creates a text stream using an in-memory text buffer."""
    output = io.StringIO()
    """change below code when more merchants are there to follow blob route.
    Below function will create the merchant csv file and assign it to the output_buffer"""
    create_iceland_merchant_file_csv(output, payment_card_provider, mid, card_identity)

    bbs = BlobServiceClient.from_connection_string(BLOB_STORAGE_DSN)
    blob_client = bbs.get_blob_client(
        TestTransactionMatchingContext.container_name,
        merchant_container + f"{TestTransactionMatchingContext.file_name}",
    )
    logging.info("The Merchant file is: \n" + output.getvalue())
    blob_client.upload_blob(output.getvalue().encode())
