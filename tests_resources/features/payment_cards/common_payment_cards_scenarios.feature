@harvey_nichols @payment_cards  @bmb
Feature: This feature file contains different features related to payment cards
  As these are the common behaviours, they are implemented for one merchant ( Harvey-Nichols)
  Note: Edit the merchant parameter as Iceland, Fatface, BurgerKing, Wasabi, WHSmith, CoOP if required
  and by default the payment card provider type is "master card"

  As a customer
  I want to utilise payment_cards endpoint
  So I can add my payment card and can link to Harvey Nichols membership card & check the details successfully


  @bink_regression @bmb_regression
    Scenario: Verify deletion of membership card linked to a Payment card deletes PLL link

    Given I register with bink service as a new customer
    When I perform POST request to add "master" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    And I perform POST request to add & auto link "HarveyNichols" membership card
    Then I perform GET request to verify the "HarveyNichols" membership card is added & linked successfully in the wallet
    And Ensure only one payment card returned in the response
    Then I perform DELETE request to delete the "HarveyNichols" membership card
    And I perform GET/payment_card/id request to verify the membership card is unlinked
    Then I perform DELETE request to delete the customer
#      Below 2 scenarios are also covered in above steps
#      Scenario: Check a customer can auto link a membership card to a payment card
#      Scenario: Verify for a new customer with one mcard & pacrd linked in wallet returns only one PLL link in the response

  @bink_regression @bmb_regression
    Scenario: Verify deletion of Payment card linked to a membership card deletes PLL link

    Given I register with bink service as a new customer
    When I perform POST request to add "master" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    And I perform POST request to add & auto link "HarveyNichols" membership card
    Then I perform GET request to verify the "HarveyNichols" membership card is added & linked successfully in the wallet
    And I perform DELETE request to delete the payment card
    And I perform GET/membership_card/id request to verify the payment card is unlinked from "HarveyNichols" membership card
    Then I perform DELETE request to delete the customer

  @bink_regression @bmb_regression
    Scenario: Check a customer can link multiple payment cards to the same membership card

    Given I register with bink service as a new customer
    When I perform POST request to add multiple payment cards to wallet
    And I perform the GET request to verify all the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "HarveyNichols" membership card
    And I perform GET request to verify the "HarveyNichols" membership card is added & linked to all payment cards
    And I perform the GET/payment_cards request to verify the membership card is linked to all payment cards
    Then I perform DELETE request to delete the "HarveyNichols" membership card
    And I perform GET request to verify the membership card is unlinked from all payment cards
    And I perform DELETE request to delete all payment cards
    And I perform DELETE request to delete the customer

#     This scenario should happen in preprod, not implemented in staging yet
  @preprod @LOY1285
    Scenario: PLL link visa _ preprod tests

    Given I register with bink service as a new customer
    When I perform POST request to add "visa" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    And I perform POST request to add & auto link "HarveyNichols" membership card
    And I perform GET request to verify the "HarveyNichols" membership card is added to the wallet
    Then I perform DELETE request to delete the "HarveyNichols" membership card
    And I perform GET/payment_card/id request to verify the membership card is unlinked
   Then I perform DELETE request to delete the customer

@bink_regression @bmb_regression
  Scenario: Delete Payment card by hash

    Given I register with bink service as a new customer
    When I perform POST request to add "amex" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    And I perform POST request to add & auto link "HarveyNichols" membership card
    Then I perform GET request to verify the "HarveyNichols" membership card is added & linked successfully in the wallet
    And I perform DELETE request to delete the payment card by hash
    And I perform GET/membership_card/id request to verify the payment card is unlinked from "HarveyNichols" membership card
    Then I perform DELETE request to delete the customer