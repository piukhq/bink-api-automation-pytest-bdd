# Created by bularaghavan on 04/07/2024
@pll_link_status_change_event @events @sanity @new
Feature: Verify event for pll status change
  As a Data Analyst, I want to see an Event logged whenever the state of the PLL link between a Payment Card and Loyalty Card changes,
  so that this Business Event can be written to ClickHouse for validation.

  @pll_link_status_add_event
  Scenario: Verify pll link status change event for add journey
    Given I register with bink service in barclays
    When I perform POST request to add "master" payment card to wallet
    And I perform POST request to add & auto link "Iceland" membership card
    Then I verify pll_link_statuschange pll event is created for barclays_user for status null to 0 and slug LOYALTY_CARD_PENDING
    And I verify pll_link_statuschange pll event is created for barclays_user for status 0 to 1 and slug null

    @pll_link_status_join_success_event
# The pll link status changes from null to 1 as we are doing a patch later.So no loyalty card pending pll status.
  Scenario: Verify pll link status change event for join success journey
    Given I register with bink service in barclays
    When I perform POST request to add "master" payment card to wallet
    And I perform POST request to create a "Iceland" membership account with enrol credentials
    And I perform GET request to verify the "Iceland" membershipcard account is created
    And I perform PATCH request to link membership card to payment card
    Then I verify pll_link_statuschange pll event is created for barclays_user for status null to 1 and slug null

    @pll_link_status_register_success_event
# The pll link status changes from null to 1 as we are doing a patch later.So no loyalty card pending pll status.
  Scenario: Verify pll link status change event for register success journey
    Given I register with bink service in barclays
    When I perform POST request to add "master" payment card to wallet
    And I perform POST request to add "Iceland" membership card for "successful_register"
    And I perform PATCH request to create a "Iceland" ghost membership account with enrol credentials
    And For barclays I perform GET request to verify the Iceland membership card is added to the wallet after successful_register
    And I perform PATCH request to link membership card to payment card
    Then I verify pll_link_statuschange pll event is created for barclays_user for status null to 1 and slug null

  @pll_link_status_remove_pc_event
  Scenario: Verify pll link status change event for remove payment card event
    Given I register with bink service in barclays
    When I perform POST request to add "master" payment card to wallet
    And I perform POST request to create a "Iceland" membership account with enrol credentials
    And I perform GET request to verify the "Iceland" membershipcard account is created
    And I perform PATCH request to link membership card to payment card
    Then I perform DELETE request to delete the payment card
    And I verify pll_link_statuschange pll event is created for barclays_user for status 1 to null and slug null

    @pll_link_status_remove_lc_event
  Scenario: Verify pll link status change event for remove loyalty card event
    Given I register with bink service in barclays
    When I perform POST request to add "master" payment card to wallet
    And I perform POST request to create a "Iceland" membership account with enrol credentials
    And I perform GET request to verify the "Iceland" membershipcard account is created
    And I perform PATCH request to link membership card to payment card
    Then I perform DELETE request to delete the "Iceland" membership card
    And I verify pll_link_statuschange pll event is created for barclays_user for status 1 to null and slug null

  @multi_wallet_addauth_success_pll_status_event
  Scenario: Verify event generate for add and auth success in multiwallet
    Given I register with bink service in bink
    When I perform POST request to add new payment card to wallet of master type
    And I perform POST request to add & auto link "Iceland" membership card
    Then I verify pll_link_statuschange pll event is created for bink_user for status null to 0 and slug LOYALTY_CARD_PENDING
    And I verify pll_link_statuschange pll event is created for bink_user for status 0 to 1 and slug null

    Given I register with bink service in barclays
    When I perform POST request to add existing payment card to wallet of master type
    And I perform POST request to add & auto link "Iceland" membership card
    Then I verify pll_link_statuschange pll event is created for barclays_user for status null to 0 and slug LOYALTY_CARD_PENDING
    And I verify pll_link_statuschange pll event is created for bar_claysuser for status 0 to 1 and slug null
