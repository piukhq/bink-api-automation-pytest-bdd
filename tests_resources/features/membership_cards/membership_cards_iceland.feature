@il @bink
Feature: Merchant Iceland - Ensure a customer can add their membership card & view its details
  As a customer
  I want to utilise membership_cards endpoint of the Banking API
  So I can add my card, with the scheme provider Iceland & check its details successfully


   @add
    Scenario: Add Journey_Iceland

    Given I am a Bink user
    When I submit the POST request to add "iceland" membership card
    And I submit the GET request to verify "iceland" membership card is added to the wallet
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    And I submit the DELETE request to delete the "iceland" membership card


  @add_patch
  Scenario:  PATCH membership card details_Iceland

    Given I am a Bink user
    When I submit the POST request to add "iceland" membership card with "invalid_data"
    And I submit the GET request to verify "iceland" membership card is added to the wallet with invalid data
    And I submit the PATCH request to update "iceland" membership card
    And I submit the GET request to verify "iceland" membership card details got updated after a successful PATCH
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    And I submit the DELETE request to delete the "iceland" membership card

