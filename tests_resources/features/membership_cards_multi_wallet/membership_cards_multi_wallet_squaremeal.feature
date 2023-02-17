# Created by nehapatil at 17/02/2023
@multi_wallet @multi_wallet_squaremeal @sanity_bmb
Feature: Merchant SquareMeal - Ensure a customer can add membership card in multiple wallet and view each wallet details
  As a customer
  I want to add and auth a membership card in multiple wallets
  So that status of membership card in each wallet is independent

  
    @multi_wallet_add
  Scenario: Multi wallet auth auth SquareMeal
    Given I register with bink service in barclays
    When I perform POST request to add and auth "SquareMeal" membership card with "valid_credentials"
    When I perform POST request to add new payment card to wallet of master type
    And For barclays I perform GET request to verify the SquareMeal membership card is added to the wallet after successful_add
    When For barclays I perform GET request to verify the SquareMeal membership card is added to the wallet after successful_pll
    Then verify the data stored in DB after "Add" journey for "SquareMeal"
    Given I register with bink service in bink
    When I perform POST request to add and auth "SquareMeal" membership card with "valid_credentials"
    When I perform POST request to add existing payment card to wallet of master type
    And For bink I perform GET request to verify the SquareMeal membership card is added to the wallet after successful_add
    When For bink I perform GET request to verify the SquareMeal membership card is added to the wallet after successful_pll
    And For barclays I perform GET request to verify the SquareMeal membership card is added to the wallet after successful_add
    When For barclays I perform GET request to verify the SquareMeal membership card is added to the wallet after successful_pll
    Then verify the data stored in DB after "Add" journey for "SquareMeal"
    And I perform DELETE request to delete all users

  @multi_wallet_balances_transactions
  Scenario: Multi wallet auth auth Balances and Transactions SquareMeal

    Given I register with bink service in bink
    When I perform POST request to add and auth "SquareMeal" membership card with "valid_credentials"
    And For bink I perform GET request to verify the SquareMeal membership card is added to the wallet after successful_add
    Given I register with bink service in barclays
    When I perform POST request to add and auth "SquareMeal" membership card with "valid_credentials"
    And For barclays I perform GET request to verify the SquareMeal membership card is added to the wallet after successful_add
    When For bink I perform GET request to view balance for "authorised" "SquareMeal" membership card
    And For bink I perform GET request to view transactions for "authorised" "SquareMeal" membership card
    Then For bink I perform GET request to view a specific transaction for "authorised" "SquareMeal" membership card
    When For barclays I perform GET request to view balance for "authorised" "SquareMeal" membership card
    And For barclays I perform GET request to view transactions for "authorised" "SquareMeal" membership card
    Then For barclays I perform GET request to view a specific transaction for "authorised" "SquareMeal" membership card
    Then verify the data stored in DB after "Add" journey for "SquareMeal"
    And I perform DELETE request to delete all users

  @multi_wallet_unauth_auth
  Scenario: Multi wallet unauth auth SquareMeal
    Given I register with bink service in bink
    When I perform POST request to add and auth "SquareMeal" membership card with "invalid_credentials"
    When I perform POST request to add new payment card to wallet of master type
    And For bink I perform GET request to verify the SquareMeal membership card is added to the wallet with invalid data
    When For bink I perform GET request to verify the SquareMeal membership card is added to the wallet after failed_pll
    Then verify the data stored in DB after "Add" journey for "SquareMeal"
    Given I register with bink service in barclays
    When I perform POST request to add and auth "SquareMeal" membership card with "valid_credentials"
    When I perform POST request to add existing payment card to wallet of master type
    And For barclays I perform GET request to verify the SquareMeal membership card is added to the wallet after successful_add
    When For barclays I perform GET request to verify the SquareMeal membership card is added to the wallet after successful_pll
    And For bink I perform GET request to verify the SquareMeal membership card is added to the wallet with invalid data
    When For bink I perform GET request to verify the SquareMeal membership card is added to the wallet after failed_pll
    And For bink I perform GET request to view balance for "unauthorised" "SquareMeal" membership card
    And For bink I perform GET request to view transactions for "unauthorised" "SquareMeal" membership card
    When For barclays I perform GET request to view balance for "authorised" "SquareMeal" membership card
    And For barclays I perform GET request to view transactions for "authorised" "SquareMeal" membership card
    Then For barclays I perform GET request to view a specific transaction for "authorised" "SquareMeal" membership card
    And I perform DELETE request to delete all users


  @multi_wallet_auth_unauth_sm
  Scenario: Multi wallet auth unauth SquareMeal
    Given I register with bink service in bink
    When I perform POST request to add and auth "SquareMeal" membership card with "valid_credentials"
    When I perform POST request to add new payment card to wallet of master type
    And For bink I perform GET request to verify the SquareMeal membership card is added to the wallet after successful_add
    When For bink I perform GET request to verify the SquareMeal membership card is added to the wallet after successful_pll
    Then verify the data stored in DB after "Add" journey for "SquareMeal"
    Given I register with bink service in barclays
    When I perform POST request to add and auth "SquareMeal" membership card with "invalid_credentials"
    When I perform POST request to add existing payment card to wallet of master type
    And For barclays I perform GET request to verify the SquareMeal membership card is added to the wallet with invalid data
    When For barclays I perform GET request to verify the SquareMeal membership card is added to the wallet after failed_pll
    And For bink I perform GET request to verify the SquareMeal membership card is added to the wallet after successful_add
    When For bink I perform GET request to verify the SquareMeal membership card is added to the wallet after successful_pll
    And For bink I perform GET request to view balance for "authorised" "SquareMeal" membership card
    And For bink I perform GET request to view transactions for "authorised" "SquareMeal" membership card
#    Then For bink I perform GET request to view a specific transaction for "authorised" "SquareMeal" membership card
    When For barclays I perform GET request to view balance for "unauthorised" "SquareMeal" membership card
    And For barclays I perform GET request to view transactions for "unauthorised" "SquareMeal" membership card
    Then I perform DELETE request to delete all users


  @multi_wallet_unauth_unauth_sm
  Scenario: Multi wallet unauth unauth SquareMeal
    Given I register with bink service in bink
    When I perform POST request to add and auth "SquareMeal" membership card with "invalid_credentials"
    When I perform POST request to add new payment card to wallet of master type
    And For bink I perform GET request to verify the SquareMeal membership card is added to the wallet with invalid data
    When For bink I perform GET request to verify the SquareMeal membership card is added to the wallet after failed_pll
    Given I register with bink service in barclays
    When I perform POST request to add and auth "SquareMeal" membership card with "invalid_credentials"
    When I perform POST request to add existing payment card to wallet of master type
    And For barclays I perform GET request to verify the SquareMeal membership card is added to the wallet with invalid data
    When For barclays I perform GET request to verify the SquareMeal membership card is added to the wallet after failed_pll
    And For bink I perform GET request to verify the SquareMeal membership card is added to the wallet with invalid data
    When For bink I perform GET request to verify the SquareMeal membership card is added to the wallet after failed_pll
    And For bink I perform GET request to view balance for "unauthorised" "SquareMeal" membership card
    And For bink I perform GET request to view transactions for "unauthorised" "SquareMeal" membership card
    When For barclays I perform GET request to view balance for "unauthorised" "SquareMeal" membership card
    And For barclays I perform GET request to view transactions for "unauthorised" "SquareMeal" membership card
    Then I perform DELETE request to delete all users
    

  @multi_wallet_enrol
  Scenario: Multi wallet Join
    Given I register with bink service in bink
    When I perform POST request to successful_enrol membership card for SquareMeal
    And For bink I perform GET request to verify the SquareMeal membership card is added to the wallet after successful_enrol
    Then verify the data stored in DB after "Enrol" journey for "SquareMeal"
    Given I register with bink service in barclays
    When I perform POST request to successful_enrol membership card for SquareMeal
    And For barclays I perform GET request to verify the SquareMeal membership card is added to the wallet after successful_enrol
    Then verify the data stored in DB after "Enrol" journey for "SquareMeal"
    And I perform DELETE request to delete all users


  @identical_joins
  Scenario: merchant fails to identify duplicate join requests
    Given I register with bink service in bink
    When I perform POST request to identical_enrol membership card for SquareMeal
    And For bink I perform GET request to verify the SquareMeal membership card is added to the wallet after successful_enrol
    Then verify the data stored in DB after "join" journey for "SquareMeal"
    Given I register with bink service in barclays
    When I perform POST request to identical_enrol membership card for SquareMeal
    When For barclays I perform GET request to verify the SquareMeal membership card is added to the wallet after identical_enrol
    Then I perform DELETE request to delete all users
    