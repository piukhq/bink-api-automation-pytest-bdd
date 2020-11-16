@harvey_nichols
Feature: Merchant CooP - Ensure a customer can add their payment card & link it to loyalty membership card
  and view their card(s) details

  As a customer
  I want to utilise payment_cards endpoint
  So I can add my payment card and can link to CooP membership card & check the details successfully

#  @dev @staging
  Scenario Outline: ADD & LINK Journey_CooP

    Given I am a Bink user
    And I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link an existing "CooP" membership card
    And I perform GET request to verify the "CooP" membership card is added & linked successfully in the wallet
    Then I perform DELETE request to delete the "CooP" membership card
    And I perform DELETE request to delete the payment card
    Examples:
    | payment_card_provider|
    |           amex       |
    |          master      |
    |          visa        |