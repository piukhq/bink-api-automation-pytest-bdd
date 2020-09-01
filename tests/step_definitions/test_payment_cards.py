from pytest_bdd import (
    scenarios,
    given,
    then,
    when,
    parsers,
)
import logging
import json
import tests.api as api

from requests.exceptions import HTTPError

from tests.requests.payment_cards import PaymentCards
from tests.api.base import Endpoint
import tests.helpers.constants as constants
from tests.helpers.test_helpers import TestData
from tests.helpers.test_context import TestContext
from tests.helpers.test_helpers import PaymentCardTestData
from tests.requests.membership_cards import MembershipCards

scenarios("payment_cards/")


def customer_can_add_payment_card():
    """Verify a customer can add payment card."""
    pass


"""Step definitions - Add Payment Card """


@given('I perform POST request to add "<payment_card_provider>" payment card to wallet')
def add_payment_card_specific_card_provider(login_user, context, test_email, payment_card_provider):
    context["token"] = login_user
    response = PaymentCards.add_payment_card(context["token"], test_email, payment_card_provider)
    response_json = response.json()
    logging.info("The response of POST/PaymentCard is: \n\n"
                 + Endpoint.BASE_URL + api.ENDPOINT_PAYMENT_CARDS + "\n\n"
                 + json.dumps(response_json, indent=4))
    context["payment_card_id"] = response_json.get("id")
    assert response.status_code == 201 or 200, "Payment card addition is not successful"
    return context["payment_card_id"]


@when(parsers.parse('I perform POST request to add & auto link an existing "{merchant}" membership card'))
def add_an_existing_membership_card(merchant, login_user, context):
    context["token"] = login_user
    response = MembershipCards.add_card_auto_link(context["token"], merchant)
    response_json = response.json()
    context["scheme_account_id"] = response_json.get("id")
    TestContext.set_scheme_account(context["scheme_account_id"])
    logging.info(
        "The response of Add&Link Journey (POST) is:\n\n" +
        Endpoint.BASE_URL + api.ENDPOINT_AUTO_LINK_PAYMENT_AND_MEMBERSHIP_CARD + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ADD)
    ), ("Add & Link Journey for " + merchant + " failed")


@when(
    parsers.parse(
        'I perform GET request to verify the "{merchant}" membership card is added & linked successfully '
        "in the wallet"
    )
)
def verify_membership_card_is_add_linked(merchant, context):
    response = MembershipCards.get_scheme_account_auto_link(context["token"], context["scheme_account_id"])
    response_json = response.json()
    logging.info(
        "The response of GET/MembershipCard after Membership card Add & AutoLink is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(context["scheme_account_id"]) + "\n\n"
        + json.dumps(response_json, indent=4))

    try:
        payment_card_present = "no"
        for current_payment_card in response_json["payment_cards"]:
            if current_payment_card["id"] == context["payment_card_id"]:
                payment_card_present = "yes"
        assert (
                response.status_code == 200
                and response_json["id"] == context["scheme_account_id"]
                and response_json["membership_plan"] == TestData.get_membership_plan_id(merchant)
                and response_json["status"]["state"] == TestData.get_membership_card_status_states().
                get(constants.AUTHORIZED)
                and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
                get(constants.REASON_CODE_AUTHORIZED)
                and response_json["card"]["membership_id"] == TestData.get_data(merchant).get(constants.CARD_NUM)
                and response_json["payment_cards"][0]["active_link"] ==
                # TestDataUtils.TEST_DATA.payment_card.get(constants.ACTIVE_LINK)
                PaymentCardTestData.get_data().get(constants.ACTIVE_LINK)
                and payment_card_present == "yes"

        ), ("Validations in GET/membership_cards after AutoLink for " + merchant + " failed")
    except IndexError:
        raise Exception("PLL link for " + merchant + " failed and the payment array in the response is empty")
    except AssertionError as error:
        raise Exception("Add&Link Journey for " + merchant + " failed due to " + error.__str__())


@then(parsers.parse('I perform DELETE request to delete the "{merchant}" membership card'))
def delete_request_scheme_account(context, merchant=None):
    response_del_schemes = MembershipCards.delete_scheme_account(context["token"], context["scheme_account_id"])
    try:
        if response_del_schemes.status_code == 200:
            logging.info("Scheme account is deleted successfully")
        elif response_del_schemes.status_code == 404:
            logging.info("Scheme account is not exist ")

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error("Scheme account deletion for ", merchant, "failed due to HTTP error: {network_response}")
