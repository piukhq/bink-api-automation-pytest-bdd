@harvey_nichols
Feature: Merchant BurgerKing - Ensure a customer can add their payment card & link it to loyalty membership card
  and view their card(s) details

  As a customer
  I want to utilise payment_cards endpoint
  So I can add my payment card and can link to BurgerKing membership card & check the details successfully


  Scenario Outline: ADD & LINK Journey_BurgerKing

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add & auto link "BurgerKing" membership card
    Then I perform GET request to verify the "BurgerKing" membership card is added & linked successfully in the wallet

    Examples:
    | payment_card_provider|
    |           master     |


    @patch_mcard_pcard
    Scenario Outline: PLL Link by PATCH(mcard_pcard)_BurgerKing

    Given I am a Bink user
    And I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add "HarveyNichols" membership card to my wallet
    And I perform GET request to verify the "HarveyNichols" membership card is added to my wallet
    And I perform PATCH request to link membership card to payment card
#    And I perform GET request to verify the "BurgerKing" membership card is linked successfully in the wallet
#    And I perform GET membership_cards request to verify the "BurgerKing" membership card is linked successfully in the wallet
#    And I perform GET payment_cards request to verify the "BurgerKing" membership card is linked successfully in the wallet
    #Then I perform DELETE request to delete the link between membership_card & payment_card
#    And I perform GET membership_cards request to verify the link is removed successfully
#    And I perform GET payment_cards request to to verify the link is removed successfully

  Examples:
    | payment_card_provider|
    |           master     |

    @patch_pcard_mcard

    Scenario Outline: PLL Link by PATCH(pcard_mcard)_BurgerKing

    Given I am a Bink user
    When I perform POST request to add "<payment_card_provider>" payment card to wallet
    And I perform the GET request to verify the payment card has been added successfully to the wallet
    When I perform POST request to add "HarveyNichols" membership card to my wallet
    And I perform GET request to verify the "HarveyNichols" membership card is added to my wallet
    And I perform PATCH request to link payment card to membership card
    And I perform GET membership_cards request to verify the membership card is linked successfully in the wallet
#    And I perform GET payment_cards request to verify the "BurgerKing" membership card is linked successfully in the wallet
    #Then I perform DELETE request to delete the link between payment_card & membership_card
#    And I perform GET membership_cards request to verify the link is removed successfully
#    And I perform GET payment_cards request to to verify the link is removed successfully

    Examples:
    | payment_card_provider|
    |           master     |
