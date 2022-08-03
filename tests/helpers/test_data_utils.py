import config
from settings import logger


class TestDataUtils:
    """Setting the test data sheet based on the environment"""

    @staticmethod
    def set_test_data(env):
        # TestDataUtils.TEST_DATA = EnvironmentDetails.return_current_env(env).test_data
        TestDataUtils.TEST_DATA = getattr(config, env.upper()).test_data

        logger.info("ENV: " + env)
        logger.info("ATTRIBUTES: " + str(getattr(config, env.upper())))
        logger.info("TEST_DATA: " + str(TestDataUtils.TEST_DATA.master_payment_card))
