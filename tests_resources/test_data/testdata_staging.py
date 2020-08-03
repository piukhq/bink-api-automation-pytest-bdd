# ------------------------------------ ---PAYMENT  CARDS ------------------------------------------------------- #

barclays_payment_card = {
    "first_six_digits": "555555",
    "last_four_digits": "4444",
}

# ------------------------------------ MEMBERSHIP  CARDS ------------------------------------------------------- #

burger_king_membership_card = {
    "card_num": "BK00000031049422"
    # "BK00000035620277",
}
burger_king_invalid_data = {
    "card_num": "BK00000035941500",
    "email": "fail@unknown.com",
}

coop_membership_card = {
    "card_num": "633174918511516552",
    "dob": "11/11/1984",
    "postcode": "BN16 4HE",
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

fat_face_membership_card = {
    "card_num": "FF00000059702811",
}

fat_face_invalid_data = {
    "card_num": "FF00000059702810",
}

harvey_nichols_membership_card = {
    "id": "ryanedwards3@mac.com",
    "password": "BinkTesting",
    "points": 1896,
    "transactions": 5,
    "card_num": "1000000729692",
}

harvey_nichols_invalid_data = {
    "id": "fail@unknown.com"
}

iceland_membership_card = {
    "card_num": "6332040030473324721",
    "last_name": "Bransden",
    "postcode": "BN16 4HE",
    "points": 380.01
}

coop_ghost_card = {
    "card_num": "6332040030522672674",
    "last_name": "Binktest",
    "dob": "01/01/2000",
    "postcode": "SL5 9FE",
    "points": "",
    "transactions": "",
}

iceland_invalid_data = {
    "email": "",
}
wasabi_membership_card = {
    "card_num": "",
}
whsmith_membership_card = {
    "card_num": "FF00000004827176",
}

whsmith_invalid_data = {
    "card_num": "WHSmithInvalid_Card",
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
}
# ----------------------------------------MEMBERSHIP ACCOUNT STATES & REASON_CODES ---------------------------------- #

membership_card_status_states = {
    "state_pending": "pending",
    "state_authorised": "authorised",
    "state_failed": "failed",
}
reason_codes = {
    "pending": "[X100]",
    "authorised": "X300",
    "failed": "X303",
}

# ---------------------------------------------USER ACCOUNTS ---------------------------------------------------- #

user_accounts = {
    "bink_uid": "njames@bink.com",
    "bink_pwd": "Password@200",
}
django_user_accounts = {
    "django_uid": "njames@bink.com",
    "django_pwd": "Password@200",
}
