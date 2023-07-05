import json
import logging
import time
from json import JSONDecodeError

from pytest_bdd import parsers, scenarios, then, when

import tests.api as api
import tests.helpers.constants as constants
from tests.api.base import Endpoint
from tests.helpers.test_context import TestContext
from tests.helpers.test_data_utils import TestDataUtils
from tests.helpers.test_helpers import PaymentCardTestData, TestData
from tests.requests.membership_cards import MembershipCards
from tests.requests.membership_transactions import MembershipTransactions
from tests.requests.payment_cards import PaymentCards
from tests.step_definitions import test_membership_cards

scenarios("membership_cards_multi_wallet/")


"""Step definitions - Multi-wallet"""

"""This step is created as part of Trusted channel work and will be used mainly for multi-wallet scenarios."""


@when(parsers.parse('I perform POST request to add and auth "{merchant}" membership card with "{credentials}"'))
def add_auth_membership_card(merchant, credentials):
    if credentials == "valid_credentials":
        response = MembershipCards.add_card(TestContext.token, merchant)
    elif credentials == "valid_credentials2":
        response = MembershipCards.add_card2(TestContext.token, merchant)
    elif credentials == "invalid_credentials2":
        response = MembershipCards.add_card2(TestContext.token, merchant, credentials)
    elif credentials == "invalid_credentials":
        response = MembershipCards.add_card(TestContext.token, merchant, credentials)
    response_json = response_to_json(response)
    TestContext.current_scheme_account_id = response_json.get("id")
    logging.info(
        "The response of Add Journey (POST) is:\n\n"
        + Endpoint.BASE_URL
        + api.ENDPOINT_MEMBERSHIP_CARDS
        + "\n\n"
        + json.dumps(response_json, indent=4)
    )
    assert response.status_code == 201 or 200


"""This step is created as part of Trusted channel work and will be used mainly for multi-wallet scenarios."""


@when(parsers.parse('I perform POST request to add "{merchant}" membership card for "{scheme_status}"'))
def add_only_membership_card(merchant, scheme_status):
    response = MembershipCards.add_auth_card(TestContext.token, merchant)
    response_json = response_to_json(response)
    TestContext.current_scheme_account_id = response_json.get("id")
    logging.info(
        "The response of Add only (POST) is:"
        + Endpoint.BASE_URL
        + api.ENDPOINT_MEMBERSHIP_CARDS
        + "\n\n"
        + json.dumps(response_json, indent=4)
    )
    assert (
        response.status_code == 201
        or response.status_code == 200
        and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.UNAUTHORIZED)
        and response_json["status"]["reason_codes"][0]
        == TestData.get_membership_card_status_reason_codes().get(constants.REASON_CODE_UNAUTHORIZED)
    ), ("Add Ghost Journey for " + merchant + " failed")


"""Step definitions - Enrol Journey - Copy of existing step defination in test_membership_cards.
It is required in multi-wallet trusted channel scenarios"""


@when(parsers.parse("I perform POST request to {enrol_status} membership card for {merchant}"))
def enrol_membership_card_account(enrol_status, merchant, test_email, env, channel):
    response = MembershipCards.enrol_membership_card(
        TestContext.token, enrol_status, merchant, test_email, env, channel
    )
    response_json = response_to_json(response)
    TestContext.current_scheme_account_id = response_json.get("id")
    logging.info(
        "The response of Enrol Journey (POST) is:\n\n"
        + Endpoint.BASE_URL
        + api.ENDPOINT_MEMBERSHIP_CARDS
        + "\n\n"
        + json.dumps(response_json, indent=4)
    )
    assert (
        response.status_code == 201
        and response_json["membership_plan"] == TestData.get_membership_plan_id(merchant)
        and response_json["payment_cards"] == []
        and response_json["membership_transactions"] == []
        and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
        and response_json["status"]["reason_codes"][0]
        == TestData.get_membership_card_status_reason_codes().get(constants.REASON_CODE_PENDING_ENROL)
        and response_json["card"] is not None
        and response_json["images"] is not None
        and response_json["account"]["tier"] == 0
        and response_json["balances"] == []
    ), ("Enrol journey for " + merchant + " failed")


"""Step Definations - Register ghost membership_card- Copy of existing step defination in test_membership_cards.
It is required in multi-wallet trusted channel scenarios"""


@when(parsers.parse('I perform PATCH request to create a "{merchant}" ghost membership account with enrol credentials'))
def register_ghost_membership_account(merchant, test_email, env, channel):
    test_membership_cards.register_ghost_membership_account(merchant, test_email, env, channel)


"""This step is created as part of Trusted channel work and will be used mainly for multi-wallet scenarios."""


@when(parsers.parse('I perform PATCH request to create "{merchant}" "{scheme_status}"'))
def register_fail(merchant, test_email, env, channel, scheme_status):
    if scheme_status == "failed_register":
        test_email = TestDataUtils.TEST_DATA.iceland_ghost_membership_card.get(constants.REGISTER_FAILED_EMAIL)
    response = MembershipCards.register_ghost_card(
        TestContext.token, merchant, test_email, TestContext.current_scheme_account_id, env, channel, scheme_status
    )
    response_json = response_to_json(response)
    TestContext.current_scheme_account_id = response_json.get("id")
    logging.info(
        "The response of Register ghost Journey (PATCH) is:\n\n"
        + Endpoint.BASE_URL
        + api.ENDPOINT_MEMBERSHIP_CARDS.format(TestContext.current_scheme_account_id)
        + "\n\n"
        + json.dumps(response_json, indent=4)
    )
    assert (
        response.status_code == 200
        and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
        and response_json["status"]["reason_codes"][0]
        == TestData.get_membership_card_status_reason_codes().get(constants.REASON_CODE_PENDING_ENROL)
    ), ("Enrol journey for " + merchant + " failed")


"""Step definitions - GET Scheme Account """

"""This step is created as part of Trusted channel work and will be used mainly for multi-wallet scenarios."""

"""pll will show in API response based on global variable regardless of membership card status.
This part needs to be reviewed after TC changes are ready in staging"""


@when(
    parsers.parse(
        "For {user} I perform GET request to verify the {merchant} membership card is added to the wallet"
        " after {scheme_status}"
    )
)
def get_membership_card(user, merchant, scheme_status):
    print("TestContext.all_users", TestContext.all_users)
    TestContext.token = TestContext.all_users[user]
    response = MembershipCards.get_scheme_account(TestContext.token, TestContext.current_scheme_account_id)
    time.sleep(15)
    response = MembershipCards.get_scheme_account(TestContext.token, TestContext.current_scheme_account_id)
    TestContext.response = response
    response_json = response_to_json(response)
    logging.info(
        "The response of GET/MembershipCard/id is:\n\n"
        + Endpoint.BASE_URL
        + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.current_scheme_account_id)
        + "\n\n"
        + json.dumps(response_json, indent=4)
    )
    assert (
        response.status_code == 200
        and response_json["id"] == TestContext.current_scheme_account_id
        and response_json["membership_plan"] == TestData.get_membership_plan_id(merchant)
        and response_json["card"] != []
        and response_json["images"] != []
        and ((response_json["account"]["tier"] == 0) or (response_json["account"]["tier"] == 1))
    ), (
        "Validations in GET/membership_cards for "
        + merchant
        + " failed with reason code "
        + response_json["status"]["reason_codes"][0]
    )
    if scheme_status == "successful_add":
        assert response_json["card"]["membership_id"] == TestData.get_data(merchant).get(
            constants.CARD_NUM
        ), "membership_id do not match"
    elif scheme_status == "successful_add2":
        assert response_json["card"]["membership_id"] == TestData.get_data(merchant).get(
            constants.CARD_NUM2
        ), "membership_id do not match"
    if scheme_status in ["successful_add", "successful_enrol", "successful_register"]:
        TestContext.existing_card = response_json["card"]["membership_id"]
        assert response_json["status"]["state"] == TestData.get_membership_card_status_states().get(
            constants.AUTHORIZED
        ), "state does not match"
        assert response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().get(
            constants.REASON_CODE_AUTHORIZED
        ), "reason code does not match"
        assert response_json["balances"] != [], "balances does not match"
        if merchant == "Iceland":
            assert (
                response_json["card"]["barcode"] == TestData.get_data(merchant).get(constants.BARCODE)
                or response_json["card"]["barcode"] == TestContext.existing_card + "0080"
            ), ("Barcode verification for " + merchant + " failed")
    elif scheme_status == "identical_enrol":
        assert response_json["status"]["state"] == TestData.get_membership_card_status_states().get(
            constants.FAILED
        ), "state do not match"
        assert response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().get(
            constants.REASON_CODE_FAILED_INVALID_ENROL
        ), "reason code does not match"
        assert response_json["balances"] == [], "balances does not match"
    elif scheme_status == "successful_pll":
        assert response_json["payment_cards"][0]["id"] == TestContext.current_payment_card_id, "pll link does not match"
        assert response_json["payment_cards"][0]["active_link"] == PaymentCardTestData.get_data().get(
            constants.ACTIVE_LINK
        ), "active_link does not match"
    elif scheme_status == "failed_pll":
        assert response_json["payment_cards"] == [], "pll link does not match"

    return response


"""This step is created as part of Trusted channel work and will be used mainly for multi-wallet scenarios."""


@when(
    parsers.parse(
        "For {user} I perform GET request to verify the {merchant} "
        "membership card is added to the wallet with "
        "invalid data"
    )
)
def invalid_membership_card_is_added_to_wallet(user, merchant):
    TestContext.token = TestContext.all_users[user]
    response = MembershipCards.get_scheme_account(TestContext.token, TestContext.current_scheme_account_id)
    response_json = response_to_json(response)
    logging.info(
        "The response of GET/MembershipCard with invalid data in the request is:\n\n"
        + Endpoint.BASE_URL
        + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.current_scheme_account_id)
        + "\n\n"
        + json.dumps(response_json, indent=4)
    )
    if merchant != "SquareMeal":
        TestContext.existing_card = response_json["card"]["membership_id"]
    assert (
        response.status_code == 200
        and response_json["id"] == TestContext.current_scheme_account_id
        and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.FAILED)
        and (
            response_json["status"]["reason_codes"][0]
            == TestData.get_membership_card_status_reason_codes().get(constants.REASON_CODE_FAILED)
            or response_json["status"]["reason_codes"][0]
            == TestData.get_membership_card_status_reason_codes().get(constants.REASON_CODE_ADD_FAILED)
            or response_json["status"]["reason_codes"][0]
            == TestData.get_membership_card_status_reason_codes().get(constants.REASON_CODE_GHOST_FAILED)
        )
    ), (
        "Validations in GET/membership_cards with invalid data for  "
        + merchant
        + " failed with reason code"
        + response_json["status"]["reason_codes"][0]
    )


"""This step is created as part of Trusted channel work and will be used mainly for multi-wallet scenarios."""


@when(
    parsers.parse(
        "For {user} I perform GET request to view balance for " '"{loyalty_card_status}" "{merchant}" membership card'
    )
)
def membership_card_balance(user, loyalty_card_status, merchant):
    TestContext.token = TestContext.all_users[user]
    current_membership_card_response_array = MembershipCards.get_membership_card_balance(
        TestContext.token, TestContext.current_scheme_account_id
    )
    logging.info(
        "The response of GET/MembershipCardBalances for the current membership card is : \n\n"
        + Endpoint.BASE_URL
        + api.ENDPOINT_CHECK_MEMBERSHIP_CARDS_BALANCE
        + "\n\n"
        + json.dumps(current_membership_card_response_array, indent=4)
    )
    if loyalty_card_status in ["authorised", "authorised2"]:
        assert (
            current_membership_card_response_array["id"] == TestContext.current_scheme_account_id
        ), "id does not match"
        assert current_membership_card_response_array["status"][
            "state"
        ] == TestData.get_membership_card_status_states().get(constants.AUTHORIZED), "status_state does not match"

        assert current_membership_card_response_array["status"]["reason_codes"][
            0
        ] == TestData.get_membership_card_status_reason_codes().get(
            constants.REASON_CODE_AUTHORIZED
        ), "status_reason_code does not match"
        assert current_membership_card_response_array["balances"][0]["currency"] == TestData.get_data(merchant).get(
            constants.CURRENCY
        ), "balance currency does not match"
        if loyalty_card_status == "authorised":
            assert current_membership_card_response_array["card"]["membership_id"] == TestData.get_data(merchant).get(
                constants.CARD_NUM
            ), "card num does not match"
            assert current_membership_card_response_array["balances"][0]["value"] == TestData.get_data(merchant).get(
                constants.POINTS
            ), "balance value does not match"
        elif loyalty_card_status == "authorised2":
            assert current_membership_card_response_array["card"]["membership_id"] == TestData.get_data(merchant).get(
                constants.CARD_NUM2
            ), "card num does not match"
    elif loyalty_card_status in ["unauthorised", "unauthorised2"]:
        assert (
            current_membership_card_response_array["id"] == TestContext.current_scheme_account_id
        ), "id does not match"
        assert current_membership_card_response_array["status"][
            "state"
        ] == TestData.get_membership_card_status_states().get(constants.FAILED), "status_state does not match"
        assert current_membership_card_response_array["status"]["reason_codes"][
            0
        ] == TestData.get_membership_card_status_reason_codes().get(
            constants.REASON_CODE_ADD_FAILED
        ) or current_membership_card_response_array[
            "status"
        ][
            "reason_codes"
        ][
            0
        ] == TestData.get_membership_card_status_reason_codes().get(
            constants.REASON_CODE_FAILED
        ), "status_reason_code does not match"
        assert current_membership_card_response_array["balances"] == [], "balance does not match"
        if loyalty_card_status == "unauthorised" and merchant != "SquareMeal":
            assert current_membership_card_response_array["card"]["membership_id"] == TestData.get_data(merchant).get(
                constants.CARD_NUM
            ), "card num does not match"
        elif loyalty_card_status == "unauthorised2":
            assert current_membership_card_response_array["card"]["membership_id"] == TestData.get_data(merchant).get(
                constants.CARD_NUM2
            ), "card num does not match"


""""Step definitions for Membership_Transactions"""

"""This step is created as part of Trusted channel work and will be used mainly for multi-wallet scenarios."""


@when(
    parsers.parse(
        'For {user} I perform GET request to view transactions for "{loyalty_card_status}" "{merchant}" membership card'
    )
)
def membership_card_transactions(user, loyalty_card_status, merchant):
    TestContext.token = TestContext.all_users[user]
    if loyalty_card_status == "authorised":
        response = MembershipTransactions.get_membership_transactions(
            TestContext.token, TestContext.current_scheme_account_id
        )
        response_json = response_to_json(response)
        logging.info(
            "The response of GET/MembershipTransactions:\n\n"
            + Endpoint.BASE_URL
            + api.ENDPOINT_MEMBERSHIP_CARD_TRANSACTIONS.format(TestContext.current_scheme_account_id)
            + "\n\n"
            + json.dumps(response_json, indent=4)
        )
        if response_json[0] == []:
            logging.info(
                "There are no matched transactions associated with "
                + merchant
                + " membership card: "
                + TestData.get_data(merchant).get(constants.CARD_NUM)
            )
        else:
            try:
                assert response.status_code == 200
                TestContext.transaction_id = response_json[0].get("id")
            except IndexError:
                raise Exception(
                    "Existing transactions associated with "
                    + merchant
                    + " membership card: "
                    + TestData.get_data(merchant).get(constants.CARD_NUM)
                    + " are not populated the response of \n"
                    + Endpoint.BASE_URL
                    + api.ENDPOINT_MEMBERSHIP_CARD_TRANSACTIONS.format(TestContext.current_scheme_account_id)
                )
            except AssertionError as error:
                raise Exception(
                    "The response of "
                    + Endpoint.BASE_URL
                    + api.ENDPOINT_MEMBERSHIP_CARD_TRANSACTIONS.format(TestContext.current_scheme_account_id)
                    + " is not as expected. Error is "
                    + error.__str__()
                )
    elif loyalty_card_status == "authorised2":
        response = MembershipTransactions.get_membership_transactions(
            TestContext.token, TestContext.current_scheme_account_id
        )
        response_json = response_to_json(response)
        assert response_json[0] != [], "empty transactions are not expected"
    elif loyalty_card_status == "unauthorised":
        url = Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD_TRANSACTIONS.format(
            TestContext.current_scheme_account_id
        )
        header = Endpoint.request_header(TestContext.token)
        response = Endpoint.call(url, header, "GET")
        response_json = response.json()
        assert response_json == [], "transaction info should not be available for unauthorised card"


"""This step is created as part of Trusted channel work and will be used mainly for multi-wallet scenarios."""


@then(
    parsers.parse(
        "For {user} I perform GET request to view a specific transaction "
        'for "{loyalty_card_status}" "{merchant}" membership card'
    )
)
def membership_card_single_transaction_detail(user, loyalty_card_status, merchant):
    TestContext.token = TestContext.all_users[user]
    response = MembershipTransactions.get_membership_card_single_transaction_detail(
        TestContext.token, TestContext.transaction_id
    )
    response_json = response_to_json(response)
    logging.info(
        "The response of GET/MembershipTransaction:\n\n"
        + Endpoint.BASE_URL
        + api.ENDPOINT_MEMBERSHIP_CARD_SINGLE_TRANSACTION.format(TestContext.transaction_id)
        + "\n\n"
        + json.dumps(response_json, indent=4)
    )
    if response_json == "[]":
        logging.info(
            "There are no matched transactions associated with "
            + merchant
            + " membership card: "
            + TestData.get_data(merchant).get(constants.CARD_NUM)
        )
    else:
        assert (
            response.status_code == 200
            and response_json["id"] == TestContext.transaction_id
            and response_json["status"] == TestData.get_data(merchant).get(constants.TRANSACTIONS_STATUS)
            and response_json["amounts"][0]["currency"]
            == TestData.get_data(merchant).get(constants.TRANSACTIONS_CURRENCY)
        ), ("Validations in GET/MembershipTransaction " + merchant + " failed")


"""Step definitions - DB Verifications"""


@then(parsers.parse('verify the data stored in DB after "{journey_type}" journey for "{merchant}"'))
def verify_db_details(journey_type, merchant, env):
    test_membership_cards.verify_db_details(journey_type, merchant, env)


"""Call payment cards functions"""


@when(parsers.parse("I perform POST request to add {card_type} payment card to wallet of {payment_card_provider} type"))
def post_add_payment_card_always_autolink(card_type, payment_card_provider):
    response = PaymentCards.add_unique_payment_card(TestContext.token, card_type, payment_card_provider)
    assert response.status_code == 201, f"Payment card addition for '{payment_card_provider}' is not successful"
    response_json = response_to_json(response)
    logging.info(
        f"The response of POST/PaymentCard '{payment_card_provider}' is: \n\n"
        + Endpoint.BASE_URL
        + api.ENDPOINT_PAYMENT_CARDS
        + "\n\n"
        + json.dumps(response_json, indent=4)
    )
    TestContext.current_payment_card_id = response_json.get("id")
    return TestContext.current_payment_card_id


def response_to_json(response):
    try:
        response_json = response.json()
    except JSONDecodeError or Exception:
        raise Exception(f"Empty response and the response Status Code is {str(response.status_code)}")
    return response_json


"""This step is created as part of Trusted channel work and will be used mainly for multi-wallet scenarios."""


@when(
    parsers.parse(
        'For {user} I perform GET request to view vouchers for "{loyalty_card_status}" "{merchant}" membership card'
    )
)
def membership_card_vouchers(user, loyalty_card_status, merchant, env):
    TestContext.token = TestContext.all_users[user]
    response = MembershipCards.get_scheme_account(TestContext.token, TestContext.current_scheme_account_id)
    response_json = response.json()
    logging.info("Response for" + merchant + "vouchers details" + json.dumps(response_json, indent=4))
    with open(TestData.get_expected_membership_card_json(merchant, env)) as json_file:
        expected_response = json.load(json_file)
    actual_response = response_json
    if loyalty_card_status == "authorised":
        assert expected_response["vouchers"] == actual_response["vouchers"], "Voucher verification failed"
        logging.info("Voucher verification is successful")
    elif loyalty_card_status == "unauthorised":
        try:
            print("voucher object in response is", actual_response["vouchers"])
        except KeyError:
            print("For unauthorised loyalty card voucher object does not exist in response")


@when(parsers.parse("For {user} I perform PATCH request to update the {merchant} membership card with {credentials}"))
def membership_card_update(user, merchant, credentials):
    TestContext.token = TestContext.all_users[user]
    response = MembershipCards.update_card(
        TestContext.token, TestContext.current_scheme_account_id, merchant, credentials
    )
    response_json = response.json()
    logging.info(
        f"Response of PATCH/membership_card/'{TestContext.current_scheme_account_id}' for "
        + merchant
        + "_membership card update with"
        + credentials
        + "is "
        + json.dumps(response_json, indent=4)
    )
    assert (
        response.status_code == 200 and response_json["id"] == TestContext.current_scheme_account_id
    ), "Update membership card failed"
