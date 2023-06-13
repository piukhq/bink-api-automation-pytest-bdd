# Created by rupalpatel at 09/06/2023
@user_created @events
Feature: Add and authorise a loyalty card
  As a DM Administrator
  I want to see an Event logged when a user is created
  so that this Business Event can be written to ClickHouse for validation

  @user_created_event @bink_regression_api2 @sandbox_regression @event
  Scenario: Verify event for user created
    Given I register with bink service in bink
    Then I verify that user_created event