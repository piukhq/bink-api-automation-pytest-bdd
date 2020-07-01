import pytest
import time
import logging
from pytest_bdd import given, then
from selenium.webdriver import Chrome

import config
from tests.requests.service import CustomerAccount
from tests.api.base import Endpoint

# auto_pytest, make sure its from python
EMAIL_TEMPLATE = "pytest_email@bink.com"


# Hooks

def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    print(f'Step failed: {step}')


def pytest_html_report_title(report):
    """Customized title for html report"""
    report.title = "Bink Test Automation Result_PytestBDD"


@pytest.fixture(scope='session', autouse=True)
def configure_html_report_env(request, env, channel):
    """Delete existing data in the test report and add bink api execution details"""
    for ele in list(request.config._metadata.keys()):
        del request.config._metadata[ele]
    # if re.search(r'^(GITLAB_|CI_)', k): for git lab related extra table contents
    request.config._metadata.update(
        {'Test Environment': env,
         'Channel': channel}
    )


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


# Autouse Fixtures
@pytest.fixture(scope="session", autouse=True)
def set_environment(env):
    Endpoint.set_environment(env)
    logging.info('Environment Setup ready')


@pytest.fixture()
def test_email():
    return EMAIL_TEMPLATE.replace("email", str(time.time()))


@pytest.fixture
def driver():
    """check to be included if chrome is not there? add another browser safari"""
    if config.BROWSER.browser_name == 'chrome':
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
@given('I registers with bink service as a new customer')
def register_user(test_email, channel):
    response = CustomerAccount.create_user(test_email, channel)
    CustomerAccount.create_consent(response.json().get('api_key'), test_email)
    print('Shared given step has executed-------------', response.json().get('api_key'))
    return response


@given('I am a Bink user')
def login_user(channel):
    return CustomerAccount.login_user(channel)




