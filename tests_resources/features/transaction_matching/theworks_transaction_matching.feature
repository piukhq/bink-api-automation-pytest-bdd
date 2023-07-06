@tm @the_works

Feature: Merchant The Work - Ensure a customer can use Bink's Transaction Matching features
  As a customer
  I shopped at a Bink PLL partner that uses transaction matching
  So I can offer a near real time transaction matching service to merchants.

  @sanity @sanity_bmb
  Scenario: Verify transaction spotting for TheWorks using Visa E2E

    Given I am a Bink user
    When I perform POST request to add "visa" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "TheWorks" membership card
    Then I perform GET request to verify the "TheWorks" membershipcard is added & linked successfully in the wallet
    When I send Payment Transaction File with visa-auth-spotting-e2e and MID as works0001
    When I send Payment Transaction File with visa-settlement-spotting-e2e and MID as works0001
    Then I verify the reward transaction is exported using transaction-spotting
    When I send Payment Transaction File with visa-refund-spotting-e2e and MID as works0001
    Then I verify the reward transaction is exported using transaction-spotting

  @sanity @sanity_bmb
  Scenario: Verify transaction spotting for TheWorks using Amex E2E

    Given I am a Bink user
    When I perform POST request to add "amex" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "TheWorks" membership card
    Then I perform GET request to verify the "TheWorks" membershipcard is added & linked successfully in the wallet
    When I send Payment Transaction File with amex-settlement-spotting and MID as works0003
    Then I verify the reward transaction is exported using transaction-spotting
    When I send Payment Transaction File with amex-refund-spotting and MID as works0003
    Then I verify the reward transaction is exported using transaction-spotting

    @sanity @sanity_bmb
    Scenario: Verify transaction spotting for TheWorks using Master E2E

    Given I am a Bink user
    When I perform POST request to add "master" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "TheWorks" membership card
    Then I perform GET request to verify the "TheWorks" membershipcard is added & linked successfully in the wallet
    When I send Payment Transaction File with master-settlement-spotting and MID as works0002
    Then I verify the reward transaction is exported using transaction-spotting
    When I send Payment Transaction File with master-refund-spotting-the-works and MID as works0002
    Then I verify the reward transaction is exported using transaction-spotting-refund-the-works

  @sanity @sanity_bmb
  Scenario Outline: Verify transaction spotting for TheWorks _ dedupe

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link TheWorks membership card for Tx_spotting_dedupe_testing
    Then I perform GET request to verify the "TheWorks" membershipcard is added & linked successfully in the wallet
    When I send Payment File with a duplicate transaction using <payment_card_transaction> and <mid>
    Then I verify the reward transaction is de-duplicated using dedupe and spotting
    Examples:

      | payment_card_provider | mid       | payment_card_transaction |
      | visa                  | works0001 | visa-settle-spotting     |
#    |          visa        |  works0001    |visa-refund-spotting        |
#    |          master      |  works0002    |master-auth-spotting        |
#    |          master      |  works0002    |master-settlement-spotting  |
#    |          master      |  works0002    |master-refund-spotting      |
#    |          amex        |  works0003   |amex-settlement-spotting     |
#    |          amex        |  works0003   |amex-refund-spotting        |

#  Scenario Outline: Verify that viator AMEX auth transaction for spotting merchant is not exported
#
#    Given I am a Bink user
#    When I perform POST request to add "<payment_card_provider>" payment card to wallet
#    And I perform the GET request to verify the payment card has been added successfully to the wallet
#    When I perform POST request to add & auto link "TheWorks" membership card
#    Then I perform GET request to verify the "TheWorks" membershipcard is added & linked successfully in the wallet
#    When I send Payment Transaction File with <payment_card_transaction> <mid>
#    Then I verify transaction is imported into the import_transaction table
#    Then I verify transaction is not spotted and exported
#
#    Examples:
#      | payment_card_provider | mid        | payment_card_transaction |
#      | amex                  | 9602929481 | amex-auth-spotting       |
#
#

