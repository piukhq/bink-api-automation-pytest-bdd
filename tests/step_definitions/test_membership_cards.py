from pytest_bdd import (
    scenarios,
    then,
    when,
    given,
    parsers,
)
import json
import logging
import datetime
from json import JSONDecodeError

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
import tests.step_definitions.test_payment_cards as test_payment_cards
from tests.requests.payment_cards import PaymentCards

scenarios("membership_cards/")

"""Step definitions - Add Journey """


@when(parsers.parse('I perform POST request to add "{merchant}" membership card'))
def add_membership_card(merchant):
    response = MembershipCards.add_card(TestContext.token, merchant)
    response_json = response_to_json(response)
    TestContext.current_scheme_account_id = response_json.get("id")
    logging.info(
        "The response of Add Journey (POST) is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201
            and response_json["membership_plan"] == TestData.get_membership_plan_id(merchant)
            and response_json["payment_cards"] == []
            and response_json["membership_transactions"] == []
            and response_json["status"]["state"] == TestData.get_membership_card_status_states()
            .get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ADD)
            and response_json["card"] is not None
            and response_json["images"] is not None
            and response_json["account"]["tier"] == 0
            and response_json["balances"] == []
    ), ("Add Journey for " + merchant + " failed")


@when(parsers.parse('I perform POST request to add "{merchant}" ghost membership card'))
def add_ghost_membership_card(merchant):
    response = MembershipCards.add_ghost_card(TestContext.token, merchant)
    response_json = response_to_json(response)
    TestContext.current_scheme_account_id = response_json.get("id")
    logging.info(
        "The response of Add Ghost Journey (POST) is:"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201
            and response_json["status"]["state"] == TestData.get_membership_card_status_states()
            .get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ADD)
    ), ("Add Ghost Journey for " + merchant + " failed")


@when(parsers.parse('I perform POST request to add "{merchant}" membership card with "{invalid_data}"'))
def add_invalid_membership_card(merchant, invalid_data):
    response = MembershipCards.add_card(TestContext.token, merchant, invalid_data)
    response_json = response_to_json(response)
    TestContext.current_scheme_account_id = response_json.get("id")
    logging.info("The response of Add Journey (POST) with Invalid data is:\n \n"
                 + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n"
                 + json.dumps(response_json, indent=4))

    assert (
            response.status_code == 201
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().
            get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ADD)
    ), ("Add Journey with invalid details for " + merchant + " failed")


@when(parsers.parse(
    'I perform POST request to add "{merchant}" membership card with invalid "{email_address} and "{password}"'
)
)
def add_membership_card_invalid_credentials(merchant, email_address, password):
    response = MembershipCards.add_card(TestContext.token, merchant)
    response_json = response_to_json(response)
    TestContext.current_scheme_account_id = response_json.get("id")
    logging.info("The response of Add Journey (POST) with Invalid data is:\n \n"
                 + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n"
                 + json.dumps(response_json, indent=4))

    assert (
            response.status_code == 201
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().
            get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ADD)
    ), ("Add Journey with invalid details for " + merchant + " failed")


@when(parsers.parse('I perform POST request to add & auto link an existing "{merchant}" membership card'))
def add_and_link_membership_card(merchant):
    response = MembershipCards.add_card_auto_link(TestContext.token, merchant)
    response_json = response_to_json(response)
    TestContext.current_scheme_account_id = response_json.get("id")
    TestContext.response = response
    logging.info(
        "The response of Add&Link Journey (POST) is:\n\n" +
        Endpoint.BASE_URL + api.ENDPOINT_AUTO_LINK_PAYMENT_AND_MEMBERSHIP_CARD + "\n\n"
        + json.dumps(response_json, indent=4))

    assert (
            response.status_code == 201
            and response_json["status"]["state"] == TestData.get_membership_card_status_states()
            .get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ADD)
    ), ("Add Journey for " + merchant + " failed")


@when(parsers.parse('I perform PATCH request to update "{merchant}" membership card'))
def patch_request_to_update_membership_card_details(merchant):
    response = MembershipCards.patch_add_card(TestContext.token, TestContext.current_scheme_account_id, merchant)
    response_json = response_to_json(response)
    logging.info(
        "The response of Add Journey (PATCH) is:\n\n" +
        Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.current_scheme_account_id) + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ADD)
    ), ("Add Journey -PATCH Request for " + merchant + " failed")


"""Step definitions - Enrol Journey """


@when(parsers.parse('I perform POST request to create a "{merchant}" membership account with enrol credentials'))
def enrol_membership_account(merchant, test_email, env, channel):
    response = MembershipCards.enrol_customer(TestContext.token, merchant, test_email, env, channel)
    response_json = response_to_json(response)
    TestContext.current_scheme_account_id = response_json.get("id")
    logging.info(
        "The response of Enrol Journey (POST) is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n" +
        json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201
            and response_json["membership_plan"] == TestData.get_membership_plan_id(merchant)
            and response_json["payment_cards"] == []
            and response_json["membership_transactions"] == []
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ENROL)
            and response_json["card"] is not None
            and response_json["images"] is not None
            and response_json["account"]["tier"] == 0
            and response_json["balances"] == []
    ), ("Enrol journey for " + merchant + " failed")


"""Step Definations - Register ghost membership_card"""


@when(parsers.parse('I perform PATCH request to create a "{merchant}" ghost membership account with enrol credentials'))
def register_ghost_membership_account(merchant, test_email, env, channel):
    response = MembershipCards.register_ghost_card(TestContext.token, merchant,
                                                   test_email, TestContext.current_scheme_account_id, env, channel)
    response_json = response_to_json(response)
    TestContext.current_scheme_account_id = response_json.get("id")
    logging.info(
        "The response of Register ghost Journey (PATCH) is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS.format(TestContext.current_scheme_account_id) + "\n\n" +
        json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ENROL)
    ), ("Enrol journey for " + merchant + " failed")


@when(parsers.parse(
    'I perform POST request to create a "{merchant}" membership account with "{invalid}" enrol credentials'
)
)
def enrol_membership_account_invalid_credentials(merchant, test_email, env, channel, invalid):
    response = MembershipCards.enrol_customer(TestContext.token, merchant, test_email, env, channel, invalid)
    response_json = response_to_json(response)
    TestContext.current_scheme_account_id = response_json.get("id")
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
def put_request_to_replace_enrolled_membership_card_details(merchant, test_email):
    response = MembershipCards.put_enrol_customer(TestContext.token, TestContext.current_scheme_account_id,
                                                  merchant, test_email)
    response_json = response_to_json(response)
    logging.info(
        "The response of Enrol Journey (PUT) is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.current_scheme_account_id) + "\n\n"
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
def verify_get_membership_card(merchant):
    response = MembershipCards.get_scheme_account(TestContext.token, TestContext.current_scheme_account_id)
    TestContext.response = response
    response_json = response_to_json(response)
    logging.info(
        "The response of GET/MembershipCard/id is:\n\n"
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
            and ((response_json["card"]["membership_id"] == TestData.get_data(merchant).get(constants.CARD_NUM)) or (
                response_json["card"]["membership_id"] == TestContext.card_number))
            and response_json["card"] is not None
            and response_json["images"] is not None
            and ((response_json["account"]["tier"] == 0) or (response_json["account"]["tier"] == 1))
            and response_json["balances"] is not None
    ), ("Validations in GET/membership_cards for " + merchant + " failed with reason code " +
        response_json["status"]["reason_codes"][0])
    if merchant in ("HarveyNichols", "Iceland"):
        assert (response_json["card"]["barcode"] == TestData.get_data(merchant).get(constants.BARCODE)
                ), ("Barcode verification for " + merchant + " failed")

    return response


@when(
    parsers.parse(
        'I perform GET request to verify the enrolled "{merchant}" membership card details got '
        "replaced after a successful PUT"
    )
)
@when(parsers.parse('I perform GET request to verify the "{merchant}" membership account is created'))
def verify_membership_card_is_created(merchant):
    response = MembershipCards.get_scheme_account(TestContext.token, TestContext.current_scheme_account_id)
    response_json = response_to_json(response)
    TestContext.card_number = response_json["card"]["membership_id"]
    logging.info(
        "The response of GET/MembershipCard after Register Ghost Journey is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.current_scheme_account_id) + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
            and response_json["id"] == TestContext.current_scheme_account_id
            and response_json["membership_plan"] == TestData.get_membership_plan_id(merchant)
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().
            get(constants.AUTHORIZED)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_AUTHORIZED)
            and ((response_json["card"]["membership_id"] == TestData.get_data(merchant).get(constants.CARD_NUM)) or (
                response_json["card"]["membership_id"] == TestContext.card_number))
            and response_json["card"] is not None
            and response_json["images"] is not None
            and ((response_json["account"]["tier"] == 0) or (response_json["account"]["tier"] == 1))
            and response_json["balances"] is not None
    ), ("Validations in GET/membership_cards for " + merchant + " failed")


@when(
    parsers.parse(
        'I perform GET request to verify the "{merchant}" membership card is added & linked successfully '
        "in the wallet"
    )
)
def verify_add_and_link_membership_card(merchant):
    response = MembershipCards.get_scheme_account_auto_link(TestContext.token, TestContext.current_scheme_account_id)
    response_json = response_to_json(response)
    TestContext.response = response
    logging.info(
        "The response of GET/MembershipCard/id after PLL :\n\n"
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

        ), ("Validations in GET/membership_cards after AutoLink for " + merchant + "failed with reason code " +
            response_json["status"]["reason_codes"][0])
    except IndexError:
        raise Exception("PLL link for " + merchant + " failed and the payment array in the response is empty")
    except AssertionError as error:
        raise Exception("Add&Link Journey for " + merchant + " failed due to " + error.__str__())
    return response


@when(
    parsers.parse(
        'I perform GET request to verify the "{merchant}" membership card is added to the wallet with ' "invalid data"
    )
)
def verify_invalid_membership_card_is_added_to_wallet(merchant):
    response = MembershipCards.get_scheme_account(TestContext.token, TestContext.current_scheme_account_id)
    response_json = response_to_json(response)
    logging.info(
        "The response of GET/MembershipCard with invalid data in the request is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.current_scheme_account_id) + "\n\n"
        + json.dumps(response_json, indent=4))
    assert(
            response.status_code == 200
            and response_json["id"] == TestContext.current_scheme_account_id
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.FAILED)
            and (response_json["status"]["reason_codes"][0] ==
                 TestData.get_membership_card_status_reason_codes().get(constants.REASON_CODE_FAILED) or
                 response_json["status"]["reason_codes"][0] ==
                 TestData.get_membership_card_status_reason_codes().get(constants.REASON_CODE_ADD_FAILED))),\
        ("Validations in GET/membership_cards with invalid data for  " + merchant + " failed with reason code" +
         response_json["status"]["reason_codes"][0])


@when(parsers.parse('I perform GET request to verify the "{merchant}" membership account is created with invalid data'))
def verify_invalid_membership_card_is_created(merchant):
    response = MembershipCards.get_scheme_account(TestContext.token, TestContext.current_scheme_account_id)
    response_json = response_to_json(response)
    logging.info(
        "The response of GET/MembershipCard with invalid data in the request is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.current_scheme_account_id) + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
            and response_json["id"] == TestContext.current_scheme_account_id
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.FAILED)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_FAILED_ENROL) or TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_FAILED_INVALID_ENROL)
    ), ("Validations in GET/membership_cards with invalid data for  " + merchant + " failed with reason code" +
        response_json["status"]["reason_codes"][0])


@when(parsers.parse('I perform GET request to verify the "{merchant}" ghost membership card is added to the wallet'))
def verify_ghost_membership_card_is_created(merchant):
    response = MembershipCards.get_scheme_account(TestContext.token, TestContext.current_scheme_account_id)
    response_json = response_to_json(response)
    logging.info(
        "The response of GET/MembershipCard request is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.current_scheme_account_id) + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
            and response_json["id"] == TestContext.current_scheme_account_id
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.FAILED)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_GHOST_FAILED)
    ), ("Validations in GET/membership_cards " + merchant + " failed with reason code" +
        response_json["status"]["reason_codes"][0])


@when(parsers.parse('I perform GET request to view balance for recently added "{merchant}" membership card'))
def verify_membership_card_balance(merchant):
    current_membership_card_response_array = MembershipCards.get_membership_card_balance(TestContext.token,
                                                                                         TestContext.
                                                                                         current_scheme_account_id)
    logging.info(
        "The response of GET/MembershipCardBalances for the current membership card is : \n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_CHECK_MEMBERSHIP_CARDS_BALANCE + "\n\n"
        + json.dumps(current_membership_card_response_array, indent=4))
    assert (
            current_membership_card_response_array["id"] == TestContext.current_scheme_account_id
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
    ), ("Validations in GET/membership_cards?balances for " + merchant + " failed with reason code" +
        current_membership_card_response_array["status"]["reason_codes"][0])


""""Step definitions for Membership_Transactions"""


@when(
    parsers.parse(
        'I perform GET request to view all transactions made using the recently added "{merchant}" membership card'
    )
)
def verify_membership_card_transactions(merchant):
    response = MembershipTransactions.get_membership_transactions(TestContext.token,
                                                                  TestContext.current_scheme_account_id)
    response_json = response_to_json(response)
    logging.info(
        "The response of GET/MembershipTransactions:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD_TRANSACTIONS.format(TestContext.current_scheme_account_id)
        + "\n\n"
        + json.dumps(response_json, indent=4))
    if response_json[0] == "[]":
        logging.info("There are no matched transactions associated with " + merchant + " membership card: " +
                     TestData.get_data(merchant).get(constants.CARD_NUM))
    else:
        try:
            assert response.status_code == 200
            TestContext.transaction_id = response_json[0].get("id")
        except IndexError:
            raise Exception("Existing transactions associated with " + merchant + " membership card: " +
                            TestData.get_data(merchant).get(
                                constants.CARD_NUM) + " are not populated the response of \n"
                            + Endpoint.BASE_URL +
                            api.ENDPOINT_MEMBERSHIP_CARD_TRANSACTIONS.format(TestContext.current_scheme_account_id))
        except AssertionError as error:
            raise Exception("The response of " + Endpoint.BASE_URL +
                            api.ENDPOINT_MEMBERSHIP_CARD_TRANSACTIONS.format(TestContext.current_scheme_account_id) +
                            " is not as expected. Error is " + error.__str__())


@then(
    parsers.parse(
        'I perform GET request to view a specific transaction made using the recently added "{merchant}"'
        ' membership card'
    )
)
def verify_membership_card_single_transaction_detail(merchant):
    response = MembershipTransactions.get_membership_card_single_transaction_detail(
        TestContext.token, TestContext.transaction_id)
    response_json = response_to_json(response)
    logging.info(
        "The response of GET/MembershipTransaction:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD_SINGLE_TRANSACTION.format(TestContext.transaction_id) +
        "\n\n"
        + json.dumps(response_json, indent=4))
    if response_json == "[]":
        logging.info("There are no matched transactions associated with " + merchant + " membership card: " +
                     TestData.get_data(merchant).get(constants.CARD_NUM))
    else:
        assert (
                response.status_code == 200
                and response_json["id"] == TestContext.transaction_id
                and response_json["status"] == TestData.get_data(merchant).get(constants.TRANSACTIONS_STATUS)
                and response_json["amounts"][0]["currency"] == TestData.get_data(merchant).
                get(constants.TRANSACTIONS_CURRENCY)
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


"""Call payment cards functions"""


@given("I perform POST request to add payment card to wallet")
def post_add_payment_card():
    test_payment_cards.add_payment_card("master")


@when("I perform POST request to add payment card to wallet")
def post_add_payment_card_always_autolink():
    test_payment_cards.add_payment_card("master")


@given("I perform the GET request to verify the payment card has been added successfully")
def get_add_payment_card():
    test_payment_cards.verify_payment_card_added()


@when("I perform the GET request to verify the payment card has been added successfully")
def get_add_payment_card_always_autolink():
    test_payment_cards.verify_payment_card_added()


@when(
    parsers.parse(
        'I perform POST request to add "{master}" payment card to wallet with autolink false'))
def add_payment_cards_autolink_false(login_user, master):
    TestContext.token = login_user
    response = PaymentCards.add_payment_card(TestContext.token, master)
    response_json = response.json()
    logging.info("The response of POST/PaymentCard is: \n\n"
                 + Endpoint.BASE_URL + api.ENDPOINT_AUTO_LINK_FALSE + "\n\n"
                 + json.dumps(response_json, indent=4))
    TestContext.current_payment_card_id = response_json.get("id")
    assert response.status_code == 201 or 200, "Payment card addition is not successful"
    return TestContext.current_payment_card_id


@when(
    parsers.parse(
        'I perform GET request to verify the "{merchant}" membership card is added & not linked in the wallet'))
def verify_membership_card_is_add_and_not_linked(merchant):
    response = MembershipCards.get_scheme_account_auto_link(TestContext.token,
                                                            TestContext.current_scheme_account_id, False)
    response_json = response.json()
    logging.info(
        "The response of GET/MembershipCard after payment card added is not AutoLink is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.current_scheme_account_id) + "\n\n"
        + json.dumps(response_json, indent=4))
    try:
        assert (
                response.status_code == 200
                and response_json["id"] == TestContext.current_scheme_account_id
                and response_json["membership_plan"] == TestData.get_membership_plan_id(merchant)
                and response_json["status"]["state"] == TestData.get_membership_card_status_states().
                get(constants.AUTHORIZED)
                and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
                get(constants.REASON_CODE_AUTHORIZED)
                and response_json["card"]["membership_id"] == TestData.get_data(merchant).get(constants.CARD_NUM)
                and response_json["payment_cards"][0] == []
        ), ("Validations in GET/membership_cards after AutoLink false " + merchant + "failed with reason code " +
            response_json["status"]["reason_codes"][0])
    except IndexError:
        raise Exception("PLL link for " + merchant + " failed and the payment array in the response is not empty")
    except AssertionError as error:
        raise Exception("Add&Link Journey for " + merchant + " failed due to " + error.__str__())


def response_to_json(response):
    try:
        response_json = response.json()
    except JSONDecodeError or Exception:
        raise Exception(f"Empty response and the response Status Code is {str(response.status_code)}")
    return response_json


@when(parsers.parse('I perform POST request to add "{merchant}" membership card after enrol deleted'))
def enrol_delete_add_membership_account(merchant, test_email):
    response = MembershipCards.enrol_delete_add_card(TestContext.token, merchant, test_email)
    response_json = response_to_json(response)
    TestContext.current_scheme_account_id = response_json.get("id")
    logging.info(
        "The response of Add Journey (POST) is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201
            and response_json["status"]["state"] == TestData.get_membership_card_status_states()
            .get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ADD)

    ), ("Add Journey for " + merchant + " failed")


@when(parsers.parse('I perform Get request to verify the "{merchant}" membership card voucher details'))
def verify_membership_card_vouchers(merchant, env):
    response = MembershipCards.get_scheme_account(TestContext.token, TestContext.current_scheme_account_id)
    response_json = response.json()
    logging.info("Response for" + merchant + "vouchers details" + json.dumps(response_json, indent=4))
    with open(TestData.get_expected_membership_card_json(merchant, env)) as json_file:
        expected_response = json.load(json_file)
    logging.info("expected_Voucher_response:" + json.dumps(expected_response['vouchers'], indent=4))
    actual_response = response_json
    logging.info("actual_voucher_response:" + json.dumps(actual_response['vouchers'], indent=4))
    assert (expected_response['vouchers'] == actual_response['vouchers']), "Voucher verification failed"
    logging.info("Voucher verification is successful")


@when(parsers.parse('I perform POST request to add "{merchant}" membership card without "{field_value}"'))
def add_membership_card_without_field_value(merchant, field_value):
    response = MembershipCards.add_card_without_correct_field(TestContext.token, merchant, field_value)
    response_json = response_to_json(response)
    TestContext.detail = response_json["detail"]
    logging.info(
        "The response of Add Journey (POST) is without " + field_value + ":\n\n" + json.dumps(response_json, indent=4))
    assert (response.status_code == 400), ("Add Journey for " + merchant + " succeded")
    return response_json


@then('I should receive error message "<error_message>"')
def error_message_without_field_value(error_message):
    assert (TestContext.detail == error_message), ("Add Journey succeded")


@then('I should receive error message "<error_message>" for email missing')
def error_message_email_missing(error_message):
    assert (TestContext.email == error_message), ("Add Journey succeded")


@when(parsers.parse('I perform POST request to add "{merchant}" membership card with wrong "{field_value}"'))
def add_membership_card_withwrong_field_value(merchant, field_value, channel):
    response = MembershipCards.add_card_without_correct_field(TestContext.token, merchant, field_value)
    response_json = response_to_json(response)
    TestContext.email = response_json["email"][0]
    logging.info("The response of Add Journey (POST) is with wrong " + field_value + ":\n\n" + json.dumps(response_json,
                                                                                                          indent=4))
    assert (response.status_code == 400), ("Add Journey for " + merchant + " succeded")
    return response_json


@when(parsers.parse('I perform POST request to add "{merchant}" membership card without "{field_value}" header'))
def add_membership_card_without_token(merchant, field_value):
    if(field_value == "token"):
        response = MembershipCards.add_card_without_token(merchant, field_value)
    elif(field_value == "payload"):
        response = MembershipCards.add_card_without_payload(TestContext.token)
    response_json = response_to_json(response)
    TestContext.detail = response_json["detail"]
    logging.info(
        "The response of Add Journey (POST) is without " + field_value + ":\n\n" + json.dumps(response_json, indent=4))
    """ wrong token = 401 and empty_payload = 400 """
    assert (response.status_code == 401 or 400), ("Add Journey for " + merchant + " succeded")
    return response_json
