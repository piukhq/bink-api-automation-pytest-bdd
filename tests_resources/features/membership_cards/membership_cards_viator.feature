@viator
Feature: Merchant Viator - Ensure a customer can add their membership card & view its details for merchant Viator
  As a customer
  I want to utilise membership_cards endpoint
  So I can add my card, with the scheme provider Viator & check its details successfully

  @enrol @bink_regression @sanity @sanity_bmb
  Scenario: Join Journey_Viator

    Given I register with bink service as a new customer
    When I perform POST request to create a "Viator" membership account with enrol credentials
    And I perform GET request to verify the "Viator" membership account is created
    Then verify the data stored in DB after "Enrol" journey for "Viator"
    Then I perform DELETE request to delete the "Viator" membership card
    And I perform DELETE request to delete the customer

  @add @bink_regression @sanity @sanity_bmb
  Scenario: Add Journey_Viator

    Given I am a Bink user
    When I perform POST request to add "Viator" membership card
    And I perform GET request to verify the "Viator" membership card is added to the wallet
    Then verify the data stored in DB after "Add" journey for "Viator"
    And I perform DELETE request to delete the "Viator" membership card

  @vouchers @bink_regression @bmb_regression
  Scenario: Add Journey_Viator and verify vouchers

    Given I am a customer who is subscribing to Bink or I am Bink app user
    When I perform POST request to add "Viator" membership card
    And I perform GET request to verify the "Viator" membership card voucher details
    Then verify the data stored in DB after "Add" journey for "Viator"
    Then I perform DELETE request to delete the "Viator" membership card

  @enrol_add @sanity @sanity_bmb
  Scenario: Verify join Viator then delete membership_card from the wallet and Add membershipcard into the wallet again with enrol data

    Given I register with bink service as a new customer
    When I perform POST request to create a "Viator" membership account with enrol credentials
    And I perform GET request to verify the "Viator" membership account is created
    Then I perform DELETE request to delete the "Viator" membership card
    When I perform POST request to add "Viator" membership card after enrol deleted
    And I perform GET request to verify the "Viator" membership card is added to the wallet
    Then verify the data stored in DB after "Enrol" journey for "Viator"
    And I perform DELETE request to delete the customer


  @add_patch @bink_regression @sanity @sanity_bmb
  Scenario:  PATCH membership card details_Viator

    Given I am a Bink user
    When I perform POST request to add "Viator" membership card with "invalid_data"
    And I perform GET request to verify the "Viator" membership card is added to the wallet with invalid data
    And I perform PATCH request to update "Viator" membership card
    And I perform GET request to verify the "Viator" membership card details got updated after a successful PATCH
    Then verify the data stored in DB after "Add" journey for "Viator"
    And I perform DELETE request to delete the "Viator" membership card

  @negative_scenario @sanity @sanity_bmb
  Scenario:  Add_Journey with Invalid Credentials_Viator

    Given I am a Bink user
    When I perform POST request to add "Viator" membership card with "invalid_data"
    And I perform GET request to verify the "Viator" membership card is added to the wallet with invalid data
    Then I perform DELETE request to delete the "Viator" membership card

  @negative_scenario @sanity @sanity_bmb
  Scenario Outline: Negative test scenario for POST/membership_cards without account field_viator
    Given I am a Bink user
    When I perform POST request to add "Viator" membership card without "account"
    Then I should receive error message "<error_message>"

    Examples:
      | error_message      |
      | Malformed request. |

  @negative_scenario @sanity @sanity_bmb
  Scenario Outline: Negative test scenario for POST/membership_cards without plan field_viator
    Given I am a Bink user
    When I perform POST request to add "Viator" membership card without "membership_plan"
    Then I should receive error message "<error_message>"

    Examples:
      | error_message                             |
      | required field membership_plan is missing |

  @negative_scenario @sanity @sanity_bmb
  Scenario Outline: Negative test scenario for POST/membership_cards without token_viator
    Given I am a Bink user
    When I perform POST request to add "Viator" membership card without "token" header
    Then I should receive error message "<error_message>"

    Examples:
      | error_message                                  |
      | Invalid token header. No credentials provided. |

  @negative_scenario @sanity @sanity_bmb
  Scenario Outline: Negative test scenario for POST/membership_cards without payload_viator
    Given I am a Bink user
    When I perform POST request to add "Viator" membership card without "payload" header
    Then I should receive error message "<error_message>"

    Examples:
      | error_message                             |
      | required field membership_plan is missing |