import datetime
import json
import logging
import time
from json import JSONDecodeError

from pytest_bdd import parsers, scenarios, then, when

import tests.api as api
import tests.helpers.constants as constants
from tests.api.base import Endpoint
from tests.helpers.database.query_hermes import QueryHermes
from tests.helpers.test_context import TestContext
from tests.helpers.test_data_utils import TestDataUtils
from tests.helpers.test_helpers import Merchant, PaymentCardTestData, TestData
from tests.requests.membership_cards import MembershipCards
from tests.requests.membership_transactions import MembershipTransactions
from tests.requests.payment_cards import PaymentCards

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


#
# @when(
#     parsers.parse(
#         'I perform POST request to add "{merchant}" membership card with invalid "{email_address} and "{password}"'
#     )
# )
# def add_membership_card_invalid_credentials(merchant, email_address, password):
#     response = MembershipCards.add_card(TestContext.token, merchant)
#     response_json = response_to_json(response)
#     TestContext.current_scheme_account_id = response_json.get("id")
#     logging.info(
#         "The response of Add Journey (POST) with Invalid data is:\n \n"
#         + Endpoint.BASE_URL
#         + api.ENDPOINT_MEMBERSHIP_CARDS
#         + "\n\n"
#         + json.dumps(response_json, indent=4)
#     )
#
#     assert (
#         response.status_code == 201
#         and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
#         and response_json["status"]["reason_codes"][0]
#         == TestData.get_membership_card_status_reason_codes().get(constants.REASON_CODE_PENDING_ADD)
#     ), ("Add Journey with invalid details for " + merchant + " failed")
#
#
# @when(parsers.parse('I perform POST request to add & auto link an existing "{merchant}" membership card'))
# def add_and_link_membership_card(merchant):
#     response = MembershipCards.add_card_auto_link(TestContext.token, merchant)
#     response_json = response_to_json(response)
#     TestContext.current_scheme_account_id = response_json.get("id")
#     TestContext.response = response
#     logging.info(
#         "The response of Add&Link Journey (POST) is:\n\n"
#         + Endpoint.BASE_URL
#         + api.ENDPOINT_AUTO_LINK_PAYMENT_AND_MEMBERSHIP_CARD
#         + "\n\n"
#         + json.dumps(response_json, indent=4)
#     )
#
#     assert (
#         response.status_code == 201
#         and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
#         and response_json["status"]["reason_codes"][0]
#         == TestData.get_membership_card_status_reason_codes().get(constants.REASON_CODE_PENDING_ADD)
#     ), ("Add Journey for " + merchant + " failed")


# @when(parsers.parse('I perform PATCH request to update "{merchant}" membership card'))
# def patch_request_to_update_membership_card_details(merchant):
#     response = MembershipCards.patch_add_card(TestContext.token, TestContext.current_scheme_account_id, merchant)
#     response_json = response_to_json(response)
#     logging.info(
#         "The response of Add Journey (PATCH) is:\n\n"
#         + Endpoint.BASE_URL
#         + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.current_scheme_account_id)
#         + "\n\n"
#         + json.dumps(response_json, indent=4)
#     )
#     assert (
#         response.status_code == 200
#         and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
#         and response_json["status"]["reason_codes"][0]
#         == TestData.get_membership_card_status_reason_codes().get(constants.REASON_CODE_PENDING_ADD)
#     ), ("Add Journey -PATCH Request for " + merchant + " failed")


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
    response = MembershipCards.register_ghost_card(
        TestContext.token, merchant, test_email, TestContext.current_scheme_account_id, env, channel
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


# @when(parsers.parse('I perform PUT request to replace information of the enrolled "{merchant}" membership card'))
# def put_request_to_replace_enrolled_membership_card_details(merchant, test_email):
#     response = MembershipCards.put_enrol_customer(
#         TestContext.token, TestContext.current_scheme_account_id, merchant, test_email
#     )
#     response_json = response_to_json(response)
#     logging.info(
#         "The response of Enrol Journey (PUT) is:\n\n"
#         + Endpoint.BASE_URL
#         + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.current_scheme_account_id)
#         + "\n\n"
#         + json.dumps(response_json, indent=4)
#     )
#     assert (
#         response.status_code == 200
#         and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
#         and response_json["status"]["reason_codes"][0]
#         == TestData.get_membership_card_status_reason_codes().get(constants.REASON_CODE_PENDING_ENROL)
#     ), ("Enrol Journey PUT Request for " + merchant + "failed")


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


# @when(
#     parsers.parse(
#         'I perform GET request to verify the enrolled "{merchant}" membership card details got '
#         "replaced after a successful PUT"
#     )
# )
# @when(parsers.parse('I perform GET request to verify the "{merchant}" membership account is created'))
# def verify_membership_card_is_created(merchant):
#     time.sleep(3)
#     response = MembershipCards.get_scheme_account(TestContext.token, TestContext.current_scheme_account_id)
#     response_json = response_to_json(response)
#     # logging.info(f"response_json:{response_json}")
#     TestContext.card_number = response_json["card"]["membership_id"]
#     TestContext.existing_card = response_json["card"]["membership_id"]
#     logging.info(
#         "The response of GET/MembershipCard after Register Ghost Journey is:\n\n"
#         + Endpoint.BASE_URL
#         + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.current_scheme_account_id)
#         + "\n\n"
#         + json.dumps(response_json, indent=4)
#     )
#     assert (
#         response.status_code == 200
#         and response_json["id"] == TestContext.current_scheme_account_id
#         and response_json["membership_plan"] == TestData.get_membership_plan_id(merchant)
#         and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.AUTHORIZED)
#         and response_json["status"]["reason_codes"][0]
#         == TestData.get_membership_card_status_reason_codes().get(constants.REASON_CODE_AUTHORIZED)
#         and (
#             (response_json["card"]["membership_id"] == TestData.get_data(merchant).get(constants.CARD_NUM))
#             or (response_json["card"]["membership_id"] == TestContext.card_number)
#         )
#         and response_json["card"] is not None
#         and response_json["images"] is not None
#         and ((response_json["account"]["tier"] == 0) or (response_json["account"]["tier"] == 1))
#         and response_json["balances"] is not None
#     ), ("Validations in GET/membership_cards for " + merchant + " failed")


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
    if env in ("dev", "staging", "prod"):
        """There is no DB validation in production suite"""
        pass

    else:

        scheme_account = QueryHermes.fetch_scheme_account(journey_type, TestContext.current_scheme_account_id)

        assert scheme_account.status == 1, f"Scheme Account is not Active and the status is '{scheme_account.status}'"
        logging.info(f"The scheme account is Active with status '{scheme_account.status}'")

        assert (
            scheme_account.id == TestContext.current_scheme_account_id
            and scheme_account.scheme_id == TestData.get_membership_plan_id(merchant)
            and scheme_account.link_or_join_date.date() == datetime.datetime.now().date()
        ), f"Details of scheme account '{scheme_account.id}'in DB is not as expected"

        """Below function call will display all Scheme account credential answers for Add & Enrol Journeys"""

        cred_ans = QueryHermes.fetch_credential_ans(merchant, TestContext.current_scheme_account_id)

        if journey_type == "Add":
            logging.info(
                f"The Link Date for scheme_account '{scheme_account.id}' is " f"{scheme_account.link_or_join_date}'"
            )

            assert scheme_account.main_answer == Merchant.get_scheme_cred_main_ans(
                merchant
            ), "The Main Scheme Account answer is not saved as expected "

            """Verifying the request data is getting stored in DB after Add Journey """
            verify_scheme_account_ans(cred_ans, merchant)

        elif journey_type == "Enrol":
            logging.info(
                f"The Join Date for scheme_account '{scheme_account.id}' is " f"{scheme_account.link_or_join_date}'"
            )


def verify_scheme_account_ans(cred_ans, merchant):
    """For HN , BK, FF, WHsmith the  main scheme_account_ans is validated against
    'main_answer' column in scheme_schemeaccount table

    HN 'Password' scheme_account_ans is not validating as it has to remain as encrypted

    The remaining columns in scheme_schemeaccountcredentialanswers table are already validated
    as a part of the API response

    This function validates Iceland's  last_name & post_code and Wasabi's  email field in the request."""
    if merchant == "Iceland":
        assert cred_ans.last_name == TestDataUtils.TEST_DATA.iceland_membership_card.get(
            constants.LAST_NAME
        ) and cred_ans.postcode == TestDataUtils.TEST_DATA.iceland_membership_card.get(
            constants.POSTCODE
        ), "Iceland scheme_account answers are not saved as expected"

    elif merchant == "Wasabi":
        assert cred_ans.email == TestDataUtils.TEST_DATA.wasabi_membership_card.get(
            constants.EMAIL
        ), "Wasabi scheme_account answers are not saved as expected"


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


#
# @when(parsers.parse('I perform POST request to add "{master}" payment card to wallet with autolink false'))
# def add_payment_cards_autolink_false(login_user, master):
#     TestContext.token = login_user
#     response = PaymentCards.add_payment_card(TestContext.token, master)
#     response_json = response.json()
#     logging.info(
#         "The response of POST/PaymentCard is: \n\n"
#         + Endpoint.BASE_URL
#         + api.ENDPOINT_AUTO_LINK_FALSE
#         + "\n\n"
#         + json.dumps(response_json, indent=4)
#     )
#     TestContext.current_payment_card_id = response_json.get("id")
#     assert response.status_code == 201 or 200, "Payment card addition is not successful"
#     return TestContext.current_payment_card_id


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
