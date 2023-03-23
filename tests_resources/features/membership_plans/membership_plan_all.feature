@view_all_plans @dev @sanity @sanity_bmb
Feature: View all retailer plans details
  As a customer
  I want to access all membership plans
  So I can view all schemes membership plans details

  Verify a customer can use Banking API to view available membership plans v1.2


  @all_membership_plans 
   Scenario: All retailers membership plans
    Given I am a Bink user
    Then I perform GET request to view all available membership plans
