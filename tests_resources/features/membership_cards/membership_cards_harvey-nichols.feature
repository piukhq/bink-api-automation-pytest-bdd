@hn @bink
Feature: Merchant Harvey Nichols - Ensure a customer can add their membership card & view its details for merchant Harvey Nichols
  As a customer
  I want to utilise membership_cards endpoint of the Banking API
  So I can add my card, with the scheme provider Harvey Nichols & check its details successfully

 @add
    Scenario: Verify Harvey Nichols customer can add membership card ( Add Journey )
    Given I am a Bink user
    When I submit POST request to add "harvey-nichols" membership card
    And I submit GET request to verify "harvey-nichols" membership card is added to the wallet
    Then verify membership account Join date, Card Number and Merchant identifier populated in Django
    And I perform DELETE request to delete the "harvey-nichols" membership card



#    When they POST request to add & auto link an existing Iceland membership card
#    Then they perform GET request to verify Iceland membership card is added & linked successfully in their Barclays wallet
#    And they can make GET request to check balance for recently added membership card
#    And they can perform Delete operation to delete the membership card
   @addAndLink
  Scenario: Verify a user can add & link their existing HN membership card (ADD & LINK journey)
    Given I am a Bink user
    And I perform POST request to add payment card to wallet
#    Then I perform GET request to verify the payment card has been added successfully
#    When I perform POST request to add & auto link an existing "harvey-nichols" membership card
#    Then I perform GET request to verify "harvey-nichols" membership card is added & linked successfully in the wallet
#    Then verify membership account Join date, Card Number and Merchant identifier populated in Django
#    And I perform GET request to view balance for recently added membership card
#    When I perform DELETE request to delete the "harvey-nichols" membership card
#    And I perform DELETE request to delete the payment card
#    Then the payment card is deleted successfully from their wallet

#  Scenario: Verify a user can add & link their existing HN membership card and verify Voucher details in wallet
#
#
#  @enrol
#   Scenario: Verify a new Harvey Nichols customer can enrol membership scheme (Join journey)v1.1
#    Given I registers with bink service as a new customer
#    When I submit POST request to create a "harvey-nichols" membership account with enrol details
#    And they can perform PUT request to replace information of enrol membership card
#    And I submit GET request to verify "harvey-nichols" account is created
#    Then I perform DELETE request to delete the "harvey-nichols" membership card
#    Then verify membership account Join date, Card Number and Merchant identifier populated in Django

