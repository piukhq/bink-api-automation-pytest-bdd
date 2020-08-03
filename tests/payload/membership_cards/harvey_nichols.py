import logging
import json
from faker import Faker

from tests.helpers.test_data_utils import TestDataUtils
# from tests.helpers.encrypter import RSACipher
from tests.api.base import Endpoint
import tests.api as api
import tests.helpers.constants as constants


# import base64
# from Crypto.Cipher import PKCS1_OAEP
# from Crypto.PublicKey import RSA

class HarveyNicholsCard:
    @staticmethod
    def add_membership_card_payload(invalid_data=None):
        if invalid_data:
            value = TestDataUtils.TEST_DATA.harvey_nichols_invalid_data.get(constants.ID)
            logging.info("Invalid data is: " + value)
            data_type = "Invalid data"
        else:
            value = TestDataUtils.TEST_DATA.harvey_nichols_membership_card.get(constants.ID)
            data_type = "Valid data"

        payload = {
            "account": {
                "authorise_fields": [
                    {"column": "Email",
                     "value": value
                     },
                    {
                        "column": "Password",
                        "value": TestDataUtils.TEST_DATA.harvey_nichols_membership_card.get(constants.PASSWORD)
                        # HarveyNicholsCard.encrypt_field(constants.PASSWORD)
                        # "value": RSACipher.encrypt_field("Password01")
                    }
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("harvey_nichols"),
        }
        logging.info("The Request for Add Journey with " + data_type + " :\n\n"
                     + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n" + json.dumps(payload, indent=4))
        return payload

    @staticmethod
    def enrol_membership_scheme_payload(email, invalid_data=None):
        faker = Faker()

        if invalid_data:
            value = TestDataUtils.TEST_DATA.coop_invalid_data.get("email")
            logging.info("Invalid data is: " + value)
            data_type = "Invalid data"
        else:
            value = email
            data_type = "Valid data"
        payload = {
            "account": {
                "enrol_fields": [
                    {"column": "Title", "value": constants.TITLE},
                    {"column": "First name", "value": faker.name()},
                    {"column": "Last name", "value": faker.name()},
                    {"column": "Email", "value": value},
                    {"column": "Password", "value": constants.PASSWORD_ENROL},
                    {"column": "Mobile number", "value": faker.phone_number()},
                    {"column": "Consent 1", "value": constants.CONSENT},
                ]
            },
            "membership_plan": TestDataUtils.TEST_DATA.membership_plan_id.get("harvey_nichols"),
        }
        logging.info("The Request for Enrol Journey with " + data_type + " :\n\n"
                     + Endpoint.BASE_URL + api.ENDPOINT_MEMBERSHIP_CARDS + "\n\n" + json.dumps(payload, indent=4))
        return payload
    #
    # def _encrypt(val):
    #     # convert all values to string before encoding as some values may be integers
    #     # pub_key =  RSA.importKey("self.hashing_secret")
    #     keypair = RSA.generate(2048)
    #     pub_key = keypair.publickey()
    #     # pub_key =  RSA.importKey("self.hashing_secret")
    #     encrypted_val = PKCS1_OAEP.new(pub_key).encrypt(str(val).encode())
    #     # encrypted byte string cannot be sent in JSON so must be converted
    #     return base64.b64encode(encrypted_val).decode('utf-8')
    #
    # def encrypt_field(field):
    #     return HarveyNicholsCard._encrypt(field)
