@square_meal @dev

Feature: Merchant Square-meal - Ensure a customer can add their membership card & view its details for merchant Square-meal
  As a customer
  I want to utilise membership_cards endpoint
  So I can add my card, with the scheme provider Square-meal & check its details successfully

  @enrol @bink_regression @bmb_regression @sanity_bmb @sanity
  Scenario: Join Journey_SquareMeal

    Given I register with bink service as a new customer
    When I perform POST request to create a "SquareMeal" membership account with enrol credentials
    And I perform GET request to verify the "SquareMeal" membership account is created
    Then verify the data stored in DB after "Enrol" journey for "SquareMeal"
    Then I perform DELETE request to delete the "SquareMeal" membership card
    And I perform DELETE request to delete the customer


  @add @bink_regression @bmb_regression @sanity_bmb @sanity
  Scenario: Add Journey_SquareMeal

    Given I am a Bink user
    When I perform POST request to add "SquareMeal" membership card
    And I perform GET request to verify the "SquareMeal" membership card is added to the wallet
    Then verify the data stored in DB after "Add" journey for "SquareMeal"
    And I perform DELETE request to delete the "SquareMeal" membership card

  @enrol_put @bink_regression @sanity
  Scenario: Join Journey with invalid credentials and replace with valid credentials_SquareMeal

    Given I register with bink service as a new customer
    When I perform POST request to create a "SquareMeal" membership account with "invalid" enrol credentials
    And I perform GET request to verify the "SquareMeal" membership account is created with invalid data
    And I perform PUT request to replace information of the enrolled "SquareMeal" membership card
    And I perform GET request to verify the enrolled "SquareMeal" membership card details got replaced after a successful PUT
    Then verify the data stored in DB after "Enrol" journey for "SquareMeal"
    Then I perform DELETE request to delete the "SquareMeal" membership card
    And I perform DELETE request to delete the customer

