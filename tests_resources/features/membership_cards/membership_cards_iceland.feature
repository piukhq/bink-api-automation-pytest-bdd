@iceland @bink
Feature: Merchant Iceland - Ensure a customer can add their membership card & view its details for merchant Iceland
  As a customer
  I want to utilise membership_cards endpoint of the Banking API
  So I can add my card, with the scheme provider Iceland & check its details successfully


  @add
  Scenario: Add Journey_Iceland

    Given I am a Bink user
    When I perform POST request to add "Iceland" membership card
    And I perform GET request to verify the "Iceland" membership card is added to the wallet
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    And I perform DELETE request to delete the "Iceland" membership card


  @add_patch
  Scenario:  PATCH membership card details_Iceland

    Given I am a Bink user
    When I perform POST request to add "Iceland" membership card with "invalid_data"
    And I perform GET request to verify the "Iceland" membership card is added to the wallet with invalid data
    And I perform PATCH request to update "Iceland" membership card
    And I perform GET request to verify the "Iceland" membership card details got updated after a successful PATCH
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    And I perform DELETE request to delete the "Iceland" membership card

  @add_and_link
  Scenario: ADD & LINK Journey_Iceland

    Given I am a Bink user
    And I perform POST request to add payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully
    When I perform POST request to add & auto link an existing "Iceland" membership card
    And I perform GET request to verify the "Iceland" membership card is added & linked successfully in the wallet
    And I perform GET request to view balance for recently added "Iceland" membership card
    When I perform GET request to view all transactions made using the recently added "Iceland" membership card
    Then I perform GET request to view a specific transaction made using the recently added "Iceland" membership card
    Then verify membership account Link date, Card Number and Merchant identifier populated in Django
    Then I perform DELETE request to delete the "Iceland" membership card
    And I perform DELETE request to delete the payment card

  @enrol
    Scenario: Join Journey_Iceland


    Given I register with bink service as a new customer
    When I perform POST request to create a "Iceland" membership account with enrol credentials
    And I perform GET request to verify the "Iceland" membership account is created
    Then verify membership account Join date, Card Number and Merchant identifier populated in Django
    Then I perform DELETE request to delete the "Iceland" membership card
    And Delete the new customer

  @enrol_put
  Scenario: Join Journey_PUT_Iceland


    Given I register with bink service as a new customer
    When I perform POST request to create a "Iceland" membership account with "invalid" enrol credentials
    And I perform GET request to verify the "Iceland" membership account is created with invalid data
    And I perform PUT request to replace information of the enrolled "Iceland" membership card
    And I perform GET request to verify the enrolled "Iceland" membership card details got replaced after a successful PUT
    Then verify membership account Join date, Card Number and Merchant identifier populated in Django
    Then I perform DELETE request to delete the "Iceland" membership card


