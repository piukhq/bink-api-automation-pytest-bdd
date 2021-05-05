import pytest
import logging
import time
from pytest_bdd import given, then, parsers
from requests.exceptions import HTTPError

import config
import tests.helpers.constants as constants
from tests.api.transactionmatching_base import TransactionMatching_Endpoint
from tests.requests.service import CustomerAccount
from tests.requests.payment_cards import PaymentCards
from tests.requests.membership_cards import MembershipCards
from tests.api.base import Endpoint
from tests.helpers.test_data_utils import TestDataUtils
from tests.helpers.test_context import TestContext

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
    parser.addoption("--channel", action="store", default="bink", help="Channel: can be bink or barclays should pass")
    parser.addoption("--env", action="store", default="dev", help="env : can be dev or staging or prod")
    parser.addoption("--encryption", action="store", default="false", help="encryption : can be true or false")


"""Terminal parameter Fixtures"""


@pytest.fixture(scope="session")
def channel(pytestconfig):
    """Returns current channel"""
    return pytestconfig.getoption("channel")


@pytest.fixture(scope="session")
def env(pytestconfig):
    """Returns current environment"""
    return pytestconfig.getoption("env")


@pytest.fixture(scope="session")
def encryption(pytestconfig):
    """Returns the choice: with/without encryption"""
    return pytestconfig.getoption("encryption")


@pytest.fixture(scope="session", autouse=True)
def set_environment(env):
    Endpoint.set_environment(env)
    TransactionMatching_Endpoint.set_environment(env)
    logging.info("Environment Setup ready")
    TestDataUtils.set_test_data(env)


@pytest.fixture(scope="session", autouse=True)
def handle_optional_encryption(encryption):
    TestContext.flag_encrypt = encryption


@pytest.fixture()
def test_email():
    # return constants.EMAIL_TEMPLATE.replace("email", str(time.time()))
    faker = Faker()
    return constants.EMAIL_TEMPLATE.replace("email", str(faker.random_int(100, 999999)))


"""Shared  Steps"""


@given("I register with bink service as a new customer")
def register_user(test_email, channel, env):
    TestContext.channel_name = channel
    if channel == config.BINK.channel_name:
        response = CustomerAccount.register_bink_user(test_email)
        if response is not None:
            try:
                response_consent = CustomerAccount.service_consent_bink_user(TestContext.token, test_email)
                assert response_consent.status_code == 201, "User Registration _ service consent is not successful"
                logging.info("User registration is successful and the token is: \n\n" + TestContext.token + "\n\n"
                             + f"POST Login  response: {response.json()}")
                return TestContext.token
            except Exception as e:
                logging.info(f"Gateway Timeout error :{e}")

    elif channel == config.BARCLAYS.channel_name:
        response = CustomerAccount.service_consent_banking_user(test_email)
        if response is not None:
            try:
                logging.info("Banking user subscription to Bink is successful and the token is: \n\n" +
                             TestContext.token + "\n")
                logging.info(f"POST service consent response status code: {response.status_code} \n\n" +
                             f"POST service consent actual response: {response.json()}")
                timestamp = response.json().get("consent").get("timestamp")
                expected_user_consent = expected_user_consent_json(test_email, timestamp)
                actual_user_consent = response.json()
                logging.info(f"expected response: {expected_user_consent}")
                assert response.status_code == 201 and expected_user_consent == actual_user_consent, \
                    "Banking user subscription is not successful"
                return TestContext.token
            except Exception as e:
                logging.info(f"Gateway Timeout error :{e}")


@given("I am a customer who is subscribing to Bink or I am Bink app user")
@given("I am a Bink user")
@given("I am a customer in channel_1")
def login_user(channel, env):
    TestContext.channel_name = channel
    if channel == config.BINK.channel_name:
        response = CustomerAccount.login_bink_user()
        if response.status_code != 504:
            try:
                logging.info("Token is: \n\n" + TestContext.token + "\n" + f"POST Login response: {response.json()} ")
                assert response.status_code == 200, "User login in Bink Channel is not successful"
                return TestContext.token
            except Exception as e:
                logging.info(f"Gateway Timeout error :{e}")
    elif channel == config.BARCLAYS.channel_name:
        response = CustomerAccount.service_consent_banking_user(
            TestDataUtils.TEST_DATA.barclays_user_accounts.get(constants.USER_ID))
        if response.status_code != 504:
            try:
                timestamp = response.json().get("consent").get("timestamp")
                expected_existing_user_consent = expected_existing_user_consent_json(timestamp)
                actual_user_consent = response.json()
                logging.info(f"actual BMB user service consent response : {response.json()}" +
                             f"expected service consent response: {expected_existing_user_consent}")
                logging.info("The JWT Token is: \n\n" +
                             TestContext.token + "\n")
                assert response.status_code == 200 and expected_existing_user_consent == actual_user_consent, \
                    "Banking user subscription is not successful"
                return TestContext.token
            except Exception as e:
                logging.info(f"Gateway Timeout error :{e}")


@then("I perform DELETE request to delete the customer")
def delete_user():
    response = CustomerAccount.delete_new_user(TestContext.token)
    assert response.status_code == 200, "The user deletion is not successful"
    logging.info("User is deleted successfully from the system")


@then("I perform DELETE request to delete the payment card")
def delete_payment_card():
    response = PaymentCards.delete_payment_card(TestContext.token, TestContext.current_payment_card_id)
    response1 = PaymentCards.delete_payment_card(TestContext.token_channel_1, TestContext.current_payment_card_id)
    TestContext.response = response
    """Even if the scheme account is deleted, it is not updating DB so quickly
        so his delay is required before next execution"""
    time.sleep(2)
    try:
        if response.status_code == 200 or response1.status_code == 200:
            logging.info("Payment card is deleted successfully")
        elif response.status_code == 404 or response1.status_code == 404:
            logging.info("Payment card is already  deleted")

    except HTTPError as network_response:

        assert network_response.response.status_code == 404 or 400, "Payment card deletion is not successful"


@then(parsers.parse('I perform DELETE request to delete the "{merchant}" membership card'))
def delete_scheme_account(merchant=None):
    response_del_schemes = MembershipCards.delete_scheme_account(TestContext.token,
                                                                 TestContext.current_scheme_account_id)
    response_del_schemes_1 = MembershipCards.delete_scheme_account(TestContext.token_channel_1,
                                                                   TestContext.scheme_account_id1)
    """Even if the scheme account is deleted, it is not updating DB so quickly
     so his delay is required before next execution"""
    time.sleep(2)
    try:
        if response_del_schemes.status_code == 200 or response_del_schemes_1.status_code == 200:
            logging.info("Scheme account is deleted successfully")
        elif response_del_schemes.status_code == 404:
            logging.info("Scheme account is already  deleted")

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400


def expected_user_consent_json(test_email, timestamp):
    response = {
        "consent": {
            "email": test_email,
            "timestamp": timestamp,
            "latitude": 0.0123,
            "longitude": 12.345
        }
    }
    return response


def expected_existing_user_consent_json(timestamp):
    response = {
        "consent": {
            "email": TestDataUtils.TEST_DATA.barclays_user_accounts.get(constants.USER_ID),
            "timestamp": timestamp,
            "latitude": 0.0,
            "longitude": 12.345
        }
    }
    return response
