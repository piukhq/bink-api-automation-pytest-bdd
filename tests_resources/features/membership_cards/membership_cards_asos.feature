@asos @sanity
Feature: Merchant Asos - Ensure a customer can add their membership card & view its details for merchant Asos
  As a customer
  I want to utilise membership_cards endpoint
  So I can add my card, with the scheme provider asos & check its details successfully


  @add @bink_regression
  Scenario: Add Journey_Asos

    Given I am a Bink user
    When I perform POST request to add "Asos" membership card
    And I perform GET request to verify the "Asos" membership card is added to the wallet
    Then verify the data stored in DB after "Add" journey for "Asos"
    And I perform DELETE request to delete the "Asos" membership card

  @enrol @bink_regression
  Scenario: Join Journey_Asos

    Given I register with bink service as a new customer
    When I perform POST request to create a "Asos" membership account with enrol credentials
    And I perform GET request to verify the "Asos" membership account is created
    Then verify the data stored in DB after "Enrol" journey for "Asos"
    Then I perform DELETE request to delete the "Asos" membership card
    And I perform DELETE request to delete the customer

  @add_patch @bink_regression
  Scenario:  PATCH membership card details_Asos

    Given I am a Bink user
    When I perform POST request to add "Asos" membership card with "invalid_data"
    And I perform GET request to verify the "Asos" membership card is added to the wallet with invalid data
    And I perform PATCH request to update "Asos" membership card
    And I perform GET request to verify the "Asos" membership card details got updated after a successful PATCH
    Then verify the data stored in DB after "Add" journey for "Asos"
    And I perform DELETE request to delete the "Asos" membership card

  @negative_scenario
  Scenario:  Add_Journey with Invalid Credentials_Asos

    Given I am a Bink user
    When I perform POST request to add "Asos" membership card with "invalid_data"
    And I perform GET request to verify the "Asos" membership card is added to the wallet with invalid data
    Then I perform DELETE request to delete the "Asos" membership card

  @negative_scenario
  Scenario Outline: Negative test scenario for POST/membership_cards without account field_Asos
    Given I am a Bink user
    When I perform POST request to add "Asos" membership card without "account"
    Then I should receive error message "<error_message>"

    Examples:
      | error_message      |
      | Malformed request. |

  @negative_scenario
  Scenario Outline: Negative test scenario for POST/membership_cards without plan field_Asos
    Given I am a Bink user
    When I perform POST request to add "Asos" membership card without "membership_plan"
    Then I should receive error message "<error_message>"

    Examples:
      | error_message                             |
      | required field membership_plan is missing |

  @negative_scenario
  Scenario Outline: Negative test scenario for POST/membership_cards without token_Asos
    Given I am a Bink user
    When I perform POST request to add "Asos" membership card without "token" header
    Then I should receive error message "<error_message>"

    Examples:
      | error_message                                  |
      | Invalid token header. No credentials provided. |

  @negative_scenario
  Scenario Outline: Negative test scenario for POST/membership_cards without payload_Asos
    Given I am a Bink user
    When I perform POST request to add "Asos" membership card without "payload" header
    Then I should receive error message "<error_message>"

    Examples:
      | error_message                             |
      | required field membership_plan is missing |