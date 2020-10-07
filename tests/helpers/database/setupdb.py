import psycopg2
import logging

from tests.helpers.test_data_utils import TestDataUtils


def connect_db():
    """Connect to Hermes"""
    try:
        connection = psycopg2.connect(
            user=get_db_credentials("user"),
            password="",
            host=get_db_credentials("host"),
            port=get_db_credentials("port"),
            database=get_db_credentials("database")
        )
        logging.info("Connected to Hermes")

    except (Exception, psycopg2.Error) as error:
        logging.info("Error while connecting to Hermes" + error)
    return connection


def execute_query_fetch_one(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchone()


def execute_query_fetch_all(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def clear_db(connection):
    if connection:
        connection.close()


def get_db_credentials(variable):
    """This function returns DB details for each environment"""
    return TestDataUtils.TEST_DATA.db_details.get(variable)
