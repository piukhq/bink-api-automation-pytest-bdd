import pytest
import logging
import json
from faker import Faker
from pytest_bdd import given, then
from selenium.webdriver import Chrome

import config
from tests.requests.service import CustomerAccount
from tests.requests.payment_cards import PaymentCards
from tests.api.base import Endpoint
from tests.helpers.test_data_utils import TestDataUtils
import tests.helpers.constants as constants


# Hooks
def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    print(f"Step failed: {step}")


# def pytest_bdd_after_scenario(request, feature, scenario)


def pytest_html_report_title(report):
    """Customized title for html report"""
    report.title = "Bink Test Automation Result_PytestBDD"


@pytest.fixture(scope="session", autouse=True)
def configure_html_report_env(request, env, channel):
    """Delete existing data in the test report and add bink api execution details"""
    for ele in list(request.config._metadata.keys()):
        del request.config._metadata[ele]
    # if re.search(r'^(GITLAB_|CI_)', k): for git lab related extra table contents
    request.config._metadata.update({"Test Environment": env, "Channel": channel})


# To delete the individual details on Environment section in report
# def pytest_metadata(metadata):
#     metadata.pop("Packages", None)


# Reading inputs from terminal
def pytest_addoption(parser):
    parser.addoption("--channel", action="store", default="bink", help="Channel names like Bink,Barclays should pass")
    parser.addoption("--env", action="store", default="dev", help="env : can be staging or dev")


# Terminal parameter Fixtures
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


@pytest.fixture
def driver():
    """check to be included if chrome is not there? add another browser safari"""
    if config.BROWSER.browser_name == "chrome":
        driver = Chrome(executable_path=config.BROWSER.driver_path)
        driver.maximize_window()

    # elif launch in safari
    else:
        raise Exception(f'"{config.BROWSER.browser_name}" is not a supported browser')
    driver.implicitly_wait(config.BROWSER.wait_time)
    """Return driver object after set up """
    yield driver
    """Quit driver for cleanup """
    driver.quit()


# Shared  Steps
@given("I register with bink service as a new customer")
def register_user(test_email, channel):
    response = CustomerAccount.create_user(test_email, channel)
    CustomerAccount.create_consent(response.json().get("api_key"), test_email)
    logging.info("User registration is successful and the token is: \n\n" + response.json().get("api_key") + "\n")
    return response


@given("I am a Bink user")
def login_user(channel):
    return CustomerAccount.login_user(channel)


@pytest.fixture(scope="function")
def context():
    return {}


@given("I perform POST request to add payment card to wallet")
def add_payment_card(login_user, context):
    context["token"] = login_user.json().get("api_key")
    response = PaymentCards.add_payment_card(context["token"])
    response_json = response.json()
    logging.info("The response of POST/PaymentCards :\n " + json.dumps(response_json, indent=4))
    context["payment_card_id"] = response_json.get("id")
    assert response.status_code == 201 or 200, "Payment card addition is not successful"
    return context["payment_card_id"]


@given("I perform the GET request to verify the payment card has been added successfully")
def verify_payment_card_added(context):
    response = PaymentCards.get_payment_card(context["token"], context["payment_card_id"])
    response_json = response.json()
    logging.info("The response of GET/PaymentCards : \n" + json.dumps(response_json, indent=4))
    assert response.status_code == 200
    # try:
    #     assert response.status_code == 200
    #     logging.info('Payment card is added successfully : \n' + str(response.content))
    #     #  Add status check later
    # except AssertionError as error:
    #     raise Exception('Add Journey for ' + merchant + ' failed due to error ' + error.__str__())


@then("I perform DELETE request to delete the payment card")
def delete_payment_card(context, merchant):
    response = PaymentCards.delete_payment_card(context["token"], context["payment_card_id"])
    try:
        assert response.status_code == 200
        logging.info("Payment card is deleted successfully")
        #  Add status check later
    except AssertionError as error:
        raise Exception("Add Journey for " + merchant + " failed due to error " + error.__str__())


# def pytest_html_results_table_html(report, data):
#    if report.failed:
#        del data[:]
#        data.append(html.div('No log output captured.', class_='empty log'))
