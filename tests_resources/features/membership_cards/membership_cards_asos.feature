@asos @sanity


Feature: Merchant Asos - Ensure a customer can add their membership card & view its details for merchant Asos
  As a customer
  I want to utilise membership_cards endpoint
  So I can add my card, with the scheme provider asos & check its details successfully


  @add @bink_regression
  Scenario: Add Journey_Asos

    Given I am a Bink user
    When I perform POST request to add "Asos" membership card
    And I perform GET request to verify the "Asos" membership card is added to the wallet
    Then verify the data stored in DB after "Add" journey for "Asos"
    And I perform DELETE request to delete the "Asos" membership card
