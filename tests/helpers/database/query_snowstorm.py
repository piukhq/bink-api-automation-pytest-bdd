import datetime
import logging

from dataclasses import dataclass

import tests.helpers.database.setupdb as db


@dataclass
class EventRecord:
    id: int
    event_date_time: datetime.datetime
    event_type: str
    json: bool


class QuerySnowstorm:
    @staticmethod
    def fetch_event(journey_type, email, event_slug=None, scheme_id=None):
        """Fetch the event using scheme account id or event_slug """
        connection = db.connect_snowstorm_db()
        if event_slug or event_slug == '':
            record = db.execute_query_fetch_one(connection,
                                                get_pll_status_change_event(journey_type, event_slug, email))
        elif scheme_id:
            record = db.execute_query_fetch_one(connection,
                                                get_user_with_scheme_created_event(journey_type, email, scheme_id))
        else:
            record = db.execute_query_fetch_one(connection, get_user_created_event(journey_type, email))

        if record is None:
            raise Exception("Record not found")
        else:
            event_record = EventRecord(record[0], record[1], record[2], record[3])
        db.clear_db(connection)
        return event_record


def get_user_created_event(journey_type, email):
    if journey_type == "":
        logging.info("Scheme did not attach to the wallet")
    else:
        query_event_record = f"""SELECT id, event_date_time, event_type, json FROM snowstorm.public.events \
        WHERE event_type = '{journey_type}' AND json ->> 'email' = '{email}' ORDER BY event_date_time DESC"""

    return query_event_record


def get_user_with_scheme_created_event(journey_type, email, scheme_id):
    query_event_record = f"""SELECT id, event_date_time, event_type, json FROM snowstorm.public.events \
    WHERE event_type = '{journey_type}' AND json ->> 'email' = '{email}' \
    AND json ->> 'scheme_account_id' = '{scheme_id}' ORDER BY event_date_time DESC"""
    logging.info(f"scheme id is: {scheme_id}")
    return query_event_record


def get_pll_status_change_event(journey_type, event_slug, email):
    query_event_record = f"""SELECT id, event_date_time, event_type, json FROM snowstorm.public.events \
    WHERE event_type = '{journey_type}' AND json ->> 'email' = '{email}' \
    AND json ->> 'slug' = '{event_slug}' ORDER BY event_date_time DESC"""
    logging.info(query_event_record)
    return query_event_record
