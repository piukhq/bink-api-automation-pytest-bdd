@the_works
Feature: Merchant TheWorks - Ensure a customer can view Scheme plan details
  As a customer
  I want to access a particular scheme membership plan
  So I can the view membership plan details

  Verify a customer can use Banking API to view available Asos membership plans v1.2


  @membership_plan @tst
   Scenario: Membership plan TheWorks
    Given I am a Bink user
    Then I can ensure the "TheWorks" plan details match with expected data