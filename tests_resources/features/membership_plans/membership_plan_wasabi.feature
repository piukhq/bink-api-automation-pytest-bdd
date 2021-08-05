@wasabi @bink
Feature: Merchant Wasabi - Ensure a customer can view Scheme plan details
  As a customer
  I want to access membership plans
  So I can choose a membership plan to view its details

  Verify a customer can use Banking API to view available Wasabi membership plans v1.2

  @membership_plan @prod
  Scenario: Membership plans v1.2_Wasabi
    Given I am a Bink user
    When I perform GET request to view all available membership plans
    Then I can ensure the "Wasabi" plan details match with expected data