@tm @square_meal
Feature: Merchant SquareMeal - Ensure a customer can use Bink's Transaction Matching features
  As a customer
  I shopped at a Bink PLL partner that uses transaction matching
  So I can offer a near real time transaction matching service to merchants.

  @sanity @sanity_bmb @test

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
#    |          visa        |  29047531     |visa-settlement-streaming    |
#    |          visa        |  29047531     |visa-refund-streaming         |
#    |          master      |  29047531     |master-auth-streaming        |
#     |          master      |  29047531     |master-settlement-streaming   |
     |          master      |  29047531     |master-refund-streaming       |
#    |          amex        |  9449819796   |amex-settlement-streaming     |
#    |          amex        |  9449819796   |amex-refund-streaming          |

  @sanity @sanity_bmb
    Scenario Outline: Verify that Squaremeal AMEX auth transaction for streaming merchant is not exported

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "SquareMeal" membership card
    Then I perform GET request to verify the "SquareMeal" membershipcard is added & linked successfully in the wallet
    When I send Payment Transaction File with <payment_card_transaction> <mid>
    Then I verify transaction is imported into the import_transaction table
    Then I verify transaction is not streamed and exported

    Examples:
    | payment_card_provider|     mid       |payment_card_transaction      |
    |          amex        |  9449819796   |amex-auth-streaming           |

  @sanity @sanity_bmb
    Scenario Outline: Verify transaction streaming for squaremeal negative scenario (invalid mid)

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "SquareMeal" membership card
    Then I perform GET request to verify the "SquareMeal" membershipcard is added & linked successfully in the wallet
    When I send Payment Transaction File with <payment_card_transaction> <mid>
    Then I verify transaction is not streamed and exported

    Examples:
    | payment_card_provider|     mid       |payment_card_transaction |
    |          visa        |  29047530     |visa-auth-streaming       |
    |          visa        |  29047530     |visa-settlement-streaming |
    |          visa        |  29047530     |visa-refund-streaming     |


    Scenario Outline: Verify transaction streaming for squaremeal negative scenario(invalid payment card token)

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "SquareMeal" membership card
    Then I perform GET request to verify the "SquareMeal" membershipcard is added & linked successfully in the wallet
      When I send Payment Transaction File with <payment_card_transaction> <mid>
    Then I verify transaction is not streamed and exported

    Examples:
    | payment_card_provider|     mid       |payment_card_transaction               |
    |          visa        |  29047531     |visa-auth-streaming_invalid_token       |
