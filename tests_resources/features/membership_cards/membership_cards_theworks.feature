@works
Feature: Merchant The Works - Ensure a customer can add their membership card & view its details for merchant TheWorks
  As a customer
  I want to utilise membership_cards endpoint
  So I can add my card, with the scheme provider TheWorks & check its details successfully


  @add
  Scenario: Add Journey_The Works

    Given I am a Bink user
    When I perform POST request to add "TheWorks" membership card
    And I perform GET request to verify the "TheWorks" membership card is added to the wallet
    Then verify the data stored in DB after "Add" journey for "TheWorks"
    And I perform DELETE request to delete the "TheWorks" membership card

  @balances_transactions
  Scenario: Balances verification_The Works

    Given I am a Bink user
    When I perform POST request to add "TheWorks" membership card
    And I perform GET request to verify the "TheWorks" membership card is added to the wallet
    And I perform GET request to view balance for recently added "TheWorks" membership card
#    When I perform GET request to view all transactions made using the recently added "TheWorks" membership card
#    Then I perform GET request to view a specific transaction made using the recently added "TheWorks" membership card
    Then verify the data stored in DB after "Add" journey for "TheWorks"
    And I perform DELETE request to delete the "TheWorks" membership card


  @add_patch   @sanity_bmb
  Scenario: Add Journey_PATCH with Valid Credentials_The Works

    Given I am a Bink user
    When I perform POST request to add "TheWorks" membership card with "invalid_data"
    And I perform GET request to verify the "TheWorks" membership card is added to the wallet with invalid data
    And I perform PATCH request to update "TheWorks" membership card
    And I perform GET request to verify the "TheWorks" membership card details got updated after a successful PATCH
    Then verify the data stored in DB after "Add" journey for "TheWorks"
    And I perform DELETE request to delete the "TheWorks" membership card

  @add_patch
  Scenario: Add Journey_PATCH with InValid Credentials_The Works

    Given I am a Bink user
    When I perform POST request to add "TheWorks" membership card
    And I perform GET request to verify the "TheWorks" membership card is added to the wallet
    And I perform PATCH request to update "TheWorks" membership card with "invalid_credentials"
    And I perform GET request to verify the "TheWorks" membership card details got updated after an unsuccessful PATCH
    Then verify the data stored in DB after "Add" journey for "TheWorks"
    And I perform DELETE request to delete the "TheWorks" membership card

  @add_and_link
  Scenario: ADD & LINK Journey_The Works

    Given I am a Bink user
    And I perform POST request to add payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully
    When I perform POST request to add & auto link an existing "TheWorks" membership card
    And I perform GET request to verify the "TheWorks" membership card is added & linked successfully in the wallet
    Then verify the data stored in DB after "Add" journey for "TheWorks"
    Then I perform DELETE request to delete the "TheWorks" membership card
    And I perform DELETE request to delete the payment card


  Scenario:  Add_Journey with Invalid Credentials_The Works

    Given I am a Bink user
    When I perform POST request to add "TheWorks" membership card with "invalid_data"
    And I perform GET request to verify the "TheWorks" membership card is added to the wallet with invalid data
#    Then Verify the card status as "Invalid Credentials" in Django
    Then I perform DELETE request to delete the "TheWorks" membership card


  @enrol
  Scenario: Join Journey_The Works

    Given I register with bink service as a new customer
    When I perform POST request to create a "TheWorks" membership account with enrol credentials
    And I perform GET request to verify the "TheWorks" membership account is created
    Then verify the data stored in DB after "Enrol" journey for "TheWorks"
    Then I perform DELETE request to delete the "TheWorks" membership card
    And I perform DELETE request to delete the customer


  @enrol_put
  Scenario: Join Journey_PUT_The Works

    Given I register with bink service as a new customer
    When I perform POST request to create a "TheWorks" membership account with "invalid" enrol credentials
    And I perform GET request to verify the "TheWorks" membership account is created with invalid data
    And I perform PUT request to replace information of the enrolled "TheWorks" membership card
    And I perform GET request to verify the enrolled "TheWorks" membership card details got replaced after a successful PUT
    Then verify the data stored in DB after "Enrol" journey for "TheWorks"
    Then I perform DELETE request to delete the "TheWorks" membership card
    And I perform DELETE request to delete the customer

  @add_always_link
  Scenario: Adding payments cards to always auto-link_The Works

    Given I am a Bink user
    When I perform POST request to add "TheWorks" membership card
    And I perform POST request to add payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully
    And I perform GET request to verify the "TheWorks" membership card is added & linked successfully in the wallet
    Then I perform DELETE request to delete the "TheWorks" membership card
    And I perform DELETE request to delete the payment card

  @ghost_journey
  Scenario: Ghost card Journey The Works

    Given I am a Bink user
    When I perform POST request to add "TheWorks" ghost membership card
    And I perform GET request to verify the "TheWorks" ghost membership card is added to the wallet
    When I perform PATCH request to create a "TheWorks" ghost membership account with enrol credentials
    And I perform GET request to verify the "TheWorks" membership account is created
    Then I perform DELETE request to delete the "TheWorks" membership card


     @enrol_failed
  Scenario Outline: Join Journey_The Works enrol failed

    Given I register with bink service as a new customer
    When I perform POST request to create a "TheWorks" membership account with "<invalid_lastname>" enrol credentials
    And I perform GET request to verify the "TheWorks" membership account is created with invalid data
    Then verify the data stored in DB after "Enrol" journey for "TheWorks"
    Then I perform DELETE request to delete the "TheWorks" membership card
    And I perform DELETE request to delete the customer

    Examples:
      | invalid_lastname |
      |account_already_exists|
      |join_failed           |
      |join_http_failed      |


  Scenario Outline: Negative test scenario for POST/membership_cards wrong payload field values _ the Works
    Given I am a Bink user
    When I perform POST request to add "TheWorks" membership card without "<field_value>"
    Then I should receive error message "<error_message>"

    Examples:
      | error_message                             | field_value     |
      | required field membership_plan is missing | membership_plan |
      | Malformed request.                        | lastname        |
      | Malformed request.                        | postcode        |
      | Malformed request.                        | account         |


  @negative_scenario
  Scenario Outline: Negative test scenario for POST/membership_cards without token or Payload _ the Works
    Given I am a Bink user
    When I perform POST request to add "TheWorks" membership card without "<field_value>" header
    Then I should receive error message "<error_message>"

    Examples:
      | error_message                                  | field_value |
      | Invalid token header. No credentials provided. | token       |
      | required field membership_plan is missing      | payload     |
