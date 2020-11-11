from pytest_bdd import (
    scenarios,
    then,
    when,
    parsers,
)
import pytest
import json
import logging
import config

import tests.api as api
import tests.helpers.constants as constants
from tests.api.base import Endpoint
from tests.helpers.test_helpers import TestData
from tests.helpers.test_context import TestContext
from tests.helpers.test_data_utils import TestDataUtils
from tests.requests.service import CustomerAccount
from tests.requests.payment_cards import PaymentCards
from tests.helpers.test_helpers import PaymentCardTestData
from tests.requests.membership_cards import MembershipCards

scenarios("ubiquity/")


def ubiquity_features():
    """Verify Ubiquity features"""
    pass


@pytest.fixture(scope="session")
def context():
    return {}


"""Step definitions - Ubiquity features """


@when(parsers.parse('I switch to "{channel_name}"'))
def ubiquity_login_user(env, channel, channel_name):
    """This function is used to switch between the channels for ubiquity feature
    if user is in BINK, switch to BARCLAYS and vice-versa"""

    if channel == config.BINK.channel_name:
        logging.info("Switching to another channel: " + config.BARCLAYS.channel_name)
        TestContext.set_channel(config.BARCLAYS.channel_name)
        response = CustomerAccount.service_consent_banking_user(
            TestDataUtils.TEST_DATA.barclays_user_accounts.get(constants.USER_ID))
        logging.info("The JWT Token is: \n\n" +
                     TestContext.get_token() + "\n")
        assert response.status_code == 200, "Banking user subscription to Bink is not successful"

    elif channel == config.BARCLAYS.channel_name:
        logging.info("Switching to another channel: " + config.BINK.channel_name)
        TestContext.set_channel(config.BINK.channel_name)
        response = CustomerAccount.login_bink_user()
        logging.info("Token is: \n\n" + TestContext.get_token() + "\n")
        assert response.status_code == 200, "User login in Bink Channel is not successful"


@when(parsers.re('I perform POST request to add payment_card_1 to my wallet in (?P<channel_name>.*)'))
def ubiquity_add_payment_card(test_email, channel_name, context):
    response = PaymentCards.add_payment_card(TestContext.get_token(), test_email)
    response_json = response.json()
    TestContext.set_payment_card_id(response_json.get("id"))
    if channel_name == "channel_1":
        TestContext.set_token_channel_1(TestContext.get_token())
    logging.info("The response of POST/PaymentCard is: \n\n"
                 + Endpoint.BASE_URL + api.ENDPOINT_PAYMENT_CARDS + "\n\n"
                 + json.dumps(response_json, indent=4))
    assert response.status_code == 201 or 200, "Payment card addition is not successful"


@when(parsers.re(
    'I perform the GET request to verify the payment_card_1 has been added successfully to the'
    ' wallet in (?P<channel_name>.*)'))
def ubiquity_verify_payment_card_added(channel_name):
    response = PaymentCards.get_payment_card(TestContext.get_token(), TestContext.get_payment_card_id())
    response_json = response.json()
    logging.info("The response of GET/PaymentCards is: \n\n"
                 + Endpoint.BASE_URL + api.ENDPOINT_PAYMENT_CARD.format(TestContext.get_payment_card_id()) + "\n\n"
                 + json.dumps(response_json, indent=4))
    if channel_name == "channel_2":
        assert (
                response_json["membership_cards"][0]["id"] == TestContext.get_scheme_account_id_1()
                and response_json["membership_cards"][0]["active_link"] ==
                PaymentCardTestData.get_data().get(constants.ACTIVE_LINK)
        ), "Membership_card_1 is not successfully linked to payment_card_1 in channel_1"
    assert (
            response.status_code == 200
            and response_json["id"] == TestContext.get_payment_card_id()
            and response_json["status"] == PaymentCardTestData.get_data().get(constants.PAYMENT_CARD_STATUS)
    ), "Payment card addition is not successful"


@when(parsers.parse(
    'I perform POST request to add & auto link an existing "{merchant}" membership_card_1 to my wallet in channel_1'))
def ubiquity_add_existing_membership_card_1(merchant):
    response = MembershipCards.add_card_auto_link(TestContext.get_token(), merchant)
    response_json = response.json()
    TestContext.set_scheme_account_id_1(response_json.get("id"))
    logging.info(
        "The response of Add&Link Journey (POST) is:\n\n" +
        Endpoint.BASE_URL + api.ENDPOINT_AUTO_LINK_PAYMENT_AND_MEMBERSHIP_CARD + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201 or 200
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ADD)
    ), ("Add & Link Journey for " + merchant + " failed")


@when(
    parsers.parse(
        'I perform GET request to verify the "{merchant}" membership_card_1 is added & linked successfully in the '
        'wallet in channel_1'
    )
)
def ubiquity_verify_membership_card_1_is_add_and_linked(merchant, channel, context):
    response = MembershipCards.get_scheme_account_auto_link(TestContext.get_token(),
                                                            TestContext.get_scheme_account_id_1())
    response_json = response.json()
    logging.info(
        "The response of GET/MembershipCard after Membership card Add & AutoLink is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.get_scheme_account_id_1()) + "\n\n"
        + json.dumps(response_json, indent=4))

    try:
        payment_card_present = "no"
        for current_payment_card in response_json["payment_cards"]:
            if current_payment_card["id"] == TestContext.get_payment_card_id():
                payment_card_present = "yes"
        assert (
                response.status_code == 200
                and response_json["id"] == TestContext.get_scheme_account_id_1()
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


@when(parsers.parse(
    'I perform POST request to add & auto link an existing "{merchant}" membership_card_2 to the same wallet '
    'in "{channel}"'))
def ubiquity_add_existing_membership_card2(merchant, channel):
    response = MembershipCards.add_card_auto_link(TestContext.get_token(), merchant)
    response_json = response.json()
    TestContext.set_scheme_account(response_json.get("id"))
    logging.info(
        "The response of Add&Link Journey (POST) is:\n\n" +
        Endpoint.BASE_URL + api.ENDPOINT_AUTO_LINK_PAYMENT_AND_MEMBERSHIP_CARD + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201 or 200
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ADD)
    ), ("Add & Link Journey for " + merchant + " failed")


@when(parsers.parse(
    'I perform POST request to add & auto link an existing "{merchant}" membership_card_2 to my wallet in channel_2'))
def ubiquity_add_existing_membership_card2_channel2(merchant):
    response = MembershipCards.add_card_auto_link(TestContext.get_token(), merchant, "card_2")
    response_json = response.json()
    TestContext.set_scheme_account(response_json.get("id"))
    logging.info(
        "The response of Add&Link Journey (POST) is:\n\n" +
        Endpoint.BASE_URL + api.ENDPOINT_AUTO_LINK_PAYMENT_AND_MEMBERSHIP_CARD + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201 or 200
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ADD)
    ), ("Add & Link Journey for " + merchant + " failed")


@then(
    parsers.parse(
        'I perform GET request to verify the "{merchant}" membership_card_2 is successfully added to my wallet in '
        'channel_2'
    )
)
def ubiquity_verify_membership_card2_is_added(merchant):
    response = MembershipCards.get_scheme_account(TestContext.get_token(),
                                                  TestContext.get_scheme_account_id())
    response_json = response.json()
    logging.info(
        "The response of GET/MembershipCard after Membership_card_2 Added is :\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.get_scheme_account_id()) + "\n\n"
        + json.dumps(response_json, indent=4))
    payment_card_present = "no"
    for current_payment_card in response_json["payment_cards"]:
        if current_payment_card["id"] == TestContext.get_payment_card_id():
            payment_card_present = "yes"
    assert (
            response.status_code == 200
            and response_json["id"] == TestContext.get_scheme_account_id()
            and response_json["membership_plan"] == TestData.get_membership_plan_id(merchant)
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().
            get(constants.AUTHORIZED)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_AUTHORIZED)
            and response_json["payment_cards"] == []
            and payment_card_present == "no"
    ), ("Validations in GET/membership_cards after AutoLink for membership_card_2 " + merchant + " failed")


@when(parsers.parse(
    'I perform POST request to add & auto link an existing "{merchant}" membership_card_2 to my wallet in channel_1'))
def ubiquity_add_existing_membership_card2_channel1(merchant):
    response = MembershipCards.add_card_auto_link(TestContext.get_token(), merchant, "card_2")
    response_json = response.json()
    TestContext.set_scheme_account(response_json.get("id"))
    logging.info(
        "The response of Add&Link Journey (POST) is:\n\n" +
        Endpoint.BASE_URL + api.ENDPOINT_AUTO_LINK_PAYMENT_AND_MEMBERSHIP_CARD + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 201 or 200
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_PENDING_ADD)
    ), ("Add & Link Journey for " + merchant + " failed")


@then(
    parsers.parse(
        'I perform GET request to verify the "{merchant}" membership_card_2 is successfully added to my wallet in '
        'channel_1'
    )
)
def ubiquity_verify_membership_card2_channel_1(merchant):
    response = MembershipCards.get_scheme_account(TestContext.get_token(),
                                                  TestContext.get_scheme_account_id())
    response_json = response.json()
    logging.info(
        "The response of GET/MembershipCard after Membership_card_2 Added is :\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.get_scheme_account_id()) + "\n\n"
        + json.dumps(response_json, indent=4))
    payment_card_present = "no"
    for current_payment_card in response_json["payment_cards"]:
        if current_payment_card["id"] == TestContext.get_payment_card_id():
            payment_card_present = "yes"
    assert (
            response.status_code == 200
            and response_json["id"] == TestContext.get_scheme_account_id()
            and response_json["membership_plan"] == TestData.get_membership_plan_id(merchant)
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().
            get(constants.AUTHORIZED)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_AUTHORIZED)
            and response_json["payment_cards"] == []
            and payment_card_present == "no"
    ), ("Validations in GET/membership_cards after AutoLink for membership_card_2 " + merchant + " failed")


@then(
    parsers.parse(
        'There is no link created between payment_card_1 and "{merchant}" membership_card_2')
)
def ubiquity_verify_no_card_link(merchant):
    response = MembershipCards.get_scheme_account(TestContext.get_token(),
                                                  TestContext.get_scheme_account_id())

    response_json = response.json()
    payment_card_present = "no"
    for current_payment_card in response_json["payment_cards"]:
        if current_payment_card["id"] == TestContext.get_payment_card_id():
            payment_card_present = "yes"
    assert (payment_card_present == "no"
            ), ("There is a link created between payment_card_1 and " + merchant + " membership_card2")
    logging.info("There is no link created between payment_card_1 and " + merchant + " membership_card_2")


@then(
    parsers.parse(
        'The response shows the original link between "{merchant}" membership_card_1 and payment_card_1 remains in'
        ' force')
)
def ubiquity_verify_link(merchant):
    response_membership_card_1 = MembershipCards.get_scheme_account(TestContext.get_token(),
                                                                    TestContext.get_scheme_account_id_1())

    response_json = response_membership_card_1.json()
    payment_card_present = "no"
    for current_payment_card in response_json["payment_cards"]:
        if current_payment_card["id"] == TestContext.get_payment_card_id():
            payment_card_present = "yes"
    assert (payment_card_present == "yes"
            ), ("There is a link created between payment_card_1 and " + merchant + " membership_card2")
    logging.info("There is no link created between payment_card_1 and " + merchant + " membership_card_2")
