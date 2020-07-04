import tests.api as api
import json
import jsonpath
import time
import logging
from tests.payload.membership_cards.burgerking import BKCard
from tests.payload.membership_cards.cooperative import CoopCard
from tests.payload.membership_cards.fatface import FFCard
from tests.payload.membership_cards.harvey_nichols import HNCard
from tests.payload.membership_cards.iceland import IcelandCard
from tests.api.base import Endpoint


class MembershipCards(Endpoint):

    # ---------------------------------------- Add Journey---------------------------------------------------
    @staticmethod
    def add_card(token, merchant, invalid_data=None):
        url = MembershipCards.get_url()
        header = Endpoint.request_header(token)
        if not invalid_data:
            payload = MembershipCards.get_merchant(merchant).add_membership_card_payload()
        else:
            payload = MembershipCards.get_merchant(merchant).add_membership_card_payload(invalid_data)
        return Endpoint.call(url, header, "POST", payload)

    @staticmethod
    def patch_add_card(token, scheme_account_id, merchant):
        url = MembershipCards.get_url(scheme_account_id)
        header = Endpoint.request_header(token)
        payload = MembershipCards.get_merchant(merchant).add_membership_card_payload()
        return Endpoint.call(url, header, "PATCH", payload)

    # ---------------------------------------- Enrol Journey---------------------------------------------------
    @staticmethod
    def enrol_customer(token, merchant):

        url = MembershipCards.get_url()
        header = Endpoint.request_header(token)
        if merchant == 'burgerking':
            payload = BKCard.enrol_membership_scheme()
        elif merchant == 'coop':
            payload = CoopCard.enrol_membership_scheme()
        elif merchant == 'fatface':
            payload = FFCard.enrol_membership_scheme()
        elif merchant == 'harvey-nichols':
            payload = HNCard.enrol_membership_scheme()
        elif merchant == 'iceland':
            payload = IcelandCard.enrol_membership_scheme()

        return Endpoint.call(MembershipCards.get_url(), Endpoint.request_header(token), "POST", payload)

    @staticmethod
    def put_enrol_customer(token, merchant):

        url = MembershipCards.get_url()

    # ---------------------------------------- Ghost Card Registration -------------------------------------------
    @staticmethod
    def register_ghost_card(token, merchant):

        url = MembershipCards.get_url()

    @staticmethod
    def patch_ghost_card(token, merchant):

        url = MembershipCards.get_url()

    # Get Membership Card
    @staticmethod
    def get_scheme_account(token, scheme_account_id):
        """Waiting max up to 30 sec to change status from Pending to Authorized"""
        for i in range(1, 30):
            response = Endpoint.call(MembershipCards.get_url(scheme_account_id), Endpoint.request_header(token), "GET")
            response_json = response.json()
            if response_json['status']['state'] == Endpoint.TEST_DATA.membership_account_states.get('state_pending'):
                time.sleep(1)
            else:
                break
        return response
        # return Endpoint.call(MembershipCards.get_url(scheme_account_id), Endpoint.request_header(token), "GET")

    # Delete Membership Card
    @staticmethod
    def delete_scheme_account(token, scheme_account_id):

        return Endpoint.call(MembershipCards.get_url(scheme_account_id), Endpoint.request_header(token), "DELETE")

    @staticmethod
    def get_url(scheme_account_id=None):

        if scheme_account_id is None:
            return Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS
        else:
            return Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(scheme_account_id)

    @staticmethod
    def get_merchant(merchant):
        switcher = {
            'burgerking': BKCard,
            'coop': CoopCard,
            'fatface': FFCard,
            'harvey-nichols': HNCard,
            'iceland': IcelandCard,
            'whsmith': '',
            'wasabi': ''
        }
        return switcher.get(merchant)
