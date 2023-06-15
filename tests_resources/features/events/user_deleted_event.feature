# Created by rupalpatel at 13/06/2023
@user_deleted @events
Feature: Add and authorise a loyalty card
  As a DM Administrator
  I want to see an Event logged when a user is deleted
  so that this Business Event can be written to ClickHouse for validation

  @user_deleted_event @sanity
  Scenario: Verify event for user deleted
    Given I register with bink service in bink
    Then I perform DELETE request to delete the customer
    And I verify that user_deleted event
