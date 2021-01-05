@burgerking @bink
Feature: Merchant BurgerKing - Ensure a customer can add & link their membership card and enrol for a new membership card & view its details
  As a customer
  I want to utilise membership_cards endpoint
  So I can add my card, with the scheme provider BurgerKing & check its details successfully

  @add @bink_regression
  Scenario: Add Journey_BurgerKing

    Given I am a customer who is subscribing to Bink or I am Bink app user
    When I perform POST request to add "BurgerKing" membership card
    And I perform GET request to verify the "BurgerKing" membership card is added to the wallet
    Then verify the data stored in DB after "Add" journey for "BurgerKing"
    Then I perform DELETE request to delete the "BurgerKing" membership card


  @balances_transactions @bink_regression
  Scenario: Balances and Burgerking

    Given I am a Bink user
    When I perform POST request to add "BurgerKing" membership card
    And I perform GET request to verify the "BurgerKing" membership card is added to the wallet
    And I perform GET request to view balance for recently added "BurgerKing" membership card
#    When I perform GET request to view all transactions made using the recently added "BurgerKing" membership card
#    Then I perform GET request to view a specific transaction made using the recently added "BurgerKing" membership card
    Then verify the data stored in DB after "Add" journey for "BurgerKing"
    And I perform DELETE request to delete the "BurgerKing" membership card

  @vouchers @bink_regression
  Scenario: Add Journey BurgerKing and verify vouchers

    Given I am a customer who is subscribing to Bink or I am Bink app user
    When I perform POST request to add "BurgerKing" membership card
    And I perform GET request to verify the "BurgerKing" membership card voucher details
    Then verify the data stored in DB after "Add" journey for "BurgerKing"
    Then I perform DELETE request to delete the "BurgerKing" membership card

  @add_patch @bink_regression
  Scenario: PATCH membership card details_BurgerKing

    Given I am a Bink user
    When I perform POST request to add "BurgerKing" membership card with "invalid_data"
    And I perform GET request to verify the "BurgerKing" membership card is added to the wallet with invalid data
    And I perform PATCH request to update "BurgerKing" membership card
    And I perform GET request to verify the "BurgerKing" membership card details got updated after a successful PATCH
    Then verify the data stored in DB after "Add" journey for "BurgerKing"
    And I perform DELETE request to delete the "BurgerKing" membership card

  @add_and_link @bink_regression
  Scenario: ADD & LINK Journey_BurgerKing

    Given I am a Bink user
    And I perform POST request to add payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully
    When I perform POST request to add & auto link an existing "BurgerKing" membership card
    And I perform GET request to verify the "BurgerKing" membership card is added & linked successfully in the wallet
    And I perform GET request to view balance for recently added "BurgerKing" membership card
    Then verify the data stored in DB after "Add" journey for "BurgerKing"
    Then I perform DELETE request to delete the "BurgerKing" membership card
    And I perform DELETE request to delete the payment card

  @enrol @bink_regression
  Scenario: Join Journey_BurgerKing

    Given I register with bink service as a new customer
    When I perform POST request to create a "BurgerKing" membership account with enrol credentials
    And I perform GET request to verify the "BurgerKing" membership account is created
    Then verify the data stored in DB after "Enrol" journey for "BurgerKing"
    Then I perform DELETE request to delete the "BurgerKing" membership card
    And I perform DELETE request to delete the customer

  @enrol_put @bink_regression
  Scenario: Join Journey_PUT_BurgerKing

    Given I register with bink service as a new customer
    When I perform POST request to create a "BurgerKing" membership account with "invalid" enrol credentials
    And I perform GET request to verify the "BurgerKing" membership account is created with invalid data
    And I perform PUT request to replace information of the enrolled "BurgerKing" membership card
    And I perform GET request to verify the enrolled "BurgerKing" membership card details got replaced after a successful PUT
    Then verify the data stored in DB after "Enrol" journey for "BurgerKing"
    Then I perform DELETE request to delete the "BurgerKing" membership card
    And I perform DELETE request to delete the customer

  @add_always_link  @LOY-1211
  Scenario: Adding payments cards to always auto-link

   Given I am a Bink user
   When I perform POST request to add "BurgerKing" membership card
   And I perform POST request to add payment card to wallet
   And I perform the GET request to verify the payment card has been added successfully
   And I perform GET request to verify the "BurgerKing" membership card is added & linked successfully in the wallet
   Then I perform DELETE request to delete the payment card

  @enrol_add @bink_regression
  Scenario: Verify join burgerking then delete membership_card from the wallet and Add membershipcard into the wallet again with enrol data

    Given I register with bink service as a new customer
    When I perform POST request to create a "BurgerKing" membership account with enrol credentials
    And I perform GET request to verify the "BurgerKing" membership account is created
    Then I perform DELETE request to delete the "BurgerKing" membership card
    When I perform POST request to add "BurgerKing" membership card after enrol deleted
    And I perform GET request to verify the "BurgerKing" membership card is added to the wallet
    Then verify the data stored in DB after "Enrol" journey for "BurgerKing"
