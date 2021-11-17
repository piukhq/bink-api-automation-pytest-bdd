from pytest_bdd import (
    scenarios,
    then,
    when,
    given,
    parsers,
)
import logging

import config
from tests.helpers.test_context import TestContext
from tests.payload.service.customer_accounts import UserDetails
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
def user_sent_without_consent():
    response_consent = CustomerAccount.without_consent_key_bink_user(TestContext.token)
    TestContext.response = response_consent.json().__str__()
    TestContext.status_code = response_consent.status_code
    logging.info(f"User registration is not successful and bad request occured: \n\n {TestContext.response} \n")


@when(parsers.parse('I send a POST service request without the consent mandatory field into request'))
def user_sent_without_mandatory_field():
    response_consent = CustomerAccount.without_mandatory_consent_field(TestContext.token)
    TestContext.response = response_consent.json().__str__()
    TestContext.status_code = response_consent.status_code
    logging.info(f"User registration is not successful and bad request occured: \n\n {TestContext.response} \n")


@when(parsers.parse('I send a POST service request "{longitude}" as alphabet'))
def user_sent_longitude_with_alphabet(longitude, test_email):
    response_consent = CustomerAccount.longitude_as_alphabet(TestContext.token, test_email)
    TestContext.response = response_consent.json().__str__()
    TestContext.status_code = response_consent.status_code
    logging.info(f"User registration is not successful and bad request occured: \n\n {TestContext.response} \n")


@when(parsers.parse('I send a POST service request with "{input}" in the request body enclosed in quotes'))
def user_sent_timestamp_with_quotes(input, test_email):
    response_consent = CustomerAccount.optional_consent_field(TestContext.token, input, test_email)
    TestContext.response = response_consent.json()
    TestContext.status_code = response_consent.status_code
    TestContext.timestamp = response_consent.json().get("consent").get("timestamp")
    logging.info(f"User registration is not successful and bad request occured: \n\n {TestContext.response} \n")


@when(parsers.parse('I send a POST service request without "{input}" in the request body enclosed in quotes'))
def user_sent_optional_field(input, test_email):
    response_consent = CustomerAccount.optional_consent_field(TestContext.token, input, test_email)
    TestContext.response = response_consent.json()
    TestContext.status_code = response_consent.status_code
    TestContext.timestamp = response_consent.json().get("consent").get("timestamp")
    logging.info(f"User registration is not successful and bad request occured: \n\n {TestContext.response} \n")


@then(parsers.parse('I should receive an HTTP "{statuscode}" with a "{errordetail}"'))
def consent_error_message(statuscode, errordetail):
    assert (TestContext.status_code == int(statuscode) and
            TestContext.response == errordetail), ("User Registration_service consent is Invalid")


@then(parsers.parse('I should receive an HTTP "{statuscode}" and success response'))
def consent_response(test_email, statuscode):
    expected_user_consent_json = UserDetails.expected_user_consent_json(test_email, TestContext.timestamp)
    actual_user_consent = TestContext.response
    logging.info(f"Actual user service consent response : {actual_user_consent}" +
                 f"Expected service consent response: {expected_user_consent_json}")
    assert TestContext.status_code == int(statuscode) and expected_user_consent_json == actual_user_consent, \
        "Banking user subscription is not successful"
    return TestContext.token


@then(parsers.parse('I should receive an statuscode and success response with email and timestamp without "{input}"'))
def consent_without_latitude(test_email, input):
    if input == "latitude":
        expected_user_consent_json = \
            UserDetails.expected_user_consent_with_optional_field(test_email, TestContext.timestamp)
        actual_user_consent = TestContext.response
        logging.info(f"Actual user service consent response : {actual_user_consent}" + "\n\n" +
                     f"Expected service consent response: {expected_user_consent_json}")
        assert TestContext.status_code == 201 and \
               expected_user_consent_json == actual_user_consent, "Banking user subscription is not successful"

    elif input == "longitude":
        expected_user_consent_json = \
            UserDetails.expected_user_consent_with_optional_field(test_email, TestContext.timestamp)
        actual_user_consent = TestContext.response
        logging.info(f"Actual user service consent response : {actual_user_consent}" + "\n\n" +
                     f"Expected service consent response: {expected_user_consent_json}")
        assert TestContext.status_code == 201 and \
               expected_user_consent_json == actual_user_consent, "User subscription is not successful"

    return TestContext.token
