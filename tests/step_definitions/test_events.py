import logging
import time

from pytest_bdd import parsers, scenarios, then

from tests.helpers import constants

from tests.helpers.database.query_snowstorm import QuerySnowstorm
from tests.helpers.test_context import TestContext
from tests.helpers.test_data_utils import TestDataUtils

scenarios("events/")

"""Step definitions - Events """


@then(parsers.parse("I verify that {journey_type} event"))
def verify_loyalty_card_into_event_database(journey_type):
    # TestContext.extid = TestContext.external_id[user]
    time.sleep(5)
    logging.info(TestDataUtils.TEST_DATA.event_type.get(journey_type))
    event_record = QuerySnowstorm.fetch_event(TestDataUtils.TEST_DATA.event_type.get(journey_type))
    logging.info(str(event_record))

    assert (
        event_record.event_type == TestDataUtils.TEST_DATA.event_type.get(journey_type)
        and event_record.json["origin"] == TestDataUtils.TEST_DATA.event_info.get(constants.ORIGIN)
        and event_record.json["external_user_ref"] == ""
        and event_record.json["channel"] == TestDataUtils.TEST_DATA.event_info.get(constants.CHANNEL_BINK)
        and event_record.json["email"] == TestContext.email
    )
    return event_record
