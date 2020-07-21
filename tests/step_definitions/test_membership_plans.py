from pytest_bdd import (
    scenarios,
    then,
    when,
    parsers,
)
import pytest
import json
import logging
from json_diff import Comparator

from tests.requests.membership_plans import MembershipPlans
from tests.helpers.test_helpers import TestHelpers
import tests.helpers.constants as constants

scenarios('membership_plans/')


def customer_can_view_membership_plan():
    """Verify a customer can view membership plan."""
    pass


@when('I perform GET request to view all available membership plans')
def view_all_available_membership_plans(register_user):
    token = register_user.json().get('api_key')
    response = MembershipPlans.get_all_membership_plans(token)
    if response is not None:
        logging.info('GET/Membership_plans is working as expected')


@then(parsers.parse('I can ensure the "{merchant}" plan details match with expected data'))
def ensure_the_merchants_plan_details_match_with_expected_data(merchant, register_user):
    """GET a merchant's membership plan and compare with
     expected membership plan of that merchant"""

    token = register_user.json().get('api_key')
    response = MembershipPlans.get_membership_plan(token, merchant)
    logging.info('The Membership plan for ' + merchant + ' is: \n' + json.dumps(response.json(), indent=4))
    with open(TestHelpers.get_expected_membership_plan_json(merchant)) as json_file:
        json_data = json.load(json_file)
    stored_json = json.dumps(json_data)
    expected_membership_plan = json.loads(stored_json)
    actual_membership_plan = response.json()
    difference = json_compare(actual_membership_plan, expected_membership_plan)
    if json.dumps(difference) != '{}':
        logging.info('The expected and actual membership plan of ' + merchant + ' has following differences' +
                     json.dumps(difference, sort_keys=True, indent=4))
        raise Exception('The expected and actual membership plan of ' + merchant + ' is not the same')
    else:
        logging.info('The expected and actual membership plan of' + merchant + 'is same')


def json_compare(actual_membership_plan, expected_membership_plan):
    """This function will compare two Json objects using json_diff and
    create a third json with comparison results """

    json.dump(actual_membership_plan, open(constants.JSON_DIFF_ACTUAL_JSON, "w"), indent=4)
    json.dump(expected_membership_plan, open(constants.JSON_DIFF_EXPECTED_JSON, "w"), indent=4)
    actual_membership_plan = open(constants.JSON_DIFF_ACTUAL_JSON, "r")
    expected_membership_plan = open(constants.JSON_DIFF_EXPECTED_JSON, "r")
    engine = Comparator(actual_membership_plan, expected_membership_plan)
    return engine.compare_dicts()
