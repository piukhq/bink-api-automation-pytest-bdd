@coop @bink
Feature: Merchant CooP- Ensure a customer can add their membership card & view its details
  As a customer
  I want to utilise membership_cards endpoint of the Banking API
  So I can add my card, with the scheme provider CooP & check its details successfully


   @add
    Scenario: Add Journey_CooP

    Given I am a Bink user
    When I perform POST request to add "coop" membership card
    And I perform GET request to verify "coop" membership card is added to the wallet
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    And I perform DELETE request to delete the "coop" membership card


  @add_patch
  Scenario:  PATCH membership card details_Coop

    Given I am a Bink user
    When I perform POST request to add "coop" membership card with "invalid_data"
    And I perform GET request to verify "coop" membership card is added to the wallet with invalid data
    And I perform PATCH request to update "coop" membership card
    And I perform GET request to verify "coop" membership card details got updated after a successful PATCH
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    And I perform DELETE request to delete the "coop" membership card