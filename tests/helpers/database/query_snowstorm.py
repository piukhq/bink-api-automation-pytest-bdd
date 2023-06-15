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
    def fetch_event(journey_type, email):
        """Fetch the event using scheme account id"""
        connection = db.connect_snowstorm_db()
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
        query_event_record = f"""SELECT id, event_date_time, event_type, json
                               FROM snowstorm.public.events
                               WHERE event_type = '{journey_type}'
                               AND json ->> 'email' = '{email}' ORDER BY event_date_time DESC"""
    return query_event_record
