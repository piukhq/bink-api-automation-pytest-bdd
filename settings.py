import logging
import os

from environment import env_var, read_env

os.chdir(os.path.dirname(__file__))
read_env()

logging.basicConfig(format="%(process)s %(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("automation_tests_logger")
logger.setLevel(logging.DEBUG)

LOCAL_CHANNELS = env_var("LOCAL_CHANNELS", False)
LOCAL_SECRETS_PATH = env_var("LOCAL_SECRETS_PATH", "vault/local_channels.json")
VAULT_URL = env_var("VAULT_URL", "http://localhost:8200")
CHANNEL_VAULT_PATH = env_var("CHANNEL_VAULT_PATH", "/channels")
