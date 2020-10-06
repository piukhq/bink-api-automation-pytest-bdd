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

# ------------------------------------------ DB DETAILS ---------------------------------------------------- #

db_details = {
    "user": "common@bink-uksouth-dev-common",
    "password": "",
    "host": "127.0.0.1",
    "port": "5432",
    "database": "hermes",
}
