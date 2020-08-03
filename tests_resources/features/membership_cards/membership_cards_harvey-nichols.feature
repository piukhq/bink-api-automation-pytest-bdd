@harvey_nichols @bink
Feature: Merchant Harvey Nichols - Ensure a customer can add their membership card & view its details for merchant Harvey Nichols
  As a customer
  I want to utilise membership_cards endpoint of the Banking API
  So I can add my card, with the scheme provider Harvey Nichols & check its details successfully


  @add
  Scenario: Add Journey_HarveyNichols

    Given I am a Bink user
    When I perform POST request to add "HarveyNichols" membership card
    And I perform GET request to verify the "HarveyNichols" membership card is added to the wallet
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    And I perform DELETE request to delete the "HarveyNichols" membership card


  @add_patch
  Scenario:  PATCH membership card details_HarveyNichols

    Given I am a Bink user
    When I perform POST request to add "HarveyNichols" membership card with "invalid_data"
    And I perform GET request to verify the "HarveyNichols" membership card is added to the wallet with invalid data
    And I perform PATCH request to update "HarveyNichols" membership card
    And I perform GET request to verify the "HarveyNichols" membership card details got updated after a successful PATCH
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    And I perform DELETE request to delete the "HarveyNichols" membership card

  @add_and_link
  Scenario: ADD & LINK Journey_HarveyNichols

    Given I am a Bink user
    And I perform POST request to add payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully
    When I perform POST request to add & auto link an existing "HarveyNichols" membership card
    And I perform GET request to verify the "HarveyNichols" membership card is added & linked successfully in the wallet
#    Check if balance array is same for PLL & PLR . If not create separate scenarios
    And I perform GET request to view balance for recently added "HarveyNichols" membership card
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    Then I perform DELETE request to delete the "HarveyNichols" membership card
    And I perform DELETE request to delete the payment card

  @enrol
    Scenario: Join Journey(Enrol)_HarveyNichols


    Given I register with bink service as a new customer
    When I perform POST request to create a "HarveyNichols" membership account with enrol credentials
    And I perform GET request to verify the "HarveyNichols" membership account is created
    Then verify membership account Join date, Card Number and Merchant identifier populated in Django
    Then I perform DELETE request to delete the "HarveyNichols" membership card

  @enrol_put
  Scenario: Join Journey(Enrol)_PUT_HarveyNichols


    Given I register with bink service as a new customer
    When I perform POST request to create a "HarveyNichols" membership account with "invalid" enrol credentials
    And I perform GET request to verify the "HarveyNichols" membership account is created with invalid data
    And I perform PUT request to replace information of the enrolled "HarveyNichols" membership card
    And I perform GET request to verify the enrolled "HarveyNichols" membership card details got replaced after a successful PUT
    Then verify membership account Join date, Card Number and Merchant identifier populated in Django
    Then I perform DELETE request to delete the "HarveyNichols" membership card


