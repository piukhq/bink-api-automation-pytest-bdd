import config
from tests.api.base import Endpoint
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
        switcher = {
            'BurgerKing': Endpoint.TEST_DATA.membership_plan_id.get('burger_king'),
            'CooP': Endpoint.TEST_DATA.membership_plan_id.get('coop'),
            'FatFace': Endpoint.TEST_DATA.membership_plan_id.get('fat_face'),
            'HarveyNichols': Endpoint.TEST_DATA.membership_plan_id.get('harvey_nichols'),
            'Iceland': Endpoint.TEST_DATA.membership_plan_id.get('iceland'),
            'WHSmith': Endpoint.TEST_DATA.membership_plan_id.get('whsmith'),
            'Wasabi': Endpoint.TEST_DATA.membership_plan_id.get('wasabi')
        }
        return switcher.get(merchant)

