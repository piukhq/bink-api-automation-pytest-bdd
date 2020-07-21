import config
import tests.helpers.constants as constants
from tests.helpers.test_data_utils import TestDataUtils
from tests.payload.membership_cards.burgerking import BurgerKingCard
from tests.payload.membership_cards.cooperative import CoopCard
from tests.payload.membership_cards.fatface import FatFaceCard
from tests.payload.membership_cards.harvey_nichols import HarveyNicholsCard
from tests.payload.membership_cards.iceland import IcelandCard
from tests.payload.membership_cards.whsmith import WHSmithCard
from tests.payload.membership_cards.wasabi import WasabiCard


class TestHelpers:

    @staticmethod
    def get_merchant(merchant):
        """Get merchant class object based on the merchnat name from BDD feature file
        Each merchant class contains payload for membership_cads end point"""

        switcher = {
            'BurgerKing': BurgerKingCard,
            'CooP': CoopCard,
            'FatFace': FatFaceCard,
            'HarveyNichols': HarveyNicholsCard,
            'Iceland': IcelandCard,
            'WHSmith': WHSmithCard,
            'Wasabi': WasabiCard
        }
        return switcher.get(merchant)

    @staticmethod
    def get_membership_plan_id(merchant):
        merchant_key = TestHelpers.get_merchant_key(merchant)
        return TestDataUtils.TEST_DATA.membership_plan_id.get(merchant_key)

    @staticmethod
    def get_expected_membership_plan_json(merchant):
        merchant_key = TestHelpers.get_merchant_key(merchant)
        return constants.EXPECTED_MEMBERSHIP_PLANS_PATH + '/' + merchant_key + '_membership_plan.json'

    @staticmethod
    def get_membership_card_number(merchant):
        switcher = {
            'BurgerKing': TEST_DATA.burger_king_membership_card1.get(constants.CARD_NUM),
            'CooP': TEST_DATA.coop_membership_card1.get(constants.CARD_NUM),
            'FatFace': TEST_DATA.fat_face_membership_card1.get(constants.CARD_NUM),
            'HarveyNichols': TEST_DATA.harvey_nichols_membership_card1.get(constants.CARD_NUM),
            'Iceland': TEST_DATA.iceland_membership_card1.get(constants.CARD_NUM),
            'WHSmith': TEST_DATA.whsmith_membership_card1.get(constants.CARD_NUM),
            'Wasabi': TEST_DATA.wasabi_membership_card1.get(constants.CARD_NUM),
        }
        return switcher.get(merchant)

    @staticmethod
    def get_merchant_key(merchant):
        """Generate the merchant key based on the merchant value from bdd feature file"""

        switcher = {
            'BurgerKing': 'burger_king',
            'CooP': 'coop',
            'FatFace': 'fat_face',
            'HarveyNichols': 'harvey_nichols',
            'Iceland': 'iceland',
            'WHSmith': 'whsmith',
            'Wasabi': 'wasabi'
        }
        return switcher.get(merchant)
