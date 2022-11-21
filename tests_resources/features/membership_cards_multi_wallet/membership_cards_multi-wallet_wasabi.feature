# Created by nehapatil at 06/10/2022
@multi_wallet @multi_wallet_wasabi
Feature: Merchant Wasabi - Ensure a customer can add membership card in multiple wallet and view each wallet details
  As a customer
  I want to add and auth a membership card in multiple wallets
  So that status of membership card in each wallet is independent

  @multi_wallet_add
  Scenario: Multi wallet auth auth Wasabi
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Wasabi" membership card with "valid_credentials"
    When I perform POST request to add payment card to wallet
    When For barclays I perform GET request to verify the Wasabi membership card is added to the wallet after successful_add
    When For barclays I perform GET request to verify the Wasabi membership card is added to the wallet after successful_pll
    Then verify the data stored in DB after "Add" journey for "Wasabi"
    Given I register with bink service in bink
    When I perform POST request to add and auth "Wasabi" membership card with "valid_credentials"
    When I perform POST request to add payment card to wallet
    And For bink I perform GET request to verify the Wasabi membership card is added to the wallet after successful_add
    When For bink I perform GET request to verify the Wasabi membership card is added to the wallet after successful_pll
    And For barclays I perform GET request to verify the Wasabi membership card is added to the wallet after successful_add
    When For barclays I perform GET request to verify the Wasabi membership card is added to the wallet after successful_pll
    Then verify the data stored in DB after "Add" journey for "Wasabi"
    And I perform DELETE request to delete all users

  @multi_wallet_balances_transactions
  Scenario: Multi wallet auth auth Balances and Transactions_Wasabi

    Given I register with bink service in bink
    When I perform POST request to add and auth "Wasabi" membership card with "valid_credentials"
    And For bink I perform GET request to verify the Wasabi membership card is added to the wallet after successful_add
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Wasabi" membership card with "valid_credentials"
    And For barclays I perform GET request to verify the Wasabi membership card is added to the wallet after successful_add
    When For bink I perform GET request to view balance for "authorised" "Wasabi" membership card
    And For bink I perform GET request to view vouchers for "authorised" "Wasabi" membership card
    And For bink I perform GET request to view transactions for "authorised" "Wasabi" membership card
    Then For bink I perform GET request to view a specific transaction for "authorised" "Wasabi" membership card
    When For barclays I perform GET request to view balance for "authorised" "Wasabi" membership card
    And For barclays I perform GET request to view vouchers for "authorised" "Wasabi" membership card
    And For barclays I perform GET request to view transactions for "authorised" "Wasabi" membership card
    Then For barclays I perform GET request to view a specific transaction for "authorised" "Wasabi" membership card
    Then verify the data stored in DB after "Add" journey for "Wasabi"
    And I perform DELETE request to delete all users

  @multi_wallet_unauth_auth
  Scenario: Multi wallet unauth auth Wasabi
    Given I register with bink service in bink
    When I perform POST request to add and auth "Wasabi" membership card with "invalid_credentials"
    When I perform POST request to add payment card to wallet
    And For bink I perform GET request to verify the Wasabi membership card is added to the wallet with invalid data
    When For bink I perform GET request to verify the Wasabi membership card is added to the wallet after failed_pll
    Then verify the data stored in DB after "Add" journey for "Wasabi"
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Wasabi" membership card with "valid_credentials"
    When I perform POST request to add payment card to wallet
    And For barclays I perform GET request to verify the "Wasabi" membership card is added to the wallet after successful_add
    When For barclays I perform GET request to verify the Wasabi membership card is added to the wallet after successful_pll
    And For bink I perform GET request to verify the "Wasabi" membership card is added to the wallet with invalid data
    When For bink I perform GET request to verify the Wasabi membership card is added to the wallet after successful_pll
    And For bink I perform GET request to view balance for "unauthorised" "Wasabi" membership card
    And For bink I perform GET request to view vouchers for "unauthorised" "Wasabi" membership card
    And For bink I perform GET request to view transactions for "unauthorised" "Wasabi" membership card
    When For barclays I perform GET request to view balance for "authorised" "Wasabi" membership card
    And For barclays I perform GET request to view vouchers for "authorised" "Wasabi" membership card
    And For barclays I perform GET request to view transactions for "authorised" "Wasabi" membership card
    Then For barclays I perform GET request to view a specific transaction for "authorised" "Wasabi" membership card
    And I perform DELETE request to delete all users


    @multi_wallet_auth_unauth
  Scenario: Multi wallet auth unauth Wasabi
    Given I register with bink service in bink
    When I perform POST request to add and auth "Wasabi" membership card with "valid_credentials"
    When I perform POST request to add payment card to wallet
    And For bink I perform GET request to verify the Wasabi membership card is added to the wallet after successful_add
    When For bink I perform GET request to verify the Wasabi membership card is added to the wallet after successful_pll
    Then verify the data stored in DB after "Add" journey for "Wasabi"
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Wasabi" membership card with "invalid_credentials"
    When I perform POST request to add payment card to wallet
    And For barclays I perform GET request to verify the Wasabi membership card is added to the wallet with invalid data
    When For barclays I perform GET request to verify the Wasabi membership card is added to the wallet after successful_pll
    And For bink I perform GET request to verify the Wasabi membership card is added to the wallet after successful_add
    When For bink I perform GET request to verify the Wasabi membership card is added to the wallet after successful_pll
    And For bink I perform GET request to view balance for "authorised" "Wasabi" membership card
    And For bink I perform GET request to view vouchers for "authorised" "Wasabi" membership card
    And For bink I perform GET request to view transactions for "authorised" "Wasabi" membership card
    Then For bink I perform GET request to view a specific transaction for "authorised" "Wasabi" membership card
    When For barclays I perform GET request to view balance for "unauthorised" "Wasabi" membership card
    And For barclays I perform GET request to view vouchers for "unauthorised" "Wasabi" membership card
    And For barclays I perform GET request to view transactions for "unauthorised" "Wasabi" membership card
    Then I perform DELETE request to delete all users


  @multi_wallet_unauth_unauth_wasabi
  Scenario: Multi wallet unauth unauth Wasabi
    Given I register with bink service in bink
    When I perform POST request to add and auth "Wasabi" membership card with "invalid_credentials"
    When I perform POST request to add payment card to wallet
    And For bink I perform GET request to verify the Wasabi membership card is added to the wallet with invalid data
    When For bink I perform GET request to verify the Wasabi membership card is added to the wallet after failed_pll
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Wasabi" membership card with "invalid_credentials"
    When I perform POST request to add payment card to wallet
    And For barclays I perform GET request to verify the Wasabi membership card is added to the wallet with invalid data
    When For barclays I perform GET request to verify the Wasabi membership card is added to the wallet after failed_pll
    And For bink I perform GET request to verify the Wasabi membership card is added to the wallet with invalid data
    When For bink I perform GET request to verify the Wasabi membership card is added to the wallet after failed_pll
    And For bink I perform GET request to view balance for "unauthorised" "Wasabi" membership card
    And For bink I perform GET request to view vouchers for "unauthorised" "Wasabi" membership card
    And For bink I perform GET request to view transactions for "unauthorised" "Wasabi" membership card
    When For barclays I perform GET request to view balance for "unauthorised" "Wasabi" membership card
    And For barclays I perform GET request to view vouchers for "unauthorised" "Wasabi" membership card
    And For barclays I perform GET request to view transactions for "unauthorised" "Wasabi" membership card
    Then I perform DELETE request to delete all users

#...............................................Update Scenarios.......................................................
  #Steps:
  # add & auth loyalty card in wallet 1 & 2 with good credentials
  # PATCH with Invalid auth credentials
  # Get wallet 1 has authorised details. Also balance vouchers and transactions returned
  # Get wallet 2 has unauthorised details .Also balance vouchers and transactions null
  #Note: Assume the PLL will travel across the wallet after trusted channel implementation.

  @multi_wallet_update_1
  Scenario: Wallet 1& 2 have authorised cards, PATCH with invalid cred in wallet 2
          # add & auth loyalty card in wallet 1
    Given I register with bink service in bink
    When I perform POST request to add and auth "Wasabi" membership card with "valid_credentials"
    And For bink I perform GET request to verify the Wasabi membership card is added to the wallet after successful_add
    And I perform POST request to add payment card to wallet
    And For bink I perform GET request to verify the Wasabi membership card is added to the wallet after successful_pll
          # add & auth loyalty card in wallet 2
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Wasabi" membership card with "valid_credentials"
    And For barclays I perform GET request to verify the Wasabi membership card is added to the wallet after successful_add
    And I perform POST request to add payment card to wallet
    And For barclays I perform GET request to verify the Wasabi membership card is added to the wallet after successful_pll
         # Patch with Invalid auth credentials  in wallet2 and verify bal, vouchers,txns in wallet2
    And For barclays I perform PATCH request to update the Wasabi membership card with "invalid_credentials"
    And For barclays I perform GET request to verify the Wasabi membership card is added to the wallet with invalid data
    When For barclays I perform GET request to verify the Wasabi membership card is added to the wallet after successful_pll
    And For barclays I perform GET request to view balance for "unauthorised" "Wasabi" membership card
    And For barclays I perform GET request to view vouchers for "unauthorised" "Wasabi" membership card
    And For barclays I perform GET request to view transactions for "unauthorised" "Wasabi" membership card
     # Switch to wallet 1 to make sure the Status of Wallet_2's LC1 does not impact the Status of LC1 in wallet_1
    When For bink I perform GET request to view balance for "authorised" "Wasabi" membership card
    And For bink I perform GET request to view vouchers for "authorised" "Wasabi" membership card
    And For bink I perform GET request to view transactions for "authorised" "Wasabi" membership card
    Then For bink I perform GET request to view a specific transaction for "authorised" "Wasabi" membership card
    And I perform DELETE request to delete all users


    @multi_wallet_update_2
  Scenario: Wallet 1& 2 have authorised cards, PATCH with invalid cred in wallet 1
          # add & auth loyalty card in wallet 1
    Given I register with bink service in bink
    When I perform POST request to add and auth "Wasabi" membership card with "valid_credentials"
    And For bink I perform GET request to verify the Wasabi membership card is added to the wallet after successful_add
    And I perform POST request to add payment card to wallet
    And For bink I perform GET request to verify the Wasabi membership card is added to the wallet after successful_pll
          # add & auth loyalty card in wallet 2
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Wasabi" membership card with "valid_credentials"
    And For barclays I perform GET request to verify the Wasabi membership card is added to the wallet after successful_add
    And I perform POST request to add payment card to wallet
    And For barclays I perform GET request to verify the Wasabi membership card is added to the wallet after successful_pll
         # Patch with Invalid auth credentials  in wallet1 and verify bal, vouchers,txns in wallet2
    And For bink I perform PATCH request to update the Wasabi membership card with "invalid_credentials"
    And For bink I perform GET request to verify the Wasabi membership card is added to the wallet with invalid data
    When For bink I perform GET request to verify the Wasabi membership card is added to the wallet after successful_pll
    And For bink I perform GET request to view balance for "unauthorised" "Wasabi" membership card
    And For bink I perform GET request to view vouchers for "unauthorised" "Wasabi" membership card
    And For bink I perform GET request to view transactions for "unauthorised" "Wasabi" membership card
     # Switch to wallet 2 to make sure the Status of Wallet_2's LC1 does not impact the Status of LC1 in wallet_1
    When For barclays I perform GET request to view balance for "authorised" "Wasabi" membership card
    And For barclays I perform GET request to view vouchers for "authorised" "Wasabi" membership card
    And For barclays I perform GET request to view transactions for "authorised" "Wasabi" membership card
    Then For barclays I perform GET request to view a specific transaction for "authorised" "Wasabi" membership card
    And I perform DELETE request to delete all users







