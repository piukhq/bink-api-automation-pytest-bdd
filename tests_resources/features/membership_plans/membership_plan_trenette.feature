@trenette @dev @sanity
Feature: Merchant Trenette - Ensure a customer can view Scheme plan details
  As a customer
  I want to access a particular scheme membership plan
  So I can the view membership plan details

  Verify a customer can use Banking API to view available Trenette membership plans v1.2


  @membership_plan 
   Scenario: Membership plan Trenette
    Given I am a Bink user
    Then I can ensure the "Trenette" plan details match with expected data