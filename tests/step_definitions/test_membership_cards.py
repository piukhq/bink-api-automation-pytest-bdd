from pytest_bdd import (
    scenarios,
    then,
    when,
    parsers,
)
import time
import pytest
import json
import jsonpath
import logging
from requests.exceptions import HTTPError
from tests.requests.membership_cards import MembershipCards
from tests.api.base import Endpoint
from selenium.webdriver.support.ui import Select

# from tests.helpers.test_data_utils import TestDataUtils
# import tests.helpers.test_data_utils as test_data

scenarios('membership_cards/')


def customer_can_add_membership_card():
    """Verify a customer can add membership card."""
    pass


@pytest.fixture(scope='function')
def context():
    return {}


"""Step definitions - Add Journey """


@when(parsers.parse('I perform POST request to add "{merchant}" membership card'))
def add_membership_card(merchant, login_user, context):
    context['token'] = login_user.json().get('api_key')
    response = MembershipCards.add_card(context['token'], merchant)
    context['scheme_account_id'] = response.json().get('id')
    response_json = response.json()
    logging.info('HELLO WORLD')
    try:
        assert response.status_code == 201 \
               and response_json['status']['state'] == \
               Endpoint.TEST_DATA.membership_account_states.get('state_pending')

    except AssertionError as error:
        # assert network_response.response.status_code == 404 or 400
        # logging.info('jidhjfhdjfjd')
        logging.error('Add Journey for ', merchant, ' failed due to error')
        raise
        # raise Exception('Add Journey for ' + merchant + ' failed due to error ' + error.__str__())


@when(parsers.parse('I perform POST request to add "{merchant}" membership card with "{invalid_data}"'))
def add_membership_card(merchant, login_user, context, invalid_data):
    context['token'] = login_user.json().get('api_key')
    response = MembershipCards.add_card(context['token'], merchant, invalid_data)
    response_json = response.json()
    context['scheme_account_id'] = response_json.get('id')
    try:
        assert response.status_code == 201 \
               and response_json['status']['state'] == \
               Endpoint.TEST_DATA.membership_account_states.get('state_pending')
        logging.info('Response after POST with invalid data is:\n ' + str(response.content))

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error('Add journey for' + merchant +
                      's with invalid data got failed due to HTTP error: {network_response')


@when(parsers.parse('I perform POST request to add & auto link an existing "{merchant}" membership card'))
def add_membership_card(merchant, login_user, context):
    context['token'] = login_user.json().get('api_key')
    print('toen`55' + context['token'])
    response = MembershipCards.add_card_auto_link(login_user.json().get('api_key'), merchant)
    response_json = response.json()
    context['scheme_account_id'] = response_json.get('id')
    try:
        assert response.status_code == 201 \
               and response_json['status']['state'] == \
               Endpoint.TEST_DATA.membership_account_states.get('state_pending')

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error(merchant + ' membership card Add Journey failed due to HTTP error: {network_response')


@when(parsers.parse('I perform PATCH request to update "{merchant}" membership card'))
def patch_request_to_update_membership_card_details(merchant, context):
    response = MembershipCards.patch_add_card(context['token'], context['scheme_account_id'], merchant)
    response_json = response.json()
    try:
        assert response.status_code == 200 \
               and response_json['status']['state'] == \
               Endpoint.TEST_DATA.membership_account_states.get('state_pending')
        logging.info('Successfully performed PATCH on ' + merchant + 's membership card ')

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error(merchant + ' membership card PATCH failed due to HTTP error: {network_response')


"""Step definitions - Enrol Journey """


@when(parsers.parse('I perform POST request to create a "{merchant}" membership account with enrol credentials'))
def enrol_membership_account(merchant, register_user, context, test_email):
    context['token'] = register_user.json().get('api_key')
    response = MembershipCards.enrol_customer(context['token'], merchant, test_email)
    context['scheme_account_id'] = response.json().get('id')
    try:
        assert response.status_code == 201
    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error('Enrol journey for ', merchant, 'failed due to HTTP error: {network_response}')


@when(parsers.parse('I perform POST request to create a "{merchant}" membership account with "{invalid}" enrol '
                    'credentials'))
def enrol_membership_account_invalid_credentials(merchant, register_user, context, test_email, invalid):
    context['token'] = register_user.json().get('api_key')
    response = MembershipCards.enrol_customer(context['token'], merchant, test_email, invalid)
    context['scheme_account_id'] = response.json().get('id')
    response_json = response.json()

    assert response.status_code == 201 \
           and response_json['status']['state'] == \
           Endpoint.TEST_DATA.membership_account_states.get('state_pending')


@when(parsers.parse('I perform PUT request to replace information of the enrolled "{merchant}" membership card'))
def put_request_to_replace_enrolled_membership_card_details(merchant, context):
    response = MembershipCards.put_enrol_customer(context['token'], context['scheme_account_id'], merchant)
    response_json = response.json()
    try:
        assert response.status_code == 200 \
               and response_json['status']['state'] == \
               Endpoint.TEST_DATA.membership_account_states.get('state_pending')
        logging.info('Successfully performed PATCH on ' + merchant + 's membership card ')

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error(merchant + ' membership card PATCH failed due to HTTP error: {network_response')


"""Step definitions - GET Scheme Account """


@when(parsers.parse('I perform GET request to verify the "{merchant}" membership card is added to the wallet'))
@when(parsers.parse('I perform GET request to verify the "{merchant}" membership card details got updated after a '
                    'successful PATCH'))
@when(parsers.parse('I perform GET request to verify the "{merchant}" membership account is created'))
@when(parsers.parse('I perform GET request to verify the enrolled "{merchant}" membership card details got '
                    'replaced after a successful PUT'))
def verify_membership_card_is_added_to_wallet(merchant, context):
    response = MembershipCards.get_scheme_account(context['token'], context['scheme_account_id'])
    response_json = response.json()
    try:
        assert response.status_code == 200 \
               and response_json['id'] == context['scheme_account_id'] \
               and response_json['status']['state'] == Endpoint.TEST_DATA.membership_account_states.get(
            'state_authorised')

        # implement a new test data util class and re-write the following
        # and str(response_json['membership_plan']) == Endpoint.TEST_DATA.membership_plan_id.get(merchant)
        # and response_json['card']['membership_id'] == test_data.get_card_number(merchant)

        logging.info(merchant + ' membership card is created/ added/ updated successfully: \n' + str(response.content))

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error(
            merchant + ' membership card add /updated(POST/PATCH) failed due to HTTP error: {network_response')


@when(parsers.parse('I perform GET request to verify the "{merchant}" membership card is added & linked successfully '
                    'in the wallet'))
def verify_membership_card_is_add_and_linked(merchant, context, add_payment_card):
    response = MembershipCards.get_scheme_account_auto_link(context['token'])
    response_json = response.json()
    try:
        assert response.status_code == 200 \
               and response_json[0]['id'] == context['scheme_account_id'] \
               and response_json[0]['status']['state'] == \
               Endpoint.TEST_DATA.membership_account_states.get('state_authorised')
        logging.info(merchant + ' Membership card is added and auto linked : \n' + str(response.content))

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error('Add and AutoLink of' + merchant + ' Membership card failed due to HTTP error: {network_response')


@when(parsers.parse('I perform GET request to verify the "{merchant}" membership card is added to the wallet with '
                    'invalid data'))
@when(parsers.parse('I perform GET request to verify the "{merchant}" membership account is created with invalid data'))
def verify_membership_card_is_added_to_wallet(merchant, context):
    response = MembershipCards.get_scheme_account(context['token'], context['scheme_account_id'])
    response_json = response.json()
    try:
        assert response.status_code == 200 \
               and response_json['id'] == context['scheme_account_id'] \
               and response_json['status']['state'] == \
               Endpoint.TEST_DATA.membership_account_states.get('state_failed')

        logging.info('Response after GET (invalid data) is: \n ' + str(response.content))

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error('Unable to add membership card for', merchant, 'due to HTTP error: {network_response')


@when(parsers.parse('I perform GET request to view balance for recently added membership card'))
def verify_membership_card_is_added_to_wallet(context):
    response = MembershipCards.get_membership_card_balance(context['token'])
    response_json = response.json()
    logging.info(' GET request to view balance for recently added membership card: \n ' + str(response.content))

    try:
        # Assert other balance realted field checks
        assert response.status_code == 200 \
               and response_json[0]['id'] == context['scheme_account_id'] \
               and response_json[0]['status']['state'] == \
               Endpoint.TEST_DATA.membership_account_states.get('state_authorised')

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error('Unable to add membership card for', merchant, 'due to HTTP error: {network_response')


"""Step definitions - DELETE Scheme Account """


@then(parsers.parse('I perform DELETE request to delete the "{merchant}" membership card'))
def perform_delete_request_scheme_account(merchant, context):
    response_del_schemes = MembershipCards.delete_scheme_account(context['token'], context['scheme_account_id'])
    try:
        assert response_del_schemes.status_code == 200
        logging.info('Scheme account is deleted successfully')

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error('Scheme account deletion for ', merchant, 'failed due to HTTP error: {network_response}')


"""Step definitions - Django Verifications"""


@then('verify membership account Link date, Card Number and Merchant identifier populated in Django')
def verify_membership_account_link_date_card_number_and_merchant_identifier_populated_in_django(driver, context):
    scheme_account_id = str(context['scheme_account_id'])
    driver.get(Endpoint.DJANGO_URL + 'scheme/schemeaccount/' + scheme_account_id + '/change/')
    driver.find_element_by_name('username').send_keys(Endpoint.TEST_DATA.django_user_accounts.get('django_uid'))
    driver.find_element_by_name('password').send_keys(Endpoint.TEST_DATA.django_user_accounts.get('django_pwd'))
    driver.find_element_by_xpath("//input[@type='submit']").click()
    select = Select(driver.find_element_by_name('status'))
    assert select.first_selected_option.text == 'Active'
    link_date = driver.find_element_by_xpath('//form[@id="schemeaccount_form"]/div/fieldset/div[13]/div/div').text
    current_date = time.strftime("%d %b %Y").lstrip('0')
    if str(link_date).__contains__(current_date):
        logging.info("Link date in Django (" + link_date + ") is close to current date ""(" + current_date +
                     time.strftime(", %I:%M %p").lower() + ")")
    logging.info('Merchant Identifier in Django is: ' + driver.find_element_by_name
    ('schemeaccountcredentialanswer_set-1-answer').get_attribute('value'))


@then('verify membership account Join date, Card Number and Merchant identifier populated in Django')
def verify_membership_account_join_date_card_number_and_merchant_identifier_populated_in_django(driver, context):
    scheme_account_id = str(context['scheme_account_id'])
    driver.get(Endpoint.DJANGO_URL + 'scheme/schemeaccount/' + scheme_account_id + '/change/')
    driver.find_element_by_name('username').send_keys(Endpoint.TEST_DATA.django_user_accounts.get('django_uid'))
    driver.find_element_by_name('password').send_keys(Endpoint.TEST_DATA.django_user_accounts.get('django_pwd'))
    driver.find_element_by_xpath("//input[@type='submit']").click()
    select = Select(driver.find_element_by_name('status'))
    assert select.first_selected_option.text == 'Active'
    # join_date = driver.find_element_by_xpath("//input[@name='join_date_0']/div").text
    # join_time = driver.find_element_by_name('join_date_1').text
    # current_date = time.strftime("%d/%b/%Y").lstrip('0')
    # logging.info(join_date+current_date)
    #
    # if str(join_date).__contains__(current_date):
    #     logging.info("Link date in Django (" + join_date + join_time + ") is close to current date ""(" + current_date +
    #                  time.strftime(", %I:%M %p").lower() + ")")
    # logging.info('Merchant Identifier in Django is: ' + driver.find_element_by_name
    # ('schemeaccountcredentialanswer_set-1-answer').get_attribute('value'))
