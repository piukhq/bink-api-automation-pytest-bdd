import tests.api as api
import json
import jsonpath
import time
import logging
from tests.api.base import Endpoint
from tests.helpers.test_helpers import TestHelpers


class MembershipPlans(Endpoint):

    @staticmethod
    def get_all_membership_plans(token):
        url = Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_PLANS
        header = Endpoint.request_header(token)
        response = Endpoint.call(url, header, "GET")
        logging.info('The Membership plans response is: \n' + json.dumps(response.json(), indent=4))
        return response

    @staticmethod
    def get_membership_plan(token, merchant):
        url = Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_PLAN.format(TestHelpers.get_membership_plan_id(merchant))
        header = Endpoint.request_header(token)
        response = Endpoint.call(url, header, "GET")
        logging.info('The Membership plan for ' + merchant+' is: \n' + json.dumps(response.json(), indent=4))
        return response
