import config


class TestDataUtils:
    TEST_DATA = ''

    @staticmethod
    def set_test_data(env):
        if env == 'dev':
            TestDataUtils.TEST_DATA = config.DEV.test_data
        elif env == 'staging':
            TestDataUtils.TEST_DATA = config.STAGING.test_data
