@itsu
Feature: Merchant Itsu - Ensure a customer can use Bink's Transaction Matching features
  As a customer
  I shopped at a Bink PLL partner that uses transaction matching
  So I can offer a near real time transaction matching service to merchants.


  Scenario Outline: Verify transaction matching for itsu with payment provider

    Given I am a Bink user
#    When I perform POST request to add "<payment_card_provider>" payment card to wallet
#    And I perform the GET request to verify the payment card has been added successfully to the wallet
#    When I perform POST request to add & auto link "Iceland" membership card
#    Then I perform GET request to verify the "Iceland" membershipcard is added & linked successfully in the wallet
    When I send Retailer Transaction File with <merchant_container> <payment_card_provider> <mid> <card_identity>
    And I send Payment Transaction File with <payment_card_transaction> <mid>
#    Then I verify the reward transaction is exported using transaction_matching

    Examples:
      | payment_card_provider | merchant_container | mid        | card_identity             | payment_card_transaction   |
      | master                | scheme/itsu/    | 22222222   | MasterCard/MasterCard One    | master-settlement-matching |
