from tests_resources.test_data import testdata_dev
from tests_resources.test_data import testdata_staging


class EnvironmentDetails:
    def __init__(self, base_url, test_data, django_url):
        self.base_url = base_url
        self.test_data = test_data
        self.django_url = django_url


DEV = EnvironmentDetails(
    base_url="https://api.dev.gb.bink.com",
    test_data=testdata_dev,
    django_url="https://api.dev.gb.bink.com/admin/"
)
STAGING = EnvironmentDetails(
    base_url="https://api.staging.gb.bink.com",
    test_data=testdata_staging,
    django_url="https://staging.dev.gb.bink.com/admin/"
)


class ChannelDetails:
    def __init__(self, channel_name, bundle_id, client_id):
        self.channel_name = channel_name
        self.bundle_id = bundle_id
        self.client_id = client_id


BINK = ChannelDetails(
    channel_name="bink",
    bundle_id="com.bink.wallet",
    client_id="MKd3FfDGBi1CIUQwtahmPap64lneCa2R6GvVWKg6dNg4w9Jnpd"
)

BARCLAYS = ChannelDetails(
    channel_name="barclays",
    bundle_id="com.barclays.test",
    client_id="2zXAKlzMwU5mefvs4NtWrQNDNXYrDdLwWeSCoCCrjd8N0VBHoi"
)


class BrowserDetails:
    def __init__(self, browser_name, driver_path, wait_time):
        self.browser_name = browser_name
        self.driver_path = driver_path
        self.wait_time = wait_time


BROWSER = BrowserDetails(
    browser_name="chrome",
    driver_path="tests_resources/drivers/chromedriver",
    wait_time=10
)
