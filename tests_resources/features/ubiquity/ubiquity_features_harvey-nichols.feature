
Feature: Merchant Harvey Nichols - Ensure a customer can use Bink's Ubiquity features
  As a customer
  I want to utilise membership_cards endpoint
  So I can add my card, with the scheme provider Harvey Nichols & check its details successfully


   @ubiquity @dev
  Scenario: Add a second membership card single channel_HarveyNichols

    Given I am a customer in channel_1
    When I perform POST request to add payment_card_1 to my wallet in channel_1
    And I perform the GET request to verify the payment_card_1 has been added successfully to the wallet in channel_1
    And I perform POST request to add & auto link an existing "HarveyNichols" membership_card_1 to my wallet in channel_1
    And I perform GET request to verify the "HarveyNichols" membership_card_1 is added & linked successfully in the wallet in channel_1
    And I perform POST request to add & auto link an existing "HarveyNichols" membership_card_2 to my wallet in channel_1
    Then I perform GET request to verify the "HarveyNichols" membership_card_2 is successfully added to my wallet in channel_1
    And The response shows the original link between "HarveyNichols" membership_card_1 and payment_card_1 remains in force
    And There is no link created between payment_card_1 and "HarveyNichols" membership_card_2

    @ubiquity @dev
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
#
#  Scenario Outline:  Add_Journey_Invalid data_Error code checks
#
#    Given I am a Bink user
#    When I perform POST request to add "HarveyNichols" membership card with invalid "<email_address>" and "<password>"
#    And I perform GET request to verify the "HarveyNichols" membership card fails to add & link in their wallet with "<state>"
#    Then I can see relevant "<reason code>" is present in the response
#    Then they can perform Delete operation to delete the membership card
#
#
#    Examples:
#      | email_address             | password    | state  |reason code |
#      |auto_zer@testbink.com      | BinkT       | failed |  X303      |
#      |auto_zero@testbink.web     | BinkTesting | failed |  X303      |
#      |auto_zero@testbink.com     | BinkT       | failed |  X303      |


#  Scenario: Delete membership card to a payment card, then verify PLL link is automatically deleted
#    Given I am a Bink user
#    And I perform POST request to add payment card to wallet
#    And I perform the GET request to verify the payment card has been added successfully
#    When I perform POST request to add & auto link an existing "HarveyNichols" membership card
#    And I perform GET request to verify the "HarveyNichols" membership card is added & linked successfully in the wallet
#    Then I perform DELETE request to delete the "HarveyNichols" membership card
#    Then PLL link should be automatically deleted


  #    Check if balance array is same for PLL & PLR . If not create separate scenarios

   @schema_membership_cards
  Scenario: Schema check MembershipCards

     Given I am a Bink user
    When I perform POST request to add "HarveyNichols" membership card
    And I perform GET request to verify the "HarveyNichols" membership card is added to the wallet
    Then I perform schema validation for GET/membership cards response for "HarveyNichols"
    Then I perform DELETE request to delete the "HarveyNichols" membership card
    And I perform DELETE request to delete the customer