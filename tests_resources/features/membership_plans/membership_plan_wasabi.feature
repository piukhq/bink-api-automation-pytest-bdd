@wasabi @dev @sanity @sanity_bmb
Feature: Merchant Wasabi - Ensure a customer can view Scheme plan details
  As a customer
  I want to access a particular scheme membership plan
  So I can the view membership plan details

  Verify a customer can use Banking API to view available Wasabi membership plans v1.2

  @membership_plan @bink_regression @bmb_regression
  Scenario: Membership plan Wasabi
    Given I am a Bink user
    Then I can ensure the "Wasabi" plan details match with expected data