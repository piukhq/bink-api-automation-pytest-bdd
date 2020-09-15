@iceland @bink
Feature: Merchant Iceland - Ensure a customer can view Scheme plan details
  As a customer
  I want to access membership plans
  So I can choose a membership plan to view its details

  Verify a customer can use Banking API to view available Iceland membership plans v1.2
`
  @membership_plan_iceland_bink
  Scenario: Membership plans v1.2_Iceland
    Given I am a Bink user
    When I perform GET request to view all available membership plans
    Then I can ensure the "Iceland" plan details match with expected data


  @membership_plan @dev
#  @staging @prod @CR257
   Scenario: Membership plan_Iceland
    Given I am a Bink user
    When I perform GET request to view all available membership plans
    Then I can ensure the "Iceland" plan details for "Barclays" match with expected data


