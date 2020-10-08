from pytest_bdd import (
    scenarios,
    then,
    when,
    parsers,
)
import datetime
import pytest
import json
import logging
from requests.exceptions import HTTPError

import tests.api as api
import tests.helpers.constants as constants
from tests.api.base import Endpoint
from tests.helpers.test_helpers import TestData
from tests.helpers.test_context import TestContext
from tests.helpers.test_data_utils import TestDataUtils
from tests.helpers.test_helpers import PaymentCardTestData
from tests.requests.membership_cards import MembershipCards
from tests.requests.membership_transactions import MembershipTransactions
from tests.helpers.test_helpers import Merchant
from tests.helpers.database.query_hermes import QueryHermes

scenarios("membership_cards/")


def customer_can_add_membership_card():
    """Verify a customer can add membership card."""
    pass


@pytest.fixture(scope="session")
def context():
    return {}


"""Step definitions - Add Journey """


@when(parsers.parse('I perform POST request to add "{merchant}" membership card'))
def add_membership_card(merchant, login_user, context):
    context["token"] = login_user
    response = MembershipCards.add_card(context["token"], merchant)
    response_json = response.json()
    context["scheme_account_id"] = response_json.get("id")
    TestContext.set_scheme_account(context["scheme_account_id"])
    logging.info(
        "The response of Add Journey (POST) is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ADD)
    ), ("Add Journey for " + merchant + " failed")


@when(parsers.parse('I perform POST request to add "{merchant}" membership card with "{invalid_data}"'))
def add_invalid_membership_card(merchant, login_user, context, invalid_data):
    context["token"] = login_user
    response = MembershipCards.add_card(context["token"], merchant, invalid_data)
    response_json = response.json()
    context["scheme_account_id"] = response_json.get("id")
    TestContext.set_scheme_account(context["scheme_account_id"])
    logging.info("The response of Add Journey (POST) with Invalid data is:\n \n"
                 + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n"
                 + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ADD)
    ), ("Add Journey with invalid details for " + merchant + " failed")


@when(parsers.parse(
    'I perform POST request to add "{merchant}" membership card with invalid "{email_address} and "{password}"'
)
)
def add_membership_card_invalid_credentials(merchant, login_user, context, email_address, password):
    context["token"] = login_user
    response = MembershipCards.add_card(context["token"], merchant)
    response_json = response.json()
    context["scheme_account_id"] = response_json.get("id")
    TestContext.set_scheme_account(context["scheme_account_id"])
    logging.info("The response of Add Journey (POST) with Invalid data is:\n \n"
                 + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n"
                 + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ADD)
    ), ("Add Journey with invalid details for " + merchant + " failed")


@when(parsers.parse('I perform POST request to add & auto link an existing "{merchant}" membership card'))
def add_existing_membership_card(merchant, login_user, context):
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
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ADD)
    ), ("Add Journey -PATCH Request for " + merchant + " failed")


"""Step definitions - Enrol Journey """


@when(parsers.parse('I perform POST request to create a "{merchant}" membership account with enrol credentials'))
def enrol_membership_account(merchant, register_user, context, test_email, env, channel):
    context["token"] = register_user
    response = MembershipCards.enrol_customer(context["token"], merchant, test_email, env, channel)
    response_json = response.json()
    context["scheme_account_id"] = response_json.get("id")
    TestContext.set_scheme_account(context["scheme_account_id"])
    logging.info(
        "The response of Enrol Journey (POST) is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n" +
        json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ENROL)
    ), ("Enrol journey for " + merchant + " failed")


@when(parsers.parse(
    'I perform POST request to create a "{merchant}" membership account with "{invalid}" enrol credentials'
)
)
def enrol_membership_account_invalid_credentials(merchant, register_user, context, test_email, env, channel, invalid):
    context["token"] = register_user
    response = MembershipCards.enrol_customer(context["token"], merchant, test_email, env, channel, invalid)
    response_json = response.json()
    context["scheme_account_id"] = response_json.get("id")
    TestContext.set_scheme_account(context["scheme_account_id"])
    logging.info(
        "The response of Enrol Journey (POST) with Invalid data is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n" +
        json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ENROL)
    ), ("Enrol Journey with invalid details for " + merchant + " failed")


@when(parsers.parse('I perform PUT request to replace information of the enrolled "{merchant}" membership card'))
def put_request_to_replace_enrolled_membership_card_details(merchant, context, test_email):
    response = MembershipCards.put_enrol_customer(context["token"], context["scheme_account_id"],
                                                  merchant, test_email)
    response_json = response.json()
    logging.info(
        "The response of Enrol Journey (PUT) is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(context["scheme_account_id"]) + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ENROL)
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
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_AUTHORIZED)
            and response_json["card"]["membership_id"] == TestData.get_data(merchant).get(constants.CARD_NUM)
    ), ("Validations in GET/membership_cards for " + merchant + " failed with reason code " +
        response_json["status"]["reason_codes"][0])
    if merchant in ("HarveyNichols", "Iceland"):
        assert (response_json["card"]["barcode"] == TestData.get_data(merchant).get(constants.BARCODE)
                ), ("Barcode verification for " + merchant + " failed")


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
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_AUTHORIZED)
    ), ("Validations in GET/membership_cards for " + merchant + " failed")


@when(
    parsers.parse(
        'I perform GET request to verify the "{merchant}" membership card is added & linked successfully '
        "in the wallet"
    )
)
def verify_membership_card_is_add_and_linked(merchant, context):
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
                PaymentCardTestData.get_data().get(constants.ACTIVE_LINK)
                and payment_card_present == "yes"

        ), ("Validations in GET/membership_cards after AutoLink for " + merchant + "failed with reason code " +
            response_json["status"]["reason_codes"][0])
    except IndexError:
        raise Exception("PLL link for " + merchant + " failed and the payment array in the response is empty")
    except AssertionError as error:
        raise Exception("Add&Link Journey for " + merchant + " failed due to " + error.__str__())


@when(
    parsers.parse(
        'I perform GET request to verify the "{merchant}" membership card is added to the wallet with ' "invalid data"
    )
)
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
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_FAILED)
    ), ("Validations in GET/membership_cards with invalid data for  " + merchant + " failed with reason code" +
        response_json["status"]["reason_codes"][0])


@when(parsers.parse('I perform GET request to verify the "{merchant}" membership account is created with invalid data'))
def verify_invalid_membership_card_is_created(merchant, context):
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
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_FAILED_ENROL)
    ), ("Validations in GET/membership_cards with invalid data for  " + merchant + " failed with reason code" +
        response_json["status"]["reason_codes"][0])


@when(parsers.parse('I perform GET request to view balance for recently added "{merchant}" membership card'))
def verify_membership_card_balance(context, merchant):
    current_membership_card_response_array = MembershipCards.get_membership_card_balance(context["token"],
                                                                                         context["scheme_account_id"])
    logging.info(
        "The response of GET/MembershipCardBalances for the current membership card is : \n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_CHECK_MEMBERSHIP_CARDS_BALANCE + "\n\n"
        + json.dumps(current_membership_card_response_array, indent=4))
    assert (
            current_membership_card_response_array["id"] == context["scheme_account_id"]
            and current_membership_card_response_array["status"]["state"] ==
            TestData.get_membership_card_status_states().get(constants.AUTHORIZED)
            and current_membership_card_response_array["status"]["reason_codes"][0] ==
            TestData.get_membership_card_status_reason_codes().get(constants.REASON_CODE_AUTHORIZED)
            and current_membership_card_response_array["card"]["membership_id"] ==
            TestData.get_data(merchant).get(constants.CARD_NUM)
            and current_membership_card_response_array["balances"][0]["value"] ==
            TestData.get_data(merchant).get(constants.POINTS)
            and current_membership_card_response_array["balances"][0]["currency"] ==
            TestData.get_data(merchant).get(constants.CURRENCY)
            and current_membership_card_response_array["balances"][0]["description"] ==
            TestData.get_data(merchant).get(constants.DESCRIPTION)
    ), ("Validations in GET/membership_cards?balances for " + merchant + " failed with reason code" +
        current_membership_card_response_array["status"]["reason_codes"][0])


""""Step definitions for Membership_Transactions"""


@when(
    parsers.parse(
        'I perform GET request to view all transactions made using the recently added "{merchant}" membership card'
    )
)
def verify_membership_card_transactions(context, merchant):
    response = MembershipTransactions.get_all_membership_transactions(context["token"])
    response_json = response.json()
    logging.info(
        "The response of GET/MembershipTransactions:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_TRANSACTIONS + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
    ), "GET/ubiquity/membership_transactions is not working as expected"
    if response_json[0] == "[]":
        logging.info("There are no matched transactions")
    response = MembershipTransactions.get_membership_transactions(context["token"], context["scheme_account_id"])
    response_json = response.json()
    logging.info(
        "The response of GET/MembershipTransactions:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD_TRANSACTIONS.format(context["scheme_account_id"]) + "\n\n"
        + json.dumps(response_json, indent=4))
    if response_json[0] == "[]":
        logging.info("There are no matched transactions associated with " + merchant + " membership card: " +
                     TestData.get_data(merchant).get(constants.CARD_NUM))
    else:
        try:
            assert response.status_code == 200
            context["transaction_id"] = response_json[0].get("id")
        except IndexError:
            logging.info("Existing transactions associated with " + merchant + " membership card: " +
                         TestData.get_data(merchant).get(constants.CARD_NUM) + " are not populated the response of \n"
                         + Endpoint.BASE_URL +
                         api.ENDPOINT_MEMBERSHIP_CARD_TRANSACTIONS.format(context["scheme_account_id"]))
            raise Exception("Existing transactions associated with " + merchant + " membership card: " +
                            TestData.get_data(merchant).get(
                                constants.CARD_NUM) + " are not populated the response of \n"
                            + Endpoint.BASE_URL +
                            api.ENDPOINT_MEMBERSHIP_CARD_TRANSACTIONS.format(context["scheme_account_id"]))
        except AssertionError as error:
            logging.info("The response of " + Endpoint.BASE_URL +
                         api.ENDPOINT_MEMBERSHIP_CARD_TRANSACTIONS.format(context["scheme_account_id"]) +
                         " is not as expected")
            raise Exception("The response of " + Endpoint.BASE_URL +
                            api.ENDPOINT_MEMBERSHIP_CARD_TRANSACTIONS.format(context["scheme_account_id"]) +
                            " is not as expected. Error is " + error.__str__())


@then(
    parsers.parse(
        'I perform GET request to view a specific transaction made using the recently added "{merchant}"'
        ' membership card'
    )
)
def verify_membership_card_single_transaction_detail(context, merchant):
    response = MembershipTransactions.get_membership_card_single_transaction_detail(
        context["token"], context["transaction_id"])
    response_json = response.json()
    logging.info(
        "The response of GET/MembershipTransaction:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD_SINGLE_TRANSACTION.format(context["transaction_id"]) +
        "\n\n"
        + json.dumps(response_json, indent=4))
    if response_json == "[]":
        logging.info("There are no matched transactions associated with " + merchant + " membership card: " +
                     TestData.get_data(merchant).get(constants.CARD_NUM))
    else:
        assert (
                response.status_code == 200
                and response_json["id"] == context["transaction_id"]
                and response_json["status"] == TestData.get_data(merchant).get(constants.TRANSACTIONS_STATUS)
                and response_json["amounts"][0]["currency"] == TestData.get_data(merchant).
                get(constants.TRANSACTIONS_CURRENCY)
        ), ("Validations in GET/MembershipTransaction " + merchant + " failed")


"""Step definitions - DELETE Scheme Account """


@then(parsers.parse('I perform DELETE request to delete the "{merchant}" membership card'))
def perform_delete_request_scheme_account(context, merchant=None):
    response_del_schemes = MembershipCards.delete_scheme_account(context["token"], context["scheme_account_id"])
    try:
        if response_del_schemes.status_code == 200:
            logging.info("Scheme account is deleted successfully")
        elif response_del_schemes.status_code == 404:
            logging.info("Scheme account is not exist ")

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error("Scheme account deletion for ", merchant, "failed due to HTTP error: {network_response}")


"""Step definitions - DB Verifications"""


@then(parsers.parse('verify the data stored in DB after "{journey_type}" journey for "{merchant}"'))
def verify_db_details(journey_type, merchant, env):
    if env == "prod":
        """There is no DB validation in production suite"""
        pass

    elif env in ("dev", "staging"):

        scheme_account = QueryHermes.fetch_scheme_account(journey_type, TestContext.current_scheme_account_id)

        assert scheme_account.status == 1, f"Scheme Account is not Active and the status is '{scheme_account.status}'"
        logging.info(f"The scheme account is Active with status '{scheme_account.status}'")

        assert (scheme_account.id == TestContext.current_scheme_account_id
                and scheme_account.scheme_id == TestData.get_membership_plan_id(merchant)
                and scheme_account.link_or_join_date.date() == datetime.datetime.now().date()
                ), f"Details of scheme account '{scheme_account.id}'in DB is not as expected"

        """Below function call will display all Scheme account credential answers for Add & Enrol Journeys"""

        cred_ans = QueryHermes.fetch_credential_ans(merchant, TestContext.current_scheme_account_id)

        if journey_type == "Add":
            logging.info(f"The Link Date for scheme_account '{scheme_account.id}' is "
                         f"{scheme_account.link_or_join_date}'")

            assert (scheme_account.main_answer == Merchant.get_scheme_cred_main_ans(merchant)
                    ), "The Main Scheme Account answer is not saved as expected "

            """Verifying the request data is getting stored in DB after Add Journey """
            verify_scheme_account_ans(cred_ans, merchant)

        elif journey_type == "Enrol":
            logging.info(f"The Join Date for scheme_account '{scheme_account.id}' is "
                         f"{scheme_account.link_or_join_date}'")


def verify_scheme_account_ans(cred_ans, merchant):
    """For HN , BK, FF, WHsmith the  main scheme_account_ans is validated against
    'main_answer' column in scheme_schemeaccount table

    HN 'Password' scheme_account_ans is not validating as it has to remain as encrypted

    The remaining columns in scheme_schemeaccountcredentialanswers table are already validated
    as a part of the API response

    This function validates Iceland's  last_name & post_code and Wasabi's  email field in the request."""
    if merchant == "Iceland":
        assert (cred_ans.last_name == TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.LAST_NAME)
                and cred_ans.postcode == TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.POSTCODE)
                ), "Iceland scheme_account answers are not saved as expected"

    elif merchant == "Wasabi":
        assert (cred_ans.email == TestDataUtils.TEST_DATA.wasabi_membership_card.get(constants.EMAIL)
                ), "Wasabi scheme_account answers are not saved as expected"
