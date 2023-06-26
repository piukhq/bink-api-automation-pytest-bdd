@tm

Feature: Merchant The Work - Ensure a customer can use Bink's Transaction Matching features
  As a customer
  I shopped at a Bink PLL partner that uses transaction matching
  So I can offer a near real time transaction matching service to merchants.


  Scenario Outline: Verify transaction spotting for TheWorks _ dedupe

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "TheWorks" membership card
    Then I perform GET request to verify the "TheWorks" membershipcard is added & linked successfully in the wallet
    When I send Payment Transaction File with <payment_card_transaction> <mid>
    Then I verify the reward transaction is exported using transaction-spotting
    Examples:
    | payment_card_provider|     mid       |payment_card_transaction    |
    |          visa        |  works0001    |visa-auth-spotting          |
    |          visa        |  works0001    |visa-settlement-spotting    |
    |          visa        |  works0001    |visa-refund-spotting        |
    |          master      |  works0002    |master-auth-spotting        |
    |          master      |  works0002    |master-settlement-spotting  |
    |          master      |  works0002    |master-refund-spotting      |
    |          amex        |  works0003   |amex-settlement-spotting     |
    |          amex        |  works0003   |amex-refund-spotting        |

    @sanity @sanity_bmb @chk
  Scenario: Verify transaction spotting for TheWorks using Visa E2E

    Given I am a Bink user
    When I perform POST request to add "visa" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "TheWorks" membership card
    Then I perform GET request to verify the "TheWorks" membershipcard is added & linked successfully in the wallet
    When I send Payment Transaction File with visa-auth-spotting and MID as works0001
    When I send Payment Transaction File with visa-settlement-spotting and MID as works0001
    Then I verify the reward transaction is exported using transaction-spotting
    When I send Payment Transaction File with visa-refund-spotting and MID as works0001
    Then I verify the reward transaction is exported using transaction-spotting

   @sanity @sanity_bmb @chk
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

  Scenario Outline: Verify transaction spotting with de-dupe for TheWorks

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link TheWorks membership card for Tx_spotting_dedupe_testing
    Then I perform GET request to verify the "TheWorks" membershipcard is added & linked successfully in the wallet
    When I send Payment Transaction File with <payment_card_transaction> <mid>
    Then I verify the reward transaction is exported using transaction-spotting
    Examples:
    | payment_card_provider|     mid       |payment_card_transaction    |
    |          visa        |  works0001    |visa-auth-spotting          |
#    |          visa        |  works0001    |visa-settlement-spotting    |
#    |          visa        |  works0001    |visa-refund-spotting        |
#    |          master      |  works0002    |master-auth-spotting        |
#    |          master      |  works0002    |master-settlement-spotting  |
#    |          master      |  works0002    |master-refund-spotting      |
#    |          amex        |  works0003   |amex-settlement-spotting     |
#    |          amex        |  works0003   |amex-refund-spotting        |


  Scenario Outline: Verify that viator AMEX auth transaction for spotting merchant is not exported

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "TheWorks" membership card
    Then I perform GET request to verify the "TheWorks" membershipcard is added & linked successfully in the wallet
    When I send Payment Transaction File with <payment_card_transaction> <mid>
    Then I verify transaction is imported into the import_transaction table
    Then I verify transaction is not spotted and exported

    Examples:
    | payment_card_provider|     mid       |payment_card_transaction      |
    |          amex        |  9602929481   |amex-auth-spotting            |




  Scenario Outline: Verify transaction Spotting for viator negative scenario(invalid mid)

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "TheWorks" membership card
    Then I perform GET request to verify the "TheWorks" membershipcard is added & linked successfully in the wallet
    When I send Payment Transaction File with <payment_card_transaction> <mid>
    Then I verify transaction is not streamed and exported


    Examples:
    | payment_card_provider|     mid       |payment_card_transaction |
    |          visa        |  29047530     |visa-auth-spotting       |
    |          visa        |  29047530     |visa-settlement-spotting |
    |          visa        |  29047530     |visa-refund-spotting     |
    |          master      |  29047530     |master-auth-spotting        |
    |          master      |  29047530     |master-settlement-spotting  |
    |          master      |  29047530     |master-refund-spotting      |

    Scenario Outline: Verify transaction spotting for TheWorks negative scenario(invalid payment card token)

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "TheWorks" membership card
    Then I perform GET request to verify the "TheWorks" membershipcard is added & linked successfully in the wallet
    When I send matching "<payment_card_transaction>" "<mid>" Authorisation
    Then I verify transaction is not spotted and exported

    Examples:
    | payment_card_provider|     mid       |payment_card_transaction               |
    |          visa        |  020150514     |visa-auth-spotting_invalid_token      |




    Scenario Outline: Verify End to End transaction spotting for TheWorks

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "TheWorks" membership card
    Then I perform GET request to verify the "TheWorks" membershipcard is added & linked successfully in the wallet
    When I post both settlement and auth transaction file "<mid>" Authorisation
    Then I verify transaction is spotted and exported
    

    Examples:
    | payment_card_provider|     mid       |
    |          visa        |  020150514    |

