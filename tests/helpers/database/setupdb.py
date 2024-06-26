import psycopg2
import logging
from settings import HERMES_DATABASE_URI, HARMONIA_DATABASE_URI, SNOWSTORM_DATABASE_URI


def connect_db():
    """Connect to Hermes"""
    try:
        connection = psycopg2.connect(HERMES_DATABASE_URI)
        logging.info("Connected to Hermes")

    except Exception as error:
        raise Exception(f"Error while connecting to Hermes '{str(error)}'")
    return connection


def connect_harmonia_db():
    """Connect to Harmonia"""
    try:
        connection = psycopg2.connect(HARMONIA_DATABASE_URI)
        logging.info("Connected to Harmonia")

    except Exception as error:
        raise Exception(f"Error while connecting to Harmonia '{str(error)}'")
    return connection


def connect_snowstorm_db():
    """Connect to Snowstorm"""
    try:
        connection = psycopg2.connect(SNOWSTORM_DATABASE_URI)
        logging.info("Connected to Snowstorm")

    except Exception as error:
        raise Exception(f"Error while connecting to Snowstorm '{str(error)}'")
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
