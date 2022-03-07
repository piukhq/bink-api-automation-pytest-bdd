@trenette @sanity
Feature: Merchant Trenette - Ensure a customer can add their membership card & view its details for merchant Wasabi
  As a customer
  I want to utilise membership_cards endpoint
  So I can add my card, with the scheme provider Trenette & check its details successfully


  @enrol @bink_regression
  Scenario: Join Journey_Trenette

    Given I register with bink service as a new customer
    When I perform POST request to create a "Trenette" membership account with enrol credentials
    And I perform GET request to verify the "Trenette" membership account is created
    Then verify the data stored in DB after "Enrol" journey for "Trenette"
    Then I perform DELETE request to delete the "Trenette" membership card
    And I perform DELETE request to delete the customer

  @add @bink_regression
  Scenario: Add Journey_Trenette

    Given I am a Bink user
    When I perform POST request to add "Trenette" membership card
    And I perform GET request to verify the "Trenette" membership card is added to the wallet
    Then verify the data stored in DB after "Add" journey for "Trenette"
    And I perform DELETE request to delete the "Trenette" membership card