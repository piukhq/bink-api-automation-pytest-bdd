@wasabi @sanity @sanity_bmb
Feature: Merchant Wasabi - Ensure a customer can add their payment card & link it to loyalty membership card
  and view their card(s) details

  As a customer
  I want to utilise payment_cards endpoint
  So I can add my payment card and can link to Wasabi membership card & check the details successfully

  @add_link
  Scenario Outline: ADD & LINK Journey_Wasabi

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "Wasabi" membership card
    Then I perform GET request to verify the "Wasabi" membership card is added & linked successfully in the wallet

    Examples:
    | payment_card_provider|
    |          amex        |
    |          master      |
    |          visa        |

  @patch_mcard_pcard 
  Scenario: PLL Link by PATCH_(mcard_pcard)_Wasabi

    Given I am a customer who is subscribing to Bink or I am Bink app user
    When I perform POST request to add "master" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add "Wasabi" membership card to my wallet
    And I perform GET request to verify the "Wasabi" membership card is added to the wallet
    And I perform PATCH request to link membership card to payment card
    And I perform GET request to verify the "Wasabi" membership card is linked successfully in the wallet
    And I perform GET/payment_card/id request to verify the membership card is linked to the payment card
    Then I perform DELETE request to delete the link between membership_card & payment_card
    And I perform GET/membership_card/id request to verify the payment card is unlinked from "Wasabi" membership card
    And I perform GET/payment_card/id request to verify the membership card is unlinked


  @patch_pcard_mcard 
  Scenario: PLL Link by PATCH_(pcard_mcard)_Wasabi

    Given I am a customer who is subscribing to Bink or I am Bink app user
    When I perform POST request to add "master" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add "Wasabi" membership card to my wallet
    And I perform GET request to verify the "Wasabi" membership card is added to the wallet
    And I perform PATCH request to link payment card to membership card
    And I perform GET request to verify the "Wasabi" membership card is linked successfully in the wallet
    And I perform GET/payment_card/id request to verify the membership card is linked to the payment card
    Then I perform DELETE request to delete the link between payment_card & membership_card
    And I perform GET/membership_card/id request to verify the payment card is unlinked from "Wasabi" membership card
    And I perform GET/payment_card/id request to verify the membership card is unlinked

  @enrol_new_paymentcard  
  Scenario Outline: Enrol new paymentcard and link to wasabi

    Given I am a Bink user
    When I perform POST request to enrol new "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the new payment card "<payment_card_provider>" has been added successfully to the wallet
    When I perform POST request to add & auto link "Wasabi" membership card
    Then I perform GET request to verify the "Wasabi" membership card is added & linked successfully in the wallet
    And I perform DELETE request to delete the payment card

    Examples:
    | payment_card_provider|
    |          visa        |
    |          amex        |
    |          master      |

#    Below visa paymentcard scenario run when staging is pointing to pelops only
  @enrol_new_paymentcard  
  Scenario Outline: Enrol link and unlink the visa vop in pelops for wasabi

    Given I am a Bink user
    When I perform POST request to enrol new "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "Wasabi" membership card
    Then I perform GET request to verify the "Wasabi" membership card is added & linked successfully in the wallet
    Then I verify status of paymentcard is "activated" for "Wasabi"
    And I perform DELETE request to delete the payment card
    And I verify status of paymentcard is "deactivated" for "Wasabi"

    Examples:
    | payment_card_provider|
    |          visa        |