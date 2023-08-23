@trenette
Feature: Merchant Trenette - Ensure a customer can add their membership card & view its details for merchant Wasabi
  As a customer
  I want to utilise membership_cards endpoint
  So I can add my card, with the scheme provider Trenette & check its details successfully


  @enrol  @sanity
  Scenario: Join Journey_Trenette

    Given I register with bink service as a new customer
    When I perform POST request to create a "Trenette" membership account with enrol credentials
    And I perform GET request to verify the "Trenette" membership account is created
    Then verify the data stored in DB after "Enrol" journey for "Trenette"
    Then I perform DELETE request to delete the "Trenette" membership card
    And I perform DELETE request to delete the customer

  @add  @sanity
  Scenario: Add Journey_Trenette

    Given I am a Bink user
    When I perform POST request to add "Trenette" membership card
    And I perform GET request to verify the "Trenette" membership card is added to the wallet
    Then verify the data stored in DB after "Add" journey for "Trenette"
    And I perform DELETE request to delete the "Trenette" membership card

  @balances_transactions  
  Scenario: Balances and Transactions_Trenette

    Given I am a Bink user
    When I perform POST request to add "Trenette" membership card
    And I perform GET request to verify the "Trenette" membership card is added to the wallet
    And I perform GET request to view balance for recently added "Trenette" membership card
    When I perform GET request to view all transactions made using the recently added "Trenette" membership card
    Then I perform GET request to view a specific transaction made using the recently added "Trenette" membership card
    Then verify the data stored in DB after "Add" journey for "Trenette"
    And I perform DELETE request to delete the "Trenette" membership card

  @vouchers  
  Scenario: Add Journey_Trenette and verify vouchers

    Given I am a customer who is subscribing to Bink or I am Bink app user
    When I perform POST request to add "Trenette" membership card
    And I perform GET request to verify the "Trenette" membership card voucher details
    Then verify the data stored in DB after "Add" journey for "Trenette"
    Then I perform DELETE request to delete the "Trenette" membership card

  @images
  Scenario: Add Journey_Trenette and verify images

    Given I am a customer who is subscribing to Bink or I am Bink app user
    When I perform POST request to add "Trenette" membership card
    And I perform GET request to verify the "Trenette" membership card image details
    Then verify the data stored in DB after "Add" journey for "Trenette"
    Then I perform DELETE request to delete the "Trenette" membership card


  @add_patch  @sanity
  Scenario:  PATCH membership card details_Trenette

    Given I am a Bink user
    When I perform POST request to add "Trenette" membership card with "invalid_data"
    And I perform GET request to verify the "Trenette" membership card is added to the wallet with invalid data
    And I perform PATCH request to update "Trenette" membership card
    And I perform GET request to verify the "Trenette" membership card details got updated after a successful PATCH
    Then verify the data stored in DB after "Add" journey for "Trenette"
    And I perform DELETE request to delete the "Trenette" membership card

  @enrol_put  @sanity
  Scenario: Join Journey_PUT_Trenette

    Given I register with bink service as a new customer
    When I perform POST request to create a "Trenette" membership account with "invalid" enrol credentials
    And I perform GET request to verify the "Trenette" membership account is created with invalid data
    And I perform PUT request to replace information of the enrolled "Trenette" membership card
    And I perform GET request to verify the enrolled "Trenette" membership card details got replaced after a successful PUT
    Then verify the data stored in DB after "Enrol" journey for "Trenette"
    Then I perform DELETE request to delete the "Trenette" membership card
    And I perform DELETE request to delete the customer

  @enrol_add @sanity
  Scenario: Verify join Trenette then delete membership_card from the wallet and Add membershipcard into the wallet again with enrol data

    Given I register with bink service as a new customer
    When I perform POST request to create a "Trenette" membership account with enrol credentials
    And I perform GET request to verify the "Trenette" membership account is created
    Then I perform DELETE request to delete the "Trenette" membership card
    When I perform POST request to add "Trenette" membership card after enrol deleted
    And I perform GET request to verify the "Trenette" membership card is added to the wallet
    Then verify the data stored in DB after "Enrol" journey for "Trenette"
    And I perform DELETE request to delete the customer

  @negative_scenario @sanity
  Scenario:  Add_Journey with Invalid Credentials_Trenette

    Given I am a Bink user
    When I perform POST request to add "Trenette" membership card with "invalid_data"
    And I perform GET request to verify the "Trenette" membership card is added to the wallet with invalid data
    Then I perform DELETE request to delete the "Trenette" membership card

  @negative_scenario @sanity
  Scenario Outline: Negative test scenario for POST/membership_cards without account field_Trenette
    Given I am a Bink user
    When I perform POST request to add "Trenette" membership card without "account"
    Then I should receive error message "<error_message>"

    Examples:
      | error_message      |
      | Malformed request. |

  @negative_scenario @sanity
  Scenario Outline: Negative test scenario for POST/membership_cards without plan field_Trenette
    Given I am a Bink user
    When I perform POST request to add "Trenette" membership card without "membership_plan"
    Then I should receive error message "<error_message>"

    Examples:
      | error_message                             |
      | required field membership_plan is missing |

  @negative_scenario @sanity
  Scenario Outline: Negative test scenario for POST/membership_cards without token_Trenette
    Given I am a Bink user
    When I perform POST request to add "Trenette" membership card without "token" header
    Then I should receive error message "<error_message>"

    Examples:
      | error_message                                  |
      | Invalid token header. No credentials provided. |

  @negative_scenario @sanity
  Scenario Outline: Negative test scenario for POST/membership_cards without payload_Trenette
    Given I am a Bink user
    When I perform POST request to add "Trenette" membership card without "payload" header
    Then I should receive error message "<error_message>"

    Examples:
      | error_message                             |
      | required field membership_plan is missing |