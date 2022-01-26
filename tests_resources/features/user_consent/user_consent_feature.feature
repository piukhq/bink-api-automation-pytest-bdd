@registerConsent  @sanity
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


  @serviceConsent04 @LOY1678 @bink_regression @bmb_regression
  Scenario Outline: Verify timestamp in the request body enclosed in quotes for POST service

    Given I register with bink as a new customer
    When I send a POST service request with "timestamp" in the request body enclosed in quotes
    Then I should receive an HTTP "<statuscode>" and success response
    And I perform DELETE request to delete the customer

    Examples:
      |statuscode|
      |201       |

  @serviceConsent05 @LOY1678 @bink_regression @bmb_regression
  Scenario: Verify without latitude in the request body

    Given I register with bink as a new customer
    When I send a POST service request without "latitude" in the request body enclosed in quotes
    Then I should receive an statuscode and success response with email and timestamp without "latitude"
    And I perform DELETE request to delete the customer

  @serviceConsent06 @LOY1678 @bink_regression @bmb_regression
  Scenario: Verify without longitude in the request body

    Given I register with bink as a new customer
    When I send a POST service request without "longitude" in the request body enclosed in quotes
    Then I should receive an statuscode and success response with email and timestamp without "longitude"
    And I perform DELETE request to delete the customer

  @serviceConsent07 @LOY1678 @bink_regression @bmb_regression
  Scenario Outline: Verify longitude as alphabet

    Given I register with bink as a new customer
    When I send a POST service request "longitude" as alphabet
    Then I should receive an HTTP "<statuscode>" with a "<errordetail>"

   Examples:
     |statuscode|errordetail                     |
     |400       |{'detail': 'Malformed request.'}|

