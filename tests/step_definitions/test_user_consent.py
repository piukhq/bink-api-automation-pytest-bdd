from pytest_bdd import (
    scenarios,
    then,
    when,
    given,
    parsers,
)
import logging

import config
from tests.conftest import expected_user_consent_json
from tests.helpers.test_context import TestContext
from tests.requests.service import CustomerAccount

scenarios("user_consent/")

"""Step definitions - service consent """


@given(parsers.parse("I register with bink as a new customer"))
def register_new_user(test_email, channel, env):
    TestContext.channel_name = channel
    if channel == config.BINK.channel_name:
        response = CustomerAccount.register_bink_user(test_email)
        assert response.status_code == 201, "User Registration_service consent is not successful"
        logging.info("User registration is successful and the token is: \n\n" + TestContext.token + "\n\n"
                     + f"POST registeration  response: {response.json()}")
        return TestContext.token

    elif channel == config.BARCLAYS.channel_name:
        TestContext.token = CustomerAccount.without_service_consent_banking_user(test_email)
        logging.info("User registration service token is: \n\n" + TestContext.token)

@when(parsers.parse('I send a POST service request without the consent field'))
def user_sent_empty_consent():
    response_consent = CustomerAccount.without_service_consent_bink_user(TestContext.token)
    TestContext.response = response_consent.json().__str__()
    TestContext.status_code = response_consent.status_code
    logging.info(f"User registration is not successful and bad request occured: \n\n {TestContext.response} \n")


@when(parsers.parse('I send a POST service request without the consent key into request'))
def user_sent_empty_consent():
    response_consent = CustomerAccount.without_consent_key_bink_user(TestContext.token)
    TestContext.response = response_consent.json().__str__()
    TestContext.status_code = response_consent.status_code
    logging.info(f"User registration is not successful and bad request occured: \n\n {TestContext.response} \n")

@when(parsers.parse('I send a POST service request without the consent mandatory field into request'))
def user_sent_empty_consent():
    response_consent = CustomerAccount.without_mandatory_consent_field(TestContext.token)
    TestContext.response = response_consent.json().__str__()
    TestContext.status_code = response_consent.status_code
    logging.info(f"User registration is not successful and bad request occured: \n\n {TestContext.response} \n")

@then('I should receive an HTTP "<statuscode>" with a "<errordetail>"')
def consent_error_message(statuscode, errordetail):
    assert (TestContext.status_code == int(statuscode) and
            TestContext.response == errordetail), ("User Registration_service consent is Invalid")






