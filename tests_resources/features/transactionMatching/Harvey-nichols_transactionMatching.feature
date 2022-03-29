@transactionMatching
Feature: Merchant Harvey-nichols - Ensure a customer can use Bink's Transaction Matching features
  As a customer
  I shopped at a Bink PLL partner that uses transaction matching
  So I can offer a near real time transaction matching service to merchants.

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
