import tests.api as api
import json
import jsonpath
import time
import logging
from tests.api.base import Endpoint
from tests.helpers.test_helpers import TestData


class MembershipPlans(Endpoint):

    @staticmethod
    def get_all_membership_plans(token):
        url = Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_PLANS
        header = Endpoint.request_header(token, "1.2")
        response = Endpoint.call(url, header, "GET")
        return response

    @staticmethod
    def get_membership_plan(token, merchant):
        url = Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_PLAN.format(TestData.get_membership_plan_id(merchant))
        header = Endpoint.request_header(token, "1.2")
        response = Endpoint.call(url, header, "GET")
        return response
