# Created by nehapatil at 4/07/2023
@events @sanity
Feature: Verify event for register fail for loyalty card
  As a DM Administrator
  I want to see an event logged when a user registration is failed
  so that this Business Event can be written to ClickHouse for validation

  @register_fail_event
  Scenario: Register request and failed event
    Given I register with bink service in bink
    When I perform POST request to add "Iceland" membership card for "failed_register"
    And I perform PATCH request to create "Iceland" "failed_register"
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
    Then I verify lc_register_request loyalty scheme event is created for bink_user
    And I verify lc_status_change loyalty scheme event is created for bink_user
    And I verify lc_register_failed loyalty scheme event is created for bink_user
    Then I perform DELETE request to delete all users


  @register_fail_event
  Scenario: Register events for Multi-wallet register failed in wallet 1 and wallet 2
    Given I register with bink service in bink
    When I perform POST request to add "Iceland" membership card for "failed_register"
    And I perform PATCH request to create "Iceland" "failed_register"
    And For bink I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
    Then I verify lc_register_request loyalty scheme event is created for bink_user
    And I verify lc_status_change loyalty scheme event is created for bink_user
    And I verify lc_register_failed loyalty scheme event is created for bink_user
    Given I register with bink service in barclays
    When I perform POST request to add "Iceland" membership card for "already_registered"
    And I perform PATCH request to create "Iceland" "failed_register"
    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet with invalid data
    Then I verify lc_register_request loyalty scheme event is created for barclays_user
    And I verify lc_status_change loyalty scheme event is created for barclays_user
    And I verify lc_register_failed loyalty scheme event is created for barclays_user
    Then I perform DELETE request to delete all users
