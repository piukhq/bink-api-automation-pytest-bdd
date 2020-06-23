from pytest_bdd import (
    scenarios,
    then,
    when,
    parsers,
)
import time
import pytest
import json
import logging
from requests.exceptions import HTTPError
from tests.requests.membership_cards import MembershipCards
from tests.api.base import Endpoint

scenarios('membership_cards/')


def customer_can_add_membership_card():
    """Verify a customer can add membership card."""
    pass


@pytest.fixture(scope='function')
def context():
    return {}


@when(parsers.parse('I submit POST request to add "{merchant}" membership card'))
def add_membership_card(merchant, login_user, context):
    """I submit POST request to add merchant membership card."""
    context['token'] = login_user.json().get('api_key')
    response = MembershipCards.add_card(context['token'], merchant)
    logging.info(response.content)
    context['scheme_account_id'] = response.json().get('id')
    response_json = response.json()

    # if(status is 200 check the state as authorized and fetch the id and call a deletion)
    try:
        assert response.status_code == 201 \
            and response_json['status']['state'] == Endpoint.TEST_DATA.membership_account_states.get('state_pending') \

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error('add journey for ', merchant, 'failed')


@when(parsers.parse('I submit GET request to verify "{merchant}" membership card is added to  wallet'))
def verify_membership_card_is_added_to_wallet(merchant, context):
    """I submit GET request to verify merchant membership card is added to  wallet."""
    # handle time in inside common functions
    time.sleep(1)
    response = MembershipCards.get_scheme_account(context['token'], context['scheme_account_id'])
    response_json = response.json()
    try:
         assert response.status_code == 200 \
           and response_json['id'] == context['scheme_account_id'] \
           and response_json['status']['state'] == Endpoint.TEST_DATA.membership_account_states.get('state_authorised')
    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error('{network_response}')


@when(parsers.parse('I submit POST request to create a "{merchant}" membership account with enrol details'))
def enrol_membership_account(merchant, register_user, context, test_email):
    """I submit POST request to create a membership account with enrol details."""
    context['token'] = register_user.json().get('api_key')
    response = MembershipCards.enrol(context['token'], merchant)
    context['scheme_account_id'] = response.json().get('id')
    try:
        assert response.status_code == 201
    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400
        logging.error('Enrol journey for ', merchant, 'failed due to HTTP error: {network_response}')


@then('verify membership account Join date, Card Number and Merchant identifier populated in Django')
def verify_membership_account_join_date_card_number_and_merchant_identifier_populated_in_django():
    """verify membership account Join date, Card Number and Merchant identifier populated in Django."""


@then(parsers.parse('I perform DELETE request to delete the "{merchant}" membership card'))
def perform_delete_request_scheme_account(merchant, context):
    """they perform DELETE request to delete the "harvey-nichols" scheme account."""
    time.sleep(1)
    response_del_schemes = MembershipCards.delete_scheme_account(context['token'], context['scheme_account_id'])
    assert response_del_schemes.status_code == 200
