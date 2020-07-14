import tests.api as api
import json
import jsonpath
import time
import logging

from tests.payload.membership_cards.burgerking import BurgerKingCard
from tests.payload.membership_cards.cooperative import CoopCard
from tests.payload.membership_cards.fatface import FatFaceCard
from tests.payload.membership_cards.harvey_nichols import HarveyNicholsCard
from tests.payload.membership_cards.iceland import IcelandCard
from tests.payload.membership_cards.whsmith import WHSmithCard
from tests.payload.membership_cards.wasabi import WasabiCard

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
    def add_card_auto_link(token, merchant):
        url = Endpoint.BASE_URL + api.ENDPOINT_AUTO_LINK_PAYMENT_AND_MEMBERSHIP_CARD_URL
        header = Endpoint.request_header(token)
        payload = MembershipCards.get_merchant(merchant).add_membership_card_payload()
        return Endpoint.call(url, header, "POST", payload)

    @staticmethod
    def patch_add_card(token, scheme_account_id, merchant):
        url = MembershipCards.get_url(scheme_account_id)
        header = Endpoint.request_header(token)
        payload = MembershipCards.get_merchant(merchant).add_membership_card_payload()
        return Endpoint.call(url, header, "PATCH", payload)

    # ---------------------------------------- Enrol Journey---------------------------------------------------
    @staticmethod
    def put_enrol_customer(token, merchant):

        url = MembershipCards.get_url()

    @staticmethod
    def register_ghost_card(token, merchant):

        url = MembershipCards.get_url()

    # ---------------------------------------- Ghost Card Registration -------------------------------------------
    @staticmethod
    def patch_ghost_card(token, merchant):

        url = MembershipCards.get_url()

    @staticmethod
    def get_scheme_account(token, scheme_account_id):
        """Waiting max up to 30 sec to change status from Pending to Authorized"""
        for i in range(1, 30):
            url = MembershipCards.get_url(scheme_account_id)
            header = Endpoint.request_header(token)
            response = Endpoint.call(url, header, "GET")
            response_json = response.json()
            if response_json['status']['state'] == Endpoint.TEST_DATA.membership_account_states.get('state_pending'):
                time.sleep(1)
            else:
                break
        return response
        # Get Membership Card

    # Get Membership Card
    @staticmethod
    def get_scheme_account_auto_link(token):
        """Waiting max up to 30 sec to change status from Pending to Authorized"""
        for i in range(1, 30):
            url = Endpoint.BASE_URL + api.ENDPOINT_AUTO_LINK_PAYMENT_AND_MEMBERSHIP_CARD_URL
            header = Endpoint.request_header(token)
            response = Endpoint.call(url, header, "GET")
            response_json = response.json()
            if response_json[0]['status']['state'] == Endpoint.TEST_DATA.membership_account_states.get('state_pending'):
                time.sleep(1)
            else:
                break
        return response

    @staticmethod
    def get_membership_card_balance(token):
        """Waiting max up to 30 sec to change status from Pending to Authorized"""
        for i in range(1, 30):
            url = Endpoint.BASE_URL + api.ENDPOINT_CHECK_MEMBERSHIP_CARDS_BALANCE_URL
            header = Endpoint.request_header(token)
            response = Endpoint.call(url, header, "GET")
            response_json = response.json()
            if response_json[0]['status']['state'] == Endpoint.TEST_DATA.membership_account_states.get('state_pending'):
                time.sleep(1)
            else:
                break
        return response
    @staticmethod
    def enrol_customer(token, merchant, email, invalid_data=None):

        url = MembershipCards.get_url()
        header = Endpoint.request_header(token)
        if not invalid_data:
            payload = MembershipCards.get_merchant(merchant).enrol_membership_scheme_payload(email)
        else:
            payload = MembershipCards.get_merchant(merchant).enrol_membership_scheme_payload(email,invalid_data)
        return Endpoint.call(url, header, "POST", payload)


    # Delete Membership Card
    @staticmethod
    def delete_scheme_account(token, scheme_account_id):
        url = MembershipCards.get_url(scheme_account_id)
        header = Endpoint.request_header(token)
        response = Endpoint.call(url, header, "DELETE")
        return response

    @staticmethod
    def get_url(scheme_account_id=None):
        if scheme_account_id is None:
            return Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS
        else:
            return Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(scheme_account_id)

    @staticmethod
    def get_merchant(merchant):
        switcher = {
            'BurgerKing': BurgerKingCard,
            'CooP': CoopCard,
            'FatFace': FatFaceCard,
            'HarveyNichols': HarveyNicholsCard,
            'Iceland': IcelandCard,
            'WHSmith': WHSmithCard,
            'Wasabi': WasabiCard
        }

        return switcher.get(merchant)
