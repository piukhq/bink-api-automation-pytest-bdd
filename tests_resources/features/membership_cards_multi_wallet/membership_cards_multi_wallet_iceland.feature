# Created by nehapatil at 18/10/2022
@multi_wallet @multi_wallet_iceland
Feature: Merchant Iceland - Ensure a customer can add membership card in multiple wallet and view each wallet details
  As a customer
  I want to add and auth a membership card in multiple wallets
  So that status of membership card in each wallet is independent

  
    @multi_wallet_add @sanity @testfeb
  Scenario: Multi wallet auth auth Iceland
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Iceland" membership card with "valid_credentials"
    When I perform POST request to add payment card to wallet
    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet after successful_add
    When For barclays I perform GET request to verify the Iceland membership card is added to the wallet after successful_pll
    Then verify the data stored in DB after "Add" journey for "Iceland"
    Given I register with bink service in bink
    When I perform POST request to add and auth "Iceland" membership card with "valid_credentials"
    When I perform POST request to add payment card to wallet
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_add
    When For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_pll
    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet after successful_add
    When For barclays I perform GET request to verify the Iceland membership card is added to the wallet after successful_pll
    Then verify the data stored in DB after "Add" journey for "Iceland"
    And I perform DELETE request to delete all users

  @multi_wallet_balances_transactions @sanity @testfeb
  Scenario: Multi wallet auth auth Balances and Transactions Iceland

    Given I register with bink service in bink
    When I perform POST request to add and auth "Iceland" membership card with "valid_credentials"
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_add
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Iceland" membership card with "valid_credentials"
    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet after successful_add
    When For bink I perform GET request to view balance for "authorised" "Iceland" membership card
    And For bink I perform GET request to view transactions for "authorised" "Iceland" membership card
    Then For bink I perform GET request to view a specific transaction for "authorised" "Iceland" membership card
    When For barclays I perform GET request to view balance for "authorised" "Iceland" membership card
    And For barclays I perform GET request to view transactions for "authorised" "Iceland" membership card
    Then For barclays I perform GET request to view a specific transaction for "authorised" "Iceland" membership card
    Then verify the data stored in DB after "Add" journey for "Iceland"
    And I perform DELETE request to delete all users

  @multi_wallet_unauth_auth @sanity @testfeb
  Scenario: Multi wallet unauth auth Iceland
    Given I register with bink service in bink
    When I perform POST request to add and auth "Iceland" membership card with "invalid_credentials"
    When I perform POST request to add payment card to wallet
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
    When For bink I perform GET request to verify the Iceland membership card is added to the wallet after failed_pll
    Then verify the data stored in DB after "Add" journey for "Iceland"
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Iceland" membership card with "valid_credentials"
    When I perform POST request to add payment card to wallet
    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet after successful_add
    When For barclays I perform GET request to verify the Iceland membership card is added to the wallet after successful_pll
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
    When For bink I perform GET request to verify the Iceland membership card is added to the wallet after failed_pll
    And For bink I perform GET request to view balance for "unauthorised" "Iceland" membership card
    And For bink I perform GET request to view transactions for "unauthorised" "Iceland" membership card
    When For barclays I perform GET request to view balance for "authorised" "Iceland" membership card
    And For barclays I perform GET request to view transactions for "authorised" "Iceland" membership card
    Then For barclays I perform GET request to view a specific transaction for "authorised" "Iceland" membership card
    And I perform DELETE request to delete all users

#Need to change test data for below scenario- Data created by CP2
    @multi_wallet_auth_unauth_iceland
  Scenario: Multi wallet auth unauth Iceland
    Given I register with bink service in bink
    When I perform POST request to add and auth "Iceland" membership card with "valid_credentials"
    When I perform POST request to add payment card to wallet
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_add
    When For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_pll
    Then verify the data stored in DB after "Add" journey for "Iceland"
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Iceland" membership card with "invalid_credentials"
    When I perform POST request to add payment card to wallet
    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
    When For barclays I perform GET request to verify the Iceland membership card is added to the wallet after failed_pll
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_add
    When For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_pll
    And For bink I perform GET request to view balance for "authorised" "Iceland" membership card
    And For bink I perform GET request to view transactions for "authorised" "Iceland" membership card
    Then For bink I perform GET request to view a specific transaction for "authorised" "Iceland" membership card
    When For barclays I perform GET request to view balance for "unauthorised" "Iceland" membership card
    And For barclays I perform GET request to view transactions for "unauthorised" "Iceland" membership card
    Then I perform DELETE request to delete all users

#Need to change test data for below scenario- Data created by CP2
  @multi_wallet_unauth_unauth_iceland
  Scenario: Multi wallet unauth unauth Iceland
    Given I register with bink service in bink
    When I perform POST request to add and auth "Iceland" membership card with "invalid_credentials"
    When I perform POST request to add payment card to wallet
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
    When For bink I perform GET request to verify the Iceland membership card is added to the wallet after failed_pll
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Iceland" membership card with "invalid_credentials"
    When I perform POST request to add payment card to wallet
    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
    When For barclays I perform GET request to verify the Iceland membership card is added to the wallet after failed_pll
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
    When For bink I perform GET request to verify the Iceland membership card is added to the wallet after failed_pll
    And For bink I perform GET request to view balance for "unauthorised" "Iceland" membership card
    And For bink I perform GET request to view transactions for "unauthorised" "Iceland" membership card
    When For barclays I perform GET request to view balance for "unauthorised" "Iceland" membership card
    And For barclays I perform GET request to view transactions for "unauthorised" "Iceland" membership card
    Then I perform DELETE request to delete all users


  @multi_wallet_enrol @sanity @testfeb
  Scenario: Multi wallet Join
    Given I register with bink service in bink
    When I perform POST request to successful_enrol membership card for Iceland
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_enrol
    Then verify the data stored in DB after "Enrol" journey for "Iceland"
    Given I register with bink service in barclays
    When I perform POST request to successful_enrol membership card for Iceland
    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet after successful_enrol
    Then verify the data stored in DB after "Enrol" journey for "Iceland"
    And I perform DELETE request to delete all users

#   same_wallet_register_journey
#  ghost card journey for Iceland
  @already_register
  Scenario: Add already registered card in same wallet
    Given I register with bink service in bink
    When I perform POST request to add "Iceland" membership card for "successful_register"
    And I perform PATCH request to create a "Iceland" ghost membership account with enrol credentials
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_register
    And I perform POST request to add "Iceland" membership card for "already_registered"
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_register
    Then I perform DELETE request to delete all users

# # On 2nd post, status is 200, membership_state is failed (should it be unauth like 1ns post) confirm expected.
  @multi_wallet_failed_register
  Scenario: Multi wallet add then register already registered card which is failed
    Given I register with bink service in bink
    When I perform POST request to add "Iceland" membership card for "failed_register"
    And I perform PATCH request to create "Iceland" "failed_register"
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
    Given I register with bink service in barclays
    When I perform POST request to add "Iceland" membership card for "failed_register"
    And I perform PATCH request to create "Iceland" "failed_register"
    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
    Then I perform DELETE request to delete all users

   @identical_joins
  Scenario: merchant fails to identify duplicate join requests
    Given I register with bink service in bink
    When I perform POST request to identical_enrol membership card for Iceland
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_enrol
    Then verify the data stored in DB after "join" journey for "Iceland"
    Given I register with bink service in barclays
    When I perform POST request to identical_enrol membership card for Iceland
    When For barclays I perform GET request to verify the Iceland membership card is added to the wallet after identical_enrol
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
    When I perform POST request to add and auth "Iceland" membership card with "valid_credentials"
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_add
    And I perform POST request to add payment card to wallet
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_pll
          # add & auth loyalty card in wallet 2
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Iceland" membership card with "valid_credentials"
    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet after successful_add
    And I perform POST request to add payment card to wallet
    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet after successful_pll
         # Patch with Invalid auth credentials  in wallet2 and verify bal, vouchers,txns in wallet2
    And For barclays I perform PATCH request to update the Iceland membership card with "invalid_credentials"
    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
    When For barclays I perform GET request to verify the Iceland membership card is added to the wallet after successful_pll
    And For barclays I perform GET request to view balance for "unauthorised" "Iceland" membership card
    And For barclays I perform GET request to view vouchers for "unauthorised" "Iceland" membership card
    And For barclays I perform GET request to view transactions for "unauthorised" "Iceland" membership card
     # Switch to wallet 1 to make sure the Status of Wallet_2's LC1 does not impact the Status of LC1 in wallet_1
    When For bink I perform GET request to view balance for "authorised" "Iceland" membership card
    And For bink I perform GET request to view vouchers for "authorised" "Iceland" membership card
    And For bink I perform GET request to view transactions for "authorised" "Iceland" membership card
    Then For bink I perform GET request to view a specific transaction for "authorised" "Iceland" membership card
    And I perform DELETE request to delete all users


    @multi_wallet_update_2
  Scenario: Wallet 1& 2 have authorised cards, PATCH with invalid cred in wallet 1
          # add & auth loyalty card in wallet 1
    Given I register with bink service in bink
    When I perform POST request to add and auth "Iceland" membership card with "valid_credentials"
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_add
    And I perform POST request to add payment card to wallet
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_pll
          # add & auth loyalty card in wallet 2
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Iceland" membership card with "valid_credentials"
    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet after successful_add
    And I perform POST request to add payment card to wallet
    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet after successful_pll
         # Patch with Invalid auth credentials  in wallet1 and verify bal, vouchers,txns in wallet2
    And For bink I perform PATCH request to update the Iceland membership card with "invalid_credentials"
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
    When For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_pll
    And For bink I perform GET request to view balance for "unauthorised" "Iceland" membership card
    And For bink I perform GET request to view vouchers for "unauthorised" "Iceland" membership card
    And For bink I perform GET request to view transactions for "unauthorised" "Iceland" membership card
     # Switch to wallet 2 to make sure the Status of Wallet_2's LC1 does not impact the Status of LC1 in wallet_1
    When For barclays I perform GET request to view balance for "authorised" "Iceland" membership card
    And For barclays I perform GET request to view vouchers for "authorised" "Iceland" membership card
    And For barclays I perform GET request to view transactions for "authorised" "Iceland" membership card
    Then For barclays I perform GET request to view a specific transaction for "authorised" "Iceland" membership card
    And I perform DELETE request to delete all users