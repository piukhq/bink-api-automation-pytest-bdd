import logging
import time

from pytest_bdd import parsers, scenarios, then, when

from tests.conftest import channel, env, test_email
from tests.helpers import constants
from tests.helpers.database.query_snowstorm import QuerySnowstorm
from tests.helpers.test_context import TestContext
from tests.helpers.test_data_utils import TestDataUtils
from tests.step_definitions import test_membership_cards, test_membership_cards_multi_wallet, test_payment_cards

scenarios("events/")

"""Step definitions - Events """


@then(parsers.parse("I verify that {journey_type} event"))
def verify_loyalty_card_into_event_database(journey_type):
    time.sleep(5)
    logging.info(TestDataUtils.TEST_DATA.event_type.get(journey_type))
    event_record = QuerySnowstorm.fetch_event(
        TestDataUtils.TEST_DATA.event_type.get(journey_type), email=TestContext.user_email
    )
    logging.info(str(event_record))
    if TestContext.channel_name == "bink":
        assert event_record.json["channel"] == TestDataUtils.TEST_DATA.event_info.get(constants.CHANNEL_BINK)
        assert event_record.json["external_user_ref"] == ""
    else:
        assert event_record.json["channel"] == TestDataUtils.TEST_DATA.event_info.get(constants.CHANNEL_BARCLAYS)
        assert event_record.json["external_user_ref"] == TestContext.user_email
    assert event_record.event_type == TestDataUtils.TEST_DATA.event_type.get(journey_type)
    assert event_record.json["origin"] == TestDataUtils.TEST_DATA.event_info.get(constants.ORIGIN)
    assert event_record.json["email"] == TestContext.user_email
    return event_record


@then(parsers.parse("I verify {journey_type} loyalty scheme event is created for {user}"))
def verify_scheme_into_event_database(journey_type, user):
    time.sleep(5)
    logging.info(TestDataUtils.TEST_DATA.event_type.get(journey_type))

    event_record = QuerySnowstorm.fetch_event(
        TestDataUtils.TEST_DATA.event_type.get(journey_type),
        email=TestContext.user_email,
        scheme_id=TestContext.current_scheme_account_id,
    )

    logging.info(str(event_record))
    if user == "bink_user":
        assert event_record.json["external_user_ref"] == "", "external user ref didnt match"
        assert event_record.json["channel"] == TestDataUtils.TEST_DATA.event_info.get(
            constants.CHANNEL_BINK
        ), "channel didnt match"
    elif user == "barclays_user":
        assert event_record.json["external_user_ref"] == TestContext.user_email, "external user ref didnt match"
        assert event_record.json["channel"] == TestDataUtils.TEST_DATA.event_info.get(
            constants.CHANNEL_BARCLAYS
        ), "channel didnt match"
    assert event_record.event_type == TestDataUtils.TEST_DATA.event_type.get(journey_type), "eventype didnt match"
    assert event_record.json["email"] == TestContext.user_email, "user email didnt match"
    assert event_record.json["scheme_account_id"] == TestContext.current_scheme_account_id, "scheme id didnt match"

    if journey_type in ["lc_join_success", "lc_register_success"]:
        assert (
            event_record.json["consents"][0]["slug"] == TestDataUtils.TEST_DATA.event_info["TheWorks_slug"]
            or TestDataUtils.TEST_DATA.event_info["iceland_slug"]
        ), "consent slug didn't match"
        assert event_record.json["consents"][0]["response"] == TestDataUtils.TEST_DATA.event_info.get(
            constants.RESPONSE
        ), "consent response didn't match"
    return event_record


@then(
    parsers.parse(
        'I verify {journey_type} pll event is created for {user} for status {from_state}'
        ' to {to_state} and slug {slug}'
    )
)
def pll_link_status_change_event(journey_type, user, from_state, to_state, slug):
    if slug == "null":
        TestContext.event_slug = ""
    else:
        TestContext.event_slug = slug
    time.sleep(8)
    logging.info(TestDataUtils.TEST_DATA.event_type.get(journey_type))
    event_record = QuerySnowstorm.fetch_event(
        TestDataUtils.TEST_DATA.event_type.get(journey_type), TestContext.user_email, TestContext.event_slug,
    )
    logging.info(str(event_record))
    assert event_record.event_type == TestDataUtils.TEST_DATA.event_type.get(
        journey_type
    ), "event type do not match"

    if user == "bink_user":
        assert event_record.json["external_user_ref"] == "", "external user ref didnt match"
        assert event_record.json["channel"] == TestDataUtils.TEST_DATA.event_info.get(
            constants.CLIENT_ID_BINK
        ), "channel didnt match"
    elif user == "barclays_user":
        assert event_record.json["external_user_ref"] == TestContext.user_email, "external user ref didnt match"
        assert event_record.json["channel"] == TestDataUtils.TEST_DATA.event_info.get(
            constants.CLIENT_ID_BARCLAYS
        ), "channel didnt match"
    assert event_record.json["email"] == TestContext.user_email, "email do not match"
    assert (
        event_record.json["scheme_account_id"] == TestContext.current_scheme_account_id
    ), "scheme_account_id do not match"
    if slug == "null":
        assert event_record.json["slug"] == "", "slug do not match"
    else:
        assert event_record.json["slug"] == slug, "slug do not match"
    if from_state == "null":
        assert event_record.json["from_state"] is None, "from_state do not match"
    else:
        assert event_record.json["from_state"] == int(from_state), "from_state do not match"
    if to_state == "null":
        assert event_record.json["to_state"] is None, "to_state do not match"
    else:
        assert event_record.json["to_state"] == int(to_state), "to_state do not match"

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


@when(parsers.parse('I perform POST request to create a "{merchant}" membershipcard account with enrol credentials'))
def i_perform_post_enrol_membership_card(merchant, test_email, env, channel):
    test_membership_cards.enrol_membership_account(merchant, test_email, env, channel)


@when(parsers.parse('I perform GET request to verify the "{merchant}" membershipcard account is created'))
def i_perform_get_request(merchant):
    test_membership_cards.verify_membership_card_is_created(merchant)


@when(parsers.parse('I perform POST request to add and auth "{merchant}" membership card with "{credentials}"'))
def add_auth_membership_event(merchant, credentials):
    test_membership_cards_multi_wallet.add_auth_membership_card(merchant, credentials)


@when(parsers.parse('I perform POST request to add "{payment_card_provider}" payment card to wallet'))
def add_payment_cards_events(payment_card_provider="master"):
    """Call to add payment card in test_payment_cards"""
    test_payment_cards.add_payment_card(payment_card_provider="master")


@when(parsers.parse('I perform POST request to add & auto link "{merchant}" membership card'))
def add_and_link_event(merchant):
    test_membership_cards.add_and_link_membership_card(merchant)


@when(parsers.parse('I perform POST request to add and auth for "{merchant}" membershipcard with "{invalid_data}"'))
def post_request_to_add_invalid_membershipcard(merchant, invalid_data):
    test_membership_cards_multi_wallet.add_auth_membership_card(merchant, invalid_data)


@when("I perform PATCH request to link membership card to payment card")
def patch_mcard_pcard_event():
    test_payment_cards.patch_mcard_pcard()


@when(
    parsers.parse(
        'For {user} I perform GET request to verify the "{merchant}" '
        "membershipcard is added to the wallet with invalid data"
    )
)
def get_request_add_auth_invalid_data(user, merchant):
    test_membership_cards_multi_wallet.invalid_membership_card_is_added_to_wallet(user, merchant)


@when(
    parsers.parse(
        'I perform POST request to create a "{merchant}" membership card with "{invalid}" enrol credentials'
    )
)
def perform_join_with_invalid_credential(merchant, invalid):
    test_membership_cards.enrol_membership_account_invalid_credentials(merchant, test_email, env, channel, invalid)


@when(parsers.parse('I perform GET request to verify the "{merchant}" membership card is created with invalid data'))
def get_join_with_invalid_credential(merchant):
    test_membership_cards.verify_invalid_membership_card_is_created(merchant)


@when(
    parsers.parse(
        'I perform POST request to join "{merchant}" membershipcard with "{enrol_status}" enrol credentials'
    )
)
def post_request_for_failed_enrol(merchant, enrol_status):
    test_membership_cards_multi_wallet.enrol_membership_card_account(
        enrol_status=enrol_status,
        merchant=merchant,
        test_email="pytest_multiple_wallet@bink.com",
        env="staging",
        channel="barclays",
    )


@when(parsers.parse('I perform POST request to add "{merchant}" membership card for "{scheme_status}"'))
def add_only_membership_card(merchant, scheme_status):
    test_membership_cards_multi_wallet.add_only_membership_card(merchant, scheme_status)


@when(parsers.parse('I perform PATCH request to create "{merchant}" "{scheme_status}"'))
def register_fail(merchant, test_email, env, channel, scheme_status):
    test_membership_cards_multi_wallet.register_fail(merchant, test_email, env, channel, scheme_status)


@when(
    parsers.parse(
        "For {user} I perform GET request to verify the {merchant} "
        "membership card is added to the wallet with "
        "invalid data"
    )
)
def invalid_membership_card_is_added_to_wallet(user, merchant):
    test_membership_cards_multi_wallet.invalid_membership_card_is_added_to_wallet(user, merchant)


@when(parsers.parse('I perform PATCH request to create a "{merchant}" ghost membership account with enrol credentials'))
def register_ghost_membership_account(merchant, test_email, env, channel):
    test_membership_cards.register_ghost_membership_account(merchant, test_email, env, channel)


@when(parsers.parse('I perform POST request to create a "{merchant}" membership account with enrol credentials'))
def enrol_membership_account_event(merchant, test_email, env, channel):
    test_membership_cards.enrol_membership_account(merchant, test_email, env, channel)


@when(
    parsers.parse(
        "For {user} I perform GET request to verify the {merchant} membership card is added to the wallet"
        " after {scheme_status}"
    )
)
def get_membership_card(user, merchant, scheme_status):
    test_membership_cards_multi_wallet.get_membership_card(user, merchant, scheme_status)


@when(parsers.parse("I perform POST request to add {card_type} payment card to wallet of {payment_card_provider} type"))
def post_add_payment_card_always_autolink(card_type, payment_card_provider):
    test_membership_cards_multi_wallet.post_add_payment_card_always_autolink(card_type, payment_card_provider)
