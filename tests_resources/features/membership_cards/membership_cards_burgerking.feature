@bk @bink
Feature: Merchant Burgerking - Ensure a customer can add & link their membership card and enrol for a new membership card & view its details
  As a customer
  I want to utilise membership_cards endpoint of the Banking API
  So I can add my card, with the scheme provider Burgerking & check its details successfully

  @add
    Scenario: Add Journey Burgerking
    Given I am a Bink user
    When I submit POST request to add "burgerking" membership card
    And I submit GET request to verify "burgerking" membership card is added to the wallet
    Then I perform DELETE request to delete the "burgerking" membership card
    Then verify membership account Join date, Card Number and Merchant identifier populated in Django


#  @addAndLink
#    Scenario: Verify Burgerking customer can add membership card -  Add Journey Burgerking
#    Given I am a Bink user
#    When I submit POST request to add "burgerking" membership card
#    And I submit GET request to verify "burgerking" membership card is added to  wallet
#    Then I perform DELETE request to delete the "burgerking" membership card
#    Then verify membership account Join date, Card Number and Merchant identifier populated in Django