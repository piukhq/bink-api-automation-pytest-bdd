"""Email Template"""
EMAIL_TEMPLATE = "pytest+regression_email@bink.com"

"""Constants for Enrol_Scheme Credential Questions"""
TITLE = "Mr"
DATE_OF_BIRTH = "01/01/2000"
PASSWORD_ENROL = "Password01"
EMAIL_MARKETING = "true"
CONSENT = "true"

""" Constants for Add Journey"""
CARD_NUM = "card_num"
REGISTER_FAILED_EMAIL = "register_failed_email"
UNKNOWN_CARD = "unknown_card"
UNKNOWN_LAST_NAME = "unknown_last_name"
CARD_NUM2 = "card_num2"
ERROR_LAST_NAME = "error_last_name"
TEST_LAST_NAME = "test_last_name"
JOIN_ACCOUNT_ALREADY_EXISTS = "email_exists"
JOIN_FAILED = "join_failed"
JOIN_HTTP_FAILED = "join_http_failed"
BARCODE = "barcode"
EMAIL = "email"
IDENTICAL_ENROL_EMAIL = "identical_enrol_email"
DOB = "dob"
POSTCODE = "postcode"
ID = "id"
PASSWORD = "password"
PASSWORD_ENCRYPTED = "password_encrypted"
LAST_NAME = "last_name"
PATCH_LAST_NAME = "patch_last_name"
POINTS = "points"
POINTS2 = "points2"
CURRENCY = "currency"
DESCRIPTION = "description"
TRANSACTIONS = "transactions"
TRANSACTIONS_STATUS = "transaction_status"
TRANSACTIONS_CURRENCY = "transaction_currency"

INPROGRESS_STATE = "inprogress_state"
ISSUED_STATE = "issued_state"
EXPIRED_STATE = "expired_state"
REDEEMED_STATE = "redeemed_state"
BURN_TYPE = "burn_type"
BURN_PREFIX = "burn_prefix"
EARN_PREFIX = "earn_prefix"
SUBTEXT = "subtext"
CODE = "code"


EARN_TYPE = "earn_type"
TARGET_VALUE = "target_value"
HEADLINE = "headline"
EXPIRED_HEADLINE = "expired_headline"
REDEEMED_HEADLINE = "redeemed_headline"
BARCODE_TYPE = "barcode_type"
ISSUED_HEADLINE = "issued_headline"


""" Membership Card's Status.State"""
AUTHORIZED = "state_authorised"
PENDING = "state_pending"
FAILED = "state_failed"
UNAUTHORIZED = "state_unauthorised"

""" Membership Card's Status.Reason_Code"""
REASON_CODE_PENDING_ADD = "reason_code_pending_add"
REASON_CODE_PENDING_ENROL = "reason_code_pending_enrol"
REASON_CODE_AUTHORIZED = "reason_code_authorised"
REASON_CODE_UNAUTHORIZED = "reason_code_unauthorised"
REASON_CODE_FAILED = "reason_code_failed"
REASON_CODE_FAILED_ENROL = "reason_code_failed_enrol"
REASON_CODE_FAILED_INVALID_ENROL = "reason_code_invalid_failed_enrol"
REASON_CODE_ADD_FAILED = "reason_code_add_failed"
REASON_CODE_GHOST_FAILED = "reason_code_ghost_failed"

""" Payment Cards Constant"""
FIRST_SIX_DIGITS = "first_six_digits"
LAST_FOUR_DIGITS = "last_four_digits"
TOKEN = "token"
NAME_ON_CARD = "name_on_card"
MONTH = "month"
YEAR = "year"
FINGERPRINT = "fingerprint"
HASH = "hash"
PAYMENT_CARD_STATUS = "status"
ACTIVE_LINK = "active_link"
PAYMENT_PROVIDER = "payment_provider"
PAYMENT_URL = "payment_url"
PAYMENT_ENCODING = "payment_encoding"
PAYMENT_DISCRIPTION = "payment_discription"
PAYMENT_VERIFICATION = "payment_verification"

"""Base Path of expected membership plans and membership plans used for comparison in json_diff"""
EXPECTED_MEMBERSHIP_PLANS_PATH = "tests_resources/test_data/membership_plan"
EXPECTED_MEMBERSHIP_PLANS_PATH_DEV = "tests_resources/test_data/membership_plan/membership_plan_dev"
EXPECTED_MEMBERSHIP_PLANS_PATH_STAGING = "tests_resources/test_data/membership_plan/membership_plan_staging"
EXPECTED_MEMBERSHIP_PLANS_PATH_PROD = "tests_resources/test_data/membership_plan/membership_plan_prod"
EXPECTED_MEMBERSHIP_PLANS_PATH_SIT = "tests_resources/test_data/membership_plan/membership_plan_sit"
EXPECTED_MEMBERSHIP_PLANS_PATH_OAT = "tests_resources/test_data/membership_plan/membership_plan_oat"
EXPECTED_MEMBERSHIP_PLANS_PATH_PREPROD = "tests_resources/test_data/membership_plan/membership_plan_preprod"

JSON_DIFF_EXPECTED_JSON = "tests_resources/test_data/membership_plan/json_diff_comparator/expected_membership_plan.json"
JSON_DIFF_ACTUAL_JSON = "tests_resources/test_data/membership_plan/json_diff_comparator/actual_membership_plan.json"


MEMBERSHIP_CARD_PATH = "tests_resources/test_data/membership_card"
MEMBERSHIP_CARD_DEV = "tests_resources/test_data/membership_card/membership_card_dev"
MEMBERSHIP_CARD_STAGING = "tests_resources/test_data/membership_card/membership_card_staging"
MEMBERSHIP_CARD_PROD = "tests_resources/test_data/membership_card/membership_card_prod"
MEMBERSHIP_CARD_SIT = "tests_resources/test_data/membership_card/membership_card_sit"
MEMBERSHIP_CARD_PREPROD = "tests_resources/test_data/membership_card/membership_card_preprod"
MEMBERSHIP_CARD_OAT = "tests_resources/test_data/membership_card/membership_card_oat"
"""Channel User Details"""
USER_ID = "uid"
PWD = "pwd"

"""Event Details"""
ORIGIN = "origin"
CHANNEL_BINK = "channel_bink"
CHANNEL_BARCLAYS = "channel_barclays"
STATUS = "status"
