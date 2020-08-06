import config
import tests.api as api
from tests.api.base import Endpoint
from tests.payload.service.customer_accounts import UserDetails


class CustomerAccount:
    @staticmethod
    def create_user(test_email, channel, env):
        url = Endpoint.BASE_URL + api.ENDPOINT_REGISTER
        headers = Endpoint.request_header()
        client_id = CustomerAccount.get_client_id(channel, env)
        if channel == config.BINK.channel_name:
            payload = UserDetails.register_user_payload(test_email, client_id, config.BINK.bundle_id)
        elif channel == config.BARCLAYS.channel_name:
            payload = UserDetails.register_user_payload(test_email, client_id, config.BARCLAYS.bundle_id)
        return Endpoint.call(url, headers, "POST", payload)

    @staticmethod
    def create_consent(token, test_email):
        url = Endpoint.BASE_URL + api.ENDPOINT_SERVICE
        headers = Endpoint.request_header(token)
        payload = UserDetails.consent_user_payload(test_email)
        return Endpoint.call(url, headers, "POST", payload)

    @staticmethod
    def login_user(channel, env):

        url = Endpoint.BASE_URL + api.ENDPOINT_LOGIN
        headers = Endpoint.request_header()
        client_id = CustomerAccount.get_client_id(channel, env)
        if channel == config.BINK.channel_name:
            payload = UserDetails.bink_login_user_payload(client_id, config.BINK.bundle_id)
        elif channel == config.BARCLAYS.channel_name:
            payload = UserDetails.barclays_login_user_payload(client_id, config.BARCLAYS.bundle_id)
        return Endpoint.call(url, headers, "POST", payload)

    @staticmethod
    def get_client_id(channel, env):
        if channel == config.BINK.channel_name:
            channel = config.BINK
        elif channel == config.BARCLAYS.channel_name:
            channel = config.BARCLAYS
        if env == "dev":
            return channel.client_id_dev
        elif env == "staging":
            return channel.client_id_staging
        elif env == "prod":
            return channel.client_id_prod
