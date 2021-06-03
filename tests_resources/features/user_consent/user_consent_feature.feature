@registerConsent
Feature: Verify /service endpoint is working as expected
  As a customer
  I want to receive a correct error message when I don’t pass in the ”consent” field
  So I know this is a client error and I can look at my request to fix it

  @serviceConsent01 @LOY1677 @bink_regression @bmb_regression
  Scenario Outline: Verify POST service without "consent" field

    Given I register with bink as a new customer
    When I send a POST service request without the consent field
    Then I should receive an HTTP "<statuscode>" with a "<errordetail>"

    Examples:
      |statuscode|errordetail                     |
      |400       |{'detail': 'Malformed request.'}|


  @serviceConsent02 @LOY1677 @bink_regression @bmb_regression
  Scenario Outline: Verify POST service without "invalid payload" field

    Given I register with bink as a new customer
    When I send a POST service request without the consent key into request
    Then I should receive an HTTP "<statuscode>" with a "<errordetail>"

    Examples:
      |statuscode|errordetail                     |
      |400       |{'detail': 'Malformed request.'}|

  @serviceConsent03 @LOY1677 @bink_regression @bmb_regression
  Scenario Outline: Verify POST service without payload mandatory field

    Given I register with bink as a new customer
    When I send a POST service request without the consent mandatory field into request
    Then I should receive an HTTP "<statuscode>" with a "<errordetail>"

    Examples:
      |statuscode|errordetail                     |
      |400       |{'detail': 'Malformed request.'}|

