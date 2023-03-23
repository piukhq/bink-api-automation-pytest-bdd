@iceland @dev @sanity @sanity_bmb
Feature: Merchant Iceland - Ensure a customer can view Scheme plan details
  As a customer
  I want to access a particular scheme membership plan
  So I can the view membership plan details

  Verify a customer can use Banking API to view available Iceland membership plans v1.2


  @membership_plan @bink_regression @bmb_regression
   Scenario: Membership plan Iceland
    Given I am a Bink user
    Then I can ensure the "Iceland" plan details match with expected data


