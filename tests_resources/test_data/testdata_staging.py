# ------------------------------------ ---PAYMENT  CARDS ------------------------------------------------------- #

visa_payment_card = {
    "first_six_digits": "401288",
    "last_four_digits": "1813",
    "token": "UPBoHspUQWWTdg1Zso+1Nw==2",
    "name_on_card": "Avery",
    "month": 10,
    "year": 2026,
    "fingerprint": "b0548a5e26030ccd853fcb70e9011fb79577",
    "hash": "pytest2001",
    "status": "active",
    "active_link": True,
    "payment_provider": "Visa",
    "payment_encoding": "png",
    "payment_discription": "Visa Card Image",
    "payment_url": "https://api.staging.gb.bink.com/content/media/hermes/schemes/Visa-Payment_Eq81MWN.png",
    "payment_verification": False,
}

amex_payment_card = {
    "first_six_digits": "378282",
    "last_four_digits": "0005",
    "token": "pytest7118",
    "name_on_card": "amex_staging_test",
    "month": 1,
    "year": 2044,
    "fingerprint": "pytest7118",
    "hash": "pytestsamplehash20",
    "status": "active",
    "active_link": True,
    "payment_provider": "American Express",
    "payment_encoding": "png",
    "payment_discription": "Amex Card Image",
    "payment_url": "https://api.staging.gb.bink.com/content/media/hermes/schemes/Amex-Payment.png",
    "payment_verification": False,
}

master_payment_card = {
    "first_six_digits": "555589",
    "last_four_digits": "4490",
    "token": "pytest_auto_master",
    "name_on_card": "master_staging_test",
    "month": 1,
    "year": 2044,
    "fingerprint": "pytest_auto_master",
    "hash": "pytest4012",
    "status": "active",
    "active_link": True,
    "payment_provider": "Mastercard",
    "payment_encoding": "png",
    "payment_discription": "Mastercard Hero",
    "payment_url": "https://api.staging.gb.bink.com/content/media/hermes/schemes/Mastercard-Payment_1goHQYv.png",
    "payment_verification": False,
}

# ------------------------------------ MEMBERSHIP  CARDS ------------------------------------------------------- #

square_meal_invalid_data = {"id": "sm_auto01@testbink.com", "password": "incorrectpassword"}

square_meal_membership_card2 = {
    "id": "bola_staging_auto@bink.com",
    "password": "Password1",
    "card_num": "100680911",
    "barcode": "100680911",
    "points": 100,
    "currency": "Points",
    "description": "Placeholder Balance Description",
    "transactions": "1",
    "transaction_status": "active",
    "transaction_currency": "Points",
}
square_meal_membership_card = {
    "id": "sm_auto01@testbink.com",
    "password": "Pass01sm",
    "card_num": "100460668",
    "barcode": "100460668",
    "points": 100,
    "currency": "Points",
    "description": "Placeholder Balance Description",
    "transactions": "1",
    "transaction_status": "active",
    "transaction_currency": "Points",
    "identical_enrol_email": "identicaljoin@bink.com",
}

iceland_membership_card = {
    "card_num": "6332040066666666666",
    "barcode": "63320400666666666660080",
    "last_name": "six",
    "postcode": "rg6 6aa",
    "points": 1480,
    "currency": "GBP",
    "description": "Placeholder Balance Description",
    "transactions": "6",
    "transaction_status": "active",
    "transaction_currency": "GBP",
    "card_num2": "6332040012312354321",
    "test_last_name": "testuser",
    "error_last_name": "error",
}

iceland_ghost_membership_card = {
    "card_num": "6332040031231230001",
    "barcode": "6332040031231230001",
    "unknown_card": "6332040072345437596",
    "unknown_last_name": "odedraghostcard",
    "register_failed_email": "generalerror@testbink.com",
    "last_name": "QAUsertest11",
    "patch_last_name": "auto_ghostcardsuccess",
    "postcode": "rg6 6bb",
    "points": 1480,
    "currency": "GBP",
    "description": "Placeholder Balance Description",
    "transactions": "6",
    "transaction_status": "active",
    "transaction_currency": "GBP",
}

iceland_invalid_data = {
    # "email": "fail@unknown.com",
    "email": "joininprogress@bink.com",
    "postcode": "fail",
    "identical_enrol_email": "identicaljoin@bink.com",
    "error_last_name": "error",
}

trenette_membership_card = {
    "card_num": "TRNT2254698170",
    "email": "autorewards.bpl@gmail.com",
    "points": 0,
    "currency": "GBP",
    "transaction_currency": "GBP",
    "burn_type": "voucher",
    "burn_preffix": "Free",
    "burn_suffix": "Chocolate Hamper",
    "earn_type": "accumulator",
    "earn_prefix": "\u00a3",
    "issued_state": "issued",
    "inprogress_state": "inprogress",
    "expired_state": "expired",
    "redeemed_state": "redeemed",
    "target_value": 2.0,
    "headline": "\u00a3earn_target_remaining|floatformat:'2' to go!",
    "expired_headline": "Expired",
    "redeemed_headline": "Redeemed",
    "barcode_type": 0,
    # "code": "TESTRETVOC4",
    "issued_headline": "Earned",
    "transaction_status": "active",
}

trenette_invalid_data = {
    "card_num": "TRNT2254698170",
    "email": "fail@unknown.com",
}

viator_membership_card = {
    "card_num": "VIAT7330251401",
    "email": "autorewards.bpl@gmail.com",
    "points": 0.0,
    "prefix": "£",
    "currency": "GBP",
    # "transaction_currency": "GBP",
    "burn_type": "voucher",
    "burn_prefix": "X% off",
    # "burn_value": "10",
    # "burn_suffix": "eGift",
    "earn_type": "accumulator",
    "target_value": 200.0,
    "issued_state": "issued",
    "inprogress_state": "inprogress",
    "expired_state": "expired",
    "redeemed_state": "redeemed",
    "headline": "Spend £200 to get a 10% off Viator voucher code",
    "expired_headline": "Expired",
    "redeemed_headline": "Redeemed",
    "barcode_type": 0,
    "issued_headline": "Earned",
    # "transaction_status": "active",
}

viator_invalid_data = {
    "card_num": "VIAT7330251401",
    "email": "fail@unknown.com",
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
# ----------------------------------------MEMBERSHIP PLAN IDs   ----------------------------------------------- #

membership_plan_id = {
    "burger_king": 279,
    "coop": 243,
    "fat_face": 246,
    "harvey_nichols": 124,
    "iceland": 105,
    "whsmith": 280,
    "wasabi": 281,
    "square_meal": 286,
    "trenette": 284,
    "asos": 288,
    "viator": 292,
}

# ----------------------------------------PAYMENT CARD STATES  --------------------------------------------------- #

vop_status = {
    "activating": 1,
    "deactivating": 2,
    "activated": 3,
    "deactivated": 4,
}

# ----------------------------------------MEMBERSHIP ACCOUNT STATES & REASON_CODES ---------------------------------- #

membership_card_status_states = {
    "state_pending": "pending",
    "state_authorised": "authorised",
    "state_failed": "failed",
    "state_unauthorised": "unauthorised",
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
    "reason_code_unauthorised": "X103",
}
# ---------------------------------------------USER ACCOUNTS ---------------------------------------------------- #

bink_user_accounts = {
    "uid": "pytest_staging_auto@bink.com",
    "pwd": "Password1",
}

barclays_user_accounts = {
    "uid": "pytest_automation_barclays@bink.com",
    "pwd": "Password01",
}
