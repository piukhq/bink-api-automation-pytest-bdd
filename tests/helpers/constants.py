"""Email Template"""
EMAIL_TEMPLATE = "pytest_email@bink.com"

"""Constants for Enrol_Scheme Credential Questions"""
TITLE = "Mr"
DATE_OF_BIRTH = "01/01/2000"
PASSWORD = "Password01"
EMAIL_MARKETING = "true"
CONSENT = "true"


""" Constants for Add Journey"""
CARD_NUM = "card_num"
EMAIL = "email"
DOB = "dob"
POSTCODE = "postcode"
POINTS = "points"
TRANSACTIONS = "transactions"
ID = "id"
PASSWORD = "password"
LAST_NAME = "last_name"

""" Membership Card's Status.State"""
AUTHORIZED = "state_authorised"
PENDING = "state_pending"
FAILED = "state_failed"

"""Base Path of expected membership plans and 
membership plans used for comparison in json_diff"""
EXPECTED_MEMBERSHIP_PLANS_PATH = "tests_resources/test_data/membership_plan"
JSON_DIFF_EXPECTED_JSON = "tests_resources/test_data/membership_plan/json_diff_comparator/expected_membership_plan.json"
JSON_DIFF_ACTUAL_JSON = "tests_resources/test_data/membership_plan/json_diff_comparator/actual_membership_plan.json"
