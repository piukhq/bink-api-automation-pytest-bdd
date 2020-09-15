class TestContext:
    current_scheme_account_id = ""
    current_payment_card_id = ""
    token = ""
    """Below variables are used to ensure complete execution
     and deletion of membership& payment cards after ubiquity scenarios"""

    channel_name = ""
    token_channel_1 = ""
    scheme_account_id1 = ""

    @staticmethod
    def set_scheme_account(scheme_account_id):
        TestContext.current_scheme_account_id = scheme_account_id

    @staticmethod
    def get_scheme_account_id():
        return TestContext.current_scheme_account_id

    @staticmethod
    def set_payment_card_id(payment_card_id):
        TestContext.current_payment_card_id = payment_card_id

    @staticmethod
    def get_payment_card_id():
        return TestContext.current_payment_card_id

    @staticmethod
    def set_token(token):
        TestContext.token = token

    @staticmethod
    def get_token():
        return TestContext.token

    @staticmethod
    def set_channel(channel_name):
        TestContext.channel_name = channel_name

    @staticmethod
    def get_channel():
        return TestContext.channel_name

    @staticmethod
    def set_token_channel_1(token_channel_1):
        TestContext.token_channel_1 = token_channel_1

    @staticmethod
    def get_token_channel_1():
        return TestContext.token_channel_1

    @staticmethod
    def set_scheme_account_id_1(scheme_account_id1):
        TestContext.scheme_account_id1 = scheme_account_id1

    @staticmethod
    def get_scheme_account_id_1():
        return TestContext.scheme_account_id1
