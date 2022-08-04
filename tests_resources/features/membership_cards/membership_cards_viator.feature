@viator @sanity
Feature: Merchant Viator - Ensure a customer can add their membership card & view its details for merchant Viator
  As a customer
  I want to utilise membership_cards endpoint
  So I can add my card, with the scheme provider Viator & check its details successfully

  @enrol @bink_regression
  Scenario: Join Journey_Viator

    Given I register with bink service as a new customer
    When I perform POST request to create a "Viator" membership account with enrol credentials
    And I perform GET request to verify the "Viator" membership account is created
    Then verify the data stored in DB after "Enrol" journey for "Viator"
    Then I perform DELETE request to delete the "Viator" membership card
    And I perform DELETE request to delete the customer

  @add @bink_regression
  Scenario: Add Journey_Viator

    Given I am a Bink user
    When I perform POST request to add "Viator" membership card
    And I perform GET request to verify the "Viator" membership card is added to the wallet
    Then verify the data stored in DB after "Add" journey for "Viator"
    And I perform DELETE request to delete the "Viator" membership card