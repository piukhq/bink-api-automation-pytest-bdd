import logging
import time

from pytest_bdd import parsers, scenarios, then, when

from tests.helpers import constants

from tests.helpers.database.query_snowstorm import QuerySnowstorm
from tests.helpers.test_context import TestContext
from tests.helpers.test_data_utils import TestDataUtils
from tests.step_definitions import test_membership_cards, test_membership_cards_multi_wallet

scenarios("events/")

"""Step definitions - Events """


@then(parsers.parse("I verify that {journey_type} event"))
def verify_loyalty_card_into_event_database(journey_type):
    # TestContext.extid = TestContext.external_id[user]
    time.sleep(5)
    logging.info(TestDataUtils.TEST_DATA.event_type.get(journey_type))
    event_record = QuerySnowstorm.fetch_event(TestDataUtils.TEST_DATA.event_type.get(journey_type),
                                              email=TestContext.user_email)
    logging.info(str(event_record))
    if TestContext.channel_name == "bink":
        assert event_record.json["channel"] == TestDataUtils.TEST_DATA.event_info.get(constants.CHANNEL_BINK) \
               and event_record.json["external_user_ref"] == ""
    else:
        assert event_record.json["channel"] == TestDataUtils.TEST_DATA.event_info.get(constants.CHANNEL_BARCLAYS) \
               and event_record.json["external_user_ref"] == TestContext.user_email
    assert (
        event_record.event_type == TestDataUtils.TEST_DATA.event_type.get(journey_type)
        and event_record.json["origin"] == TestDataUtils.TEST_DATA.event_info.get(constants.ORIGIN)
        and event_record.json["email"] == TestContext.user_email
    )
    return event_record


@then(parsers.parse("I verify {journey_type} loyalty scheme event is created for {user}"))
def verify_scheme_into_event_database(journey_type, user):
    # TestContext.extid = TestContext.external_id[user]
    time.sleep(5)
    logging.info(TestDataUtils.TEST_DATA.event_type.get(journey_type))
    event_record = QuerySnowstorm.fetch_event(TestDataUtils.TEST_DATA.event_type.get(journey_type),
                                              email=TestContext.user_email)
    logging.info(str(event_record))
    if user == "bink_user":
        assert event_record.json["external_user_ref"] == "" \
               and event_record.json["channel"] == TestDataUtils.TEST_DATA.event_info.get(constants.CHANNEL_BINK)
    elif user == "barclays_user":
        assert event_record.json["external_user_ref"] == TestContext.user_email \
               and event_record.json["channel"] == TestDataUtils.TEST_DATA.event_info.get(constants.CHANNEL_BARCLAYS)
    assert (
        event_record.event_type == TestDataUtils.TEST_DATA.event_type.get(journey_type)
        and event_record.json["email"] == TestContext.user_email
        and event_record.json["scheme_account_id"] == TestContext.current_scheme_account_id
    )
    return event_record


@when(parsers.parse('I perform POST request to add "{merchant}" membership card to wallet'))
def post_membership_cards_events(merchant):
    """Call to add_card in test_membership_cards"""
    test_membership_cards.add_membership_card(merchant)


@when(parsers.parse('I perform GET request to verify the "{merchant}" membership card added to the wallet'))
def get_membership_card_events(merchant):
    """Call to add_card in test_membership_cards"""
    test_membership_cards.verify_get_membership_card(merchant)


@then(parsers.parse('I verify the data stored in DB after "{journey_type}" journey for "{merchant}"'))
def verify_data_stored_in_db(journey_type, merchant):
    test_membership_cards_multi_wallet.verify_db_details(journey_type, merchant, env="staging")


@when(parsers.parse('I perform POST request to add and auth "{merchant}" membershipcard with "{credentials}"'))
def verify_add_auth_membership(merchant, credentials):
    test_membership_cards_multi_wallet.add_auth_membership_card(merchant, credentials)
