@transactionMatching
Feature: Merchant FatFace - Ensure a customer can use Bink's Transaction Matching features
  As a customer
  I shopped at a Bink PLL partner that uses transaction matching
  So I can offer a near real time transaction matching service to merchants.

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
