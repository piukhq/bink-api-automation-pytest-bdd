# Created by rupalpatel at 15/06/2023
@add_auth_success_event @events @sanity
Feature: Verify event for add and authorise loyalty card
  As a DM Administrator
  I want to see an event logged when a user send request to add and authorise scheme
  so that this Business Event can be written to ClickHouse for validation

  @add_event
  Scenario: Verify event for add journey
    Given I register with bink service in bink
    When I perform POST request to add "Iceland" membership card to wallet
    And I perform GET request to verify the "Iceland" membership card added to the wallet
    Then I verify the data stored in DB after "Add" journey for "Iceland"
    And I verify lc_add_auth_request loyalty scheme event is created for bink_user
    And I verify lc_add_auth_success loyalty scheme event is created for bink_user

 @multi_wallet_add_event
  Scenario: Verify event for multi wallet add Iceland
    Given I register with bink service in barclays
    Then I verify that user_created event
    When I perform POST request to add and auth "Iceland" membershipcard with "valid_credentials"
    Then I verify the data stored in DB after "Add" journey for "Iceland"
    And I verify lc_add_auth_request loyalty scheme event is created for barclays_user
    And I verify lc_add_auth_success loyalty scheme event is created for barclays_user

    Given I register with bink service in bink
    Then I verify that user_created event
    When I perform POST request to add and auth "Iceland" membershipcard with "valid_credentials"
    Then I verify the data stored in DB after "Add" journey for "Iceland"
    And I verify lc_add_auth_request loyalty scheme event is created for bink_user
    And I verify lc_add_auth_success loyalty scheme event is created for bink_user
