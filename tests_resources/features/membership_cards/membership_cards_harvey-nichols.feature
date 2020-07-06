@hn @bink
Feature: Merchant Harvey Nichols - Ensure a customer can add their membership card & view its details for merchant Harvey Nichols
  As a customer
  I want to utilise membership_cards endpoint of the Banking API
  So I can add my card, with the scheme provider Harvey Nichols & check its details successfully


  @add
  Scenario: Add Journey_Harvey Nichols

    Given I am a Bink user
    When I perform POST request to add "harvey-nichols" membership card
    And I perform GET request to verify "harvey-nichols" membership card is added to the wallet
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    And I perform DELETE request to delete the "harvey-nichols" membership card


  @add_patch
  Scenario:  PATCH membership card details_Harvey Nichols

    Given I am a Bink user
    When I perform POST request to add "harvey-nichols" membership card with "invalid_data"
    And I perform GET request to verify "harvey-nichols" membership card is added to the wallet with invalid data
    And I perform PATCH request to update "harvey-nichols" membership card
    And I perform GET request to verify "harvey-nichols" membership card details got updated after a successful PATCH
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    And I perform DELETE request to delete the "harvey-nichols" membership card

  @addAndLink
  Scenario: ADD & LINK Journey_Harvey Nichols
    Given I am a Bink user
    And I perform POST request to add payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully
#    When I perform POST request to add & auto link an existing "harvey-nichols" membership card
#    Then I perform GET request to verify "harvey-nichols" membership card is added & linked successfully in the wallet
#    And I perform GET request to view balance for recently added membership card
#    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
#    And I perform GET request to view balance for recently added membership card
#    Then I perform DELETE request to delete the "harvey-nichols" membership card
#    And I perform DELETE request to delete the payment card
#    Then the payment card is deleted successfully from their wallet

