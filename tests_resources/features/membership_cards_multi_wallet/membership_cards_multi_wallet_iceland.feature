# Created by nehapatil at 18/10/2022
@multi_wallet @multi_wallet_iceland
Feature: Merchant Iceland - Ensure a customer can add membership card in multiple wallet and view each wallet details
  As a customer
  I want to add and auth a membership card in multiple wallets
  So that status of membership card in each wallet is independent

  
    @multi_wallet_add
  Scenario: Multi wallet auth auth Iceland
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Iceland" membership card with "valid_credentials"
    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet after successful_add
    Then verify the data stored in DB after "Add" journey for "Iceland"
    Given I register with bink service in bink
    When I perform POST request to add and auth "Iceland" membership card with "valid_credentials"
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_add
    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet after successful_add
    Then verify the data stored in DB after "Add" journey for "Iceland"
    And I perform DELETE request to delete all users

  @multi_wallet_balances_transactions
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

  @multi_wallet_unauth_auth
  Scenario: Multi wallet unauth auth Iceland
    Given I register with bink service in bink
    When I perform POST request to add and auth "Iceland" membership card with "invalid_credentials"
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
    Then verify the data stored in DB after "Add" journey for "Iceland"
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Iceland" membership card with "valid_credentials"
    And For barclays I perform GET request to verify the "Iceland" membership card is added to the wallet after successful_add
    And For bink I perform GET request to verify the "Iceland" membership card is added to the wallet with invalid data
    And For bink I perform GET request to view balance for "unauthorised" "Iceland" membership card
    And For bink I perform GET request to view transactions for "unauthorised" "Iceland" membership card
    When For barclays I perform GET request to view balance for "authorised" "Iceland" membership card
    And For barclays I perform GET request to view transactions for "authorised" "Iceland" membership card
    Then For barclays I perform GET request to view a specific transaction for "authorised" "Iceland" membership card
    And I perform DELETE request to delete all users


    @multi_wallet_auth_unauth_iceland
  Scenario: Multi wallet auth unauth Iceland
    Given I register with bink service in bink
    When I perform POST request to add and auth "Iceland" membership card with "valid_credentials"
    And For bink I perform GET request to verify the "Iceland" membership card is added to the wallet after successful_add
    Then verify the data stored in DB after "Add" journey for "Iceland"
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Iceland" membership card with "invalid_credentials"
    And For barclays I perform GET request to verify the "Iceland" membership card is added to the wallet with invalid data
    And For bink I perform GET request to verify the "Iceland" membership card is added to the wallet after successful_add
    And For bink I perform GET request to view balance for "authorised" "Iceland" membership card
    And For bink I perform GET request to view transactions for "authorised" "Iceland" membership card
    Then For bink I perform GET request to view a specific transaction for "authorised" "Iceland" membership card
    When For barclays I perform GET request to view balance for "unauthorised" "Iceland" membership card
    And For barclays I perform GET request to view transactions for "unauthorised" "Iceland" membership card
    Then I perform DELETE request to delete all users


  @multi_wallet_unauth_unauth_iceland
  Scenario: Multi wallet unauth unauth Iceland
    Given I register with bink service in bink
    When I perform POST request to add and auth "Iceland" membership card with "invalid_credentials"
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
    Given I register with bink service in barclays
    When I perform POST request to add and auth "Iceland" membership card with "invalid_credentials"
    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
    And For bink I perform GET request to view balance for "unauthorised" "Iceland" membership card
    And For bink I perform GET request to view transactions for "unauthorised" "Iceland" membership card
    When For barclays I perform GET request to view balance for "unauthorised" "Iceland" membership card
    And For barclays I perform GET request to view transactions for "unauthorised" "Iceland" membership card
    Then I perform DELETE request to delete all users


  @multi_wallet_enrol
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

#   @same_wallet_register_journey
  @already_register
  Scenario: Add already registered card in same wallet
    Given I register with bink service in bink
    When I perform POST request to add "Iceland" membership card for "successful_register"
    And I perform PATCH request to create a "Iceland" ghost membership account with enrol credentials
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_register
    And I perform POST request to add "Iceland" membership card for "already_registered"
    Then I perform DELETE request to delete all users

###Need to know how to retrieve last name and post code of registered card
#  @multi_wallet_register_journey
#  Scenario: Multi wallet add and auth already registered card
#    Given I register with bink service in bink
#    When I perform POST request to add "Iceland" membership card for "successful_register"
#    And I perform PATCH request to create a "Iceland" ghost membership account with enrol credentials
#    And For bink I perform GET request to verify the Iceland membership card is added to the wallet after successful_enrol
#    Given I register with bink service in barclays
#    When I perform POST request to add "Iceland" membership card for "already_registered"
#    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet after successful_add
#    And For bink I perform GET request to verify the Iceland membership card is added to the wallet
#    Then I perform DELETE request to delete all users
#
## Need to set up test data in API reflector.
#  @multi_wallet_failed_register
#  Scenario: Multi wallet add already registered card which is failed
#    Given I register with bink service in bink
#    When I perform POST request to add "Iceland" membership card for "failed_register"
#    And I perform PATCH request to create "Iceland" failed register
#    And For bink I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
#    Given I register with bink service in barclays
#    When I perform POST request to add "Iceland" membership card for "already_registered"
#    And I perform PATCH request to create a "Iceland" ghost membership account with enrol credentials
#    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet after successful_register
#    And For bink I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
#    Then I perform DELETE request to delete all users

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