
Feature: Merchant Harvey Nichols - Ensure a customer can use Bink's Ubiquity features
  As a customer
  I want to utilise membership_cards endpoint
  So I can add my card, with the scheme provider Harvey Nichols & check its details successfully


   @ubiquity @LOY988
  Scenario: Add a second membership card single channel_HarveyNichols
#  Ensure a Customer cannot link multiple membership cards of the same merchant to a payment card
    Given I am a customer in channel_1
    When I perform POST request to add payment_card_1 to my wallet in channel_1
    And I perform the GET request to verify the payment_card_1 has been added successfully to the wallet in channel_1
    And I perform POST request to add & auto link an existing "HarveyNichols" membership_card_1 to my wallet in channel_1
    And I perform GET request to verify the "HarveyNichols" membership_card_1 is added & linked successfully in the wallet in channel_1
    And I perform POST request to add & auto link an existing "HarveyNichols" membership_card_2 to my wallet in channel_1
    Then I perform GET request to verify the "HarveyNichols" membership_card_2 is successfully added to my wallet in channel_1
    And The response shows the original link between "HarveyNichols" membership_card_1 and payment_card_1 remains in force
    And There is no link created between payment_card_1 and "HarveyNichols" membership_card_2

    @ubiquity @LOY988
  Scenario: Add a second membership card second channel_HarveyNichols

    Given I am a customer in channel_1
    When I perform POST request to add payment_card_1 to my wallet in channel_1
    And I perform the GET request to verify the payment_card_1 has been added successfully to the wallet in channel_1
    And I perform POST request to add & auto link an existing "HarveyNichols" membership_card_1 to my wallet in channel_1
    And I perform GET request to verify the "HarveyNichols" membership_card_1 is added & linked successfully in the wallet in channel_1
    And I switch to "channel_2"
    And I perform POST request to add payment_card_1 to my wallet in channel_2
    And I perform the GET request to verify the payment_card_1 has been added successfully to the wallet in channel_2
    And I perform POST request to add & auto link an existing "HarveyNichols" membership_card_2 to my wallet in channel_2
    Then I perform GET request to verify the "HarveyNichols" membership_card_2 is successfully added to my wallet in channel_2
    And There is no link created between payment_card_1 and "HarveyNichols" membership_card_2


  @ubiquity @LOY975
  Scenario Outline: Attempt to replace link in a single property

    Given I am a customer in channel_1
    When I perform POST request to add payment_card_1 to my wallet in channel_1
    And I perform the GET request to verify the payment_card_1 has been added successfully to the wallet in channel_1
    And I perform POST request to add & auto link an existing "HarveyNichols" membership_card_1 to my wallet in channel_1
    And I perform GET request to verify the "HarveyNichols" membership_card_1 is added & linked successfully in the wallet in channel_1
    And I perform POST request to add an existing "HarveyNichols" membership_card_2 to my wallet in channel_1
    And I perform GET request to verify the "HarveyNichols" membership_card_2 is successfully added to my wallet in channel_1
    And I perform a PATCH request to link "HarveyNichols" membership_card_2 to the payment_card_1 in channel_1
    Then I see the following "<error>" with HTTP status code 400
    Examples:
      | error |
      |PLAN_ALREADY_LINKED: "Payment card {PCARD_ID} is already linked to a membership card that belongs to the membership plan {PLAN_ID}|

  @ubiquity @LOY975
  Scenario Outline: Attempt to replace link in another property

    Given I am a customer in channel_1
    When I perform POST request to add payment_card_1 to my wallet in channel_1
    And I perform the GET request to verify the payment_card_1 has been added successfully to the wallet in channel_1
    And I perform POST request to add & auto link an existing "HarveyNichols" membership_card_1 to my wallet in channel_1
    And I perform GET request to verify the "HarveyNichols" membership_card_1 is added & linked successfully in the wallet in channel_1
    And I switch to "channel_2"
    And I perform POST request to add payment_card_1 to my wallet in channel_2
    And I perform the GET request to verify the payment_card_1 has been added successfully to the wallet in channel_2
    And I perform POST request to add an existing "HarveyNichols" membership_card_2 to my wallet in channel_2
    And I perform GET request to verify the "HarveyNichols" membership_card_2 is successfully added to my wallet in channel_2
    And I perform a PATCH request to link "HarveyNichols" membership_card_2 to the payment_card_1 in channel_2
    Then I see the following "<error>" with HTTP status code 400
    Examples:
      | error |
      |PLAN_ALREADY_LINKED: "Payment card {PCARD_ID} is already linked to a membership card that belongs to the membership plan {PLAN_ID}|

#      This scenario won't execute in staging as it contains Enrol steps
    @ubiquity @LOY1027 
  Scenario: Sign up to a new scheme when an existing card in the wallet

    Given I am a customer in channel_1
    When I perform POST request to add payment_card_1 to my wallet in channel_1
    And I perform the GET request to verify the payment_card_1 has been added successfully to the wallet in channel_1
    And I perform POST request to add & auto link an existing "HarveyNichols" membership_card_1 to my wallet in channel_1
    And I perform GET request to verify the "HarveyNichols" membership_card_1 is added & linked successfully in the wallet in channel_1
    And I perform POST request to create a "HarveyNichols" membership account with new enrol credentials in the same wallet
    Then I perform GET request to verify the "HarveyNichols" membership account is created in the same wallet

# USe mock agents to test below ghost card scenario
    @ubiquity @LOY-854 
  Scenario: Register a card in PRE_REGISTERED_CARD status when an existing card in the wallet

    Given I am a customer in channel_1
    When I perform POST request to add & auto link an existing "Iceland" membership_card_1 to my wallet in channel_1
    And I perform GET request to verify the "HarveyNichols" membership_card_1 is added successfully in the wallet in channel_1
    And I perform POST request to add an "Iceland" ghost card
    And I perform GET request to verify the status of "Iceland" ghost card
    And I perform PATCH request update the ghost card registration details
    Then I perform a GET request to verify both the scheme accounts are returned


