import logging
import os

from environment import env_var, read_env

os.chdir(os.path.dirname(__file__))
read_env()

logging.basicConfig(format="%(process)s %(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("automation_tests_logger")
logger.setLevel(logging.DEBUG)

LOCAL_CHANNELS = env_var("LOCAL_CHANNELS", False)
LOCAL_SECRETS_PATH = env_var("LOCAL_SECRETS_PATH", "tests/helpers/vault/local_channels.json")
VAULT_URL_STAGING = env_var("VAULT_URL", "https://uksouth-staging-232w.vault.azure.net/")
CHANNEL_SECRET_NAME = env_var("CHANNEL_SECRET_NAME", "channels")
BLOB_STORAGE_DSN = env_var("BLOB_STORAGE_DSN")
HERMES_DATABASE_URI = env_var("HERMES_DATABASE_URI")
HARMONIA_DATABASE_URI = env_var("HARMONIA_DATABASE_URI")
SNOWSTORM_DATABASE_URI = env_var("SNOWSTORM_DATABASE_URI")
