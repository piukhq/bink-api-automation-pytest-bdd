@tm @square_meal
Feature: Merchant SquareMeal - Ensure a customer can use Bink's Transaction Matching features
  As a customer
  I shopped at a Bink PLL partner that uses transaction matching
  So I can offer a near real time transaction matching service to merchants.

  @sanity @sanity_bmb
    Scenario Outline: Verify transaction streaming for squareMeal

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "SquareMeal" membership card
    Then I perform GET request to verify the "SquareMeal" membershipcard is added & linked successfully in the wallet
    When I send Payment Transaction File with <payment_card_transaction> <mid>
    Then I verify the reward transaction is exported using transaction-streaming

    Examples:
    | payment_card_provider|     mid       |payment_card_transaction      |
#    |          visa        |  29047531     |visa-auth-streaming          |
#    |          visa        |  29047531     |visa-settlement-streaming     |
#    |          visa        |  29047531     |visa-refund-streaming         |
#    |          master      |  29047531     |master-auth-spotting          |
#    |          master      |  29047531     |master-settlement-spotting    |
#    |          master      |  29047531     |master-refund-spotting        |
    |          amex        |  9449819796   |amex-settlement-spotting      |
#    |          amex        |  9449819796   |amex-refund-spotting          |

  @sanity @sanity_bmb @test
    Scenario Outline: Verify that Squaremeal AMEX auth transaction for streaming/spotting merchant is not exported

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "SquareMeal" membership card
    Then I perform GET request to verify the "SquareMeal" membershipcard is added & linked successfully in the wallet
    When I send Payment Transaction File with <payment_card_transaction> <mid>
    Then I verify transaction is imported into the import_transaction table
#    Then I verify transaction is not exported
    Then I verify transaction is not streamed/spotted and exported

    Examples:
    | payment_card_provider|     mid       |payment_card_transaction      |
    |          amex        |  9449819796   |amex-auth-spotting            |


  @sanity @sanity_bmb
    Scenario Outline: Verify transaction streaming for squaremeal negative scenario(invalid mid)

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "SquareMeal" membership card
    Then I perform GET request to verify the "SquareMeal" membershipcard is added & linked successfully in the wallet
    When I send matching "<payment_card_transaction>" "<mid>" Authorisation
    Then I verify transaction is not streamed/spotted and exported

    Examples:
    | payment_card_provider|     mid       |payment_card_transaction |
    |          visa        |  29047530     |visa-auth-spotting       |
    |          visa        |  29047530     |visa-settlement-spotting |
    |          visa        |  29047530     |visa-refund-spotting     |

  @sanity @sanity_bmb
    Scenario Outline: Verify transaction streaming for squaremeal negative scenario(invalid payment card token)

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "SquareMeal" membership card
    Then I perform GET request to verify the "SquareMeal" membershipcard is added & linked successfully in the wallet
    When I send matching "<payment_card_transaction>" "<mid>" Authorisation
    Then I verify transaction is not streamed/spotted and exported

    Examples:
    | payment_card_provider|     mid       |payment_card_transaction               |
    |          visa        |  29047531     |visa-auth-spotting_invalid_token       |
