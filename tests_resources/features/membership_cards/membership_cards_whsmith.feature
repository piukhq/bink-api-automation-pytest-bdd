@whsmith @dev
Feature: Merchant WHSmith - Ensure a customer can add their membership card & view its details
  As a customer
  I want to utilise membership_cards endpoint
  So I can add my card, with the scheme provider WHSmith & check its details successfully

  @add @bink_regression
  Scenario: Add Journey_WHSmith

    Given I am a Bink user
    When I perform POST request to add "WHSmith" membership card
    And I perform GET request to verify the "WHSmith" membership card is added to the wallet
    Then verify the data stored in DB after "Add" journey for "WHSmith"
    And I perform DELETE request to delete the "WHSmith" membership card

  @add_patch @bink_regression
  Scenario:  PATCH membership card details_WHSmith

    Given I am a Bink user
    When I perform POST request to add "WHSmith" membership card with "invalid_data"
    And I perform GET request to verify the "WHSmith" membership card is added to the wallet with invalid data
    And I perform PATCH request to update "WHSmith" membership card
    And I perform GET request to verify the "WHSmith" membership card details got updated after a successful PATCH
    Then verify the data stored in DB after "Add" journey for "WHSmith"
    And I perform DELETE request to delete the "WHSmith" membership card

  @add_and_link @bink_regression
  Scenario: ADD & LINK Journey_WHSmith

    Given I am a Bink user
    And I perform POST request to add payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully
    When I perform POST request to add & auto link an existing "WHSmith" membership card
    And I perform GET request to verify the "WHSmith" membership card is added & linked successfully in the wallet
    And I perform GET request to view balance for recently added "WHSmith" membership card
    Then verify the data stored in DB after "Add" journey for "WHSmith"
    Then I perform DELETE request to delete the "WHSmith" membership card
    And I perform DELETE request to delete the payment card

  @enrol @bink_regression
  Scenario: Join Journey_WHSmith

    Given I register with bink service as a new customer
    When I perform POST request to create a "WHSmith" membership account with enrol credentials
    And I perform GET request to verify the "WHSmith" membership account is created
    Then verify the data stored in DB after "Enrol" journey for "WHSmith"
    Then I perform DELETE request to delete the "WHSmith" membership card
    Then I perform DELETE request to delete the customer

  @enrol_put @bink_regression
  Scenario: Join Journey_PUT_WHSmith

    Given I register with bink service as a new customer
    When I perform POST request to create a "WHSmith" membership account with "invalid" enrol credentials
    And I perform GET request to verify the "WHSmith" membership account is created with invalid data
    And I perform PUT request to replace information of the enrolled "WHSmith" membership card
    And I perform GET request to verify the enrolled "WHSmith" membership card details got replaced after a successful PUT
    Then verify the data stored in DB after "Enrol" journey for "WHSmith"
    Then I perform DELETE request to delete the "WHSmith" membership card
    Then I perform DELETE request to delete the customer

  @balances_transactions @bink_regression
  Scenario: Balances and Transactions_WHSmith

    Given I am a Bink user
    When I perform POST request to add "WHSmith" membership card
    And I perform GET request to verify the "WHSmith" membership card is added to the wallet
    And I perform GET request to view balance for recently added "WHSmith" membership card
#    When I perform GET request to view all transactions made using the recently added "WHSmith" membership card
#    Then I perform GET request to view a specific transaction made using the recently added "WHSmith" membership card
    Then verify the data stored in DB after "Add" journey for "WHSmith"
    And I perform DELETE request to delete the "WHSmith" membership card

  @voucher
  Scenario: Add Journey and verify vouchers WHSmith

    Given I am a customer who is subscribing to Bink or I am Bink app user
    When I perform POST request to add "WHSmith" membership card
    And I perform GET request to verify the "WHSmith" membership card voucher details
    Then verify the data stored in DB after "Add" journey for "WHSmith"
    Then I perform DELETE request to delete the "WHSmith" membership card


