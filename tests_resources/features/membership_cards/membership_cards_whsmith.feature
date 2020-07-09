@WHSmith @bink
Feature: Merchant WHSmith - Ensure a customer can add their membership card & view its details
  As a customer
  I want to utilise membership_cards endpoint of the Banking API
  So I can add my card, with the scheme provider WHSmith & check its details successfully

  @add 
    Scenario: Add Journey_WHSmith
    Given I am a Bink user
    When I perform POST request to add "WHSmith" membership card
    And I perform GET request to verify "WHSmith" membership card is added to the wallet
    And verify membership account Link date, Card Number and Merchant identifier populated in Django
    Then I perform DELETE request to delete the "WHSmith" membership card

