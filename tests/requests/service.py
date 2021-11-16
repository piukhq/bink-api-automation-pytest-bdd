import config
import tests.api as api
from tests.api.base import Endpoint
from tests.payload.service.customer_accounts import UserDetails
from tests.payload.service.jwt_token import GenerateJWToken
from tests.helpers.vault import channel_vault
from tests.helpers.test_context import TestContext


class CustomerAccount:
    """Functions used to Create a new user, Service consent and Delete a user
    and
    Login using an existing user(User Login credentials are kept in test_data_sheet based in environment)"""

    @staticmethod
    def register_bink_user(test_email):
        url = Endpoint.BASE_URL + api.ENDPOINT_REGISTER
        headers = Endpoint.request_header()
        payload = UserDetails.register_user_payload(test_email, config.BINK.client_id, config.BINK.bundle_id)
        response = Endpoint.call(url, headers, "POST", payload)
        TestContext.token = response.json().get("api_key")
        return response

    @staticmethod
    def service_consent_bink_user(token, test_email):
        url = Endpoint.BASE_URL + api.ENDPOINT_SERVICE
        headers = Endpoint.request_header(token)
        payload = UserDetails.consent_user_payload(test_email)
        return Endpoint.call(url, headers, "POST", payload)

    @staticmethod
    def without_service_consent_bink_user(token):
        url = Endpoint.BASE_URL + api.ENDPOINT_SERVICE
        headers = Endpoint.request_header(token)
        payload = UserDetails.without_consent_user_payload()
        return Endpoint.call(url, headers, "POST", payload)

    @staticmethod
    def without_consent_key_bink_user(token):
        url = Endpoint.BASE_URL + api.ENDPOINT_SERVICE
        headers = Endpoint.request_header(token)
        payload = UserDetails.without_consent_key_user_payload()
        return Endpoint.call(url, headers, "POST", payload)

    @staticmethod
    def without_mandatory_consent_field(token):
        url = Endpoint.BASE_URL + api.ENDPOINT_SERVICE
        headers = Endpoint.request_header(token)
        payload = UserDetails.without_mandatory_consent_field()
        return Endpoint.call(url, headers, "POST", payload)

    @staticmethod
    def longitude_as_alphabet(token, test_email):
        url = Endpoint.BASE_URL + api.ENDPOINT_SERVICE
        headers = Endpoint.request_header(token)
        payload = UserDetails.longitude_with_alphabet(test_email)
        return Endpoint.call(url, headers, "POST", payload)

    @staticmethod
    def optional_consent_field(token, input, test_email):
        if input == "timestamp":
            url = Endpoint.BASE_URL + api.ENDPOINT_SERVICE
            headers = Endpoint.request_header(token)
            payload = UserDetails.timestamp_with_quote(test_email)
            return Endpoint.call(url, headers, "POST", payload)

        elif input == "latitude":
            url = Endpoint.BASE_URL + api.ENDPOINT_SERVICE
            headers = Endpoint.request_header(token)
            payload = UserDetails.without_latitude(test_email)
            return Endpoint.call(url, headers, "POST", payload)

        elif input == "longitude":
            url = Endpoint.BASE_URL + api.ENDPOINT_SERVICE
            headers = Endpoint.request_header(token)
            payload = UserDetails.without_longitude(test_email)
            return Endpoint.call(url, headers, "POST", payload)

    @staticmethod
    def login_bink_user():
        url = Endpoint.BASE_URL + api.ENDPOINT_LOGIN
        headers = Endpoint.request_header()
        client_id = config.BINK.client_id
        payload = UserDetails.bink_login_user_payload(client_id, config.BINK.bundle_id)
        response = Endpoint.call(url, headers, "POST", payload)
        TestContext.token = response.json().get("api_key")
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
        TestContext.token = bearer_token
        url = Endpoint.BASE_URL + api.ENDPOINT_SERVICE
        headers = Endpoint.request_header(bearer_token)
        payload = UserDetails.register_bearer_user_payload(test_email)
        return Endpoint.call(url, headers, "POST", payload)

    @staticmethod
    def without_service_consent_banking_user(test_email):
        jwt_secret = channel_vault.get_jwt_secret(config.BARCLAYS.bundle_id)
        bearer_token = GenerateJWToken(config.BARCLAYS.organisation_id, jwt_secret, config.BARCLAYS.bundle_id,
                                       test_email).get_token()
        TestContext.token = bearer_token
        return TestContext.token

    @staticmethod
    def get_secret_key(env):
        """Temporary function to get secret keys (dev& staging) from config
        till the secret keys are taken from Vault"""
        if env == "dev":
            return config.BARCLAYS.secret_key_dev
        elif env == "staging":
            return config.BARCLAYS.secret_key_staging
