@iceland @bink
Feature: Merchant Iceland - Ensure a customer can view Scheme plan details
  As a customer
  I want to access membership plans
  So I can choose a membership plan to view its details

  Verify a customer can use Banking API to view available Iceland membership plans v1.2

  @membership_plans
  Scenario: Membership plans v1.2_Iceland
    Given I register with bink service as a new customer
    When I perform GET request to view all available membership plans
    Then I can ensure the "Iceland" plan details match with expected data