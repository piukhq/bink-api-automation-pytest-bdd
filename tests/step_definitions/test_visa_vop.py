from pytest_bdd import (
    scenarios,
    then,
    when,
    parsers,
)
import logging
from tests.helpers.database.query_hermes import QueryHermes
from tests.helpers.test_context import TestContext
from tests.helpers.test_helpers import TestData
import tests.step_definitions.test_membership_cards as test_membership_cards
from tests.step_definitions import test_payment_cards

scenarios("vop/")

"""Step definitions - Add Payment Card """


@when('I perform POST request to add "<payment_card_provider>" payment card to wallet')
def add_transaction_paymentCard(payment_card_provider):
    """Function call to get_membership_cards in test_membership_cards"""
    test_payment_cards.add_payment_card(payment_card_provider)


@when("I perform the GET request to verify the payment card has been added successfully to the wallet")
def get_transaction_paymentCard():
    test_payment_cards.verify_payment_card_added()


@when(parsers.parse('I perform POST request to add & auto link "{merchant}" membership card'))
def post_add_and_link(merchant):
    """Function call to add_and_link in test_membership_cards"""
    test_membership_cards.add_and_link_membership_card(merchant)


@when(parsers.parse(
    'I perform GET request to verify the "{merchant}" membership card is added & linked successfully '
    "in the wallet")
)
def get_add_and_link(merchant):
    """Function call to get_membership_cards in test_membership_cards"""
    test_membership_cards.verify_add_and_link_membership_card(merchant)


@then(parsers.parse('I verify status of paymentcard is "{activated}" for "{merchant}"'))
def verify_vop_activation_details(activated, merchant):
    payment_account = QueryHermes.get_vop_status(TestContext.current_payment_card_id)
    assert payment_account.status == TestData.get_vop_status().get(activated), \
        f"Payment Account is not '{activated}' and the status is '{payment_account.status}'"
    logging.info(f"The payment card is '{activated}' with status '{payment_account.status}'")

    assert (payment_account.payment_card_account_id == TestContext.current_payment_card_id
            and payment_account.status == TestData.get_vop_status().get(activated)
            and payment_account.scheme_id == TestData.get_membership_plan_id(merchant)), \
        f"Details of payment card '{payment_account.payment_card_account_id}'in DB is not as expected"
