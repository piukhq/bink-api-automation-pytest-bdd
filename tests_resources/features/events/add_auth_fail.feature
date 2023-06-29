# Created by rupalpatel at 26/06/2023
@add_auth_fail_event @events @sanity @new
Feature: Verify event for add and authorise fail loyalty card
  As a DM Administrator
  I want to see an event logged when a user send request with invalid data to add and authorise scheme
  so that this Business Event can be written to ClickHouse for validation

  @add_auth_fail
  Scenario: Verify events for add and auth field journey with unauthorised loyalty card
    Given I register with bink service in bink
    When I perform POST request to add and auth for "Iceland" membershipcard with "invalid_credentials"
    And For bink I perform GET request to verify the "Iceland" membershipcard is added to the wallet with invalid data
    Then I verify lc_add_auth_request loyalty scheme event is created for bink_user
    And I verify lc_add_auth_failed loyalty scheme event is created for bink_user


  @multi_wallet_add_auth_fail_event
  Scenario: Verify event generate for fail add and auth requests in multiwallet
    Given I register with bink service in bink
    Then I verify that user_created event
    When I perform POST request to add and auth for "Iceland" membershipcard with "invalid_credentials"
    And For bink I perform GET request to verify the "Iceland" membershipcard is added to the wallet with invalid data
    Then I verify lc_add_auth_request loyalty scheme event is created for bink_user
    And I verify lc_add_auth_failed loyalty scheme event is created for bink_user

    Given I register with bink service in barclays
    Then I verify that user_created event
    When I perform POST request to add and auth for "Iceland" membershipcard with "invalid_credentials"
    And For barclays I perform GET request to verify the "Iceland" membershipcard is added to the wallet with invalid data
    Then I verify lc_add_auth_request loyalty scheme event is created for barclays_user
    And I verify lc_add_auth_failed loyalty scheme event is created for barclays_user
