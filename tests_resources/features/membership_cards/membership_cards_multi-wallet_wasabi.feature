# Created by nehapatil at 06/10/2022
@multi_wallet @multi_wallet_wasabi
Feature: Merchant Wasabi - Ensure a customer can add membership card in multiple wallet and view each wallet details
  As a customer
  I want to add and auth a membership card in multiple wallets
  So that status of membership card in each wallet is independent

  @multi_wallet_add @sanity
  Scenario: Multi-wallet auth-auth Wasabi
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Wasabi" membership card
    And For barclays I perform GET request to verify the Wasabi membership card is added to the wallet
    Then verify the data stored in DB after "Add" journey for "Wasabi"
    Given I register with bink service in bink
    When I perform POST request to add and auth "Wasabi" membership card
    And For bink I perform GET request to verify the Wasabi membership card is added to the wallet
    And For barclays I perform GET request to verify the Wasabi membership card is added to the wallet
    Then verify the data stored in DB after "Add" journey for "Wasabi"
    And I perform DELETE request to delete all users

#  @multi_wallet_balances_transactions
#  Scenario: Multi-wallet auth-auth Balances and Transactions_Wasabi
#
#    Given I register with bink service in bink
#    When I perform POST request to add and auth "Wasabi" membership card
#    And For bink I perform GET request to verify the Wasabi membership card is added to the wallet
#    Given I register with bink service in barclays
#    When I perform POST request to add and auth "Wasabi" membership card
#    And For barclays I perform GET request to verify the Wasabi membership card is added to the wallet
#    When For bink I perform GET request to view balance for "authorised" "Wasabi" membership card
#    And For bink I perform GET request to view vouchers for "authorised" "Wasabi" membership card
#    And For bink I perform GET request to view transactions for "authorised" "Wasabi" membership card
#    Then For bink I perform GET request to view a specific transaction for "authorised" "Wasabi" membership card
#    When For barclays I perform GET request to view balance for "authorised" "Wasabi" membership card
#    And For barclays I perform GET request to view vouchers for "authorised" "Wasabi" membership card
#    And For barclays I perform GET request to view transactions for "authorised" "Wasabi" membership card
#    Then For barclays I perform GET request to view a specific transaction for "authorised" "Wasabi" membership card
#    Then verify the data stored in DB after "Add" journey for "Wasabi"
#    And I perform DELETE request to delete all users
#
#  @multi_wallet_unauth_auth
#  Scenario: Multi-wallet unauth-auth Wasabi
#    Given I register with bink service in bink
#    When I perform POST request to add "Wasabi" membership card with "invalid_data"
#    And For bink I perform GET request to verify the Wasabi membership card is added to the wallet with invalid data
#    Then verify the data stored in DB after "Add" journey for "Wasabi"
#    Given I register with bink service in barclays
#    When I perform POST request to add and auth "Wasabi" membership card
#    And For barclays I perform GET request to verify the "Wasabi" membership card is added to the wallet
#    And For bink I perform GET request to verify the "Wasabi" membership card is added to the wallet with invalid data
#    And For bink I perform GET request to view balance for "unauthorised" "Wasabi" membership card
#    And For bink I perform GET request to view vouchers for "unauthorised" "Wasabi" membership card
#    And For bink I perform GET request to view transactions for "unauthorised" "Wasabi" membership card
#    Then For bink I perform GET request to view a specific transaction for "unauthorised" "Wasabi" membership card
#    When For barclays I perform GET request to view balance for "authorised" "Wasabi" membership card
#    And For barclays I perform GET request to view vouchers for "authorised" "Wasabi" membership card
#    And For barclays I perform GET request to view transactions for "authorised" "Wasabi" membership card
#    Then For barclays I perform GET request to view a specific transaction for "authorised" "Wasabi" membership card
#    And I perform DELETE request to delete all users
#
#
#    @multi_wallet_auth_unauth
#  Scenario: Multi-wallet auth-unauth Wasabi
#    Given I register with bink service in bink
#    When I perform POST request to add and auth "Wasabi" membership card
#    And For bink I perform GET request to verify the "Wasabi" membership card is added to the wallet
#    Then verify the data stored in DB after "Add" journey for "Wasabi"
#    Given I register with bink service in barclays
#    When I perform POST request to add "Wasabi" membership card with "invalid_data"
#    And For barclays I perform GET request to verify the "Wasabi" membership card is added to the wallet with invalid data
#    And For bink I perform GET request to verify the "Wasabi" membership card is added to the wallet
#    And For bink I perform GET request to view balance for "authorised" "Wasabi" membership card
#    And For bink I perform GET request to view vouchers for "authorised" "Wasabi" membership card
#    And For bink I perform GET request to view transactions for "authorised" "Wasabi" membership card
#    Then For bink I perform GET request to view a specific transaction for "authorised" "Wasabi" membership card
#    When For barclays I perform GET request to view balance for "unauthorised" "Wasabi" membership card
#    And For barclays I perform GET request to view vouchers for "unauthorised" "Wasabi" membership card
#    And For barclays I perform GET request to view transactions for "unauthorised" "Wasabi" membership card
#    Then For barclays I perform GET request to view a specific transaction for "unauthorised" "Wasabi" membership card
#    And I perform DELETE request to delete all users
#
#
#      @multi_wallet_unauth_unauth
#  Scenario: Multi-wallet unauth-unauth Wasabi
#    Given I register with bink service in bink
#    When I perform POST request to add "Wasabi" membership card with "invalid_data"
#    And For bink I perform GET request to verify the "Wasabi" membership card is added to the wallet with invalid data
#    Given I register with bink service in barclays
#    When I perform POST request to add "Wasabi" membership card with "invalid_data"
#    And For barclays I perform GET request to verify the "Wasabi" membership card is added to the wallet with invalid data
#    And For bink I perform GET request to verify the "Wasabi" membership card is added to the wallet
#    And For bink I perform GET request to view balance for "authorised" "Wasabi" membership card
#    And For bink I perform GET request to view vouchers for "authorised" "Wasabi" membership card
#    And For bink I perform GET request to view transactions for "authorised" "Wasabi" membership card
#    Then For bink I perform GET request to view a specific transaction for "authorised" "Wasabi" membership card
#    When For barclays I perform GET request to view balance for "unauthorised" "Wasabi" membership card
#    And For barclays I perform GET request to view vouchers for "unauthorised" "Wasabi" membership card
#    And For barclays I perform GET request to view transactions for "unauthorised" "Wasabi" membership card
#    Then For barclays I perform GET request to view a specific transaction for "unauthorised" "Wasabi" membership card
#    And I perform DELETE request to delete all users

#  @mw_add_and_link
#  Scenario: Multi-wallet ADD & LINK Journey_Wasabi
#    Given I am a Bink user
#    And I perform POST request to add payment card to wallet
#    And I perform the GET request to verify the payment card has been added successfully
#    When I perform POST request to add & auto link an existing "Wasabi" membership card
#    And I perform GET request to verify the "Wasabi" membership card is added & linked successfully in the wallet
#    And I perform GET request to view balance for recently added "Wasabi" membership card
#    Then verify the data stored in DB after "Add" journey for "Wasabi"
#    Then I perform DELETE request to delete the "Wasabi" membership card
#    And I perform DELETE request to delete the payment card
#
#
#  @mw_enrol
#  Scenario: Join Journey_Wasabi
#
#    Given I register with bink service as a new customer
#    When I perform POST request to create a "Wasabi" membership account with enrol credentials
#    And I perform GET request to verify the "Wasabi" membership account is created
#    Then verify the data stored in DB after "Enrol" journey for "Wasabi"
#    Then I perform DELETE request to delete the "Wasabi" membership card
#    And I perform DELETE request to delete the customer
#
#
#  @enrol_put @bink_regression @bmb_regression
#  Scenario: Join Journey_PUT_Wasabi
#
#    Given I register with bink service as a new customer
#    When I perform POST request to create a "Wasabi" membership account with "invalid" enrol credentials
#    And I perform GET request to verify the "Wasabi" membership account is created with invalid data
#    And I perform PUT request to replace information of the enrolled "Wasabi" membership card
#    And I perform GET request to verify the enrolled "Wasabi" membership card details got replaced after a successful PUT
#    Then verify the data stored in DB after "Enrol" journey for "Wasabi"
#    Then I perform DELETE request to delete the "Wasabi" membership card
#    And I perform DELETE request to delete the customer
#
#  @enrol_add
#  Scenario: Verify join wasabi then delete membership_card from the wallet and Add membershipcard into the wallet again with enrol data
#
#    Given I register with bink service as a new customer
#    When I perform POST request to create a "Wasabi" membership account with enrol credentials
#    And I perform GET request to verify the "Wasabi" membership account is created
#    Then I perform DELETE request to delete the "Wasabi" membership card
#    When I perform POST request to add "Wasabi" membership card after enrol deleted
#    And I perform GET request to verify the "Wasabi" membership card is added to the wallet
#    Then verify the data stored in DB after "Enrol" journey for "Wasabi"
#    And I perform DELETE request to delete the customer



