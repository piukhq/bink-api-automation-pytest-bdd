import logging
import datetime
from dataclasses import dataclass

import tests.helpers.database.setupdb as db
from tests.helpers.database.settings import LOCAL_AES_KEY
from shared_config_storage.credentials.encryption import AESCipher


@dataclass
class SchemeAccountRecord:
    id: int
    status: int
    scheme_id: int
    link_or_join_date: datetime.datetime
    main_answer: str


@dataclass
class CredentialAns:

    """sub- Set of credential answers
     All credential answers need not be captured as some of them are
     already verifying as apart of response"""

    card_number: int
    email: str
    last_name: str
    post_code: str
    merchant_identifier: str


class QueryHermes:
    @staticmethod
    def fetch_scheme_account(journey_type, scheme_account_id):
        """Fetch the scheme account details using scheme_account_id """
        connection = db.connect_db()
        record = db.execute_query_fetch_one(connection, get_query(journey_type, scheme_account_id))

        if record is None:
            logging.error(f"'{scheme_account_id}' is an Invalid Scheme account id")
            raise Exception(f"'{scheme_account_id}' is an Invalid Scheme account id")
        else:
            scheme_account_record = SchemeAccountRecord(record[0],
                                                        record[1],
                                                        record[2],
                                                        record[3],
                                                        record[4])
        db.clear_db(connection)
        return scheme_account_record

    @staticmethod
    def fetch_credential_ans(merchant, scheme_account_id):

        """Query all credential answers for the current scheme"""
        connection = db.connect_db()
        query_credential_ans = """SELECT * FROM hermes.public.scheme_schemeaccountcredentialanswer
             where scheme_account_id='%s'""" % scheme_account_id
        record = db.execute_query_fetch_all(connection, query_credential_ans)

        if record is None:
            logging.error(f"Credential answers are not saved in DB for scheme account '{scheme_account_id}'")
            raise Exception(f"Credential answers are not saved in DB for scheme account '{scheme_account_id}'")
        else:
            logging.info(merchant + " Scheme Account  Credential Answers are:"
                                    "\n..............................................................................")
            for row in record:
                credential_qn_label = get_credential_qn_label(row[3], connection)
                logging.info(f"'{credential_qn_label[0]}' is '{row[1]}'")
                if credential_qn_label[0] == "card_number":
                    CredentialAns.card_number = row[1]
                elif credential_qn_label[0] == "email":
                    CredentialAns.email = row[1]
                elif credential_qn_label[0] == "last_name":
                    last_name = decrypt(row[1])
                    CredentialAns.last_name = last_name
                    logging.info(f"Decrypted value of Last Name is '{last_name}'")
                elif credential_qn_label[0] == "postcode":
                    post_code = decrypt(row[1])
                    CredentialAns.post_code = post_code
                    logging.info(f"Decrypted value of Post Code is '{post_code}'")
                elif credential_qn_label[0] == "merchant_identifier":
                    if len(row[1]) > 10:
                        merchant_identifier = decrypt(row[1])
                        logging.info(f"Decrypted value of Post Code is '{merchant_identifier}'")
                    else:
                        merchant_identifier = row[1]
                    CredentialAns.merchant_identifier = merchant_identifier

        logging.info("..............................................................................")
        db.clear_db(connection)
        return CredentialAns


def get_credential_qn_label(qn_id, connection):
    """The label for each credential answer has been fetched using the unique question_id
    which is obtained from scheme_schemeaccountcredentialanswer table"""
    query_credential_qns = """SELECT type FROM
                           hermes.public.scheme_schemecredentialquestion
                           where id='%s'""" % qn_id
    return db.execute_query_fetch_one(connection, query_credential_qns)


def get_query(journey_type, scheme_account_id):
    """Differentiate query to scheme_schemeaccount table for Add & Enrol Journeys"""
    if journey_type == "Enrol":
        query_scheme_account = """SELECT id,status,scheme_id,join_date,main_answer
         FROM hermes.public.scheme_schemeaccount WHERE id='%s'""" % scheme_account_id
    elif journey_type == "Add":
        query_scheme_account = """SELECT id,status,scheme_id,link_date,main_answer
                 FROM hermes.public.scheme_schemeaccount WHERE id='%s'""" % scheme_account_id

    return query_scheme_account


def decrypt(val):
    """Decrypt the Scheme Credential answers"""
    return AESCipher(LOCAL_AES_KEY.encode()).decrypt(val)
