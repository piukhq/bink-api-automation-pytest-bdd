@viator @dev
#@sanity @sanity_bmb
Feature: Merchant Viator - Ensure a customer can view Scheme plan details
  As a customer
  I want to access membership plans
  So I can choose a membership plan to view its details

  Verify a customer can use Banking API to view available Viator membership plans v1.2


  @membership_plan @bink_regression @bmb_regression
   Scenario: Membership plan Viator
    Given I am a Bink user
    When I perform GET request to view all available membership plans
    Then I can ensure the "Viator" plan details match with expected data