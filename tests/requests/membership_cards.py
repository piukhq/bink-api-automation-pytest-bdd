import tests.api as api
import time
import logging
from tests.helpers.test_helpers import Merchant
from tests.helpers.test_helpers import TestData
from tests.api.base import Endpoint
import tests.helpers.constants as constants


class MembershipCards(Endpoint):

    # ---------------------------------------- Add Journey---------------------------------------------------
    @staticmethod
    def add_card(token, merchant, invalid_data=None):
        url = MembershipCards.get_url()
        header = Endpoint.request_header(token)
        if not invalid_data:
            payload = Merchant.get_merchant(merchant).add_membership_card_payload()
        else:
            payload = Merchant.get_merchant(merchant).add_membership_card_payload(invalid_data)
        return Endpoint.call(url, header, "POST", payload)

    @staticmethod
    def add_card_auto_link(token, merchant, card_2=None):
        url = Endpoint.BASE_URL + api.ENDPOINT_AUTO_LINK_PAYMENT_AND_MEMBERSHIP_CARD
        header = Endpoint.request_header(token)
        if not card_2:
            payload = Merchant.get_merchant(merchant).add_membership_card_payload()

        if card_2:
            payload = Merchant.get_merchant(merchant).add_membership_card_2_payload()
        return Endpoint.call(url, header, "POST", payload)

    @staticmethod
    def patch_add_card(token, scheme_account_id, merchant):
        url = MembershipCards.get_url(scheme_account_id)
        header = Endpoint.request_header(token)
        payload = Merchant.get_merchant(merchant).add_membership_card_payload()
        return Endpoint.call(url, header, "PATCH", payload)

    # ---------------------------------------- Enrol Journey---------------------------------------------------
    @staticmethod
    def enrol_customer(token, merchant, email, env=None, channel=None, invalid_data=None):
        """"Including channel as an input as for iceland the enrol is different for
        Bink & Barclays"""

        url = MembershipCards.get_url()
        header = Endpoint.request_header(token)
        if not invalid_data:
            payload = Merchant.get_merchant(merchant).enrol_membership_scheme_payload(email, env, channel)
        else:
            payload = Merchant.get_merchant(merchant).enrol_membership_scheme_payload(email, env, channel, invalid_data)
        return Endpoint.call(url, header, "POST", payload)

    @staticmethod
    def put_enrol_customer(token, scheme_account_id, merchant, email, env=None, channel=None):

        url = MembershipCards.get_url(scheme_account_id)
        header = Endpoint.request_header(token)
        payload = Merchant.get_merchant(merchant).enrol_membership_scheme_payload(email, env, channel)
        return Endpoint.call(url, header, "PUT", payload)

    @staticmethod
    def register_ghost_card(token, merchant):
        # url = MembershipCards.get_url()
        pass

    # ---------------------------------------- Ghost Card Registration -------------------------------------------
    @staticmethod
    def patch_ghost_card(token, merchant):
        # url = MembershipCards.get_url()
        pass

    @staticmethod
    def get_scheme_account(token, scheme_account_id):
        time.sleep(10)
        """Waiting max up to 30 sec to change status from Pending to Authorized"""
        for i in range(1, 30):
            url = MembershipCards.get_url(scheme_account_id)
            header = Endpoint.request_header(token)
            response = Endpoint.call(url, header, "GET")
            response_json = response.json()
            if response_json["status"]["state"] == TestData.get_membership_card_status_states().get(constants.PENDING):
                time.sleep(1)
            else:
                break
        return response

    @staticmethod
    def get_scheme_account_auto_link(token, scheme_account_id, is_autolink=None):
        """Waiting max up to 30 sec to change status from Pending to Authorized"""
        time.sleep(5)
        for i in range(1, 30):
            url = MembershipCards.get_url(scheme_account_id)
            header = Endpoint.request_header(token)
            response = Endpoint.call(url, header, "GET")
            response_json = response.json()
            try:
                if is_autolink is not None:
                    return response
                else:
                    if not response_json["payment_cards"][0]["active_link"]:
                        time.sleep(1)
                    else:
                        break
            except IndexError:
                time.sleep(1)
                logging.info("Wait for payment card array to populate")
        return response

    @staticmethod
    def get_membership_card_balance(token, scheme_account_id):
        """Waiting max up to 30 sec to change status from Pending to Authorized"""
        for i in range(1, 30):
            ele_present = "no"
            current_membership_card_response = ""
            url = Endpoint.BASE_URL + api.ENDPOINT_CHECK_MEMBERSHIP_CARDS_BALANCE
            header = Endpoint.request_header(token)
            response = Endpoint.call(url, header, "GET")
            assert response.status_code == 200, "Validations in GET/membership_cards?balances failed"
            response_json = response.json()
            for current_membership_card in response_json:
                if current_membership_card["id"] == scheme_account_id:
                    if current_membership_card["status"]["state"] == TestData.get_membership_card_status_states(). \
                            get(constants.PENDING):
                        time.sleep(1)
                        break
                    else:
                        ele_present = "yes"
                        current_membership_card_response = current_membership_card
                        break
            if ele_present == "yes":
                break
        return current_membership_card_response

    # Delete Membership Card
    @staticmethod
    def delete_scheme_account(token, scheme_account_id):
        url = MembershipCards.get_url(scheme_account_id)
        header = Endpoint.request_header(token)
        response = Endpoint.call(url, header, "DELETE")
        return response

    @staticmethod
    def get_url(scheme_account_id=None):
        """Return URL for membership_cards and
         membership_card/scheme_account_id"""
        if scheme_account_id is None:
            return Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS
        else:
            return Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD.format(scheme_account_id)

    @staticmethod
    def enrol_delete_add_card(token, merchant, email):
        url = MembershipCards.get_url()
        header = Endpoint.request_header(token)
        payload = Merchant.get_merchant(merchant).enrol_delete_add_membership_card_payload(email)
        return Endpoint.call(url, header, "POST", payload)

    @staticmethod
    def delete_existing_scheme_account(token):
        url = MembershipCards.get_url()
        header = Endpoint.request_header(token)
        response = Endpoint.call(url, header, "GET")
        response_json = response.json()
        if(response_json != []):
            for current_membership_card in response_json:
                MembershipCards.delete_scheme_account(token, current_membership_card.get("id"))
        return response_json
