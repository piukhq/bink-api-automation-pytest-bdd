@wasabi
Feature: Merchant Wasabi - Ensure a customer can add their membership card & view its details for merchant Wasabi
  As a customer
  I want to utilise membership_cards endpoint
  So I can add my card, with the scheme provider Wasabi & check its details successfully


  @add @bink_regression 
  Scenario: Add Journey_Wasabi

    Given I am a Bink user
    When I perform POST request to add "Wasabi" membership card
    And I perform GET request to verify the "Wasabi" membership card is added to the wallet
    Then verify the data stored in DB after "Add" journey for "Wasabi"
    And I perform DELETE request to delete the "Wasabi" membership card

  @balances_transactions @bink_regression 
  Scenario: Balances and Transactions_Wasabi

    Given I am a Bink user
    When I perform POST request to add "Wasabi" membership card
    And I perform GET request to verify the "Wasabi" membership card is added to the wallet
    And I perform GET request to view balance for recently added "Wasabi" membership card
    When I perform GET request to view all transactions made using the recently added "Wasabi" membership card
    Then I perform GET request to view a specific transaction made using the recently added "Wasabi" membership card
    Then verify the data stored in DB after "Add" journey for "Wasabi"
    And I perform DELETE request to delete the "Wasabi" membership card


  @vouchers
    Scenario: Add Journey_Wasabi and verify vouchers

    Given I am a customer who is subscribing to Bink or I am Bink app user
    When I perform POST request to add "Wasabi" membership card
    And I perform GET request to verify the "Wasabi" membership card voucher details
    Then verify the data stored in DB after "Add" journey for "Wasabi"
    Then I perform DELETE request to delete the "Wasabi" membership card

  @add_patch @bink_regression 
  Scenario:  PATCH membership card details_Wasabi

    Given I am a Bink user
    When I perform POST request to add "Wasabi" membership card with "invalid_data"
    And I perform GET request to verify the "Wasabi" membership card is added to the wallet with invalid data
    And I perform PATCH request to update "Wasabi" membership card
    And I perform GET request to verify the "Wasabi" membership card details got updated after a successful PATCH
    Then verify the data stored in DB after "Add" journey for "Wasabi"
    And I perform DELETE request to delete the "Wasabi" membership card

 @add_and_link @bink_regression 
  Scenario: ADD & LINK Journey_Wasabi
    Given I am a Bink user
    And I perform POST request to add payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully
    When I perform POST request to add & auto link an existing "Wasabi" membership card
    And I perform GET request to verify the "Wasabi" membership card is added & linked successfully in the wallet
    And I perform GET request to view balance for recently added "Wasabi" membership card
    Then verify the data stored in DB after "Add" journey for "Wasabi"
    Then I perform DELETE request to delete the "Wasabi" membership card
    And I perform DELETE request to delete the payment card


  @enrol @bink_regression
    Scenario: Join Journey_Wasabi

    Given I register with bink service as a new customer
    When I perform POST request to create a "Wasabi" membership account with enrol credentials
    And I perform GET request to verify the "Wasabi" membership account is created
    Then verify the data stored in DB after "Enrol" journey for "Wasabi"
    Then I perform DELETE request to delete the "Wasabi" membership card

  @enrol_put @bink_regression
  Scenario: Join Journey_PUT_Wasabi


    Given I register with bink service as a new customer
    When I perform POST request to create a "Wasabi" membership account with "invalid" enrol credentials
    And I perform GET request to verify the "Wasabi" membership account is created with invalid data
    And I perform PUT request to replace information of the enrolled "Wasabi" membership card
    And I perform GET request to verify the enrolled "Wasabi" membership card details got replaced after a successful PUT
    Then verify the data stored in DB after "Enrol" journey for "Wasabi"
    Then I perform DELETE request to delete the "Wasabi" membership card




