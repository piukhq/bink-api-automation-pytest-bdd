@harvey_nichols @bink
Feature: Merchant HarveyNichols - Ensure a customer can view Scheme plan details
  As a customer
  I want to access membership plans
  So I can choose a membership plan to view its details

  Verify a customer can use Banking API to view available HarveyNichols membership plans v1.2

  @membership_plans
  Scenario: Membership plans v1.2_HarveyNichols
    Given I register with bink service as a new customer
    When I perform GET request to view all available membership plans
    Then I can ensure the "HarveyNichols" plan details match with expected data

  @membership_plans_barclays
  Scenario: Verify membership plans for Barclays
    Given I register with bink service as a new customer
    When I perform GET request to view all available membership plans
    Then I can ensure that only "HarveyNichols" and "Iceland" plan details are populated