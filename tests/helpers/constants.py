"""Email Template"""
EMAIL_TEMPLATE = "pytest_email@bink.com"

"""Constants for Enrol_Scheme Credential Questions"""
TITLE = "Mr"
DATE_OF_BIRTH = "01/01/2000"
PASSWORD_ENROL = "Password01"
EMAIL_MARKETING = "true"
CONSENT = "true"

""" Constants for Add Journey"""
CARD_NUM = "card_num"
BARCODE = "barcode"
EMAIL = "email"
DOB = "dob"
POSTCODE = "postcode"
ID = "id"
PASSWORD = "password"
PASSWORD_ENCRYPTED = "password_encrypted"
LAST_NAME = "last_name"
POINTS = "points"
CURRENCY = "currency"
DESCRIPTION = "description"
TRANSACTIONS = "transactions"
TRANSACTIONS_STATUS = "transaction_status"
TRANSACTIONS_CURRENCY = "transaction_currency"

INPROGRESS_STATE = "inprogress_state"
ISSUED_STATE = "issued_state"
BURN_TYPE = "burn_type"
BURN_PREFIX = "burn_prefix"
CODE = "code"


EARN_TYPE = "earn_type"
TARGET_VALUE = "target_value"
HEADLINE = "headline"
BARCODE_TYPE = "barcode_type"
ISSUED_HEADLINE = "issued_headline"



""" Membership Card's Status.State"""
AUTHORIZED = "state_authorised"
PENDING = "state_pending"
FAILED = "state_failed"

""" Membership Card's Status.Reason_Code"""
REASON_CODE_PENDING_ADD = "reason_code_pending_add"
REASON_CODE_PENDING_ENROL = "reason_code_pending_enrol"
REASON_CODE_AUTHORIZED = "reason_code_authorised"
REASON_CODE_FAILED = "reason_code_failed"
REASON_CODE_FAILED_ENROL = "reason_code_failed_enrol"
REASON_CODE_FAILED_INVALID_ENROL = "reason_code_invalid_failed_enrol"

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

"""Base Path of expected membership plans and membership plans used for comparison in json_diff"""
EXPECTED_MEMBERSHIP_PLANS_PATH = "tests_resources/test_data/membership_plan"
EXPECTED_MEMBERSHIP_PLANS_PATH_DEV = "tests_resources/test_data/membership_plan/membership_plan_dev"
EXPECTED_MEMBERSHIP_PLANS_PATH_STAGING = "tests_resources/test_data/membership_plan/membership_plan_staging"
EXPECTED_MEMBERSHIP_PLANS_PATH_PROD = "tests_resources/test_data/membership_plan/membership_plan_prod"
EXPECTED_MEMBERSHIP_PLANS_PATH_SIT = "tests_resources/test_data/membership_plan/membership_plan_sit"
EXPECTED_MEMBERSHIP_PLANS_PATH_OAT = "tests_resources/test_data/membership_plan/membership_plan_oat"
JSON_DIFF_EXPECTED_JSON = "tests_resources/test_data/membership_plan/json_diff_comparator/expected_membership_plan.json"
JSON_DIFF_ACTUAL_JSON = "tests_resources/test_data/membership_plan/json_diff_comparator/actual_membership_plan.json"

"""Channel User Details"""
USER_ID = "uid"
PWD = "pwd"
