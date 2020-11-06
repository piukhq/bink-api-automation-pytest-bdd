import json
import logging
import time
from enum import Enum

import requests
from settings import LOCAL_SECRETS_PATH, LOCAL_CHANNELS, VAULT_URL, CHANNEL_VAULT_PATH
from shared_config_storage.vault.secrets import VaultError, read_vault

logger = logging.getLogger(__name__)
loaded = False
_bundle_secrets = {}


class KeyType(str, Enum):
    PRIVATE_KEY = "private_key"
    PUBLIC_KEY = "public_key"


def retry_get_secrets_from_vault():
    retries = 3
    exception = RuntimeError("Failed to get secrets from Vault")
    for _ in range(retries):
        try:
            bundle_secrets = read_vault(CHANNEL_VAULT_PATH, VAULT_URL, "")
            return bundle_secrets
        except (VaultError, ValueError) as e:
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
            raise VaultError(err_msg) from e

        # logger.info(f"JWT bundle secrets - Found secrets for {[bundle_secrets]}")
        # logger.info(f"JWT bundle secrets - Found secrets for {[bundle_id for bundle_id in bundle_secrets]}")
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
        raise VaultError(f"No JWT secret found for bundle: {bundle_id}") from e


def get_key(bundle_id, key_type: str):
    check_and_load_vault()
    try:
        return _bundle_secrets[bundle_id][key_type]
    except KeyError as e:
        raise VaultError(f"Unable to locate {key_type} in vault for bundle {bundle_id}") from e
