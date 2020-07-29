import config


class TestDataUtils:
    """Setting the test data sheet based on the environment"""

    TEST_DATA = ""

    @staticmethod
    def set_test_data(env):
        if env == "dev":
            TestDataUtils.TEST_DATA = config.DEV.test_data
        elif env == "staging":
            TestDataUtils.TEST_DATA = config.STAGING.test_data
