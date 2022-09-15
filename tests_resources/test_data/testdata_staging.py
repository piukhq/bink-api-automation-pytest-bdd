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
    "first_six_digits": "555555",
    "last_four_digits": "4444",
    "token": "pytest4011",
    "name_on_card": "master_staging_test",
    "month": 1,
    "year": 2044,
    "fingerprint": "pytest2002",
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

burger_king_membership_card = {"card_num": "BK00000031049422", "points": 1, "currency": "stamps"}

burger_king_invalid_data = {
    "card_num": "BK00000035941500",
    "email": "fail@unknown.com",
}

coop_membership_card = {
    "card_num": "633174912301122335",
    "dob": "01/01/2000",
    "postcode": "qa1 1qa",
    "points": "0.00p",
    "transactions": "0",
}

coop_ghost_card = {
    "card_num": "",
    "dob": "",
    "postcode": "",
}

coop_invalid_data = {
    "postcode": "fail",
    "email": "fail@unknown.com",
}

coop_ghost_card = {
    "card_num": "6332040030522672674",
    "last_name": "Binktest",
    "dob": "01/01/2000",
    "postcode": "SL5 9FE",
    "points": "",
    "transactions": "",
}

fat_face_membership_card = {
    "card_num": "FF00000058556150",
    "points": 55.5,
    "currency": "GBP",
    "burn_type": "voucher",
    "burn_prefix": "15% off",
    "earn_type": "accumulator",
    "earn_prefix": "\u00a3",
    "issued_state": "issued",
    "inprogress_state": "inprogress",
    "expired_state": "expired",
    "redeemed_state": "redeemed",
    "target_value": 100.0,
    "subtext": "for spending",
    "headline": "Spend \u00a3100 to get 15 percent off to spend online",
    "expired_headline": "Expired",
    "redeemed_headline": "Redeemed",
    "barcode_type": 4,
    "code": "5AC623TDLH",
    "issued_headline": "Earned",
}

fat_face_invalid_data = {
    "card_num": "FF00000059702810",
}

harvey_nichols_membership_card = {
    "id": "andyjameshill@gmail.com",
    "password": "BinkTest",
    "card_num": "1000000962497",
    "barcode": "1000000962497",
    "points": 64,
    "currency": "Points",
    "description": "Placeholder Balance Description",
    "transactions": "5",
    "transaction_status": "active",
    "transaction_currency": "Points",
}

harvey_nichols_membership_card_2 = {
    "id": "ryanedwards3@mac.com",
    "password": "BinkTesting",
    "card_num": "1000000729692",
    "barcode": "1000000729692",
    "points": 1896,
    "currency": "Points",
    "description": "Placeholder Balance Description",
    "transactions": "0 ",
    "transaction_status": "",
    "transaction_currency": "",
}

harvey_nichols_invalid_data = {"id": "fail@unknown.com"}

square_meal_invalid_data = {"id": "sm_auto01@testbink.com", "password": "Pass"}

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
}
# iceland_membership_card = {
#     "card_num": "6332040030473324721",
#     "last_name": "Bransden",
#     "postcode": "BN16 4HE",
#     "points": 380.01
# }


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

# iceland_membership_card = {
#     "card_num": "6332040030555532506",
#     "barcode": "633204003055553250600085",
#     "last_name": "Armstrong",
#     "postcode": "SW18 4HH",
#     "points": 5,
#     "currency": "GBP",
#     "description": "Placeholder Balance Description",
#     "transactions": "5",
#     "transaction_status": "active",
#     "transaction_currency": "GBP",
# }


iceland_invalid_data = {
    # "email": "fail@unknown.com",
    "email": "joininprogress@bink.com",
    "postcode": "fail",
}

trenette_membership_card = {
    "card_num": "TRNT4551622350",
    "email": "pytest+220722@bink.com",
    "points": 6.0,
    "currency": "GBP",
    "transaction_currency": "GBP",
    "burn_type": "voucher",
    "burn_suffix": "Free bottle of house wine",
    "earn_type": "accumulator",
    "earn_prefix": "\u00a3",
    "issued_state": "issued",
    "inprogress_state": "inprogress",
    "expired_state": "expired",
    "redeemed_state": "redeemed",
    "target_value": 100.0,
    "headline": "Spend \u00a3100 stamps to go!",
    "expired_headline": "Expired",
    "redeemed_headline": "Redeemed",
    "barcode_type": 0,
    "code": "TESTRETVOC4",
    "issued_headline": "Earned",
    "transaction_status": "active",
}

trenette_invalid_data = {
    "card_num": "TRNT4551622350",
    "email": "fail@unknown.com",
}

asos_membership_card = {
    "card_num": "ASOS3279362771",
    "email": "pytest+220722@bink.com",
    "points": 14.83,
    "prefix": "£",
    "currency": "GBP",
    "transaction_currency": "GBP",
    "burn_type": "voucher",
    "burn_prefix": "£",
    "burn_value": "10",
    "burn_suffix": "Gift",
    "earn_type": "accumulator",
    "target_value": 100.0,
    "issued_state": "issued",
    "inprogress_state": "inprogress",
    "expired_state": "expired",
    "redeemed_state": "redeemed",
    "headline": "Spend £100 to get a £10 gift voucher",
    "expired_headline": "Expired",
    "redeemed_headline": "Redeemed",
    "barcode_type": 0,
    "issued_headline": "Earned",
    "transaction_status": "active",
}

asos_invalid_data = {
    "card_num": "ASOS3279362771",
    "email": "fail@unknown.com",
}

viator_membership_card = {
    "card_num": "VIAT6417218052",
    "email": "pytest+test150822@bink.com",
    "points": 27.18,
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
    "card_num": "VIAT6417218052",
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

whsmith_membership_card = {
    "card_num": "WHS00000009523459",
    "points": 0,
    "currency": "stamps",
    "description": "Customer earns one stamp for every valid transaction.",
}

whsmith_invalid_data = {
    "card_num": "WHS12000009523459",
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
    "uid": "pytest_staging_auto@bink.com",
    "pwd": "Password1",
}

barclays_user_accounts = {
    "uid": "pytest_automation_barclays@bink.com",
    "pwd": "Password01",
}
# ------------------------------------------ DB DETAILS ---------------------------------------------------- #

db_details = {
    "user": "common@bink-uksouth-staging-common",
    "password": "",
    "host": "127.0.0.1",
    "port": "5432",
    "database": "hermes",
}

harmonia_db_details = {
    "user": "common@bink-uksouth-staging-common",
    "password": "",
    "host": "127.0.0.1",
    "port": "5432",
    "database": "harmonia",
}
