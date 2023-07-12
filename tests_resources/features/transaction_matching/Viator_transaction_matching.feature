@tm @viator
Feature: Merchant VIATOR - Ensure a customer can use Bink's Transaction Matching features
  As a customer
  I shopped at a Bink PLL partner that uses transaction matching
  So I can offer a near real time transaction matching service to merchants.

   @sanity @sanity_bmb
    Scenario Outline: Verify transaction spotting for Viator

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "Viator" membership card
    Then I perform GET request to verify the "Viator" membershipcard is added & linked successfully in the wallet
    When I send Payment Transaction File with <payment_card_transaction> <mid>
    Then I verify the reward transaction is exported using transaction-spotting
    Examples:
    | payment_card_provider|     mid       |payment_card_transaction    |
    |          visa        |  020150514    |visa-auth-spotting          |
    |          visa        |  020150514    |visa-settlement-spotting    |
    |          visa        |  020150514    |visa-refund-spotting        |
    |          master      |  020150514    |master-auth-spotting        |
# Already included in E2E Test    |          master      |  020150514    |master-settlement-spotting  |
    |          amex        |  9602929481   |amex-settlement-spotting     |
    |          amex        |  9602929481   |amex-refund-spotting        |



  @sanity @sanity_bmb
    Scenario Outline: Verify that viator AMEX auth transaction for spotting merchant is not exported

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "Viator" membership card
    Then I perform GET request to verify the "Viator" membershipcard is added & linked successfully in the wallet
    When I send Payment Transaction File with <payment_card_transaction> <mid>
    Then I verify transaction is imported into the import_transaction table
    Then I verify transaction is not spotted and exported

    Examples:
    | payment_card_provider|     mid       |payment_card_transaction      |
    |          amex        |  9602929481   |amex-auth-spotting            |



    @sanity @sanity_bmb
    Scenario Outline: Verify transaction Spotting for viator negative scenario(invalid mid)

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "Viator" membership card
    Then I perform GET request to verify the "Viator" membershipcard is added & linked successfully in the wallet
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




    @sanity @sanity_bmb
    Scenario: Verify transaction Viator MasterCard Transaction Spotting E2E(Settle, Refund)

    Given I am a Bink user
    When I perform POST request to add "master" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "Viator" membership card
    Then I perform GET request to verify the "Viator" membershipcard is added & linked successfully in the wallet
    When I send Payment Transaction File with master-settlement-spotting and MID as 020150514
    Then I verify the reward transaction is exported using transaction-spotting
    When I send Payment Transaction File with master-refund-spotting and MID as 020150514
    Then I verify the reward transaction is exported using transaction-spotting-refund


    Scenario Outline: Verify transaction spotting for VIATOR negative scenario(invalid payment card token)

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "Viator" membership card
    Then I perform GET request to verify the "Viator" membershipcard is added & linked successfully in the wallet
    When I send matching "<payment_card_transaction>" "<mid>" Authorisation
    Then I verify transaction is not spotted and exported

    Examples:
    | payment_card_provider|     mid       |payment_card_transaction               |
    |          visa        |  020150514     |visa-auth-spotting_invalid_token      |




    Scenario Outline: Verify End to End transaction spotting for Viator

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "Viator" membership card
    Then I perform GET request to verify the "Viator" membershipcard is added & linked successfully in the wallet
    When I post both settlement and auth transaction file "<mid>" Authorisation
    Then I verify transaction is spotted and exported
    

    Examples:
    | payment_card_provider|     mid       |
    |          visa        |  020150514    |

