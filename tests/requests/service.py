import config
import time
import tests.api as api
from tests.api.base import Endpoint
from tests.payload.service.customer_accounts import UserDetails


class CustomerAccount:
    @staticmethod
    def create_user(test_email, channel):
        url = Endpoint.BASE_URL + api.ENDPOINT_REGISTER
        headers = Endpoint.request_header()
        if channel == config.BINK.channel_name:
            payload = UserDetails.register_user_payload(test_email, config.BINK.client_id, config.BINK.bundle_id)
        elif channel == config.BARCLAYS.channel_name:
            payload = UserDetails.register_user_payload(
                test_email, config.BARCLAYS.client_id, config.BARCLAYS.bundle_id
            )
        return Endpoint.call(url, headers, "POST", payload)

    @staticmethod
    def create_consent(token, test_email):
        url = Endpoint.BASE_URL + api.ENDPOINT_SERVICE
        headers = Endpoint.request_header(token)
        payload = UserDetails.consent_user_payload(test_email)
        return Endpoint.call(url, headers, "POST", payload)

    @staticmethod
    def login_user(channel):

        url = Endpoint.BASE_URL + api.ENDPOINT_LOGIN
        headers = Endpoint.request_header()
        if channel == config.BINK.channel_name:
            payload = UserDetails.login_user_payload(config.BINK.client_id, config.BINK.bundle_id)
        elif channel == config.BARCLAYS.channel_name:
            payload = UserDetails.login_user_payload(config.BARCLAYS.client_id, config.BARCLAYS.bundle_id)
        return Endpoint.call(url, headers, "POST", payload)
