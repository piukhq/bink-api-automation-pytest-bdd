# ------------------------------------ ---PAYMENT  CARDS ------------------------------------------------------- #

visa_payment_card = {
    "first_six_digits": "401288",
    "last_four_digits": "1813",
    "token": "UPBoHspUQWWTdg1Zso+1Nw==2",
    "name_on_card": "Avery",
    "month": 10,
    "year": 2026,
    "fingerprint": "b0548a5e26030ccd853fcb70e9011fb79577",
    "hash": "pytest7117",
    "status": "active",
    "active_link": True,
    "payment_provider": "Visa",
    "payment_encoding": "png",
    "payment_discription": "Visa Card Image",
    "payment_url": "https://api.dev.gb.bink.com/content/media/hermes/schemes/Visa-Payment_DWQzhta.png",
    "payment_verification": False,
}

amex_payment_card = {
    "first_six_digits": "378282",
    "last_four_digits": "0005",
    "token": "pytest7117",
    "name_on_card": "amex_dev_test",
    "month": 1,
    "year": 2044,
    "fingerprint": "pytest7117",
    "hash": "pytest7117",
    "status": "active",
    "active_link": True,
    "payment_provider": "American Express",
    "payment_encoding": "png",
    "payment_discription": "American Express Card Image",
    "payment_url": "https://api.dev.gb.bink.com/content/media/hermes/schemes/Amex-Payment.png",
    "payment_verification": False,
}

master_payment_card = {
    "first_six_digits": "555555",
    "last_four_digits": "4444",
    "token": "pytest4011",
    "name_on_card": "master_dev_test",
    "month": 1,
    "year": 2044,
    "fingerprint": "pytest4011",
    "hash": "pytest4011",
    "status": "active",
    "active_link": True,
    "payment_provider": "Mastercard",
    "payment_encoding": "png",
    "payment_discription": "Mastercard Card Image",
    "payment_url": "https://api.dev.gb.bink.com/content/media/hermes/schemes/Mastercard-Payment_1goHQYv.png",
    "payment_verification": False,
}

# ------------------------------------ MEMBERSHIP  CARDS ------------------------------------------------------- #

iceland_membership_card = {
    "card_num": "6332040023001122330",
    "barcode": "6332040023001122330",
    "last_name": "qa",
    "postcode": "qa1 1qa",
    "points": 380.01,
    "currency": "GBP",
    "description": "Placeholder Balance Description",
    "transactions": "5",
    "transaction_status": "active",
    "transaction_currency": "GBP",
}
iceland_ghost_membership_card = {
    "card_num": "6332040031231230001",
    "barcode": "6332040031231230001",
    "last_name": "QAUsertest11",
    "postcode": "rg6 6bb",
    "points": 1480,
    "currency": "GBP",
    "description": "Placeholder Balance Description",
    "transactions": "6",
    "transaction_status": "active",
    "transaction_currency": "GBP",
}

iceland_invalid_data = {
    "email": "fail@unknown.com",
    "postcode": "fail",
}
wasabi_membership_card = {
    "card_num": "1049108528",
    "email": "BinkBundleAuto_1625235298057@bink.com",
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
    "reason_code_invalid_failed_enrol": "X202",
    "reason_code_add_failed": "X102",
    "reason_code_ghost_failed": "X105",
}

# ---------------------------------------------USER ACCOUNTS ---------------------------------------------------- #

bink_user_accounts = {
    "uid": "pytestuser_dev_bink@testbink.com",
    "pwd": "Password01",
}

barclays_user_accounts = {
    "uid": "pytestuser_dev_barclays@testbink.com",
    "pwd": "Password01",
}
