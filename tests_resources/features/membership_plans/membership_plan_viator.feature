@viator @dev @sanity
# @sanity_bmb
Feature: Merchant Viator - Ensure a customer can view Scheme plan details
  As a customer
  I want to access a particular scheme membership plan
  So I can the view membership plan details

  Verify a customer can use Banking API to view available Viator membership plans v1.2


  @membership_plan  
   Scenario: Membership plan Viator
    Given I am a Bink user
    Then I can ensure the "Viator" plan details match with expected data