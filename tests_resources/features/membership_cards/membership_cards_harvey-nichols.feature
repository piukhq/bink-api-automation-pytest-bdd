@harvey_nichols @dev
Feature: Merchant Harvey Nichols - Ensure a customer can add their membership card & view its details for merchant Harvey Nichols
  As a customer
  I want to utilise membership_cards endpoint
  So I can add my card, with the scheme provider Harvey Nichols & check its details successfully


  @add @bink_regression @bmb_regression
  Scenario: Add Journey_HarveyNichols

    Given I am a Bink user
    When I perform POST request to add "HarveyNichols" membership card
    And I perform GET request to verify the "HarveyNichols" membership card is added to the wallet
    Then verify the data stored in DB after "Add" journey for "HarveyNichols"
    And I perform DELETE request to delete the "HarveyNichols" membership card

  @balances_transactions @bink_regression @bmb_regression
  Scenario: Balances and Transactions_HarveyNichols

    Given I am a Bink user
    When I perform POST request to add "HarveyNichols" membership card
    And I perform GET request to verify the "HarveyNichols" membership card is added to the wallet
    And I perform GET request to view balance for recently added "HarveyNichols" membership card
    When I perform GET request to view all transactions made using the recently added "HarveyNichols" membership card
    Then I perform GET request to view a specific transaction made using the recently added "HarveyNichols" membership card
    Then verify the data stored in DB after "Add" journey for "HarveyNichols"
    And I perform DELETE request to delete the "HarveyNichols" membership card

  @add_patch @bink_regression @bmb_regression
  Scenario:  Add Journey_PATCH_HarveyNichols

    Given I am a Bink user
    When I perform POST request to add "HarveyNichols" membership card with "invalid_data"
    And I perform GET request to verify the "HarveyNichols" membership card is added to the wallet with invalid data
    And I perform PATCH request to update "HarveyNichols" membership card
    And I perform GET request to verify the "HarveyNichols" membership card details got updated after a successful PATCH
    Then verify the data stored in DB after "Add" journey for "HarveyNichols"
    And I perform DELETE request to delete the "HarveyNichols" membership card

  @add_and_link @bink_regression @bmb_regression
  Scenario: ADD & LINK Journey_HarveyNichols

    Given I am a Bink user
    And I perform POST request to add payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully
    When I perform POST request to add & auto link an existing "HarveyNichols" membership card
    And I perform GET request to verify the "HarveyNichols" membership card is added & linked successfully in the wallet
    Then verify the data stored in DB after "Add" journey for "HarveyNichols"
    Then I perform DELETE request to delete the "HarveyNichols" membership card
    And I perform DELETE request to delete the payment card

  @bink_regression @bmb_regression
  Scenario:  Add_Journey with Invalid Credentials_Harvey Nichols

    Given I am a Bink user
    When I perform POST request to add "HarveyNichols" membership card with "invalid_data"
    And I perform GET request to verify the "HarveyNichols" membership card is added to the wallet with invalid data
    Then I perform DELETE request to delete the "HarveyNichols" membership card

  @enrol @bmb_regression
  Scenario: Join Journey_HarveyNichols

    Given I register with bink service as a new customer
    When I perform POST request to create a "HarveyNichols" membership account with enrol credentials
    And I perform GET request to verify the "HarveyNichols" membership account is created
    Then verify the data stored in DB after "Enrol" journey for "HarveyNichols"
    Then I perform DELETE request to delete the "HarveyNichols" membership card
    And I perform DELETE request to delete the customer

  @enrol_put
  Scenario: Join Journey_PUT_HarveyNichols

    Given I register with bink service as a new customer
    When I perform POST request to create a "HarveyNichols" membership account with "invalid" enrol credentials
    And I perform GET request to verify the "HarveyNichols" membership account is created with invalid data
    And I perform PUT request to replace information of the enrolled "HarveyNichols" membership card
    And I perform GET request to verify the enrolled "HarveyNichols" membership card details got replaced after a successful PUT
    Then verify the data stored in DB after "Enrol" journey for "HarveyNichols"
    Then I perform DELETE request to delete the "HarveyNichols" membership card
    And I perform DELETE request to delete the customer

  @add_always_link
  Scenario: Adding payments cards to always auto-link

    Given I am a Bink user
    When I perform POST request to add "HarveyNichols" membership card
    And I perform POST request to add payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully
    And I perform GET request to verify the "HarveyNichols" membership card is added & linked successfully in the wallet
    Then I perform DELETE request to delete the "HarveyNichols" membership card
    And I perform DELETE request to delete the payment card

#  This scenario won't work due to an existing defect
  @add_always_link
  Scenario: Adding payments cards with autolink false should not link membership card

    Given I am a Bink user
    When I perform POST request to add "HarveyNichols" membership card
    And I perform POST request to add "master" payment card to wallet with autolink false
    And I perform the GET request to verify the payment card has been added successfully
    And  I perform GET request to verify the "HarveyNichols" membership card is added & not linked in the wallet
    And I perform DELETE request to delete the "HarveyNichols" membership card
    And I perform DELETE request to delete the payment card

  @negative_scenario @loy1975_1 @bink_regression @bmb_regression
  Scenario Outline: Negative test scenario for POST/membership_cards without account field_HarveyNichols
    Given I am a Bink user
    When I perform POST request to add "HarveyNichols" membership card without "account"
    Then I should receive error message "<error_message>"

    Examples:
      | error_message      |
      | Malformed request. |

  @negative_scenario @loy1975_6 @bink_regression @bmb_regression
  Scenario Outline: Negative test scenario for POST/membership_cards without plan field_HarveyNichols
    Given I am a Bink user
    When I perform POST request to add "HarveyNichols" membership card without "membership_plan"
    Then I should receive error message "<error_message>"

    Examples:
      | error_message                             |
      | required field membership_plan is missing |

  @negative_scenario @loy1975_4 @bink_regression @bmb_regression
  Scenario Outline: Negative test scenario for POST/membership_cards without account field for enrol_HarveyNichols
    Given I am a Bink user
    When I perform POST request to add "HarveyNichols" membership card without "enrol_account"
    Then I should receive error message "<error_message>"

    Examples:
      | error_message      |
      | Malformed request. |

  @negative_scenario @loy1975_5 @bink_regression @bmb_regression
  Scenario Outline: Negative test scenario for POST/membership_cards without email
    Given I am a Bink user
    When I perform POST request to add "HarveyNichols" membership card with wrong format "email"
    Then I should receive error message "<error_message>" for email missing

    Examples:
      | error_message                |
      | This field may not be blank. |

  @negative_scenario @loy1975_5 @bink_regression @bmb_regression
  Scenario Outline: Negative test scenario for POST/membership_cards without email_HarveyNichols
    Given I am a Bink user
    When I perform POST request to add "HarveyNichols" membership card with wrong format "email_address"
    Then I should receive error message "<error_message>" for email missing

    Examples:
      | error_message                |
      | Enter a valid email address. |

  @negative_scenario @loy1975_7 @bink_regression @bmb_regression
  Scenario Outline: Negative test scenario for POST/membership_cards with email value in coloumn instead of Email_HarveyNichols
    Given I am a Bink user
    When I perform POST request to add "HarveyNichols" membership card without "email_coloumn_value"
    Then I should receive error message "<error_message>"

    Examples:
      | error_message      |
      | Malformed request. |

  @negative_scenario @loy1975_7 @bink_regression @bmb_regression
  Scenario Outline: Negative test scenario for POST/membership_cards with password value in coloumn instead of Password_HarveyNichols
    Given I am a Bink user
    When I perform POST request to add "HarveyNichols" membership card without "password_coloumn_value"
    Then I should receive error message "<error_message>"

    Examples:
      | error_message      |
      | Malformed request. |

  @negative_scenario @loy1975_8 @bink_regression @bmb_regression
  Scenario Outline: Negative test scenario for POST/membership_cards without token_HarveyNichols
    Given I am a Bink user
    When I perform POST request to add "HarveyNichols" membership card without "token" header
    Then I should receive error message "<error_message>"

    Examples:
      | error_message                                  |
      | Invalid token header. No credentials provided. |

  @negative_scenario @loy1975_9 @bink_regression @bmb_regression
  Scenario Outline: Negative test scenario for POST/membership_cards without payload_HarveyNichols
    Given I am a Bink user
    When I perform POST request to add "HarveyNichols" membership card without "payload" header
    Then I should receive error message "<error_message>"

    Examples:
      | error_message                             |
      | required field membership_plan is missing |

# ## This scenario required to comment out once bug been resolve
#  @negative_scenario @loy1975_2 @bink_regression @bmb_regression
#  Scenario Outline: Negative test scenario for POST/membership_cards without authorise_fields field_HarveyNichols
#    Given I am a Bink user
#    When I perform POST request to add "HarveyNichols" membership card without "authorise_fields"
#    Then I should receive error message "<error_message>"
#    Examples:
#      | error_message      |
#      | Malformed request. |