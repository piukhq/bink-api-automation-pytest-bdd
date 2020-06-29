@il @bink
Feature: Merchant Iceland - Ensure a customer can add their membership card & view its details
  As a customer
  I want to utilise membership_cards endpoint of the Banking API
  So I can add my card, with the scheme provider Iceland & check its details successfully

 @add
    Scenario: Verify Iceland customer can add membership card ( Add Journey )
    Given I am a Bink user
    When I submit POST request to add "iceland" membership card
    And I submit GET request to verify "iceland" membership card is added to the wallet
    Then I perform DELETE request to delete the "iceland" membership card
    Then verify membership account Join date, Card Number and Merchant identifier populated in Django


