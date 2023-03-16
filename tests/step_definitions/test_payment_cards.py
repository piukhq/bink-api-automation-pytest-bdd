from pytest_bdd import (
    scenarios,
    then,
    when,
    parsers,
)
import logging
import json
import time
import tests.api as api

from requests.exceptions import HTTPError

from tests.helpers.database.query_hermes import QueryHermes
from tests.requests.payment_cards import PaymentCards
from tests.api.base import Endpoint
from json import JSONDecodeError
import tests.helpers.constants as constants
from tests.helpers.test_context import TestContext
from tests.helpers.test_helpers import PaymentCardTestData, TestData
import tests.step_definitions.test_membership_cards as test_membership_cards

scenarios("payment_cards/")

"""Step definitions - Add Payment Card """


@when(parsers.parse('I perform POST request to add "{payment_card_provider}" payment card to wallet'))
@when(parsers.parse("I perform POST request to add {payment_card_provider} payment card to wallet"))
def add_payment_card(payment_card_provider="master"):
    response = PaymentCards.add_payment_card(TestContext.token, payment_card_provider)
    assert response.status_code == 201 or 200, f"Payment card addition for '{payment_card_provider}' is not successful"
    response_json = response_to_json(response)
    logging.info(
        f"The response of POST/PaymentCard '{payment_card_provider}' is: \n\n"
        + Endpoint.BASE_URL
        + api.ENDPOINT_PAYMENT_CARDS
        + "\n\n"
        + json.dumps(response_json, indent=4)
    )
    TestContext.current_payment_card_id = response_json.get("id")
    return TestContext.current_payment_card_id


@when(parsers.parse('I perform POST request to enrol new "{payment_card_provider}" payment card to wallet'))
def add_new_payment_card(payment_card_provider="master"):
    response = PaymentCards.add_new_payment_card(TestContext.token, payment_card_provider)
    response_json = response_to_json(response)
    assert (
            response.status_code == 201
            and response_json["membership_cards"] == []
            and response_json["status"] == TestData.get_membership_card_status_states().get(constants.PENDING)
            and response_json["card"]["first_six_digits"]
            == PaymentCardTestData.get_data(payment_card_provider).get(constants.FIRST_SIX_DIGITS)
            and response_json["card"]["last_four_digits"]
            == PaymentCardTestData.get_data(payment_card_provider).get(constants.LAST_FOUR_DIGITS)
            and PaymentCardTestData.get_data(payment_card_provider).get(
                constants.MONTH) == response_json["card"]["month"]
            and response_json["card"]["year"] == PaymentCardTestData.get_data(payment_card_provider).get(constants.YEAR)
            and response_json["card"]["country"] == "UK"
            and response_json["card"]["currency_code"] == "GBP"
            and response_json["card"]["name_on_card"] == TestContext.name_on_payment_card
            and response_json["card"]["provider"]
            == PaymentCardTestData.get_data(payment_card_provider).get(constants.PAYMENT_PROVIDER)
            and response_json["card"]["type"] == "debit"
            and response_json["images"][0]["url"]
            == PaymentCardTestData.get_data(payment_card_provider).get(constants.PAYMENT_URL)
            and response_json["images"][0]["type"] == 0
            and response_json["images"][0]["encoding"]
            == PaymentCardTestData.get_data(payment_card_provider).get(constants.PAYMENT_ENCODING)
            and response_json["images"][0]["description"]
            == PaymentCardTestData.get_data(payment_card_provider).get(constants.PAYMENT_DISCRIPTION)
            and response_json["account"]["verification_in_progress"]
            == PaymentCardTestData.get_data(payment_card_provider).get(constants.PAYMENT_VERIFICATION)
            and response_json["account"]["status"] == 1
            and response_json["account"]["consents"][0]["latitude"] == 51.405372
            and response_json["account"]["consents"][0]["longitude"] == -0.678357
            and response_json["account"]["consents"][0]["timestamp"] == TestContext.payment_account_timestamp
            and response_json["account"]["consents"][0]["type"] == 1
    ), f"Adding New Payment card for '{payment_card_provider}' is not successful"
    logging.info(
        f"The response of new POST/PaymentCard '{payment_card_provider}' is: \n\n"
        + Endpoint.BASE_URL
        + api.ENDPOINT_PAYMENT_CARDS
        + "\n\n"
        + json.dumps(response_json, indent=4)
    )
    TestContext.current_payment_card_id = response_json.get("id")
    return TestContext.current_payment_card_id


@when("I perform the GET request to verify the payment card has been added successfully to the wallet")
def verify_payment_card_added():
    response = PaymentCards.get_payment_card(TestContext.token, TestContext.current_payment_card_id)
    response_json = response.json()
    logging.info(
        "The response of GET/PaymentCard/id is: \n\n"
        + Endpoint.BASE_URL
        + api.ENDPOINT_PAYMENT_CARD.format(TestContext.current_payment_card_id)
        + "\n\n"
        + json.dumps(response_json, indent=4)
    )
    assert (
            response.status_code == 200
            and response_json["id"] == TestContext.current_payment_card_id
            and response_json["status"] == PaymentCardTestData.get_data().get(constants.PAYMENT_CARD_STATUS)
    ), "Payment card addition is not successful"
    return response


@when("I perform POST request to add multiple payment cards to wallet")
def add_multiple_payment_cards():
    """Adding a master card"""
    add_payment_card("master")
    add_payment_card("amex")
    # add_payment_card("visa")
    """Visa is taking more time to get authorised"""
    time.sleep(3)


@when("I perform the GET request to verify all the payment card has been added successfully to the wallet")
def verify_multi_payment_card_added():
    response = PaymentCards.get_payment_cards(TestContext.token)
    response_json = response.json()
    logging.info(
        "The response of GET/PaymentCards is: \n\n"
        + Endpoint.BASE_URL
        + api.ENDPOINT_PAYMENT_CARDS
        + "\n\n"
        + json.dumps(response_json, indent=4)
    )
    assert (
            response.status_code == 200
            and response_json[0]["status"] == PaymentCardTestData.get_data().get(constants.PAYMENT_CARD_STATUS)
            and response_json[1]["status"] == PaymentCardTestData.get_data().get(constants.PAYMENT_CARD_STATUS)
    ), "Payment card addition is not successful"
    return response


@then("Ensure only one payment card returned in the response")
def payment_card_link():
    response_json = response_to_json(TestContext.response)
    assert len(response_json["payment_cards"]) == 1, "The Pll link is not successful"
    logging.info("Only one payment card is linked to membership card")


@when("I perform PATCH request to link membership card to payment card")
def patch_mcard_pcard():
    response = PaymentCards.patch_mcard_pcard(
        TestContext.token, TestContext.current_scheme_account_id, TestContext.current_payment_card_id
    )
    response_json = response_to_json(response)

    logging.info(
        "The response of PATCH/membership_card/payment_card is :\n\n"
        + Endpoint.BASE_URL
        + api.ENDPOINT_PATCH_MEMBERSHIP_PAYMENT.format(
            TestContext.current_scheme_account_id, TestContext.current_payment_card_id
        )
        + "\n\n"
        + json.dumps(response_json, indent=4)
    )
    assert (
            response.status_code == 201
            and response_json["id"] == TestContext.current_payment_card_id
            and response_json["membership_cards"][0]["active_link"]
            and response_json["membership_cards"][0]["id"] == TestContext.current_scheme_account_id
    ), "Validations in PATCH/membership_card/payment_card failed"


@when("I perform PATCH request to link payment card to membership card")
def patch_pcard_mcard():
    response = PaymentCards.patch_pcard_mcard(
        TestContext.token, TestContext.current_payment_card_id, TestContext.current_scheme_account_id
    )
    response_json = response_to_json(response)

    logging.info(
        "The response of DELETE/membership_card/payment_card is :\n\n"
        + Endpoint.BASE_URL
        + api.ENDPOINT_PATCH_PAYMENT_MEMBERSHIP.format(
            TestContext.current_payment_card_id, TestContext.current_scheme_account_id
        )
        + "\n\n"
        + json.dumps(response_json, indent=4)
    )
    assert (
            response.status_code == 201
            and response_json["id"] == TestContext.current_scheme_account_id
            and response_json["payment_cards"][0]["active_link"]
            and response_json["payment_cards"][0]["id"] == TestContext.current_payment_card_id
    ), "Validations in PATCH/membership_card/payment_card failed"


@then("I perform DELETE request to delete the link between membership_card & payment_card")
def delete_mcard_pcard_link():
    response = PaymentCards.delete_mcard_pcard(
        TestContext.token, TestContext.current_scheme_account_id, TestContext.current_payment_card_id
    )
    assert response.status_code == 200, (
        f"DELETE/membership_card/payment_card failed with reason code" f" '{response.status_code}'"
    )
    logging.info(f"The response code of DELETE/membership_card/payment_card is '{response.status_code}'")


@then("I perform DELETE request to delete the link between payment_card & membership_card")
def delete_pcard_mcard_link():
    response = PaymentCards.delete_pcard_mcard(
        TestContext.token, TestContext.current_payment_card_id, TestContext.current_scheme_account_id
    )
    assert response.status_code == 200, (
        f"DELETE/payment_card/membership_card failed with reason code" f" '{response.status_code}'"
    )
    logging.info(f"The response code of DELETE/payment_card/membership_card is '{response.status_code}'")


@when("I perform GET/payment_card/id request to verify the membership card is linked to the payment card")
def verify_mcard_pacrd_link():
    response = verify_payment_card_added()
    response_json = response_to_json(response)
    assert (
            response_json["membership_cards"][0]["id"] == TestContext.current_scheme_account_id
            and response_json["membership_cards"][0]["active_link"]
    ), "Membership card  link to the payment cards is not a success"
    logging.info(
        f"membership card '{TestContext.current_scheme_account_id}'"
        f" is linked to the payment card '{TestContext.current_payment_card_id}'"
    )


@when("I perform the GET/payment_cards request to verify the membership card is linked to all payment cards")
def verify_multi_payment_card_add_link():
    response = verify_multi_payment_card_added()
    response_json = response_to_json(response)
    assert (
            response_json[0]["membership_cards"][0]["id"] == TestContext.current_scheme_account_id
            and response_json[0]["membership_cards"][0]["active_link"]
            and response_json[1]["membership_cards"][0]["id"] == TestContext.current_scheme_account_id
            and response_json[1]["membership_cards"][0]["active_link"]
    ), "Membership card link to all the payment cards is not a success"


@then("I perform GET/payment_card/id request to verify the membership card is unlinked")
def verify_membership_card_unlink():
    time.sleep(2)
    response = verify_payment_card_added()
    response_json = response_to_json(response)
    assert response_json["membership_cards"] == [], "membership is not successfully unlink even after deletion"
    logging.info("Membership card is successfully unlinked ")


@then("I perform GET request to verify the membership card is unlinked from all payment cards")
def verify_membership_cards_unlink():
    time.sleep(2)
    response = verify_multi_payment_card_added()
    response_json = response_to_json(response)
    assert (
            response_json[0]["membership_cards"] == []
            and response_json[1]["membership_cards"] == []
            # and response_json[2]["membership_cards"] == []
    ), "membership is not successfully unlink even after deletion"
    logging.info(
        f"Membership card '{TestContext.current_scheme_account_id}' is successfully unlinked from"
        f"Payment card '{TestContext.current_payment_card_id}'"
    )

    """Storing each payment card ids for deletion"""
    TestContext.payment_card_1 = response_json[0]["id"]
    TestContext.payment_card_2 = response_json[1]["id"]
    # TestContext.payment_card_3 = response_json[2]["id"]


@then(
    parsers.parse(
        "I perform GET/membership_card/id request to verify the payment card is unlinked from"
        ' "{merchant}" membership card'
    )
)
def verify_payment_card_unlink(merchant):
    time.sleep(2)
    response = test_membership_cards.verify_get_membership_card(merchant)
    response_json = response_to_json(response)
    assert response_json["payment_cards"] == [], "Payment card is not successfully unlink even after deletion"
    logging.info(
        f"Payment card '{TestContext.current_payment_card_id}' is successfully unlinked from "
        f"membership_card '{TestContext.current_scheme_account_id}'"
    )


@then("I perform DELETE request to delete all payment cards")
def delete_all_payment_cards():
    response_payment_card_1 = PaymentCards.delete_payment_card(TestContext.token, TestContext.payment_card_1)
    response_payment_card_2 = PaymentCards.delete_payment_card(TestContext.token, TestContext.payment_card_2)
    # response_payment_card_3 = PaymentCards.delete_payment_card(TestContext.token, TestContext.payment_card_3)

    try:
        if response_payment_card_1.status_code == 200 or response_payment_card_2.status_code == 200:
            # or response_payment_card_3.status_code == 200:
            logging.info("Payment card is deleted successfully")
        else:
            logging.info("Payment card is already  deleted")

    except HTTPError as network_response:
        assert network_response.response.status_code == 404 or 400, "Payment card deletion is not successful"


@then("I perform DELETE request to delete the payment card by hash")
def delete_payment_card():
    response = PaymentCards.delete_payment_card_with_hash(TestContext.token)
    logging.info("response.status_code" + response.status_code.__str__())
    assert response.status_code == 200, "Payment card deletion by hash is not successful"
    logging.info(f"Payment card '{TestContext.current_payment_card_id}' is deleted by hash")


"""Call to membership_cards functions"""


@when(parsers.parse('I perform POST request to add "{merchant}" membership card to my wallet'))
def post_membership_cards(merchant):
    """Call to add_card in test_membership_cards"""
    test_membership_cards.add_membership_card(merchant)


@when(parsers.parse('I perform GET request to verify the "{merchant}" membership card is added to the wallet'))
def get_membership_card(merchant):
    """Call to add_card in test_membership_cards"""
    test_membership_cards.verify_get_membership_card(merchant)


@when(parsers.parse('I perform POST request to add & auto link "{merchant}" membership card'))
def post_add_and_link(merchant):
    """Function call to add_and_link in test_membership_cards"""
    test_membership_cards.add_and_link_membership_card(merchant)


@then(
    parsers.parse(
        'I perform GET request to verify the "{merchant}" membership card is added & linked successfully '
        "in the wallet"
    )
)
def get_add_and_link(merchant):
    """Function call to get_membership_cards in test_membership_cards"""
    test_membership_cards.verify_add_and_link_membership_card(merchant)


@when(
    parsers.parse(
        'I perform GET request to verify the "{merchant}" membership card is' " linked successfully in the wallet"
    )
)
def verify_mcard_link(merchant):
    """Function call to get_membership_cards in test_membership_cards"""
    test_membership_cards.verify_add_and_link_membership_card(merchant)


@then(parsers.parse('I verify status of paymentcard is "{activated}" for "{merchant}"'))
def verify_vop_status(activated, merchant):
    time.sleep(3)
    payment_account = QueryHermes.get_vop_status(TestContext.current_payment_card_id)
    assert payment_account.status == TestData.get_vop_status().get(
        activated
    ), f"Payment Account is not '{activated}' and the status is '{payment_account.status}'"
    logging.info(f"The payment card is '{activated}' with status '{payment_account.status}'")

    assert (
            payment_account.payment_card_account_id == TestContext.current_payment_card_id
            and payment_account.status == TestData.get_vop_status().get(activated)
            and payment_account.scheme_id == TestData.get_membership_plan_id(merchant)
    ), f"Details of payment card '{payment_account.payment_card_account_id}'in DB is not as expected"


@when(
    parsers.parse(
        'I perform GET request to verify the "{merchant}" membership card is added & linked to all payment cards'
    )
)
def get_add_and_link_to_many_pcards(merchant):
    response = test_membership_cards.verify_add_and_link_membership_card(merchant)
    response_json = response_to_json(response)
    assert response_json["payment_cards"][0]["active_link"] and response_json["payment_cards"][1]["active_link"]
    # and response_json["payment_cards"][2]["active_link"])


def response_to_json(response):
    try:
        response_json = response.json()
    except JSONDecodeError or Exception:
        raise Exception(f"Empty response and the response Status Code is {str(response.status_code)}")
    return response_json


@when(
    parsers.parse(
        'I perform the GET request to verify the new payment card "{payment_card_provider}" has been '
        "added successfully to the wallet"
    )
)
def get_new_payment_provider(payment_card_provider="master"):
    response = PaymentCards.get_payment_card(TestContext.token, TestContext.current_payment_card_id)
    response_json = response.json()
    logging.info(
        "The response of GET/PaymentCard/id is: \n\n"
        + Endpoint.BASE_URL
        + api.ENDPOINT_PAYMENT_CARD.format(TestContext.current_payment_card_id)
        + "\n\n"
        + json.dumps(response_json, indent=4)
    )
    assert (
            response.status_code == 200
            and response_json["id"] == TestContext.current_payment_card_id
            and response_json["membership_cards"] == []
            and response_json["status"] == PaymentCardTestData.get_data().get(constants.PAYMENT_CARD_STATUS)
            and response_json["card"]["first_six_digits"]
            == PaymentCardTestData.get_data(payment_card_provider).get(constants.FIRST_SIX_DIGITS)
            and response_json["card"]["last_four_digits"]
            == PaymentCardTestData.get_data(payment_card_provider).get(constants.LAST_FOUR_DIGITS)
            and response_json["card"]["month"] == PaymentCardTestData.get_data(payment_card_provider).get(
                constants.MONTH)
            and response_json["card"]["year"] == PaymentCardTestData.get_data(payment_card_provider).get(constants.YEAR)
            and response_json["card"]["country"] == "UK"
            and response_json["card"]["currency_code"] == "GBP"
            and response_json["card"]["name_on_card"] == TestContext.name_on_payment_card
            and response_json["card"]["provider"]
            == PaymentCardTestData.get_data(payment_card_provider).get(constants.PAYMENT_PROVIDER)
            and response_json["card"]["type"] == "debit"
            and response_json["images"][0]["url"]
            == PaymentCardTestData.get_data(payment_card_provider).get(constants.PAYMENT_URL)
            and response_json["images"][0]["type"] == 0
            and response_json["images"][0]["encoding"]
            == PaymentCardTestData.get_data(payment_card_provider).get(constants.PAYMENT_ENCODING)
            and response_json["images"][0]["description"]
            == PaymentCardTestData.get_data(payment_card_provider).get(constants.PAYMENT_DISCRIPTION)
            and response_json["account"]["verification_in_progress"]
            == PaymentCardTestData.get_data(payment_card_provider).get(constants.PAYMENT_VERIFICATION)
            and response_json["account"]["status"] == 1
            and response_json["account"]["consents"][0]["latitude"] == 51.405372
            and response_json["account"]["consents"][0]["longitude"] == -0.678357
            and response_json["account"]["consents"][0]["timestamp"] == TestContext.payment_account_timestamp
            and response_json["account"]["consents"][0]["type"] == 1
    ), "Get Payment card addition is not successful"
    return response
