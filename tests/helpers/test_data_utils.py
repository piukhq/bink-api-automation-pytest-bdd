import config

class TestDataUtils:

    TEST_DATA = ''

    @staticmethod
    def set_test_data(env):
        if env == 'dev':
            TestDataUtils.TEST_DATA = config.DEV.test_data
        elif env == 'staging':
            TestDataUtils.TEST_DATA = config.STAGING.test_data
    @staticmethod
    def get_burger_king_card_num1():
        return TestDataUtils.TEST_DATA.burger_king_membership_card1.get('card_num')

    @staticmethod
    def get_burger_king_card_num2():
        return TestDataUtils.TEST_DATA.burger_king_membership_card1.get('card_num')

    @staticmethod
    def get_burger_king_card_num2():
        return TestDataUtils.TEST_DATA.burger_king_membership_card1.get('card_num')
