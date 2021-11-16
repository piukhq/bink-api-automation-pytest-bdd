@transactionMatching
Feature: Merchant Iceland - Ensure a customer can use Bink's Transaction Matching features
  As a customer
  I shopped at a Bink PLL partner that uses transaction matching
  So I can offer a near real time transaction matching service to merchants.

  @transactionMatchingIceland @bink_regression
  Scenario Outline: Verify transaction matching for iceland with payment provider - Mastercard - Auth

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "Iceland" membership card
    Then I perform GET request to verify the "Iceland" membershipcard is added & linked successfully in the wallet
    When I send merchant Tlog file with "<merchant_container> <payment_card_provider> <mid> <cardIdentity> <scheme>" and send to bink
    And I send matching "<payment_card_transaction> <mid>" Authorisation
    Then I verify 1 reward transaction is exported

    Examples:
    | payment_card_provider|merchant_container| mid      | cardIdentity             |payment_card_transaction| scheme |
    |          amex        |scheme/iceland/   |9421802109| Amex                     |amex-settlement         |  AMEX  |
    |          amex        |scheme/iceland/   |9445909831| Amex                     |amex-auth               |   AMEX     |
    |          master      |scheme/iceland/   |22776952  |MasterCard/MasterCard One |master-auth             |  MASTERCARD      |

  @transactionMatchingFatFace
  Scenario Outline: Verify export Csv file for Fatface - mastercard_auth

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "Fatface" membership card
    Then I perform GET request to verify the "Fatface" membershipcard is added & linked successfully in the wallet
    And I send matching "<payment_card_provider> <mid>" Authorisation
    Then I verify 1 reward transaction is exported


    Examples:
    | payment_card_provider|mid        |
   |          master      |  338681531889 |

  @transactionMatchingHarvey-nichols @bink_regression
    Scenario Outline: Verify transaction matching for harvey-nichols with payment provider - Auth

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "HarveyNichols" membership card
    Then I perform GET request to verify the "HarveyNichols" membershipcard is added & linked successfully in the wallet
    When I send merchant Tlog file with "<merchant_container> <payment_card_provider> <mid> <cardIdentity> <scheme>" and send to bink
    And I send matching "<payment_card_transaction> <mid>" Authorisation
    Then I verify 1 reward transaction is exported


    Examples:
    | payment_card_provider|merchant_container       | mid      | cardIdentity             |payment_card_transaction| scheme   |
    |          master      |scheme/harvey-nichols/   |19410201  |MasterCard/MasterCard One |master-auth             |MASTERCARD|
    |          amex        |scheme/harvey-nichols/   |9600360903| Amex                     |amex-auth               | AMEX     |