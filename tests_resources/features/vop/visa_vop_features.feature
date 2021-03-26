
Feature: VOP Verification - Ensure Visa Vop features are working as expected
  As a customer
  I want to utilise ubiquity_vop
  So I can add my payment card, with the scheme provider Harvey Nichols & check its details successfully

  @visa_vop @bink_regression @bmb_regression
  Scenario Outline: Verify visa vop Activation - Integration Testing

    Given I register with bink service as a new customer
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "HarveyNichols" membership card
    And I perform GET request to verify the "HarveyNichols" membership card is added & linked successfully in the wallet
    Then I verify status of paymentcard is "activated"
    And I perform DELETE request to delete the payment card
    And I verify status of paymentcard is "deactivated"

    Examples:
    | payment_card_provider|
    |          visa        |