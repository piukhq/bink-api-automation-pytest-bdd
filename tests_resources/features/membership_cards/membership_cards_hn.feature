@hn @bink
Feature: Merchant Harvey Nichols - Ensure a customer can add their membership card & view its details for merchant Harvey Nichols
  As a customer
  I want to utilise membership_cards endpoint of the Banking API
  So I can add my card, with the scheme provider Harvey Nichols & check its details successfully

 @add
    Scenario: Verify Harvey Nichols customer can add membership card ( Add Journey )
    Given I am a Bink user
    When I submit POST request to add "harvey-nichols" membership card
    And I submit GET request to verify "harvey-nichols" membership card is added to  wallet
    Then I perform DELETE request to delete the "harvey-nichols" membership card
    Then verify membership account Join date, Card Number and Merchant identifier populated in Django



  @enrol
    Scenario: Verify a new Harvey Nichols customer can enrol membership scheme (Join journey)v1.1
    Given I registers with bink service as a new customer
    When I submit POST request to create a "harvey-nichols" membership account with enrol details
#    And they can perform PUT request to replace information of enrol membership card
#    And I submit GET request to verify "harvey-nichols" account is created
#    Then I perform DELETE request to delete the "harvey-nichols" membership card
#    Then verify membership account Join date, Card Number and Merchant identifier populated in Django

