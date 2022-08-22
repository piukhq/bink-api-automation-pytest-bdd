@trenette @dev @sanity
Feature: Merchant Trenette - Ensure a customer can view Scheme plan details
  As a customer
  I want to access membership plans
  So I can choose a membership plan to view its details

  Verify a customer can use Banking API to view available Trenette membership plans v1.2


  @membership_plan @bink_regression @bmb_regression
   Scenario: Membership plan Trenette
    Given I am a Bink user
    When I perform GET request to view all available membership plans
    Then I can ensure the "Trenette" plan details match with expected data