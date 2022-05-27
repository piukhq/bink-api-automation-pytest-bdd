import time
import logging
from json.decoder import JSONDecodeError

import tests.api as api
from tests.api.base import Endpoint


class MembershipTransactions(Endpoint):
    @staticmethod
    def get_all_membership_transactions(token):
        url = Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_TRANSACTIONS
        header = Endpoint.request_header(token)
        for i in range(1, 30):
            response = Endpoint.call(url, header, "GET")
            try:
                response_json = response.json()
                if not response_json[0]["status"] == "active":
                    time.sleep(1)
                else:
                    break
            except JSONDecodeError:
                logging.info(
                    "The response text:  " + response.text + "\n The response Status Code: " + str(response.status_code)
                )
                time.sleep(1)
                logging.info(
                    "No response generated for end point " + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_TRANSACTIONS
                )

        return response

    @staticmethod
    def get_membership_transactions(token, membership_card_id):
        url = Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD_TRANSACTIONS.format(membership_card_id)
        header = Endpoint.request_header(token)
        for i in range(1, 30):
            response = Endpoint.call(url, header, "GET")
            try:
                response_json = response.json()
                if not response_json[0]["status"] == "active":
                    time.sleep(i)
                    continue
                else:
                    break
            except JSONDecodeError:
                logging.info(
                    "The response text:  " + response.text + "\n The response Status Code: " + str(response.status_code)
                )
                time.sleep(i)
                logging.info("No response generated for end point " + url)
        return response

    @staticmethod
    def get_membership_card_single_transaction_detail(token, transaction_id):
        url = Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARD_SINGLE_TRANSACTION.format(transaction_id)
        header = Endpoint.request_header(token)
        response = Endpoint.call(url, header, "GET")
        logging.info("The response text:  " + response.text + "\n Response Status Code: " + str(response.status_code))
        return response
