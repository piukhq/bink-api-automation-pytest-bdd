import tests.helpers.constants as constants
from tests.helpers.test_data_utils import TestDataUtils
from tests.payload.membership_cards.iceland import IcelandCard
from tests.payload.membership_cards.square_meal import SquareMealCard
from tests.payload.membership_cards.wasabi import WasabiCard
from tests.payload.membership_cards.trenette import TrenetteCard
from tests.payload.membership_cards.viator import ViatorCard
from tests.payload.membership_cards.theworks import TheWorksCard


class Merchant:
    @staticmethod
    def get_merchant(merchant):
        """Get merchant class object based on the merchnat name from BDD feature file
        Each merchant class contains payload for membership_cads end point"""

        match merchant:
            case "Iceland":
                return IcelandCard
            case "Wasabi":
                return WasabiCard
            case "SquareMeal":
                return SquareMealCard
            case "Trenette":
                return TrenetteCard
            case "Viator":
                return ViatorCard
            case "TheWorks":
                return TheWorksCard

    @staticmethod
    def get_scheme_cred_main_ans(merchant):
        """Return main_scheme_account_answers for all merchants"""

        match merchant:
            case "Iceland":
                return TestDataUtils.TEST_DATA.iceland_membership_card.get(constants.CARD_NUM)
            case "Wasabi":
                return TestDataUtils.TEST_DATA.wasabi_membership_card.get(constants.CARD_NUM)
            case "SquareMeal":
                return TestDataUtils.TEST_DATA.square_meal_membership_card.get(constants.CARD_NUM)
            case "Trenette":
                return TestDataUtils.TEST_DATA.trenette_membership_card.get(constants.CARD_NUM)
            case "Viator":
                return TestDataUtils.TEST_DATA.viator_membership_card.get(constants.CARD_NUM)
            case "TheWorks":
                return TestDataUtils.TEST_DATA.the_works_membership_card.get(constants.CARD_NUM)


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

        match merchant:
            case "Iceland":
                return TestDataUtils.TEST_DATA.iceland_membership_card
            case "Wasabi":
                return TestDataUtils.TEST_DATA.wasabi_membership_card
            case "SquareMeal":
                return TestDataUtils.TEST_DATA.square_meal_membership_card
            case "Trenette":
                return TestDataUtils.TEST_DATA.trenette_membership_card
            case "Viator":
                return TestDataUtils.TEST_DATA.viator_membership_card
            case "TheWorks":
                return TestDataUtils.TEST_DATA.the_works_membership_card

    """Below functions read test data as "data" from the test_data sheet
    ( instead of data_object in other functions)"""

    @staticmethod
    def get_membership_plan_id(merchant):
        merchant_key = TestData.get_merchant_key(merchant)
        return TestDataUtils.TEST_DATA.membership_plan_id.get(merchant_key)

    @staticmethod
    def get_expected_membership_plan_json(merchant, env, channel=None):

        merchant_key = TestData.get_merchant_key(merchant)
        mem_plan_path = TestData.get_mem_plan_path(env)

        if merchant == "Iceland" and channel == "barclays":
            """Temporary case as Iceland has different membership plan id for Bink & Barclays"""
            return mem_plan_path + "/" + merchant_key + "_membership_plan_bmb.json"
        else:
            return mem_plan_path + "/" + merchant_key + "_membership_plan.json"

    @staticmethod
    def get_mem_plan_path(env):
        """return the base path of stored membership plan json
        for any merchant based on environment"""

        match env:
            case "dev":
                return constants.EXPECTED_MEMBERSHIP_PLANS_PATH_DEV
            case "staging":
                return constants.EXPECTED_MEMBERSHIP_PLANS_PATH_STAGING
            case "prod":
                return constants.EXPECTED_MEMBERSHIP_PLANS_PATH_PROD

    @staticmethod
    def get_expected_membership_card_json(merchant, env):

        merchant_key = TestData.get_merchant_key(merchant)
        membership_card_path = TestData.get_membership_card_path(env)
        return membership_card_path + "/" + merchant_key + "_membership_card.json"

    @staticmethod
    def get_membership_card_path(env):
        """return the base path of stored membership plan json
        for any merchant based on environment"""
        match env:
            case "dev": return constants.MEMBERSHIP_CARD_DEV
            case "staging": return constants.MEMBERSHIP_CARD_STAGING
            case "prod": return constants.MEMBERSHIP_CARD_PROD

    @staticmethod
    def get_merchant_key(merchant):
        """Generate the merchant key based on the
        merchant value from bdd feature file"""

        match merchant:
            case "Iceland": return "iceland"
            case "Wasabi": return "wasabi"
            case "SquareMeal": return "square_meal"
            case "Trenette": return "trenette"
            case "Viator": return "viator"
            case "TheWorks": return "the_works"

    @staticmethod
    def get_vop_status():
        return TestDataUtils.TEST_DATA.vop_status


class PaymentCardTestData:
    """This function is for future use - when more testing in payment cards"""

    @staticmethod
    def get_data(payment_card_provider="master"):

        match payment_card_provider:
            case "amex":
                return TestDataUtils.TEST_DATA.amex_payment_card
            case "visa":
                return TestDataUtils.TEST_DATA.visa_payment_card
            case "master":
                return TestDataUtils.TEST_DATA.master_payment_card
