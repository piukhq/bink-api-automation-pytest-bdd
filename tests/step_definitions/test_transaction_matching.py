from pytest_bdd import (
    scenarios,
    then,
    when,
    parsers,
)

import json
import logging
import time

from tests import api
from tests.api.base import Endpoint
from tests.helpers.database.query_harmonia import QueryHarmonia
import tests.step_definitions.test_payment_cards as test_payment_cards
from tests.helpers.test_context import TestContext
from tests.helpers.test_transaction_matching_context import TestTransactionMatchingContext
from tests.requests.membership_cards import MembershipCards
from tests.step_definitions import test_membership_cards
from tests.requests.transaction_matching_merchant_requests import upload_retailer_file_into_blob
from tests.requests.transaction_matching_payment_requests import (
    import_payment_file_into_harmonia,
    import_payment_file_with_duplicate_txn,
    verify_exported_transaction,
    verify_deduped_transaction,
)
from tests.step_definitions.test_membership_cards import response_to_json

scenarios("transaction_matching/")


@when(parsers.parse("I send Payment Transaction File with {payment_card_transaction} {mid}"))
@when(parsers.parse("I send Payment Transaction File with {payment_card_transaction} and MID as {mid}"))
def import_payment_file(payment_card_transaction, mid):
    TestTransactionMatchingContext.mid = mid
    response = import_payment_file_into_harmonia(payment_card_transaction, mid)
    logging.info("Waiting for transaction to be exported")
    try:
        response_json = response.json()
        logging.info("The response of POST/import Payment File is: \n\n" + json.dumps(response_json, indent=4))
        assert response.status_code == 201 or 200, "Payment file import is not successful"
        time.sleep(60)
    except AttributeError:
        if response is None:
            logging.info(
                "The Master Card Settlement Transaction Text file is uploaded to blob. "
                "Waiting for transaction to be exported"
            )


@when(parsers.parse("I send Payment File with a duplicate transaction using {payment_card_transaction} and {mid}"))
def import_payment_file_with_duplicate_transaction(payment_card_transaction, mid):
    TestTransactionMatchingContext.mid = mid
    response = import_payment_file_with_duplicate_txn(
        payment_card_transaction,
        mid,
    )
    try:
        response_json = response.json()
        logging.info("The response of POST/import Payment File is: \n\n" + json.dumps(response_json, indent=4))
        assert response.status_code == 201 or 200, "Payment file import is not successful"
        time.sleep(60)
    except AttributeError:
        if response is None:
            logging.info(
                "The Master Card Settlement Transaction Text file is uploaded to blob. "
                "Waiting for transaction to be exported"
            )


@then(parsers.parse("I verify the reward transaction is exported using {transaction_matching_logic}"))
def verify_exported_transactions(transaction_matching_logic):
    logging.info("Transaction Export:\n")
    matched_transaction = verify_exported_transaction(transaction_matching_logic)

    logging.info(
        "Details of the recent transaction in export_transaction table:\n\n"
        f"provider slug           : {matched_transaction.provider_slug}"
        + f"\ntransaction_date        : {matched_transaction.transaction_date.__str__()}"
        + f"\namount                  : {matched_transaction.spend_amount}"
        + f"\nloyalty_id              : {matched_transaction.loyalty_id}"
        + f"\nmid                     : {matched_transaction.mid}"
        + f"\nscheme_account_id       : {matched_transaction.scheme_account_id}"
        + f"\nstatus                  : {matched_transaction.status}"
        + f"\nfeed_type               : {matched_transaction.feed_type}"
        + f"\npayment_card_account_id : {matched_transaction.payment_card_account_id}"
        + f"\nauth_code               : {matched_transaction.auth_code}"
        + f"\napproval_code           : {matched_transaction.approval_code}"
        + f"\npayment_provider_slug   : {matched_transaction.payment_provider_slug}"
        + f"\nprimary_identifier      : {matched_transaction.primary_identifier}"
        + f"\nexport_uid              : {matched_transaction.export_uid}"
    )

    assert (
        matched_transaction.status == "EXPORTED"
        and matched_transaction.mid == TestTransactionMatchingContext.mid
        and matched_transaction.scheme_account_id == TestContext.current_scheme_account_id
    ), "Transaction is present in transaction_export table, but is not successfully exported"


"""clearing the values at the end of tests to support e2e tests"""
TestTransactionMatchingContext.transaction_id = ""
TestTransactionMatchingContext.spend_amount = " "


@then(parsers.parse("I verify the reward transaction is de-duplicated using dedupe and spotting"))
def verify_transaction_dedupe():
    logging.info("Transaction Export:\n")
    deduped_transaction = verify_deduped_transaction()
    logging.info(
        "Details of the recent transaction in export_transaction table:\n\n"
        f"\nstatus                  : {deduped_transaction.status}"
        + f"\nprovider slug           : {deduped_transaction.provider_slug}"
        + f"\ntransaction_date        : {deduped_transaction.transaction_date.__str__()}"
        + f"\namount                  : {deduped_transaction.spend_amount}"
        + f"\nloyalty_id              : {deduped_transaction.loyalty_id}"
        + f"\nmid                     : {deduped_transaction.mid}"
        + f"\nscheme_account_id       : {deduped_transaction.scheme_account_id}"
        + f"\nfeed_type               : {deduped_transaction.feed_type}"
        + f"\npayment_card_account_id : {deduped_transaction.payment_card_account_id}"
        + f"\nauth_code               : {deduped_transaction.auth_code}"
        + f"\napproval_code           : {deduped_transaction.approval_code}"
        + f"\npayment_provider_slug   : {deduped_transaction.payment_provider_slug}"
        + f"\nprimary_identifier      : {deduped_transaction.primary_identifier}"
        + f"\nexport_uid              : {deduped_transaction.export_uid}"
    )

    assert (
        deduped_transaction.status == "PENDING"
        and deduped_transaction.mid == TestTransactionMatchingContext.mid
        and deduped_transaction.scheme_account_id == TestContext.current_scheme_account_id
    ), "Transaction is present in transaction_export table, but is not successfully exported"


@then(parsers.parse("I verify transaction is not streamed and exported"))
@then(parsers.parse("I verify transaction is not spotted and exported"))
@then(parsers.parse("I verify transaction is not exported"))
def verify_transaction_not_matched():
    matched_count = QueryHarmonia.fetch_match_transaction_count_invalid_mid(
        TestTransactionMatchingContext.transaction_matching_id,
        (TestTransactionMatchingContext.transaction_matching_amount * 100),
    )
    assert matched_count.count == 0, (
        f"Transaction didn't match and the exported transaction count" f" is '{matched_count.count}'"
    )
    logging.info(f" Transaction not matched and the exported transaction count is'{matched_count.count}'")


@then(parsers.parse("I verify transaction is not streamed/spotted and exported"))
def verify_transaction_not_spotted():
    spotted_transaction_count = QueryHarmonia.fetch_spotted_transaction_count(
        TestTransactionMatchingContext.transaction_id
    )
    assert spotted_transaction_count.count == 0, "The Transaction got spotted and exported"
    logging.info(f" Transaction not spotted and the status is not exported: '{spotted_transaction_count.count}'")


@then(parsers.parse("I verify transaction is imported into the import_transaction table"))
def verify_transaction_is_imported():
    imported_transaction_count = QueryHarmonia.fetch_imported_transaction_count(
        TestTransactionMatchingContext.transaction_id
    )
    assert imported_transaction_count.count == 1, "The Transaction is not imported into the import_transaction table"
    logging.info(f" Transaction is imported into the import_transaction table: '{imported_transaction_count}'")


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


@when(parsers.parse("I perform POST request to add & auto link {merchant} membership card for {txn_matching_testing}"))
def transaction_add_and_link(merchant, txn_matching_testing):
    response = MembershipCards.add_card_auto_link(TestContext.token, merchant, txn_matching_testing)
    response_json = response_to_json(response)
    TestContext.current_scheme_account_id = response_json.get("id")
    TestContext.response = response
    logging.info(
        "The response of Add&Link Journey (POST) is:\n\n"
        + Endpoint.BASE_URL
        + api.ENDPOINT_AUTO_LINK_PAYMENT_AND_MEMBERSHIP_CARD
        + "\n\n"
        + json.dumps(response_json, indent=4)
    )


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
        "I send Retailer Transaction File with {merchant_container} " "{payment_card_provider} {mid} {card_identity}"
    )
)
def import_merchant_file(merchant_container, payment_card_provider, mid, card_identity):
    if merchant_container == "scheme/iceland/":
        upload_retailer_file_into_blob(merchant_container, payment_card_provider, mid, card_identity)
    elif merchant_container == "scheme/itsu/":
        upload_retailer_file_into_blob(merchant_container, payment_card_provider, mid, card_identity)
