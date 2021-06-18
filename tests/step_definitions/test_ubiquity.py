from faker import Faker
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
from json import JSONDecodeError

import tests.api as api
import tests.helpers.constants as constants
from tests.api.base import Endpoint
from tests.helpers.test_helpers import TestData
from tests.helpers.test_context import TestContext
from tests.helpers.test_data_utils import TestDataUtils
from tests.payload.service.customer_accounts import UserDetails
from tests.requests.service import CustomerAccount
from tests.requests.payment_cards import PaymentCards
from tests.helpers.test_helpers import PaymentCardTestData
from tests.requests.membership_cards import MembershipCards
from tests.step_definitions import test_payment_cards, test_membership_cards

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
        TestContext.channel_name = config.BARCLAYS.channel_name
        response = CustomerAccount.service_consent_banking_user(
            TestDataUtils.TEST_DATA.barclays_user_accounts.get(constants.USER_ID))
        logging.info("The JWT Token is: \n\n" +
                     TestContext.token + "\n")
        assert response.status_code == 200, "Banking user subscription to Bink is not successful"

    elif channel == config.BARCLAYS.channel_name:
        logging.info("Switching to another channel: " + config.BINK.channel_name)
        TestContext.channel_name = config.BINK.channel_name
        response = CustomerAccount.login_bink_user()
        logging.info("Token is: \n\n" + TestContext.token + "\n")
        assert response.status_code == 200, "User login in Bink Channel is not successful"


@when(parsers.re('I perform POST request to add payment_card_1 to my wallet in (?P<channel_name>.*)'))
def ubiquity_add_payment_card(test_email, channel_name):
    response = PaymentCards.add_payment_card(TestContext.token, test_email)
    response_json = response.json()
    TestContext.current_payment_card_id = response_json.get("id")
    if channel_name == "channel_1":
        TestContext.token_channel_1 = TestContext.token
    logging.info("The response of POST/PaymentCard is: \n\n"
                 + Endpoint.BASE_URL + api.ENDPOINT_PAYMENT_CARDS + "\n\n"
                 + json.dumps(response_json, indent=4))
    assert response.status_code == 201 or 200, "Payment card addition is not successful"


@when(parsers.re(
    'I perform the GET request to verify the payment_card_1 has been added successfully to the'
    ' wallet in (?P<channel_name>.*)'))
def ubiquity_verify_payment_card_added(channel_name):
    response = PaymentCards.get_payment_card(TestContext.token, TestContext.current_payment_card_id)
    response_json = response.json()
    logging.info("The response of GET/PaymentCards is: \n\n"
                 + Endpoint.BASE_URL + api.ENDPOINT_PAYMENT_CARD.format(TestContext.current_payment_card_id) + "\n\n"
                 + json.dumps(response_json, indent=4))
    if channel_name == "channel_2":
        assert (
                response_json["membership_cards"][0]["id"] == TestContext.scheme_account_id1
                and response_json["membership_cards"][0]["active_link"] ==
                PaymentCardTestData.get_data().get(constants.ACTIVE_LINK)
        ), "Membership_card_1 is not successfully linked to payment_card_1 in channel_1"
    assert (
            response.status_code == 200
            and response_json["id"] == TestContext.current_payment_card_id
            and response_json["status"] == PaymentCardTestData.get_data().get(constants.PAYMENT_CARD_STATUS)
    ), "Payment card addition is not successful"


@when(parsers.parse(
    'I perform POST request to add & auto link an existing "{merchant}" membership_card_1 to my wallet in channel_1'))
def ubiquity_add_existing_membership_card_1(merchant):
    response = MembershipCards.add_card_auto_link(TestContext.token, merchant)
    response_json = response.json()
    TestContext.scheme_account_id1 = response_json.get("id")
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
def ubiquity_verify_membership_card_1_is_add_and_linked(merchant, channel):
    response = MembershipCards.get_scheme_account_auto_link(TestContext.token,
                                                            TestContext.scheme_account_id1)
    response_json = response.json()
    logging.info(
        "The response of GET/MembershipCard after Membership card Add & AutoLink is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.scheme_account_id1) + "\n\n"
        + json.dumps(response_json, indent=4))

    try:
        payment_card_present = "no"
        for current_payment_card in response_json["payment_cards"]:
            if current_payment_card["id"] == TestContext.current_payment_card_id:
                payment_card_present = "yes"
        assert (
                response.status_code == 200
                and response_json["id"] == TestContext.scheme_account_id1
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
    response = MembershipCards.add_card_auto_link(TestContext.token, merchant)
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
    response = MembershipCards.add_card_auto_link(TestContext.token, merchant, "card_2")
    response_json = response.json()
    TestContext.current_scheme_account_id = response_json.get("id")
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
    response = MembershipCards.get_scheme_account(TestContext.token,
                                                  TestContext.current_scheme_account_id)
    response_json = response.json()
    logging.info(
        "The response of GET/MembershipCard after Membership_card_2 Added is :\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.current_scheme_account_id) + "\n\n"
        + json.dumps(response_json, indent=4))
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
            and response_json["payment_cards"] == []
            and payment_card_present == "no"
    ), ("Validations in GET/membership_cards after AutoLink for membership_card_2 " + merchant + " failed")


@when(parsers.parse(
    'I perform POST request to add & auto link an existing "{merchant}" membership_card_2 to my wallet in channel_1'))
def ubiquity_add_existing_membership_card2_channel1(merchant):
    response = MembershipCards.add_card_auto_link(TestContext.token, merchant, "card_2")
    response_json = response.json()
    TestContext.current_scheme_account_id = response_json.get("id")
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
    response = MembershipCards.get_scheme_account(TestContext.token,
                                                  TestContext.current_scheme_account_id)
    response_json = response.json()
    logging.info(
        "The response of GET/MembershipCard after Membership_card_2 Added is :\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.current_scheme_account_id) + "\n\n"
        + json.dumps(response_json, indent=4))
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
            and response_json["payment_cards"] == []
            and payment_card_present == "no"
    ), ("Validations in GET/membership_cards after AutoLink for membership_card_2 " + merchant + " failed")


@then(
    parsers.parse(
        'There is no link created between payment_card_1 and "{merchant}" membership_card_2')
)
def ubiquity_verify_no_card_link(merchant):
    response = MembershipCards.get_scheme_account(TestContext.token,
                                                  TestContext.current_scheme_account_id)

    response_json = response.json()
    payment_card_present = "no"
    for current_payment_card in response_json["payment_cards"]:
        if current_payment_card["id"] == TestContext.current_payment_card_id:
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
    response_membership_card_1 = MembershipCards.get_scheme_account(TestContext.token,
                                                                    TestContext.scheme_account_id1)

    response_json = response_membership_card_1.json()
    payment_card_present = "no"
    for current_payment_card in response_json["payment_cards"]:
        if current_payment_card["id"] == TestContext.current_payment_card_id:
            payment_card_present = "yes"
    assert (payment_card_present == "yes"
            ), ("There is a link created between payment_card_1 and " + merchant + " membership_card2")
    logging.info("There is no link created between payment_card_1 and " + merchant + " membership_card_2")


@when(parsers.parse('I perform POST request to add "{payment_card_provider}" payment card to wallet'))
def post_ubiquity_payment_card(payment_card_provider="master"):
    test_payment_cards.add_payment_card(payment_card_provider="master")


@when(parsers.parse('I perform POST request to add existing "{payment_card_provider}" payment card to wallet'))
def post_ubiquity_card(payment_card_provider="master"):
    response = PaymentCards.add_payment_card(TestContext.different_wallet_token, payment_card_provider)
    assert response.status_code == 200, \
        f"Payment card addition for '{payment_card_provider}' is not successful"
    response_json = response_to_json(response)
    logging.info(f"The response of POST/PaymentCard '{payment_card_provider}' is: \n\n"
                 + Endpoint.BASE_URL + api.ENDPOINT_PAYMENT_CARDS + "\n\n"
                 + json.dumps(response_json, indent=4))
    TestContext.new_payment_card_id = response_json.get("id")
    logging.info(TestContext.new_payment_card_id)
    return TestContext.new_payment_card_id


def response_to_json(response):
    try:
        response_json = response.json()
    except JSONDecodeError or Exception:
        raise Exception(f"Empty response and the response Status Code is {str(response.status_code)}")
    return response_json


@when("I perform the GET request to verify the payment card has been added successfully to the wallet")
def verify_payment_card_added_succesfully():
    test_payment_cards.verify_payment_card_added()


@when("I perform the GET request to verify the existing payment card has been added successfully to the wallet")
def verify_payment_card_added():
    response = PaymentCards.get_payment_card(TestContext.different_wallet_token,
                                             TestContext.new_payment_card_id)
    logging.info(response)
    response_json = response.json()
    logging.info("The response of GET/PaymentCard/id is: \n\n"
                 + Endpoint.BASE_URL + api.ENDPOINT_PAYMENT_CARD.format(TestContext.new_payment_card_id)
                 + "\n\n" + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
            and response_json["id"] == TestContext.new_payment_card_id
            and response_json["status"] == PaymentCardTestData.get_data().get(constants.PAYMENT_CARD_STATUS)
    ), "Payment card addition is not successful"
    return response


@when(parsers.parse('I perform POST request to add "{merchant}" membership card to my wallet'))
def post_membership_cards(merchant):
    """Call to add_card in test_membership_cards"""
    test_membership_cards.add_membership_card(merchant)


@when(parsers.parse('I perform GET request to verify the "{merchant}" membership card is added to the wallet'))
def get_membership_card(merchant):
    test_membership_cards.verify_get_membership_card(merchant)


@when(parsers.parse('I perform POST request to add existing "{merchant}" membership card to my wallet'))
def post_existing_membership_cards(merchant):
    """Call to add_existing_card in test_membership_cards"""
    response = MembershipCards.add_card(TestContext.different_wallet_token, merchant)
    response_json = response_to_json(response)
    TestContext.new_scheme_account_id = response_json.get("id")
    logging.info(
        "The response of Add Journey (POST) is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n"
        + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
            and response_json["status"]["state"] == TestData.get_membership_card_status_states()
            .get(constants.AUTHORIZED)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_AUTHORIZED)
    ), ("Add Existing membership_card Journey for " + merchant + " failed")


@when(parsers.parse('I perform GET request to verify the existing "{merchant}" membership card is added to the wallet'))
def verify_get_existing_membership_card_added_to_the_wallet(merchant):
    response = MembershipCards.get_scheme_account(TestContext.different_wallet_token, TestContext.new_scheme_account_id)
    TestContext.response = response
    response_json = response_to_json(response)
    logging.info(
        "The response of GET/MembershipCard/id is:\n\n"
        + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(TestContext.new_scheme_account_id) + "\n\n" +
        json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
            and response_json["id"] == TestContext.new_scheme_account_id
            and response_json["membership_plan"] == TestData.get_membership_plan_id(merchant)
            and response_json["status"]["state"] == TestData.get_membership_card_status_states().
            get(constants.AUTHORIZED)
            and response_json["status"]["reason_codes"][0] == TestData.get_membership_card_status_reason_codes().
            get(constants.REASON_CODE_AUTHORIZED)
            and response_json["card"]["membership_id"] == TestData.get_data(merchant).get(constants.CARD_NUM)
            or TestContext.card_number
    ), ("Validations in GET/membership_cards for " + merchant + " failed with reason code " +
        response_json["status"]["reason_codes"][0])
    if merchant in ("HarveyNichols", "Iceland"):
        assert (response_json["card"]["barcode"] == TestData.get_data(merchant).get(constants.BARCODE)
                ), ("Barcode verification for " + merchant + " failed")


@when("I perform PATCH request to link payment card to membership card")
def i_perform_patch_request_to_link_paymentcard_to_memebrshipcard():
    test_payment_cards.patch_pcard_mcard()

#
# @when(parsers.parse('I perform GET request to verify the "{merchant}" membership card is'
#                     ' linked successfully in the wallet'))
# def verify_mcard_link(merchant):
#     """Function call to get_membership_cards in test_membership_cards"""
#     test_membership_cards.verify_add_and_link_membership_card(merchant)
#
#
# @when("I perform GET/payment_card/id request to verify the membership card is linked to the payment card")
# def verify_membershipcard_is_linked_to_paymentcard():
#     test_payment_cards.verify_mcard_pacrd_link()


@then('I perform DELETE request to delete the link between payment_card & membership_card '
      'which is exist into another wallet')
def delete_request_between_pcard_mcard():
    response = PaymentCards.delete_pcard_mcard(TestContext.different_wallet_token,
                                               TestContext.new_payment_card_id,
                                               TestContext.new_scheme_account_id)
    TestContext.response = response.text
    assert (response.status_code == 403), f"DELETE/payment_card/membership_card success with reason code" \
                                          f" '{response.status_code}'"
    logging.info(f"The response code of DELETE/payment_card/membership_card which is already exist into "
                 f"another wallet is: '{response.status_code}'")


@when("I am a another customer who is subscribing to Bink or I am Bink app user")
def register_another_user(channel, env):
    TestContext.channel_name = channel
    faker = Faker()
    test_email = constants.EMAIL_TEMPLATE.replace("email", str(faker.random_int(100, 999999)))
    if channel == config.BINK.channel_name:
        response = CustomerAccount.register_different_bink_user(test_email)
        logging.info(response)
        if response is not None:
            try:
                response_consent = CustomerAccount.service_consent_bink_user(TestContext.different_wallet_token,
                                                                             test_email)
                assert response_consent.status_code == 201, "User Registration _ service consent is not successful"
                logging.info("User registration is successful and the token is: \n\n" +
                             TestContext.different_wallet_token + "\n\n" + f"POST Login  response: {response.json()}")
                return TestContext.different_wallet_token
            except Exception as e:
                logging.info(f"Gateway Timeout error :{e}")

    elif channel == config.BARCLAYS.channel_name:
        response = CustomerAccount.service_consent_banking_user(test_email)
        if response is not None:
            try:
                logging.info("Banking user subscription to Bink is successful and the token is: \n\n" +
                             TestContext.different_wallet_token + "\n")
                logging.info(f"POST service consent response status code: {response.status_code} \n\n" +
                             f"POST service consent actual response: {response.json()}")
                timestamp = response.json().get("consent").get("timestamp")
                expected_user_consent = UserDetails.expected_user_consent_json(test_email, timestamp)
                actual_user_consent = response.json()
                logging.info(f"expected response: {expected_user_consent}")
                assert response.status_code == 201 and expected_user_consent == actual_user_consent, \
                    "Banking user subscription is not successful"
                return TestContext.different_wallet_token
            except Exception as e:
                logging.info(f"Gateway Timeout error :{e}")


@then('I verify the "<error_message>"')
def verify_response_error_message(error_message):
    assert (TestContext.response == error_message), f"DELETE/payment_card/membership_card success with reason code" \
                                          f" '{TestContext.response}'"
    logging.info(f"The response code of DELETE/payment_card/membership_card which is already exist into "
                 f"another wallet is: '{TestContext.response}'")
