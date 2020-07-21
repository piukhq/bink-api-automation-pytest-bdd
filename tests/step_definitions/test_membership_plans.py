from pytest_bdd import (
    scenarios,
    then,
    when,
    parsers,
)
import pytest
import json
import jsonpath
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
    MembershipPlans.get_all_membership_plans(token)


@then(parsers.parse('I can ensure the "{merchant}" plan details match with expected data'))
def ensure_the_merchants_plan_details_match_with_expected_data(merchant, register_user):
    """GET a merchant's membership plan and compare with
     expected membership plan of that merchant"""

    token = register_user.json().get('api_key')
    MembershipPlans.get_membership_plan(token, merchant)
