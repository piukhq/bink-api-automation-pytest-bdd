import json
import logging

from faker import Faker

import tests.api as api
import tests.helpers.constants as constants
from tests.api.base import Endpoint
from tests.helpers.test_context import TestContext
from tests.helpers.test_data_utils import TestDataUtils


class IcelandCard:
    @staticmethod
    def add_membership_card_payload(invalid_data=None):
        if invalid_data:
            value = TestDataUtils.TEST_DATA.iceland_invalid_data.get(constants.POSTCODE)
            logging.info("Invalid data is: " + value)
            data_type = "Invalid data"
        else:
            value = TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.POSTCODE)
            data_type = "Valid data"

        payload = {
            "account": {
                "add_fields": [
                    {
                        "column": "Bonus card number",
                        "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.CARD_NUM),
                    }
                ],
                "authorise_fields": [
                    {
                        "column": "Last name",
                        "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.LAST_NAME),
                    },
                    {"column": "Postcode", "value": value},
                ],
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("iceland"),
        }

        logging.info(
            "The Request for Add Journey with "
            + data_type
            + " :\n\n"
            + Endpoint.BASE_URL
            + api.ENDPOINT_MEMBERSHIP_CARDS
            + "\n\n"
            + json.dumps(payload, indent=4)
        )
        return payload

    @staticmethod
    def enrol_membership_scheme_payload(email, env=None, channel=None, invalid_data=None):
        faker = Faker()
        enrol_consent = "Enrol Consent 1"
        if invalid_data:
            value = TestDataUtils.TEST_DATA.iceland_invalid_data.get(constants.EMAIL)
            logging.info("Invalid data is: " + value)
            data_type = "Invalid data"
        else:
            value = email
            data_type = "Valid data"

        if channel == "barclays":
            if env == "dev":
                enrol_consent = "Consent 1"
            elif env == "staging":
                enrol_consent = "Consent 2"
        elif channel == "bink":
            enrol_consent = "Enrol Consent 1"

        payload = {
            "account": {
                "enrol_fields": [
                    {"column": "Title", "value": constants.TITLE},
                    {"column": "First name", "value": faker.name()},
                    {"column": "Last name", "value": faker.name()},
                    {"column": "Date of birth", "value": constants.DATE_OF_BIRTH},
                    {"column": "Email", "value": value},
                    {"column": "Phone", "value": faker.phone_number()},
                    {"column": "House name or number", "value": faker.building_number()},
                    {"column": "Street name", "value": faker.street_address()},
                    {"column": "City", "value": faker.city()},
                    {"column": "County", "value": faker.country()},
                    {"column": "Postcode", "value": faker.postcode()},
                    {"column": enrol_consent, "value": constants.CONSENT},
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("iceland"),
        }
        logging.info(
            "The Request for Enrol Journey with "
            + data_type
            + " :\n\n"
            + Endpoint.BASE_URL
            + api.ENDPOINT_MEMBERSHIP_CARDS
            + "\n\n"
            + json.dumps(payload, indent=4)
        )
        return payload

    @staticmethod
    def add_ghost_membership_card_payload():
        payload = {
            "account": {
                "add_fields": [
                    {
                        "column": "Bonus card number",
                        "value": TestDataUtils.TEST_DATA.iceland_ghost_membership_card.get(constants.CARD_NUM),
                    }
                ],
                "authorise_fields": [
                    {
                        "column": "Last name",
                        "value": TestDataUtils.TEST_DATA.iceland_ghost_membership_card.get(constants.LAST_NAME),
                    },
                    {
                        "column": "Postcode",
                        "value": TestDataUtils.TEST_DATA.iceland_ghost_membership_card.get(constants.POSTCODE),
                    },
                ],
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("iceland"),
        }

        logging.info(
            "The Request for Add Ghost Journey with  :\n\n"
            + Endpoint.BASE_URL
            + api.ENDPOINT_MEMBERSHIP_CARDS
            + "\n\n"
            + json.dumps(payload, indent=4)
        )
        return payload

    @staticmethod
    def update_ghost_membership_scheme_payload(email, scheme_account_id, env, channel=None, enrol_cred_status=None):
        faker = Faker()
        enrol_consent = "Consent 1"
        if channel == "barclays":
            if env == "dev":
                enrol_consent = "Consent 1"
            elif env == "staging":
                enrol_consent = "Consent 2"
        elif channel == "bink":
            enrol_consent = "Enrol Consent 1"
        TestContext.last_name = faker.name()
        payload = {
            "account": {
                "registration_fields": [
                    {"column": "Title", "value": constants.TITLE},
                    {"column": "First name", "value": faker.name()},
                    {
                        "column": "Last name",
                        "value": TestDataUtils.TEST_DATA.iceland_ghost_membership_card.get(constants.PATCH_LAST_NAME),
                    },
                    {"column": "Date of birth", "value": constants.DATE_OF_BIRTH},
                    {"column": "Email", "value": email},
                    {"column": "Phone", "value": faker.phone_number()},
                    {"column": "House name or number", "value": faker.building_number()},
                    {"column": "Street name", "value": faker.street_address()},
                    {"column": "City", "value": faker.city()},
                    {"column": "County", "value": faker.country()},
                    {"column": "Postcode", "value": faker.postcode()},
                    {"column": enrol_consent, "value": constants.CONSENT},
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("iceland"),
        }
        logging.info(
            "The Request for Register Ghost Journey with  :\n\n"
            + Endpoint.BASE_URL
            + api.ENDPOINT_MEMBERSHIP_CARD.format(scheme_account_id)
            + "\n\n"
            + json.dumps(payload, indent=4)
        )
        return payload

    @staticmethod
    def add_membership_card_payload_without_field(field):
        if field == "account":
            payload = {
                "add_fields": [
                    {
                        "column": "Bonus card number",
                        "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.CARD_NUM),
                    }
                ],
                "authorise_fields": [
                    {
                        "column": "Last name",
                        "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.LAST_NAME),
                    },
                    {
                        "column": "Postcode",
                        "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.POSTCODE),
                    },
                ],
                "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("iceland"),
            }

        elif field == "membership_plan":
            payload = {
                "account": {
                    "add_fields": [
                        {
                            "column": "Bonus card number",
                            "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.CARD_NUM),
                        }
                    ],
                    "authorise_fields": [
                        {
                            "column": "Last name",
                            "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.LAST_NAME),
                        },
                        {
                            "column": "Postcode",
                            "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.POSTCODE),
                        },
                    ],
                }
            }

        elif field == "lastname":
            payload = {
                "account": {
                    "add_fields": [
                        {
                            "column": "Bonus card number",
                            "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.CARD_NUM),
                        }
                    ],
                    "authorise_fields": [
                        {
                            "column": "lastname",
                            "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.LAST_NAME),
                        },
                        {
                            "column": "Postcode",
                            "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.POSTCODE),
                        },
                    ],
                },
                "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("iceland"),
            }

        elif field == "postcode":
            payload = {
                "account": {
                    "add_fields": [
                        {
                            "column": "Bonus card number",
                            "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.CARD_NUM),
                        }
                    ],
                    "authorise_fields": [
                        {
                            "column": "Last name",
                            "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.LAST_NAME),
                        },
                        {
                            "column": "postcode",
                            "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.POSTCODE),
                        },
                    ],
                },
                "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("iceland"),
            }

        elif field == "token":
            payload = {
                "account": {
                    "add_fields": [
                        {
                            "column": "Bonus card number",
                            "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.CARD_NUM),
                        }
                    ],
                    "authorise_fields": [
                        {
                            "column": "Last name",
                            "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.LAST_NAME),
                        },
                        {
                            "column": "Postcode",
                            "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.POSTCODE),
                        },
                    ],
                },
                "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("iceland"),
            }

        return payload

    """This step is created as part of Trusted channel work and will be used mainly for multi-wallet scenarios."""

    @staticmethod
    def add_auth_payload():
        payload = {
            "account": {
                "add_fields": [
                    {
                        "column": "Bonus card number",
                        "value": TestDataUtils.TEST_DATA.iceland_ghost_membership_card.get(constants.CARD_NUM),
                    }
                ]
            },
            "authorise_fields": [
                {
                    "column": "Last name",
                    "value": TestDataUtils.TEST_DATA.iceland_ghost_membership_card.get(constants.LAST_NAME),
                },
                {
                    "column": "Postcode",
                    "value": TestDataUtils.TEST_DATA.iceland_ghost_membership_card.get(constants.POSTCODE),
                },
            ],
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("iceland"),
        }

        logging.info(
            "The Request for add auth  :\n\n"
            + Endpoint.BASE_URL
            + api.ENDPOINT_MEMBERSHIP_CARDS
            + "\n\n"
            + json.dumps(payload, indent=4)
        )
        return payload

    """This step is created as part of Trusted channel work and will be used mainly for multi-wallet scenarios."""

    @staticmethod
    def enrol_membership_card_payload(enrol_status, test_email, env=None, channel=None):
        faker = Faker()
        enrol_consent = "Enrol Consent 1"
        if enrol_status == "identical_enrol":
            test_email = TestDataUtils.TEST_DATA.iceland_invalid_data.get(constants.IDENTICAL_ENROL_EMAIL)
        if channel == "barclays":
            if env == "dev":
                enrol_consent = "Consent 1"
            elif env == "staging":
                enrol_consent = "Consent 2"
        elif channel == "bink":
            enrol_consent = "Enrol Consent 1"

        payload = {
            "account": {
                "enrol_fields": [
                    {"column": "Title", "value": constants.TITLE},
                    {"column": "First name", "value": faker.name()},
                    {"column": "Last name", "value": faker.name()},
                    {"column": "Date of birth", "value": constants.DATE_OF_BIRTH},
                    {"column": "Email", "value": test_email},
                    {"column": "Phone", "value": faker.phone_number()},
                    {"column": "House name or number", "value": faker.building_number()},
                    {"column": "Street name", "value": faker.street_address()},
                    {"column": "City", "value": faker.city()},
                    {"column": "County", "value": faker.country()},
                    {"column": "Postcode", "value": faker.postcode()},
                    {"column": enrol_consent, "value": constants.CONSENT},
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("iceland"),
        }
        logging.info(
            "The Request for Enrol Journey with "
            + " :\n\n"
            + Endpoint.BASE_URL
            + api.ENDPOINT_MEMBERSHIP_CARDS
            + "\n\n"
            + json.dumps(payload, indent=4)
        )
        return payload

    @staticmethod
    def update_membership_card_payload(invalid_data=None):
        if invalid_data:
            value = TestDataUtils.TEST_DATA.iceland_invalid_data.get(constants.POSTCODE)
            data_type = "Invalid data"
        else:
            value = TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.LAST_NAME)
            data_type = "Valid data"
        payload = {
            "account": {
                "authorise_fields": [{"column": "Last name", "value": value}],
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("iceland"),
        }
        logging.info(
            "The Request for Update Auth credentials with "
            + data_type
            + " :\n\n"
            + Endpoint.BASE_URL
            + api.ENDPOINT_MEMBERSHIP_CARDS
            + "\n\n"
            + json.dumps(payload, indent=4)
        )
        return payload

    @staticmethod
    def add_membership_card_payload2(invalid_data=None):
        if invalid_data:
            lastname = TestDataUtils.TEST_DATA.iceland_invalid_data.get(constants.ERROR_LAST_NAME)
            data_type = "Invalid data"
        else:
            lastname = TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.TEST_LAST_NAME)
            data_type = "Valid data"

        payload = {
            "account": {
                "add_fields": [
                    {
                        "column": "Bonus card number",
                        "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.CARD_NUM2),
                    }
                ],
                "authorise_fields": [
                    {
                        "column": "Last name",
                        "value": lastname,
                    },
                    {
                        "column": "Postcode",
                        "value": TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.POSTCODE),
                    },
                ],
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("iceland"),
        }

        logging.info(
            "The Request for Add Journey with "
            + data_type
            + " :\n\n"
            + Endpoint.BASE_URL
            + api.ENDPOINT_MEMBERSHIP_CARDS
            + "\n\n"
            + json.dumps(payload, indent=4)
        )
        return payload
