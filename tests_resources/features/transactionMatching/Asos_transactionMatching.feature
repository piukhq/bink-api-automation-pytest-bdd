@transactionMatching
Feature: Merchant ASOS - Ensure a customer can use Bink's Transaction Matching features
  As a customer
  I shopped at a Bink PLL partner that uses transaction matching
  So I can offer a near real time transaction matching service to merchants.

  @transactionMatchingAsos @bink_regression @sanity
    Scenario Outline: Verify transaction streaming for Asos

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "Asos" membership card
    Then I perform GET request to verify the "Asos" membershipcard is added & linked successfully in the wallet
    When I send matching "<payment_card_transaction>" "<mid>" Authorisation
    Then I verify transaction is spotted and exported


    Examples:
    | payment_card_provider|     mid       |payment_card_transaction |
    |          visa        |  9999990001   |visa-auth-spotting       |
    |          visa        |  9999990001   |visa-settlement-spotting |
    |          visa        |  9999990001   |visa-refund-spotting     |