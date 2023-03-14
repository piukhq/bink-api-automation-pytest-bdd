# Updated by njames at 14/03/2023

 @payment_cards @sanity @sanity_bmb
Feature: This feature file contains different features related to payment cards (Loyalty Squad features)
  As these are the common behaviours, they are implemented for various merchants to increase the code coverage

  As a customer
  I want to utilise payment_cards endpoint
  So I can add my payment card and can link to Harvey Nichols membership card & check the details successfully



    Scenario: Verify deletion of membership card linked to a Payment card deletes PLL link

    Given I register with bink service as a new customer
    When I perform POST request to add "master" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    And I perform POST request to add & auto link "Trenette" membership card
    Then I perform GET request to verify the "Trenette" membership card is added & linked successfully in the wallet
    And Ensure only one payment card returned in the response
    Then I perform DELETE request to delete the "Trenette" membership card
    And I perform GET/payment_card/id request to verify the membership card is unlinked
    Then I perform DELETE request to delete the customer


    Scenario: Verify deletion of Payment card linked to a membership card deletes PLL link

    Given I register with bink service as a new customer
    When I perform POST request to add "master" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    And I perform POST request to add & auto link "SquareMeal" membership card
    Then I perform GET request to verify the "SquareMeal" membership card is added & linked successfully in the wallet
    And I perform DELETE request to delete the payment card
    And I perform GET/membership_card/id request to verify the payment card is unlinked from "SquareMeal" membership card
    Then I perform DELETE request to delete the customer


    Scenario: Check a customer can link multiple payment cards to the same membership card

    Given I register with bink service as a new customer
    When I perform POST request to add multiple payment cards to wallet
    And I perform the GET request to verify all the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "Iceland" membership card
    And I perform GET request to verify the "Iceland" membership card is added & linked to all payment cards
    And I perform the GET/payment_cards request to verify the membership card is linked to all payment cards
    Then I perform DELETE request to delete the "Iceland" membership card
    And I perform GET request to verify the membership card is unlinked from all payment cards
    And I perform DELETE request to delete all payment cards
    And I perform DELETE request to delete the customer



  Scenario: Delete Payment card by hash

    Given I register with bink service as a new customer
    When I perform POST request to add "amex" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    And I perform POST request to add & auto link "Wasabi" membership card
    Then I perform GET request to verify the "Wasabi" membership card is added & linked successfully in the wallet
    And I perform DELETE request to delete the payment card by hash
    And I perform GET/membership_card/id request to verify the payment card is unlinked from "Wasabi" membership card
    Then I perform DELETE request to delete the customer