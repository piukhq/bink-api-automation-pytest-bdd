@transactionMatching @tm_squaremeal
Feature: Merchant Harvey-nichols - Ensure a customer can use Bink's Transaction Matching features
  As a customer
  I shopped at a Bink PLL partner that uses transaction matching
  So I can offer a near real time transaction matching service to merchants.

  @transactionMatchingSquareMeal @bink_regression @sanity
    Scenario Outline: Verify transaction streaming for squaremeal

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "SquareMeal" membership card
    Then I perform GET request to verify the "SquareMeal" membershipcard is added & linked successfully in the wallet
    When I send matching "<payment_card_transaction>" "<mid>" Authorisation
    Then I verify transaction is spotted and exported <feed_type>


    Examples:
    | payment_card_provider|     mid       |payment_card_transaction | feed_type |
    |          visa        |  29047531     |visa-auth-spotting       | AUTH      |
    |          visa        |  29047531     |visa-settlement-spotting | SETTLED   |
    |          visa        |  29047531     |visa-refund-spotting     | REFUND    |

  @transactionMatchingSquareMeal @bink_regression @sanity
    Scenario Outline: Verify transaction streaming for squaremeal negative scenario(invalid mid)

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "SquareMeal" membership card
    Then I perform GET request to verify the "SquareMeal" membershipcard is added & linked successfully in the wallet
    When I send matching "<payment_card_transaction>" "<mid>" Authorisation
    Then I verify transaction is not spotted and exported <feed_type>

    Examples:
    | payment_card_provider|     mid       |payment_card_transaction | feed_type |
    |          visa        |  29047530     |visa-auth-spotting       | AUTH      |
    |          visa        |  29047530     |visa-settlement-spotting | SETTLED   |
    |          visa        |  29047530     |visa-refund-spotting     | REFUND    |

  @transactionMatchingSquareMeal @bink_regression @sanity
    Scenario Outline: Verify transaction streaming for squaremeal negative scenario(invalid payment card token)

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "SquareMeal" membership card
    Then I perform GET request to verify the "SquareMeal" membershipcard is added & linked successfully in the wallet
    When I send matching "<payment_card_transaction>" "<mid>" Authorisation
    Then I verify transaction is not spotted and exported <feed_type>

    Examples:
    | payment_card_provider|     mid       |payment_card_transaction               | feed_type |
    |          visa        |  29047531     |visa-auth-spotting_invalid_token       | AUTH      |
