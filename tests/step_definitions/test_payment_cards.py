from pytest_bdd import (
    scenarios,
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
from json import JSONDecodeError
import tests.helpers.constants as constants
from tests.helpers.test_helpers import TestData
from tests.helpers.test_context import TestContext
from tests.helpers.test_helpers import PaymentCardTestData
from tests.requests.membership_cards import MembershipCards
import tests.step_definitions.test_membership_cards as membership_card_test

scenarios("payment_cards/")


"""Step definitions - Add Payment Card """


@when(parsers.parse('I perform POST request to add "{payment_card_provider}" payment card to wallet'))
def add_payment_card_specific_card_provider(add_payment_card):
    """Calling the common add payment card function in conftest"""


@when("I perform the GET request to verify the payment card has been added successfully to the wallet")
def get_payment_card(verify_payment_card_added):
    """Calling the common add payment card function in conftest"""


@when(parsers.parse('I perform POST request to add & auto link "{merchant}" membership card'))
def add_and_link(merchant):
    membership_card_test.add_and_link_membership_card(merchant)


@when(
    parsers.parse(
        'I perform GET request to verify the "{merchant}" membership card is added & linked successfully '
        "in the wallet"
    )
)
def verify_membership_card_is_add_linked(merchant):
    response = MembershipCards.get_scheme_account_auto_link(TestContext.token, TestContext.current_scheme_account_id)
    response_json = response_to_json(response)
    logging.info(
        "The response of GET/MembershipCard after Membership card Add & AutoLink is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.current_scheme_account_id) + "\n\n"
        + json.dumps(response_json, indent=4))

    try:
        payment_card_present = "no"
        for current_payment_card in response_json["payment_cards"]:
            if current_payment_card["id"] == TestContext.current_payment_card_id:
                payment_card_present = "yes"
        assert (
                response.status_code == 200
                and response_json["id"] == TestContext.current_scheme_account_id
                and response_json["membership_plan"] == TestData.get_membership_plan_id(merchant)
                and response_json["status"]["state"] == TestData.get_membership_card_status_states().
                get(constants.AUTHORIZED)
                and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
                get(constants.REASON_CODE_AUTHORIZED)
                and response_json["card"]["membership_id"] == TestData.get_data(merchant).get(constants.CARD_NUM)
                and response_json["payment_cards"][0]["active_link"] ==
                PaymentCardTestData.get_data().get(constants.ACTIVE_LINK)
                and payment_card_present == "yes"

        ), ("Validations in GET/membership_cards after AutoLink for " + merchant + " failed")
    except IndexError:
        raise Exception("PLL link for " + merchant + " failed and the payment array in the response is empty")
    except AssertionError as error:
        raise Exception("Add&Link Journey for " + merchant + " failed due to " + error.__str__())


@then(parsers.parse('I perform DELETE request to delete the "{merchant}" membership card'))
def delete_request_scheme_account(merchant=None):
    response_del_schemes = MembershipCards.delete_scheme_account(TestContext.token,
                                                                 TestContext.current_scheme_account_id)
    try:
        if response_del_schemes.status_code == 200:
            logging.info("Scheme account is deleted successfully")
        elif response_del_schemes.status_code == 404:
            logging.info("Scheme account is not exist ")

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error("Scheme account deletion for ", merchant, "failed due to HTTP error: {network_response}")


@when(parsers.parse('I perform POST request to add "{merchant}" membership card to my wallet'))
def add_membership_card_to_wallet(merchant):
    membership_card_test.add_membership_card(merchant)


@when(parsers.parse('I perform GET request to verify the "{merchant}" membership card is added to my wallet'))
def verify_membership_card_is_added_to_wallet(merchant):
    response = MembershipCards.get_scheme_account(TestContext.token, TestContext.current_scheme_account_id)
    response_json = response_to_json(response)
    logging.info(
        "The response of GET/MembershipCard after Add Journey is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.current_scheme_account_id) + "\n\n" +
        json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
            and response_json["id"] == TestContext.current_scheme_account_id
            and response_json["membership_plan"] == TestData.get_membership_plan_id(merchant)
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().
            get(constants.AUTHORIZED)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_AUTHORIZED)
            and response_json["card"]["membership_id"] == TestData.get_data(merchant).get(constants.CARD_NUM)
    ), ("Validations in GET/membership_cards for " + merchant + " failed with reason code " +
        response_json["status"]["reason_codes"][0])


@when("I perform PATCH request to link membership card to payment card")
def patch_mcard_pcard():
    response = PaymentCards.patch_mcard_pcard(TestContext.token,
                                              TestContext.current_scheme_account_id,
                                              TestContext.current_payment_card_id)
    response_json = response_to_json(response)

    logging.info(
        "The response of PATCH/membership_card/payment_card is :\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_PATCH_MEMBERSHIP_PAYMENT.format(TestContext.current_scheme_account_id,
                                                                           TestContext.current_payment_card_id) +
        "\n\n" + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201
            and response_json["id"] == TestContext.current_payment_card_id
            and response_json["membership_cards"][0]["active_link"]
            and response_json["membership_cards"][0]["id"] == TestContext.current_scheme_account_id
    ), "Validations in PATCH/membership_card/payment_card failed"


@when("I perform PATCH request to link payment card to membership card")
def patch_pcard_mcard():
    response = PaymentCards.patch_pcard_mcard(TestContext.token,
                                              TestContext.current_payment_card_id,
                                              TestContext.current_scheme_account_id
                                              )
    response_json = response_to_json(response)

    logging.info(
        "The response of PATCH/membership_card/payment_card is :\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_PATCH_PAYMENT_MEMBERSHIP.format(TestContext.current_payment_card_id,
                                                                           TestContext.current_scheme_account_id) +
        "\n\n" + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201
            and response_json["id"] == TestContext.current_scheme_account_id
            and response_json["payment_cards"][0]["active_link"]
            and response_json["payment_cards"][0]["id"] == TestContext.current_payment_card_id
    ), "Validations in PATCH/membership_card/payment_card failed"


@when("I perform GET membership_cards request to verify the membership card is linked successfully in the wallet")
def verify_mcard_link():
    response = PaymentCards.patch_pcard_mcard(TestContext.token,
                                              TestContext.current_payment_card_id,
                                              TestContext.current_scheme_account_id
                                              )
    response_json = response_to_json(response)

    logging.info(
        "The response of PATCH/membership_card/payment_card is :\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_PATCH_PAYMENT_MEMBERSHIP.format(TestContext.current_payment_card_id,
                                                                           TestContext.current_scheme_account_id) +
        "\n\n" + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201
            and response_json["id"] == TestContext.current_scheme_account_id
            and response_json["payment_cards"][0]["active_link"]
            and response_json["payment_cards"][0]["id"] == TestContext.current_payment_card_id
    ), "Validations in PATCH/membership_card/payment_card failed"


def response_to_json(response):
    try:
        response_json = response.json()
    except JSONDecodeError or Exception:
        raise Exception(f"Empty response and the response Status Code is {str(response.status_code)}")
    return response_json
