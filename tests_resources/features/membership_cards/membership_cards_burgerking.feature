@burger_king @bink
Feature: Merchant BurgerKing - Ensure a customer can add & link their membership card and enrol for a new membership card & view its details
  As a customer
  I want to utilise membership_cards endpoint of the Banking API
  So I can add my card, with the scheme provider BurgerKing & check its details successfully

   @add
    Scenario: Add Journey_BurgerKing

    Given I am a Bink user
    When I perform POST request to add "BurgerKing" membership card
    And I perform GET request to verify the "BurgerKing" membership card is added to the wallet
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    And I perform DELETE request to delete the "BurgerKing" membership card


  @add_patch
  Scenario: PATCH membership card details_BurgerKing

    Given I am a Bink user
    When I perform POST request to add "BurgerKing" membership card with "invalid_data"
    And I perform GET request to verify the "BurgerKing" membership card is added to the wallet with invalid data
    And I perform PATCH request to update "BurgerKing" membership card
    And I perform GET request to verify the "BurgerKing" membership card details got updated after a successful PATCH
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    And I perform DELETE request to delete the "BurgerKing" membership card


 @add_and_link
  Scenario: ADD & LINK Journey_BurgerKing
    Given I am a Bink user
    And I perform POST request to add payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully
    When I perform POST request to add & auto link an existing "BurgerKing" membership card
    And I perform GET request to verify the "BurgerKing" membership card is added & linked successfully in the wallet
    And I perform GET request to view balance for recently added "BurgerKing" membership card
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    Then I perform DELETE request to delete the "BurgerKing" membership card
    And I perform DELETE request to delete the payment card

@enrol
    Scenario: Join Journey(Enrol)_BurgerKing

    Given I register with bink service as a new customer
    When I perform POST request to create a "BurgerKing" membership account with enrol credentials
    And I perform GET request to verify the "BurgerKing" membership account is created
    Then verify membership account Join date, Card Number and Merchant identifier populated in Django
    Then I perform DELETE request to delete the "BurgerKing" membership card

  @enrol_put
  Scenario: Join Journey(Enrol)_PUT_BurgerKing


    Given I register with bink service as a new customer
    When I perform POST request to create a "BurgerKing" membership account with "invalid" enrol credentials
    And I perform GET request to verify the "BurgerKing" membership account is created with invalid data
    And I perform PUT request to replace information of the enrolled "BurgerKing" membership card
    And I perform GET request to verify the enrolled "BurgerKing" membership card details got replaced after a successful PUT
    Then verify membership account Join date, Card Number and Merchant identifier populated in Django
    Then I perform DELETE request to delete the "BurgerKing" membership card

  @membership_cards_response
    Scenario: Add Journey_BurgerKing

    Given I am a Bink user
    When I perform POST request to add "BurgerKing" membership card
    And I perform GET request to verify the "BurgerKing" membership card is added to the wallet
    Then I verify the GET membership_cards response for "BurgerKing" matches with expected data
    And I perform DELETE request to delete the "BurgerKing" membership card