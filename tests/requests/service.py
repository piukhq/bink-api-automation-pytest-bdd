import config
import tests.api as api
from tests.api.base import Endpoint
from tests.payload.service.customer_accounts import UserDetails
from tests.helpers.test_data_utils import TestDataUtils
from tests.payload.service.jwt_token import GenerateJWToken
from tests.helpers.vault import channel_vault
from tests.helpers.test_context import TestContext


class CustomerAccount:
    """Functions used to Create a new user, Service consent and Delete a user
    and
    Login using an existing user(User Login credentials are kept in test_data_sheet based in environment)"""

    @staticmethod
    def register_bink_user(test_email, channel, env):
        url = Endpoint.BASE_URL + api.ENDPOINT_REGISTER
        headers = Endpoint.request_header()
        client_id = CustomerAccount.get_client_id(channel, env)
        payload = UserDetails.register_user_payload(test_email, client_id, config.BINK.bundle_id)
        response = Endpoint.call(url, headers, "POST", payload)
        TestContext.set_token(response.json().get("api_key"))
        return response

    @staticmethod
    def service_consent_bink_user(token, test_email):
        url = Endpoint.BASE_URL + api.ENDPOINT_SERVICE
        headers = Endpoint.request_header(token)
        payload = UserDetails.consent_user_payload(test_email)
        return Endpoint.call(url, headers, "POST", payload)

    @staticmethod
    def login_bink_user(channel, env):

        url = Endpoint.BASE_URL + api.ENDPOINT_LOGIN
        headers = Endpoint.request_header()
        client_id = CustomerAccount.get_client_id(channel, env)
        payload = UserDetails.bink_login_user_payload(client_id, config.BINK.bundle_id)
        response = Endpoint.call(url, headers, "POST", payload)
        TestContext.set_token(response.json().get("api_key"))
        return response

    @staticmethod
    def delete_new_user(token):
        url = Endpoint.BASE_URL + api.ENDPOINT_SERVICE
        headers = Endpoint.request_header(token)
        return Endpoint.call(url, headers, "DELETE")

    @staticmethod
    def service_consent_banking_user(test_email):
        """The Banking user creation has to be handled by ubiquity/service endpoint
        New Email Id : 201 Response
        Existing Banking user already subscribed to Bink : 200 Response"""
        jwt_secret = channel_vault.get_jwt_secret(config.BARCLAYS.bundle_id)
        bearer_token = GenerateJWToken(config.BARCLAYS.organisation_id, jwt_secret, config.BARCLAYS.bundle_id,
                                       test_email).get_token()
        TestContext.set_token(bearer_token)
        url = Endpoint.BASE_URL + api.ENDPOINT_SERVICE
        headers = Endpoint.request_header(bearer_token)
        payload = UserDetails.register_bearer_user_payload(test_email)
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
