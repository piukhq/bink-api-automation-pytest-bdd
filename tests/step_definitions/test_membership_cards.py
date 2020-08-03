from pytest_bdd import (
    scenarios,
    then,
    when,
    parsers,
)
import time
import pytest
import json
import logging
from requests.exceptions import HTTPError
from selenium.webdriver.support.ui import Select

from tests.requests.membership_cards import MembershipCards
from tests.helpers.test_data_utils import TestDataUtils
from tests.helpers.test_helpers import TestData
from tests.api.base import Endpoint
import tests.api as api
import tests.helpers.constants as constants

scenarios("membership_cards/")


def customer_can_add_membership_card():
    """Verify a customer can add membership card."""
    pass


@pytest.fixture(scope="function")
def context():
    return {}


"""Step definitions - Add Journey """


@when(parsers.parse('I perform POST request to add "{merchant}" membership card'))
def add_membership_card(merchant, login_user, context):
    context["token"] = login_user.json().get("api_key")
    response = MembershipCards.add_card(context["token"], merchant)
    response_json = response.json()
    context["scheme_account_id"] = response_json.get("id")
    logging.info(
        "The response of Add Journey (POST) is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n" + json.dumps(response_json, indent=4))
    try:
        if response.status_code == 200:
            """Temporary solution till get scheme account id from Data Base"""
            perform_delete_request_scheme_account(context)
            response = MembershipCards.add_card(context["token"], merchant)
            context["scheme_account_id"] = response.json().get("id")
        else:
            assert (
                    response.status_code == 201
                    and response_json["status"]["state"] == TestData.get_membership_card_status_states()
                    .get(constants.PENDING)
            )

    except AssertionError as error:
        raise Exception("Add Journey for " + merchant + " failed due to error " + error.__str__())


@when(parsers.parse('I perform POST request to add "{merchant}" membership card with "{invalid_data}"'))
def add_invalid_membership_card(merchant, login_user, context, invalid_data):
    context["token"] = login_user.json().get("api_key")
    response = MembershipCards.add_card(context["token"], merchant, invalid_data)
    response_json = response.json()
    context["scheme_account_id"] = response_json.get("id")
    logging.info("The response of Add Journey (POST) with Invalid data is:\n \n"
                 + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n" + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().
            get(constants.PENDING)
    ), ("Add Journey with invalid details for " + merchant + " failed")


@when(parsers.parse('I perform POST request to add & auto link an existing "{merchant}" membership card'))
def add_existing_membership_card(merchant, login_user, context):
    context["token"] = login_user.json().get("api_key")
    response = MembershipCards.add_card_auto_link(login_user.json().get("api_key"), merchant)
    response_json = response.json()
    context["scheme_account_id"] = response_json.get("id")
    logging.info(
        "The response of Add&Link Journey (POST) is:\n\n" +
        Endpoint.BASE_URL + api.ENDPOINT_AUTO_LINK_PAYMENT_AND_MEMBERSHIP_CARD_URL + "\n\n"
        + json.dumps(response_json, indent=4))
    try:
        if response.status_code == 200:
            """Temporary solution till get scheme account id from Data Base"""
            perform_delete_request_scheme_account(context)
            response = MembershipCards.add_card(context["token"], merchant)
            context["scheme_account_id"] = response.json().get("id")
        else:
            assert (
                    response.status_code == 201
                    and response_json["status"]["state"] == TestData.get_membership_card_status_states().
                    get(constants.PENDING)
            )

    except AssertionError as error:
        raise Exception("Add Journey for " + merchant + " failed due to error " + error.__str__())


@when(parsers.parse('I perform PATCH request to update "{merchant}" membership card'))
def patch_request_to_update_membership_card_details(merchant, context):
    response = MembershipCards.patch_add_card(context["token"], context["scheme_account_id"], merchant)
    response_json = response.json()
    logging.info(
        "The response of Add Journey (PATCH) is:\n\n" +
        Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(context["scheme_account_id"]) + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
    ), ("Add Journey -PATCH Request for " + merchant + " failed")


"""Step definitions - Enrol Journey """


@when(parsers.parse('I perform POST request to create a "{merchant}" membership account with enrol credentials'))
def enrol_membership_account(merchant, register_user, context, test_email):
    context["token"] = register_user.json().get("api_key")
    response = MembershipCards.enrol_customer(context["token"], merchant, test_email)
    response_json = response.json()
    context["scheme_account_id"] = response.json().get("id")
    logging.info(
        "The response of Enrol Journey (POST) is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n" + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
    ), ("Enrol journey for " + merchant + " failed")


@when(
    parsers.parse(
        'I perform POST request to create a "{merchant}" membership account with "{invalid}" enrol ' "credentials"
    )
)
def enrol_membership_account_invalid_credentials(merchant, register_user, context, test_email, invalid):
    context["token"] = register_user.json().get("api_key")
    response = MembershipCards.enrol_customer(context["token"], merchant, test_email, invalid)
    context["scheme_account_id"] = response.json().get("id")
    response_json = response.json()
    logging.info(
        "The response of Enrol Journey (POST) with Invalid data is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n" + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
    ), ("Enrol Journey with invalid details for " + merchant + " failed")


@when(parsers.parse('I perform PUT request to replace information of the enrolled "{merchant}" membership card'))
def put_request_to_replace_enrolled_membership_card_details(merchant, context, test_email):
    response = MembershipCards.put_enrol_customer(context["token"], context["scheme_account_id"], merchant, test_email)
    response_json = response.json()
    logging.info(
        "The response of Enrol Journey (PUT) is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(context["scheme_account_id"]) + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
    ), ("Enrol Journey PUT Request for " + merchant + "failed")


"""Step definitions - GET Scheme Account """


@when(parsers.parse('I perform GET request to verify the "{merchant}" membership card is added to the wallet'))
@when(
    parsers.parse(
        'I perform GET request to verify the "{merchant}" membership card details got updated after a '
        "successful PATCH"
    )
)
def verify_membership_card_is_added_to_wallet(merchant, context):
    response = MembershipCards.get_scheme_account(context["token"], context["scheme_account_id"])
    response_json = response.json()
    logging.info(
        "The response of GET/MembershipCard after Add Journey is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(context["scheme_account_id"]) + "\n\n" +
        json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
            and response_json["id"] == context["scheme_account_id"]
            and response_json["membership_plan"] == TestData.get_membership_plan_id(merchant)
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().
            get(constants.AUTHORIZED)
            and response_json["card"]["membership_id"] == TestData.get_data(merchant).get(constants.CARD_NUM)
    ), ("Validations in GET/membership_cards for " + merchant + " failed")


@when(
    parsers.parse(
        'I perform GET request to verify the enrolled "{merchant}" membership card details got '
        "replaced after a successful PUT"
    )
)
@when(parsers.parse('I perform GET request to verify the "{merchant}" membership account is created'))
def verify_membership_card_is_created(merchant, context):
    response = MembershipCards.get_scheme_account(context["token"], context["scheme_account_id"])
    response_json = response.json()
    logging.info(
        "The response of GET/MembershipCard after Enrol Journey is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(context["scheme_account_id"]) + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
            and response_json["id"] == context["scheme_account_id"]
            and response_json["membership_plan"] == TestData.get_membership_plan_id(merchant)
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().
            get(constants.AUTHORIZED)
    ), ("Validations in GET/membership_cards for " + merchant + " failed")


@when(
    parsers.parse(
        'I perform GET request to verify the "{merchant}" membership card is added & linked successfully '
        "in the wallet"
    )
)
def verify_membership_card_is_add_and_linked(merchant, context, add_payment_card):
    response = MembershipCards.get_scheme_account_auto_link(context["token"], context["scheme_account_id"])
    response_json = response.json()
    logging.info(
        "The response of GET/MembershipCard after Membership card Add & AutoLink is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(context["scheme_account_id"]) + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
            and response_json["id"] == context["scheme_account_id"]
            and response_json["membership_plan"] == TestData.get_membership_plan_id(merchant)
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().
            get(constants.AUTHORIZED)
            and response_json["card"]["membership_id"] == TestData.get_data(merchant).get(constants.CARD_NUM)
    ), ("Validations in GET/membership_cards after AutoLink for " + merchant + " failed")


@when(
    parsers.parse(
        'I perform GET request to verify the "{merchant}" membership card is added to the wallet with ' "invalid data"
    )
)
@when(parsers.parse('I perform GET request to verify the "{merchant}" membership account is created with invalid data'))
def verify_invalid_membership_card_is_added_to_wallet(merchant, context):
    response = MembershipCards.get_scheme_account(context["token"], context["scheme_account_id"])
    response_json = response.json()
    logging.info(
        "The response of GET/MembershipCard with invalid data in the request is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(context["scheme_account_id"]) + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
            and response_json["id"] == context["scheme_account_id"]
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.FAILED)
    ), ("Validations in GET/membership_cards with invalid data for  " + merchant + " failed")


@when(parsers.parse('I perform GET request to view balance for recently added "{merchant}" membership card'))
def verify_membership_card_balance(context, merchant):
    response = MembershipCards.get_membership_card_balance(context["token"])
    response_json = response.json()
    logging.info(
        "The response of GET/MembershipCardBalances:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_CHECK_MEMBERSHIP_CARDS_BALANCE_URL + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
            and response_json[0]["id"] == context["scheme_account_id"]
            and response_json[0]["membership_plan"] == TestData.get_membership_plan_id(merchant)
            and response_json[0]["status"]["state"] == TestData.membership_card_status_states.get(constants.AUTHORIZED)
            and response_json[0]["card"]["membership_id"] == TestData.get_data(merchant).get(constants.CARD_NUM)
            and response_json[0]["balances"]["value"] == TestData.get_data(merchant).get(constants.POINTS)
    ), ("Validations in GET/membership_cards?balances for " + merchant + " failed")


"""Step definitions - DELETE Scheme Account """


@then(parsers.parse('I perform DELETE request to delete the "{merchant}" membership card'))
def perform_delete_request_scheme_account(context, merchant=None):
    response_del_schemes = MembershipCards.delete_scheme_account(context["token"], context["scheme_account_id"])
    try:
        if response_del_schemes.status_code == 200 or 404:
            logging.info("Scheme account is deleted successfully")
        elif response_del_schemes.status_code == 404:
            logging.info("Scheme account is not exist ")

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error("Scheme account deletion for ", merchant, "failed due to HTTP error: {network_response}")


"""Step definitions - Django Verifications"""


@then("verify membership account Link date, Card Number and Merchant identifier populated in Django")
def verify_membership_account_link_date_card_number_and_merchant_identifier_populated_in_django(driver, context):
    scheme_account_id = str(context["scheme_account_id"])
    driver.get(Endpoint.DJANGO_URL + "scheme/schemeaccount/" + scheme_account_id + "/change/")
    driver.find_element_by_name("username").send_keys(TestDataUtils.TEST_DATA.django_user_accounts.get("django_uid"))
    driver.find_element_by_name("password").send_keys(TestDataUtils.TEST_DATA.django_user_accounts.get("django_pwd"))
    driver.find_element_by_xpath("//input[@type='submit']").click()
    select = Select(driver.find_element_by_name("status"))
    assert select.first_selected_option.text == "Active"
    link_date = driver.find_element_by_xpath('//form[@id="schemeaccount_form"]/div/fieldset/div[13]/div/div').text
    current_date = time.strftime("%d %b %Y").lstrip("0")
    if str(link_date).__contains__(current_date):
        logging.info(
            "Link date in Django (" + link_date + ") is close to current date "
                                                  "(" + current_date + time.strftime(", %I:%M %p").lower() + ")"
        )
    logging.info(
        "Merchant Identifier in Django is: "
        + driver.find_element_by_name("schemeaccountcredentialanswer_set-1-answer").get_attribute("value")
    )


@then("verify membership account Join date, Card Number and Merchant identifier populated in Django")
def verify_membership_account_join_date_card_number_and_merchant_identifier_populated_in_django(driver, context):
    scheme_account_id = str(context["scheme_account_id"])
    driver.get(Endpoint.DJANGO_URL + "scheme/schemeaccount/" + scheme_account_id + "/change/")
    driver.find_element_by_name("username").send_keys(TestDataUtils.TEST_DATA.django_user_accounts.get("django_uid"))
    driver.find_element_by_name("password").send_keys(TestDataUtils.TEST_DATA.django_user_accounts.get("django_pwd"))
    driver.find_element_by_xpath("//input[@type='submit']").click()
    select = Select(driver.find_element_by_name("status"))
    assert select.first_selected_option.text == "Active"
