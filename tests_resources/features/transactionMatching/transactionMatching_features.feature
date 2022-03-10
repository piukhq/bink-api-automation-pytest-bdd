@transactionMatching
Feature: Merchant Iceland - Ensure a customer can use Bink's Transaction Matching features
  As a customer
  I shopped at a Bink PLL partner that uses transaction matching
  So I can offer a near real time transaction matching service to merchants.

  @transactionMatchingIceland @bink_regression @sanity
  Scenario Outline: Verify transaction matching for iceland with payment provider

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "Iceland" membership card
    Then I perform GET request to verify the "Iceland" membershipcard is added & linked successfully in the wallet
    When I send merchant Tlog file with "<merchant_container>" "<payment_card_provider>" "<mid>" "<cardIdentity>" "<scheme>" and send to bink
    And I send matching "<payment_card_transaction>" "<mid>" Authorisation
    Then I verify 1 reward transaction is exported

    Examples:
    | payment_card_provider|merchant_container| mid      | cardIdentity             |payment_card_transaction| scheme |
    |          amex        |scheme/iceland/   |9421802109| Amex                     |amex-settlement         |  AMEX  |
    |          amex        |scheme/iceland/   |9445909831| Amex                     |amex-auth               |   AMEX     |
    |          master      |scheme/iceland/   |22776952  |MasterCard/MasterCard One |master-auth             |  MASTERCARD|
    |          visa        |scheme/iceland/   |10209723  | Visa                     |visa-auth               |   VISA     |


 @transactionMatchingIceland @bink_regression @sanity
  Scenario Outline: Verify transaction matching for iceland with payment provider but invalid mid

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "Iceland" membership card
    Then I perform GET request to verify the "Iceland" membershipcard is added & linked successfully in the wallet
    When I send merchant Tlog file with "<merchant_container>" "<payment_card_provider>" "<mid>" "<cardIdentity>" "<scheme>" and send to bink
    And I send matching "<payment_card_transaction>" "<mid>" Authorisation
    Then I verify transaction is not matched and not exported

    Examples:
    | payment_card_provider|merchant_container| mid      | cardIdentity             |payment_card_transaction| scheme |
    |          amex        |scheme/iceland/   |7821802109| Amex                     |amex-settlement         |  AMEX  |
    |          amex        |scheme/iceland/   |8445909831| Amex                     |amex-auth               |   AMEX     |
    |          master      |scheme/iceland/   |72776952  |MasterCard/MasterCard One |master-auth             |  MASTERCARD|
    |          visa        |scheme/iceland/   |80209723  | Visa                     |visa-auth               |   VISA     |

  @transactionMatchingFatFace
  Scenario Outline: Verify export Csv file for Fatface - mastercard_auth

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "Fatface" membership card
    Then I perform GET request to verify the "Fatface" membershipcard is added & linked successfully in the wallet
    And I send matching "<payment_card_provider>" "<mid>" Authorisation
    Then I verify 1 reward transaction is exported


    Examples:
    | payment_card_provider|mid        |
   |          master      |  338681531889 |

  @transactionMatchingHarvey-nichols @bink_regression
    Scenario Outline: Verify transaction matching for harvey-nichols with payment provider

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "HarveyNichols" membership card
    Then I perform GET request to verify the "HarveyNichols" membershipcard is added & linked successfully in the wallet
    When I send merchant Tlog file with "<merchant_container>" "<payment_card_provider>" "<mid>" "<cardIdentity>" "<scheme>" and send to bink
    And I send matching "<payment_card_transaction>" "<mid>" Authorisation
    Then I verify 1 reward transaction is exported


    Examples:
    | payment_card_provider|merchant_container       | mid      | cardIdentity             |payment_card_transaction| scheme   |
    |          master      |scheme/harvey-nichols/   |19410201  |MasterCard/MasterCard One |master-auth             |MASTERCARD|
    |          amex        |scheme/harvey-nichols/   |9600360903| Amex                     |amex-auth               | AMEX     |


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
