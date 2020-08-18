import config
import tests.api as api
from tests.api.base import Endpoint
from tests.payload.service.customer_accounts import UserDetails
import logging


class CustomerAccount:
    """Functions used to Create a new user, Service consent and Delete a user
    and
    Login using an existing user(User Login credentials are kept in test_data_sheet based in environment)"""

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
    def delete_new_user(token):
        url = Endpoint.BASE_URL + api.ENDPOINT_SERVICE
        headers = Endpoint.request_header(token)
        return Endpoint.call(url, headers, "DELETE")

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
    def return_jwt_token(test_email, env):
        """Generate JWT token for External channel"""
        return UserDetails.generate_jwt_token(test_email, "unused", config.BARCLAYS.bundle_id,
                                              config.BARCLAYS.organisation_id, CustomerAccount.get_secret_key(env))

    @staticmethod
    def register_bearer_user(jwt_token, test_email):
        """Register user using Service endpoint & bearer token"""
        url = Endpoint.BASE_URL + api.ENDPOINT_SERVICE
        headers = Endpoint.request_header(jwt_token)
        logging.info(headers)
        payload = UserDetails.register_bearer_user_payload(test_email)
        logging.info(payload)
        return Endpoint.call(url, headers, "POST", payload)

    @staticmethod
    def get_client_id(channel, env):
        """Get the client_ids based on channel & environment"""
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

    @staticmethod
    def get_secret_key(env):
        """Temporary function to get secret keys (dev& staging) from config
        till the secret keys are taken from Vault"""
        if env == "dev":
            return config.BARCLAYS.secret_key_dev
        elif env == "staging":
            return config.BARCLAYS.secret_key_staging
