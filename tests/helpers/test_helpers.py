import tests.helpers.constants as constants
from tests.helpers.test_data_utils import TestDataUtils
from tests.payload.membership_cards.burgerking import BurgerKingCard
from tests.payload.membership_cards.cooperative import CoopCard
from tests.payload.membership_cards.fatface import FatFaceCard
from tests.payload.membership_cards.harvey_nichols import HarveyNicholsCard
from tests.payload.membership_cards.iceland import IcelandCard
from tests.payload.membership_cards.whsmith import WHSmithCard
from tests.payload.membership_cards.wasabi import WasabiCard


class Merchant:
    @staticmethod
    def get_merchant(merchant):
        """Get merchant class object based on the merchnat name from BDD feature file
        Each merchant class contains payload for membership_cads end point"""

        switcher = {
            "BurgerKing": BurgerKingCard,
            "CooP": CoopCard,
            "FatFace": FatFaceCard,
            "HarveyNichols": HarveyNicholsCard,
            "Iceland": IcelandCard,
            "WHSmith": WHSmithCard,
            "Wasabi": WasabiCard,
        }
        return switcher.get(merchant)


class TestData:
    """Functions used to supply expected data to pytest test_ classes"""
    """Below functions read test data as "object" from test_data_sheet
     and retrieve the data from object inside the test class"""

    @staticmethod
    def get_membership_card_status_states():
        return TestDataUtils.TEST_DATA.membership_card_status_states

    @staticmethod
    def get_membership_card_status_reason_codes():
        return TestDataUtils.TEST_DATA.membership_card_status_reason_codes

    @staticmethod
    def get_data(merchant):
        switcher = {
            "BurgerKing": TestDataUtils.TEST_DATA.burger_king_membership_card,
            "CooP": TestDataUtils.TEST_DATA.coop_membership_card,
            "FatFace": TestDataUtils.TEST_DATA.fat_face_membership_card,
            "HarveyNichols": TestDataUtils.TEST_DATA.harvey_nichols_membership_card,
            "Iceland": TestDataUtils.TEST_DATA.iceland_membership_card,
            "WHSmith": TestDataUtils.TEST_DATA.whsmith_membership_card,
            "Wasabi": TestDataUtils.TEST_DATA.wasabi_membership_card,
        }
        return switcher.get(merchant)

    """Below functions read test data as "data" from the test_data sheet
    ( instead of data_object in other functions)"""

    @staticmethod
    def get_membership_plan_id(merchant):
        merchant_key = TestData.get_merchant_key(merchant)
        return TestDataUtils.TEST_DATA.membership_plan_id.get(merchant_key)

    @staticmethod
    def get_expected_membership_plan_json(merchant, env, channel=None):
        merchant_key = TestData.get_merchant_key(merchant)
        """Temporary solution as Iceland has different membership plan id for Bink & Barclays"""
        if env == "dev":
            if merchant == "Iceland" and channel == "Barclays":
                return constants.EXPECTED_MEMBERSHIP_PLANS_PATH_DEV + "/iceland_membership_plan_bmb.json"
            else:
                return constants.EXPECTED_MEMBERSHIP_PLANS_PATH_DEV + "/" + merchant_key + "_membership_plan.json"
        elif env == "staging":
            if merchant == "Iceland" and channel == "Barclays":
                return constants.EXPECTED_MEMBERSHIP_PLANS_PATH_STAGING + "/iceland_membership_plan_bmb.json"
            else:
                return constants.EXPECTED_MEMBERSHIP_PLANS_PATH_STAGING + "/" + merchant_key + "_membership_plan.json"
        elif env == "prod":
            if merchant == "Iceland" and channel == "barclays":
                return constants.EXPECTED_MEMBERSHIP_PLANS_PATH_PROD + "/iceland_membership_plan_bmb.json"
            elif merchant == "HarveyNichols" and channel == "barclays":
                return constants.EXPECTED_MEMBERSHIP_PLANS_PATH_PROD + "/harvey_nichols_membership_plan_bmb.json"
            else:
                return constants.EXPECTED_MEMBERSHIP_PLANS_PATH_PROD + "/" + merchant_key + "_membership_plan.json"

    @staticmethod
    def get_merchant_key(merchant):
        """Generate the merchant key based on the merchant value from bdd feature file"""

        switcher = {
            "BurgerKing": "burger_king",
            "CooP": "coop",
            "FatFace": "fat_face",
            "HarveyNichols": "harvey_nichols",
            "Iceland": "iceland",
            "WHSmith": "whsmith",
            "Wasabi": "wasabi",
        }
        return switcher.get(merchant)


class PaymentCardTestData:
    """This function is for future use - when more testing in payment cards"""

    @staticmethod
    def get_data(payment_card_provider="master"):
        switcher = {
            # "barclays": TestDataUtils.TEST_DATA.payment_card,
            "amex": TestDataUtils.TEST_DATA.amex_payment_card,
            "visa": TestDataUtils.TEST_DATA.visa_payment_card,
            "master": TestDataUtils.TEST_DATA.master_payment_card,
        }
        return switcher.get(payment_card_provider)
