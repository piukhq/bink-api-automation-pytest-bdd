@harvey_nichols @bmb @bink
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

#  @enrol
#    Scenario: Join Journey_HarveyNichols
#
#    Given I register with bink service as a new customer
#    When I perform POST request to create a "HarveyNichols" membership account with enrol credentials
#    And I perform GET request to verify the "HarveyNichols" membership account is created
#    Then verify the data stored in DB after "Enrol" journey for "HarveyNichols"
#    Then I perform DELETE request to delete the "HarveyNichols" membership card
#    And I perform DELETE request to delete the customer
#
#  @enrol_put
#  Scenario: Join Journey_PUT_HarveyNichols
#
#    Given I register with bink service as a new customer
#    When I perform POST request to create a "HarveyNichols" membership account with "invalid" enrol credentials
#    And I perform GET request to verify the "HarveyNichols" membership account is created with invalid data
#    And I perform PUT request to replace information of the enrolled "HarveyNichols" membership card
#    And I perform GET request to verify the enrolled "HarveyNichols" membership card details got replaced after a successful PUT
#    Then verify the data stored in DB after "Enrol" journey for "HarveyNichols"
#    Then I perform DELETE request to delete the "HarveyNichols" membership card
#    And I perform DELETE request to delete the customer

#
#  Scenario Outline:  Add_Journey_Invalid data_Error code checks
#
#    Given I am a Bink user
#    When I perform POST request to add "HarveyNichols" membership card with invalid "<email_address>" and "<password>"
#    And I perform GET request to verify the "HarveyNichols" membership card fails to add & link in their wallet with "<state>"
#    Then I can see relevant "<reason code>" is present in the response
#    Then they can perform Delete operation to delete the membership card
#
#
#    Examples:
#      | email_address             | password    | state  |reason code |
#      |auto_zer@testbink.com      | BinkT       | failed |  X303      |
#      |auto_zero@testbink.web     | BinkTesting | failed |  X303      |
#      |auto_zero@testbink.com     | BinkT       | failed |  X303      |

@add_always_link
Scenario: Adding payments cards to always auto-link

  Given I am a Bink user
  When I perform POST request to add "HarveyNichols" membership card
  And I perform POST request to add payment card to wallet
  And I perform the GET request to verify the payment card has been added successfully
  And I perform GET request to verify the "HarveyNichols" membership card is added & linked successfully in the wallet
  Then I perform DELETE request to delete the "HarveyNichols" membership card
  And I perform DELETE request to delete the payment card

#@add_always_link
#Scenario: Adding payments cards with autolink false should not link membership card
#
#  Given I am a Bink user
#  When I perform POST request to add "HarveyNichols" membership card
#  And I perform POST request to add "master" payment card to wallet with autolink false
#  And I perform the GET request to verify the payment card has been added successfully
#  And  I perform GET request to verify the "HarveyNichols" membership card is added & not linked in the wallet
#  And I perform DELETE request to delete the "HarveyNichols" membership card
#  And I perform DELETE request to delete the payment card