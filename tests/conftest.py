import pytest
import logging
import json
from pytest_bdd import given, then
from requests.exceptions import HTTPError

import config
import tests.api as api
import tests.helpers.constants as constants
from tests.requests.service import CustomerAccount
from tests.requests.payment_cards import PaymentCards
from tests.requests.membership_cards import MembershipCards
from tests.api.base import Endpoint
from tests.helpers.test_data_utils import TestDataUtils
from tests.helpers.test_context import TestContext
from tests.helpers.test_helpers import PaymentCardTestData

from faker import Faker


# Hooks
def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    """This function will log the failed BDD-Step at the end of logs"""
    logging.info(f"Step failed: {step}")


def pytest_bdd_after_scenario(request, feature, scenario):
    """Called after scenario is executed (even if one of steps has failed)
    So the scheme_account will be deleted always and make sure the test data is ready"""

    """Below functions make sure the scheme account id and payment_card id deleted from
          first channel after the execution of ubiquity scenarios
          By default second channel becomes the default channel so above functions delete the
           scheme account id  and payment_card id from channel_2"""
    delete_scheme_account()
    delete_payment_card()


def pytest_html_report_title(report):
    """Customized title for html report"""
    report.title = "Bink Test Automation Result_PytestBDD"


@pytest.fixture(scope="session", autouse=True)
def configure_html_report_env(request, env, channel):
    """Delete existing data in the test report and add bink api execution details"""
    for ele in list(request.config._metadata.keys()):
        del request.config._metadata[ele]
    # if re.search(r'^(GITLAB_|CI_)', k): for git lab related extra table contents
    request.config._metadata.update({"Test Environment": env.upper(), "Channel": channel.upper()})


"""Reading inputs from terminal"""


def pytest_addoption(parser):
    parser.addoption("--channel", action="store", default="bink", help="Channel names like Bink,Barclays should pass")
    parser.addoption("--env", action="store", default="dev", help="env : can be dev or staging or prod")


"""Terminal parameter Fixtures"""


@pytest.fixture(scope="session")
def channel(pytestconfig):
    """Returns current channel"""
    return pytestconfig.getoption("channel")


@pytest.fixture(scope="session")
def env(pytestconfig):
    """Returns current environment"""
    return pytestconfig.getoption("env")


@pytest.fixture(scope="session", autouse=True)
def set_environment(env):
    Endpoint.set_environment(env)
    logging.info("Environment Setup ready")
    TestDataUtils.set_test_data(env)


@pytest.fixture()
def test_email():
    # return constants.EMAIL_TEMPLATE.replace("email", str(time.time()))
    faker = Faker()
    return constants.EMAIL_TEMPLATE.replace("email", str(faker.random_int()))


"""Shared  Steps"""


@given("I register with bink service as a new customer")
def register_user(test_email, channel, env):
    if channel == config.BINK.channel_name:
        TestContext.set_channel(channel)
        response = CustomerAccount.register_bink_user(test_email, channel, env)
        token = response.json().get("api_key")
        TestContext.set_token(token)
        response_consent = CustomerAccount.service_consent_bink_user(TestContext.get_token(), test_email)
        assert response_consent.status_code == 201, "User Registration _ service consent is not successful"
        logging.info("User registration is successful and the token is: \n\n" + response.json().get("api_key") + "\n")
        return token
    elif channel == config.BARCLAYS.channel_name:
        TestContext.set_channel(channel)
        response = CustomerAccount.service_consent_banking_user(test_email)
        logging.info("Banking user subscription to Bink is successful and the token is: \n\n" +
                     TestContext.get_token() + "\n")
        assert response.status_code == 201, "Banking user subscription to Bink is not successful"
        return TestContext.get_token()


@given("I am a customer who is subscribing to Bink or I am Bink app user")
@given("I am a Bink user")
@given("I am a customer in channel_1")
def login_user(channel, env):
    TestContext.set_channel(channel)
    if channel == config.BINK.channel_name:
        response = CustomerAccount.login_bink_user()
        logging.info("Token is: \n\n" + TestContext.get_token() + "\n")
        assert response.status_code == 200, "User login in Bink Channel is not successful"
        return TestContext.get_token()
    elif channel == config.BARCLAYS.channel_name:
        response = CustomerAccount.service_consent_banking_user(
            TestDataUtils.TEST_DATA.barclays_user_accounts.get(constants.USER_ID))
        logging.info("The JWT Token is: \n\n" +
                     TestContext.get_token() + "\n")
        assert response.status_code == 200, "Banking user subscription to Bink is not successful"
        return TestContext.get_token()


@then("I perform DELETE request to delete the customer")
def delete_user():
    response = CustomerAccount.delete_new_user(TestContext.get_token())
    assert response.status_code == 200, "Te user deletion is not successful"
    logging.info("User is deleted successfully from the system")


@pytest.fixture(scope="function")
def context():
    return {}


@given("I perform POST request to add payment card to wallet")
def add_payment_card(login_user, context, test_email):
    context["token"] = login_user
    response = PaymentCards.add_payment_card(context["token"], test_email)
    response_json = response.json()
    logging.info("The response of POST/PaymentCard is: \n\n"
                 + Endpoint.BASE_URL + api.ENDPOINT_PAYMENT_CARDS + "\n\n"
                 + json.dumps(response_json, indent=4))
    context["payment_card_id"] = response_json.get("id")
    TestContext.set_payment_card_id(response_json.get("id"))
    assert response.status_code == 201 or 200, "Payment card addition is not successful"
    return context["payment_card_id"]


@given("I perform the GET request to verify the payment card has been added successfully")
def verify_payment_card_added(context):
    response = PaymentCards.get_payment_card(context["token"], context["payment_card_id"])
    response_json = response.json()
    logging.info("The response of GET/PaymentCards is: \n\n"
                 + Endpoint.BASE_URL + api.ENDPOINT_PAYMENT_CARD.format(context["payment_card_id"]) + "\n\n"
                 + json.dumps(response_json, indent=4))
    assert (
            response.status_code == 200
            and response_json["id"] == context["payment_card_id"]
            and response_json["status"] == PaymentCardTestData.get_data().get(constants.PAYMENT_CARD_STATUS)
    ), "Payment card addition is not successful"


@then("I perform DELETE request to delete the payment card")
def delete_payment_card():
    response = PaymentCards.delete_payment_card(TestContext.get_token(), TestContext.get_payment_card_id())
    response1 = PaymentCards.delete_payment_card(TestContext.get_token_channel_1(), TestContext.get_payment_card_id())

    try:
        if response.status_code == 200 or response1.status_code == 200:
            logging.info("Payment card is deleted successfully")
        elif response.status_code == 404 or response1.status_code == 200:
            logging.info("Payment card is already  deleted ")

    except HTTPError as network_response:

        assert network_response.response.status_code == 404 or 400, "Payment card deletion is not successful"


def delete_scheme_account():
    """ To make sure the scheme_account is deleted successfully,even if the add/enrol journey failed """

    response_del_schemes = MembershipCards.delete_scheme_account(TestContext.get_token(),
                                                                 TestContext.get_scheme_account_id())
    response_del_schemes1 = MembershipCards.delete_scheme_account(TestContext.get_token_channel_1(),
                                                                  TestContext.get_scheme_account_id_1())

    try:
        if response_del_schemes.status_code == 200 or response_del_schemes1.status_code == 200:
            logging.info("Scheme account is deleted successfully")
        elif response_del_schemes.status_code == 404:
            logging.info("Scheme account is already  deleted ")

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400, "Scheme account deletion is not successful"
