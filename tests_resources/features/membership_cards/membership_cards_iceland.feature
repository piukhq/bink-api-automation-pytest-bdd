@iceland @dev
Feature: Merchant Iceland - Ensure a customer can add their membership card & view its details for merchant Iceland
  As a customer
  I want to utilise membership_cards endpoint
  So I can add my card, with the scheme provider Iceland & check its details successfully


  @add @bink_regression @bmb_regression
  Scenario: Add Journey_Iceland

    Given I am a Bink user
    When I perform POST request to add "Iceland" membership card
    And I perform GET request to verify the "Iceland" membership card is added to the wallet
    Then verify the data stored in DB after "Add" journey for "Iceland"
    And I perform DELETE request to delete the "Iceland" membership card

#   Use below commented line for production execution once iceland test data with transactions is ready
  @balances_transactions @bink_regression @bmb_regression
  Scenario: Balances verification_Iceland

    Given I am a Bink user
    When I perform POST request to add "Iceland" membership card
    And I perform GET request to verify the "Iceland" membership card is added to the wallet
    And I perform GET request to view balance for recently added "Iceland" membership card
#    When I perform GET request to view all transactions made using the recently added "Iceland" membership card
#    Then I perform GET request to view a specific transaction made using the recently added "Iceland" membership card
    Then verify the data stored in DB after "Add" journey for "Iceland"
    And I perform DELETE request to delete the "Iceland" membership card


  @add_patch @bink_regression @bmb_regression
  Scenario: Add Journey_PATCH_Iceland

    Given I am a Bink user
    When I perform POST request to add "Iceland" membership card with "invalid_data"
    And I perform GET request to verify the "Iceland" membership card is added to the wallet with invalid data
    And I perform PATCH request to update "Iceland" membership card
    And I perform GET request to verify the "Iceland" membership card details got updated after a successful PATCH
    Then verify the data stored in DB after "Add" journey for "Iceland"
    And I perform DELETE request to delete the "Iceland" membership card

  @add_and_link @staging
  Scenario: ADD & LINK Journey_Iceland

    Given I am a Bink user
    And I perform POST request to add payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully
    When I perform POST request to add & auto link an existing "Iceland" membership card
    And I perform GET request to verify the "Iceland" membership card is added & linked successfully in the wallet
    Then verify the data stored in DB after "Add" journey for "Iceland"
    Then I perform DELETE request to delete the "Iceland" membership card
    And I perform DELETE request to delete the payment card

  @bink_regression @bmb_regression
  Scenario:  Add_Journey with Invalid Credentials_Iceland

    Given I am a Bink user
    When I perform POST request to add "Iceland" membership card with "invalid_data"
    And I perform GET request to verify the "Iceland" membership card is added to the wallet with invalid data
#    Then Verify the card status as "Invalid Credentials" in Django
    Then I perform DELETE request to delete the "Iceland" membership card


  @enrol @bink_regression @bmb_regression
  Scenario: Join Journey_Iceland

    Given I register with bink service as a new customer
    When I perform POST request to create a "Iceland" membership account with enrol credentials
    And I perform GET request to verify the "Iceland" membership account is created
    Then verify the data stored in DB after "Enrol" journey for "Iceland"
    Then I perform DELETE request to delete the "Iceland" membership card
    And I perform DELETE request to delete the customer


  @enrol_put
  Scenario: Join Journey_PUT_Iceland

    Given I register with bink service as a new customer
    When I perform POST request to create a "Iceland" membership account with "invalid" enrol credentials
    And I perform GET request to verify the "Iceland" membership account is created with invalid data
    And I perform PUT request to replace information of the enrolled "Iceland" membership card
    And I perform GET request to verify the enrolled "Iceland" membership card details got replaced after a successful PUT
    Then verify the data stored in DB after "Enrol" journey for "Iceland"
    Then I perform DELETE request to delete the "Iceland" membership card
    And I perform DELETE request to delete the customer

  @add_always_link
  Scenario: Adding payments cards to always auto-link_Iceland

    Given I am a Bink user
    When I perform POST request to add "Iceland" membership card
    And I perform POST request to add payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully
    And I perform GET request to verify the "Iceland" membership card is added & linked successfully in the wallet
    Then I perform DELETE request to delete the "Iceland" membership card
    And I perform DELETE request to delete the payment card

  @ghost_journey @bink_regression @bmb_regression
  Scenario: Ghost card Journey Iceland

    Given I am a Bink user
    When I perform POST request to add "Iceland" ghost membership card
    And I perform GET request to verify the "Iceland" ghost membership card is added to the wallet
    When I perform PATCH request to create a "Iceland" ghost membership account with enrol credentials
    And I perform GET request to verify the "Iceland" membership account is created
    Then I perform DELETE request to delete the "Iceland" membership card

  @negative_scenario @loy1975_1 @bink_regression @bmb_regression
  Scenario Outline: Negative test scenario for POST/membership_cards without account field_Iceland
    Given I am a Bink user
    When I perform POST request to add "Iceland" membership card without "account"
    Then I should receive error message "<error_message>"

    Examples:
      | error_message      |
      | Malformed request. |

  @negative_scenario @loy1975_6 @bink_regression @bmb_regression
  Scenario Outline: Negative test scenario for POST/membership_cards without plan field_Iceland
    Given I am a Bink user
    When I perform POST request to add "Iceland" membership card without "membership_plan"
    Then I should receive error message "<error_message>"

    Examples:
      | error_message                             |
      | required field membership_plan is missing |

  @negative_scenario @loy1975_4 @bink_regression @bmb_regression
  Scenario Outline: Negative test scenario for POST/membership_cards with key value lastname instead of Last name_Iceland
    Given I am a Bink user
    When I perform POST request to add "Iceland" membership card without "lastname"
    Then I should receive error message "<error_message>"

    Examples:
      | error_message      |
      | Malformed request. |

  @negative_scenario @loy1975_4 @bink_regression @bmb_regression
  Scenario Outline: Negative test scenario for POST/membership_cards with key value postcode instead of Postcode_Iceland
    Given I am a Bink user
    When I perform POST request to add "Iceland" membership card without "postcode"
    Then I should receive error message "<error_message>"

    Examples:
      | error_message      |
      | Malformed request. |

  @negative_scenario @loy1975_8 @bink_regression @bmb_regression
  Scenario Outline: Negative test scenario for POST/membership_cards without token_Iceland
    Given I am a Bink user
    When I perform POST request to add "Iceland" membership card without "token" header
    Then I should receive error message "<error_message>"

    Examples:
      | error_message                                  |
      | Invalid token header. No credentials provided. |

  @negative_scenario @loy1975_9 @bink_regression @bmb_regression
  Scenario Outline: Negative test scenario for POST/membership_cards without payload_Iceland
    Given I am a Bink user
    When I perform POST request to add "Iceland" membership card without "payload" header
    Then I should receive error message "<error_message>"

    Examples:
      | error_message                             |
      | required field membership_plan is missing |

## This scenario required to comment out once bug been resolve
##  @negative_scenario @loy1975_2 @bink_regression @bmb_regression
##  Scenario Outline: Negative test scenario for POST/membership_cards without authorise_fields field_Iceland
##    Given I am a Bink user
##    When I perform POST request to add "Iceland" membership card without "authorise_fields"
##    Then I should receive error message "<error_message>"
##    Examples:
##      | error_message      |
##      | Malformed request. |