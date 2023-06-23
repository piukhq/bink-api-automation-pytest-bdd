# Created by rupalpatel at 23/06/2023
@user_join_loyalty @events @sanity
Feature: Verify event for join loyalty card
  As a DM Administrator
  I want to see an event logged when a user joined scheme
  so that this Business Event can be written to ClickHouse for validation

  @user_join_event
  Scenario: Verify join journey events for single wallet
    Given I register with bink service in bink

    When I perform POST request to create a "TheWorks" membershipcard account with enrol credentials
    And I perform GET request to verify the "TheWorks" membershipcard account is created
    Then I verify the data stored in DB after "Enrol" journey for "TheWorks"

    And I verify lc_join_request loyalty scheme event is created for bink_user
    And I verify lc_join_success loyalty scheme event is created for bink_user


  @multi_wallet_joins_event
  Scenario: Verify event generate for join requests in multiwallet

    Given I register with bink service in barclays
    When I perform POST request to create a "TheWorks" membershipcard account with enrol credentials
    And I perform GET request to verify the "TheWorks" membershipcard account is created
    Then I verify the data stored in DB after "Enrol" journey for "TheWorks"

    And I verify lc_join_request loyalty scheme event is created for barclays_user
    And I verify lc_join_success loyalty scheme event is created for barclays_user


    Given I register with bink service in bink
    When I perform POST request to create a "TheWorks" membershipcard account with enrol credentials
    And I perform GET request to verify the "TheWorks" membershipcard account is created
    Then I verify the data stored in DB after "Enrol" journey for "TheWorks"

    And I verify lc_join_request loyalty scheme event is created for bink_user
    And I verify lc_join_success loyalty scheme event is created for bink_user
