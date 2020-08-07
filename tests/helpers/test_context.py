class TestContext:
    current_scheme_account_id = ""
    token = ""

    @staticmethod
    def set_scheme_account(scheme_account_id):
        TestContext.current_scheme_account_id = scheme_account_id

    @staticmethod
    def get_scheme_account_id():
        return TestContext.current_scheme_account_id

    @staticmethod
    def set_token(token):
        TestContext.token = token

    @staticmethod
    def get_token():
        return TestContext.token
