# Created by rupalpatel at 26/06/2023
@events @sanity @new
Feature: Verify event for join fail for loyalty card
  As a DM Administrator
  I want to see an event logged when a user joined failed scheme
  so that this Business Event can be written to ClickHouse for validation

  @join_fail_event
  Scenario: Remove a failed join request from the wallet and verify the event
    Given I register with bink service in bink
    When I perform POST request to create a "Iceland" membership card with "invalid" enrol credentials
    And I perform GET request to verify the "Iceland" membership card is created with invalid data
    Then I verify lc_join_request loyalty scheme event is created for bink_user
    And I verify lc_join_failed loyalty scheme event is created for bink_user

  @multi_wallet_joins_fail_event @join_fail_event
  Scenario: Verify event generate for join fail requests for multiwallet
    Given I register with bink service in bink
    When I perform POST request to create a "Iceland" membership card with "invalid" enrol credentials
    And I perform GET request to verify the "Iceland" membership card is created with invalid data
    Then I verify lc_join_request loyalty scheme event is created for bink_user
    And I verify lc_join_failed loyalty scheme event is created for bink_user

    Given I register with bink service in barclays
    When I perform POST request to join "Iceland" membershipcard with "invalid_join" enrol credentials
    And I perform GET request to verify the "Iceland" membership card is created with invalid data
    Then I verify lc_join_request loyalty scheme event is created for barclays_user
    And I verify lc_join_failed loyalty scheme event is created for barclays_user