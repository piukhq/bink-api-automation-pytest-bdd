@coop @bink
Feature: Merchant CooP - Ensure a customer can view Scheme plan details
  As a customer
  I want to access membership plans
  So I can choose a membership plan to view its details

  Verify a customer can use Banking API to view available CooP membership plans v1.2

"""CooP is not in use for current launch. So removed the execution tags"""
  Scenario: Membership plans_CooP
    Given I am a Bink user
    When I perform GET request to view all available membership plans
    Then I can ensure the "CooP" plan details match with expected data