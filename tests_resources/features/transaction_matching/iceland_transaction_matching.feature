@tm @iceland
Feature: Merchant Iceland - Ensure a customer can use Bink's Transaction Matching features
  As a customer
  I shopped at a Bink PLL partner that uses transaction matching
  So I can offer a near real time transaction matching service to merchants.

  @sanity @sanity_bmb @test
  Scenario Outline: Verify transaction matching for iceland with payment provider

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "Iceland" membership card
    Then I perform GET request to verify the "Iceland" membershipcard is added & linked successfully in the wallet
    When I send Retailer Transaction File with <merchant_container> <payment_card_provider> <mid> <card_identity>
    And I send Payment Transaction File with <payment_card_transaction> <mid>
    Then I verify the reward transaction is exported

    Examples:
      | payment_card_provider | merchant_container | mid        | card_identity             | payment_card_transaction   |
#      | visa                  | scheme/iceland/    | 10209723   | Visa                      | visa-auth-matching         |
#      | visa                  | scheme/iceland/    | 10209723   | Visa                      | visa-settlement-matching   |
#      | master                | scheme/iceland/    | 22776952   | MasterCard/MasterCard One | master-auth-matching       |
#      | master                | scheme/iceland/    | 22776952   | MasterCard/MasterCard One | master-settlement-matching |
      | amex                  | scheme/iceland/    | 9445909831 | Amex                      | amex-auth-matching         |
      | amex                  | scheme/iceland/    | 9421802109 | Amex                      | amex-settlement-matching   |


  @sanity @sanity_bmb
  Scenario Outline: Verify transaction matching for iceland with payment provider but invalid mid

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "Iceland" membership card
    Then I perform GET request to verify the "Iceland" membershipcard is added & linked successfully in the wallet
    When I send Retailer Transaction File with <merchant_container> <payment_card_provider> <mid> <card_identity>
    And I send Payment Transaction File with <payment_card_transaction> <mid>
    Then I verify transaction is not matched and exported

    Examples:
      | payment_card_provider | merchant_container | mid        | card_identity              | payment_card_transaction   |
      | amex                  | scheme/iceland/    | 7821802109 | Amex                      | amex-settlement-matching   |
      | amex                  | scheme/iceland/    | 8445909831 | Amex                      | amex-auth-matching         |
      | visa                  | scheme/iceland/    | 80209723   | Visa                      | visa-auth-matching         |
      | visa                  | scheme/iceland/    | 80209723   | Visa                      | visa-settlement-matching   |
      | master                | scheme/iceland/    | 72776952   | MasterCard/MasterCard One | master-settlement-matching |
      | master                | scheme/iceland/    | 72776952   | MasterCard/MasterCard One | master-auth-matching       |


