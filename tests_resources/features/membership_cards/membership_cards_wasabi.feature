@wasabi
Feature: Merchant Wasabi - Ensure a customer can add their membership card & view its details for merchant Wasabi
  As a customer
  I want to utilise membership_cards endpoint
  So I can add my card, with the scheme provider Wasabi & check its details successfully


  @add @prod
  Scenario: Add Journey_Wasabi

    Given I am a Bink user
    When I perform POST request to add "Wasabi" membership card
    And I perform GET request to verify the "Wasabi" membership card is added to the wallet
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    And I perform DELETE request to delete the "Wasabi" membership card

  @balances_transactions @dev @staging @prod
  Scenario: Balances and Transactions_Wasabi

    Given I am a Bink user
    When I perform POST request to add "Wasabi" membership card
    And I perform GET request to verify the "Wasabi" membership card is added to the wallet
    And I perform GET request to view balance for recently added "Wasabi" membership card
    When I perform GET request to view all transactions made using the recently added "Wasabi" membership card
#    Then I perform GET request to view a specific transaction made using the recently added "HarveyNichols" membership card
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    And I perform DELETE request to delete the "Wasabi" membership card

  @add_patch @prod
  Scenario:  PATCH membership card details_Wasabi

    Given I am a Bink user
    When I perform POST request to add "Wasabi" membership card with "invalid_data"
    And I perform GET request to verify the "Wasabi" membership card is added to the wallet with invalid data
    And I perform PATCH request to update "Wasabi" membership card
    And I perform GET request to verify the "Wasabi" membership card details got updated after a successful PATCH
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    And I perform DELETE request to delete the "Wasabi" membership card

 @add_and_link
  Scenario: ADD & LINK Journey_Wasabi
    Given I am a Bink user
    And I perform POST request to add payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully
    When I perform POST request to add & auto link an existing "Wasabi" membership card
    And I perform GET request to verify the "Wasabi" membership card is added & linked successfully in the wallet
    And I perform GET request to view balance for recently added "Wasabi" membership card
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    Then I perform DELETE request to delete the "Wasabi" membership card
    And I perform DELETE request to delete the payment card

  @error_codes
    Scenario Outline:  Add Journey_Error code checks

    Given I am a Bink user
    When I perform POST request to add "Wasabi" membership card with invalid "<card_number>" and "<email_address>"
    And I perform GET request to verify the "Wasabi" membership card fails to add & link in their wallet with "<state>"
    Then I can see relevant "<reason code>" is present in the response
    Then they can perform Delete operation to delete the membership card


    Examples:
      | card_number               | email_address             | state  |reason code |
      |104817410                  | binktestuser16@wasabi.com | failed |  X102      |
      |1048173057                 |binktestuser16@wasabi.com  | failed |  X303      |

  @enrol
    Scenario: Join Journey_Wasabi

    Given I register with bink service as a new customer
    When I perform POST request to create a "Wasabi" membership account with enrol credentials
    And I perform GET request to verify the "Wasabi" membership account is created
    Then verify membership account Join date, Card Number and Merchant identifier populated in Django
    Then I perform DELETE request to delete the "Wasabi" membership card

  @enrol_put
  Scenario: Join Journey_PUT_Wasabi


    Given I register with bink service as a new customer
    When I perform POST request to create a "Wasabi" membership account with "invalid" enrol credentials
    And I perform GET request to verify the "Wasabi" membership account is created with invalid data
    And I perform PUT request to replace information of the enrolled "Wasabi" membership card
    And I perform GET request to verify the enrolled "Wasabi" membership card details got replaced after a successful PUT
    Then verify membership account Join date, Card Number and Merchant identifier populated in Django
    Then I perform DELETE request to delete the "Wasabi" membership card


  @dev @staging @prod
  Scenario:  Add_Journey with Invalid Credentials_Iceland

    Given I am a Bink user
    When I perform POST request to add "Iceland" membership card with "invalid_data"
    And I perform GET request to verify the "Iceland" membership card is added to the wallet with invalid data
#    Then Verify the card status as "Invalid Credentials" in Django
    Then I perform DELETE request to delete the "Iceland" membership card



