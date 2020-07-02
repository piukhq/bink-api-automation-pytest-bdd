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

scenarios('membership_cards/')


def customer_can_add_membership_card():
    """Verify a customer can add membership card."""
    pass


@pytest.fixture(scope='function')
def context():
    return {}


@when(parsers.parse('I submit POST request to add "{merchant}" membership card'))
def add_membership_card(merchant, login_user, context):
    context['token'] = login_user.json().get('api_key')
    response = MembershipCards.add_card(context['token'], merchant)
    logging.info(response.content)
    context['scheme_account_id'] = response.json().get('id')
    response_json = response.json()
    try:
        assert response.status_code == 201 \
               and response_json['status']['state'] == \
               Endpoint.TEST_DATA.membership_account_states.get('state_pending')

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error('add journey for ', merchant, 'failed')


@when(parsers.parse('I perform PATCH request to update "{merchant}" membership card'))
def patch_request_to_update_membership_card_details(merchant, context):
    response = MembershipCards.patch_membership_card(context['token'], context['scheme_account_id'])
    try:
        assert response.status_code == 201 \
               and response_json['status']['state'] == \
               Endpoint.TEST_DATA.membership_account_states.get('state_pending')

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error('add journey for ', merchant, 'failed')


@when(parsers.parse('I submit GET request to verify "{merchant}" membership card is added to the wallet'))
def verify_membership_card_is_added_to_wallet(merchant, context):
    response = MembershipCards.get_scheme_account(context['token'], context['scheme_account_id'])
    response_json = response.json()
    logging.info(response_json['status']['state'])
    try:
        assert response.status_code == 200 \
               and response_json['id'] == context['scheme_account_id'] \
               and response_json['status']['state'] == Endpoint.TEST_DATA.membership_account_states. \
                   get('state_authorised')
    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error('{network_response}')

@when(parsers.parse('I submit POST request to create a "{merchant}" membership account with enrol details'))
def enrol_membership_account(merchant, register_user, context, test_email):
    context['token'] = register_user.json().get('api_key')
    response = MembershipCards.enrol(context['token'], merchant)
    context['scheme_account_id'] = response.json().get('id')
    try:
        assert response.status_code == 201
    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error('Enrol journey for ', merchant, 'failed due to HTTP error: {network_response}')


@then(parsers.parse('I perform DELETE request to delete the "{merchant}" membership card'))
def perform_delete_request_scheme_account(merchant, context):
    time.sleep(1)
    response_del_schemes = MembershipCards.delete_scheme_account(context['token'], context['scheme_account_id'])
    try:
        assert response_del_schemes.status_code == 200
    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error('Delete Scheme Account ', merchant, 'failed due to HTTP error: {network_response}')


# Common Django verifications
@then('verify membership account Join date, Card Number and Merchant identifier populated in Django')
def verify_membership_account_join_date_card_number_and_merchant_identifier_populated_in_django(driver, context):
    """verify membership account Join date, Card Number and Merchant identifier populated in Django."""
    scheme_account_id = str(context['scheme_account_id'])
    driver.get(Endpoint.DJANGO_URL + 'scheme/schemeaccount/' + scheme_account_id + '/change/')
    driver.find_element_by_name('username').send_keys(Endpoint.TEST_DATA.django_user_accounts.get('django_uid'))
    driver.find_element_by_name('password').send_keys(Endpoint.TEST_DATA.django_user_accounts.get('django_pwd'))
    driver.find_element_by_xpath("//input[@type='submit']").click()
    # time.sleep(1)
    select = Select(driver.find_element_by_name('status'))
    assert select.first_selected_option.text == 'Active'
    link_date = driver.find_element_by_xpath('//form[@id="schemeaccount_form"]/div/fieldset/div[12]/div/div').text
    current_date = time.strftime("%d %b %Y").lstrip('0')
    if str(link_date).__contains__(current_date):
        logging.info("Link date ("+link_date+") is close to current date "
                     "("+current_date + time.strftime(", %I:%M %p").lower()+")")
    logging.info('Merchant Identifier is: ' + driver.find_element_by_name('schemeaccountcredentialanswer_set-1-answer').
                 get_attribute('value'))
