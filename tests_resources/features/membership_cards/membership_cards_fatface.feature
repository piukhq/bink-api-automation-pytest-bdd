@fatface
Feature: Merchant FatFace - Ensure a customer can add their membership card & view its details
  As a customer
  I want to utilise membership_cards endpoint of the Banking API
  So I can add my card, with the scheme provider FatFace & check its details successfully


   
@add
    Scenario: Add Journey_FatFace

    Given I am a Bink user
    When I perform POST request to add "FatFace" membership card
    And I perform GET request to verify the "FatFace" membership card is added to the wallet
    Then verify the data stored in DB after "Add" journey for "FatFace"
    And I perform DELETE request to delete the "FatFace" membership card


  @add_patch
  Scenario: PATCH membership card details_FatFace

    Given I am a Bink user
    When I perform POST request to add "FatFace" membership card with "invalid_data"
    And I perform GET request to verify the "FatFace" membership card is added to the wallet with invalid data
    And I perform PATCH request to update "FatFace" membership card
    And I perform GET request to verify the "FatFace" membership card details got updated after a successful PATCH
    Then verify the data stored in DB after "Add" journey for "FatFace"
    And I perform DELETE request to delete the "FatFace" membership card


 @add_and_link
  Scenario: ADD & LINK Journey_FatFace
    Given I am a Bink user
    And I perform POST request to add payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully
    When I perform POST request to add & auto link an existing "FatFace" membership card
    And I perform GET request to verify the "FatFace" membership card is added & linked successfully in the wallet
    And I perform GET request to view balance for recently added "FatFace" membership card
    Then verify the data stored in DB after "Add" journey for "FatFace"
    Then I perform DELETE request to delete the "FatFace" membership card
    And I perform DELETE request to delete the payment card
@enrol
    Scenario: Join Journey_FatFace

    Given I register with bink service as a new customer
    When I perform POST request to create a "FatFace" membership account with enrol credentials
    And I perform GET request to verify the "FatFace" membership account is created
    Then verify the data stored in DB after "Enrol" journey for "FatFace"
    Then I perform DELETE request to delete the "FatFace" membership card
    And I perform DELETE request to delete the customer

  @enrol_put
  Scenario: Join Journey_PUT_FatFace


    Given I register with bink service as a new customer
    When I perform POST request to create a "FatFace" membership account with "invalid" enrol credentials
    And I perform GET request to verify the "FatFace" membership account is created with invalid data
    And I perform PUT request to replace information of the enrolled "FatFace" membership card
    And I perform GET request to verify the enrolled "FatFace" membership card details got replaced after a successful PUT
    Then verify the data stored in DB after "Enrol" journey for "FatFace"
    Then I perform DELETE request to delete the "FatFace" membership card
    And I perform DELETE request to delete the customer