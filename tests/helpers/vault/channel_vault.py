import json
import logging
import time
from enum import Enum
import requests
from settings import LOCAL_SECRETS_PATH, LOCAL_CHANNELS, VAULT_URL, CHANNEL_SECRET_NAME

from azure.core.exceptions import ServiceRequestError, ResourceNotFoundError, HttpResponseError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

logger = logging.getLogger(__name__)
loaded = False
_bundle_secrets = {}

logging.basicConfig(level=logging.INFO)
logging.getLogger("azure").setLevel(logging.ERROR)


class KeyType(str, Enum):
    PRIVATE_KEY = "private_key"
    PUBLIC_KEY = "public_key"


class KeyVaultError(Exception):
    pass


def retry_get_secrets_from_vault():
    retries = 3
    exception = RuntimeError("Failed to get secrets from Vault")
    for _ in range(retries):
        try:
            client = SecretClient(vault_url=VAULT_URL, credential=DefaultAzureCredential())
            # secret = client.get_secret(CHANNEL_SECRET_NAME)
            secrets = {}
            secrets_to_load = []

            secrets_in_vault = client.list_properties_of_secrets()

            for secret in secrets_in_vault:
                if 'ubiquity-channel' in secret.name:
                    secrets_to_load.append(secret.name)
                    logger.info(f"Found secret {secret.name}. Adding to load list")

            for secret_name in secrets_to_load:
                try:
                    secrets.update(json.loads(client.get_secret(secret_name).value))
                except Exception:
                    logger.error(f"Failed to load secret {secret_name}")

            return secrets

        except (ServiceRequestError, ResourceNotFoundError, HttpResponseError) as e:
            exception = e
            time.sleep(3)

    raise exception


def load_secrets():
    """
    Retrieves security credential values from channel storage vault and stores them
    in _bundle_secrets which are used as a cache.
    Secrets contained in _bundle_secrets are bundle specific.

    Example:

    _bundle_secrets = {
        "com.bink.wallet": {"key": "value"}
    }

    """
    global loaded
    global _bundle_secrets

    if loaded:
        logger.info("Tried to load the vault secrets more than once, ignoring the request.")

    elif LOCAL_CHANNELS:
        with open(LOCAL_SECRETS_PATH) as fp:
            all_secrets = json.load(fp)

        _bundle_secrets = all_secrets
        loaded = True

    else:
        try:
            bundle_secrets = retry_get_secrets_from_vault()
        except requests.RequestException as e:
            err_msg = f"JWT bundle secrets - Vault Exception {e}"
            logger.exception(err_msg)
            raise KeyVaultError(err_msg) from e

        _bundle_secrets = bundle_secrets
        loaded = True


def check_and_load_vault():
    if not _bundle_secrets:
        load_secrets()


def get_jwt_secret(bundle_id):
    check_and_load_vault()
    try:
        return _bundle_secrets[bundle_id]['jwt_secret']
    except KeyError as e:
        raise KeyVaultError(f"No JWT secret found for bundle: {bundle_id}") from e


def get_key(bundle_id, key_type: str):
    check_and_load_vault()
    try:
        return _bundle_secrets[bundle_id][key_type]
    except KeyError as e:
        raise KeyVaultError(f"Unable to locate {key_type} in vault for bundle {bundle_id}") from e
