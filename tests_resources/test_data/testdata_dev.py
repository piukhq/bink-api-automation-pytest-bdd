# ------------------------------------ ---PAYMENT  CARDS ------------------------------------------------------- #

visa_payment_card = {
    "first_six_digits": "555555",
    "last_four_digits": "4444",
    "token": "auto1093448038331testbinkcom",
    "name_on_card": "auto1093448038331testbinkcom",
    "month": 1,
    "year": 2044,
    "fingerprint": "auto1093448038331testbinkcom",
    "status": "active",
    "active_link": True
}

amex_payment_card = {
    "first_six_digits": "555555",
    "last_four_digits": "4444",
    "token": "auto1093448038331testbinkcom",
    "name_on_card": "auto1093448038331testbinkcom",
    "month": 1,
    "year": 2044,
    "fingerprint": "auto1093448038331testbinkcom",
    "status": "active",
    "active_link": True
}

master_payment_card = {
    "first_six_digits": "555555",
    "last_four_digits": "4444",
    "month": 1,
    "year": 2044,
    "status": "active",
    "active_link": True
}

# ------------------------------------ MEMBERSHIP  CARDS ------------------------------------------------------- #

burger_king_membership_card = {
    "card_num": "BK00000035941509",
    "points": "",
    "currency": "",
    "description": "",
    "transactions": "",
    "transaction_status": "",
    "transaction_currency": "",
}
burger_king_invalid_data = {
    "card_num": "BK00000035941500",
    "email": "fail@unknown.com",
}

coop_membership_card = {
    "card_num": "633174912301122330",
    "dob": "01/01/2000",
    "postcode": "qa1 1qa",
    "points": "",
    "currency": "",
    "description": "",
    "transactions": "",
    "transaction_status": "",
    "transaction_currency": "",
}

coop_ghost_card = {
    "card_num": "633174921231230004",
    "dob": "01/02/1994",
    "postcode": "cr6 0bg",
}

coop_invalid_data = {
    "postcode": "fail",
    "email": "fail@unknown.com",
}

fat_face_membership_card = {
    "card_num": "FF00000059702811",
    "points": "",
    "currency": "",
    "description": "",
    "transactions": "",
    "transaction_status": "",
    "transaction_currency": "",
}

fat_face_invalid_data = {
    "card_num": "FF00000059702810",
}

harvey_nichols_membership_card = {
    "id": "auto_five@testbink.com",
    "password": "Password01",
    "card_num": "9123001122335",
    "barcode": "9123001122335",
    "points": 380,
    "currency": "Points",
    "description": "Placeholder Balance Description",
    "transactions": "5",
    "transaction_status": "active",
    "transaction_currency": "Points",

}

harvey_nichols_membership_card_2 = {
    "id": "auto_zero@testbink.com",
    "password": "Password01",
    "card_num": "9123001122330",
    "barcode": "9123001122330",
    "points": 0,
    "currency": "Points",
    "description": "Placeholder Balance Description",
    "transactions": "0 ",
    "transaction_status": "",
    "transaction_currency": "",

}
harvey_nichols_invalid_data = {
    "id": "fail@unknown.com"
}

iceland_membership_card = {
    "card_num": "5555555555555555555",
    "barcode": "5555555555555555555",
    "last_name": "five",
    "postcode": "rg5 5aa",
    "points": 380.01,
    "currency": "GBP",
    "description": "Placeholder Balance Description",
    "transactions": "5",
    "transaction_status": "active",
    "transaction_currency": "GBP",
}

iceland_invalid_data = {
    "email": "fail@unknown.com",
    "postcode": "fail",
}
wasabi_membership_card = {
    "card_num": "1048172852",
    "email": "binktestuser14@wasabi.com",
    "points": 6,
    "currency": "stamps",
    "description": "",
    "transactions": "",
    "transaction_status": "active",
    "transaction_currency": "stamps",
}

wasabi_invalid_data = {
    "card_num": "",
    "email": "fail@unknown.com",
}

whsmith_membership_card = {
    "card_num": "FF00000004827176",
    "points": "",
    "currency": "",
    "description": "",
    "transactions": "",
    "transaction_status": "",
    "transaction_currency": "",
}

whsmith_invalid_data = {
    "card_num": "WHSmithInvalid_Card",
    "email": "fail@unknown.com",
}

# ----------------------------------------MEMBERSHIP PLAN IDs   ----------------------------------------------- #

membership_plan_id = {
    "burger_king": 314,
    "coop": 242,
    "fat_face": 281,
    "harvey_nichols": 194,
    "iceland": 105,
    "whsmith": 316,
    "wasabi": 315,
}
# ----------------------------------------MEMBERSHIP ACCOUNT STATES & REASON_CODES ---------------------------------- #

membership_card_status_states = {
    "state_pending": "pending",
    "state_authorised": "authorised",
    "state_failed": "failed",
}
membership_card_status_reason_codes = {
    "reason_code_pending_add": "X100",
    "reason_code_pending_enrol": "X200",
    "reason_code_authorised": "X300",
    "reason_code_failed": "X303",
    "reason_code_failed_enrol": "X201",
}

# ---------------------------------------------USER ACCOUNTS ---------------------------------------------------- #

bink_user_accounts = {
    "uid": "njames@bink.com",
    "pwd": "Password@200",
}

barclays_user_accounts = {
    "uid": "pytestuser_dev_barclays@testbink.com",
    "pwd": "Password01",
}

django_user_accounts = {
    "django_uid": "njames@bink.com",
    "django_pwd": "Password@200",
}

# ------------------------------------------ DB DETAILS ---------------------------------------------------- #

db_details = {
    "user": "laadmin@bink-dev-uksouth",
    "password": "",
    "host": "127.0.0.1",
    "port": "5432",
    "database": "hermes",
}

# ------------------------------------------ Encrypted Fields ---------------------------------------------------- #
"""Temporary solution till encryption feature is included as a part of framework
Keeping the required values as encrypted and then using
"""

bink_encrypted_values = {
    "encrypted_pwd": "MSsxtWZjwthttoXGvzPQMShHV0qlbo7u5Q+mQbdkC"
                     "+U0JfttPKNdF4F1h693kBnP6ZReCbjak7ALj8rmKUCzMuSBG9DxmfvZBjPbcCYQVF9ld906ZdkfIh7geKLLPijxSlH"
                     "+ylOl0Nj+hEv/6vq8psJKNUeXYt4AXnqyI7hhYPRjOzsVL3L2lezyh/5uVgoyvhANJZfdqQKoCTchn48OqlV"
                     "/hxy7MHgtUQDwRS5QTUYY3Z9vAiZizRNiaSLI6bKIGqDbBo7vXXY+Rq4XHdTNB465s3L0SYzk2+/jXlhQWyVOqDYCx"
                     "+8lfTGRgoHXome8vzwp4lrBb5mqeennHgUQuZX9tf57qRYPN379iMzjpoiSKWN2GY38+EmvjZ4aN8"
                     "/3R0laxAZ2g1T4VskU9toCpFw/SuFtSwt1/w7qIGHXRe5rdrvwz6eC4cfcerr1laECgav2"
                     "+bDk2RdvwAnhZUElbXFdHtS2f5Mwot21MHhb2vXeeqfeppw"
                     "+ctE8PHQwzbQLeAQBIS0Qw4EUEizSR33Yuqj1V2McJ4O0g65rodT1LhrXcnQfBKG1GSNXLSnNQ4XyIyCFoR6Tgqcw"
                     "+XUYM0JnJOEff94hXiGV+MbUzMkwVLiwwFYTsjDaok5bqNf+f6HqOkdx1QrABKlJZWKbqKno7Gm6GqsUDzEzvcDcPLGOvZQ"
                     "=",
}

barclays_encrypted_values = {
    "encrypted_pwd": "MLhOJSqQQ00H32Lj9kFuIGTCeH8ka7qEC/AXKi7fUdRFsmsyQ88S9CMxGmKDwzoOtarwrhYx"
                     "/XpTX8BWzIMqIQl3wtRLwnFNtNdaRPvaW6d0PYe0SWVkDDrEtkixL8Qg0wliUVlIbx8Js8FnsboJ7"
                     "/H33rCFkKaF5I0m1DZq21yB+T5LjKHFbSUhT2ccu6+hhrTDvWbtNLNLCsG5OvddxxLuvIdSYht"
                     "+Og3oWGkMv9Fti7qVMmvo2q/+VRS2frW81ljgfY0lRz4w4l+XY1WQAXOWi+hTFu7daN/DI4raD/7pn/sVWsjRptZYgq"
                     "/x5FVr5sf6HfghymRnrP7d3wcgchG/iZP9WKHT3Ic77qVGWONLypfERKAMcjDRWtGvsLfSUMU4bHi1iEwPypmv0QiyZ"
                     "//MVOw3qHv5G7tQFMBp6WFNsSk7cn9VZMjxRFcOfZ899HwbgVM3JJCDMHq03xQ"
                     "/if9vypZwqAWV92lA8dt8n16Rx9SPUGJVzGEEnV"
                     "/a2YVTalU53J0yX78wc3QPWU7u5f0XuoKy9oQQu9K3thtE8u9fNMwdIrt4dkJsKxZRn1ekgRcjMRGU86YyGBH7cdtsEs2S"
                     "+KvMT20eZCSZWUYG2blqF8Mu14gc1IldII3yBsbC56KYTL2syGxzcLTkFrHwh5eZZCm2j6GByCcmdWJF6Ko=",
}
