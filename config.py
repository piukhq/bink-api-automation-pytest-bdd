from tests_resources.test_data import testdata_dev
from tests_resources.test_data import testdata_staging
from tests_resources.test_data import testdata_prod
from tests_resources.test_data import testdata_sit


class EnvironmentDetails:
    def __init__(self, base_url, test_data):
        self.base_url = base_url
        self.test_data = test_data


DEV = EnvironmentDetails(
    base_url="https://api.dev.gb.bink.com",
    test_data=testdata_dev,
)
STAGING = EnvironmentDetails(
    base_url="https://api.staging.gb.bink.com",
    test_data=testdata_staging,
)
PROD = EnvironmentDetails(
    base_url="https://api.gb.bink.com",
    test_data=testdata_prod,
)

SIT = EnvironmentDetails(
    base_url="https://api.sandbox.gb.bink.com",
    test_data=testdata_sit,
)

class ChannelDetails:
    def __init__(self, channel_name, bundle_id, client_id_dev, client_id_staging, client_id_prod,
                 organisation_id):
        self.channel_name = channel_name
        self.bundle_id = bundle_id
        self.client_id_dev = client_id_dev
        self.client_id_staging = client_id_staging
        self.client_id_prod = client_id_prod
        self.organisation_id = organisation_id


BINK = ChannelDetails(
    channel_name="bink",
    bundle_id="com.bink.wallet",
    client_id_dev="MKd3FfDGBi1CIUQwtahmPap64lneCa2R6GvVWKg6dNg4w9Jnpd",
    client_id_staging="MKd3FfDGBi1CIUQwtahmPap64lneCa2R6GvVWKg6dNg4w9Jnpd",
    client_id_prod="MKd3FfDGBi1CIUQwtahmPap64lneCa2R6GvVWKg6dNg4w9Jnpd",
    organisation_id="",
)

BARCLAYS = ChannelDetails(
    channel_name="barclays",
    bundle_id="com.barclays.bmb",
    client_id_dev="zQXVE6WnCXi5WCHa7p7PgAeszP9zZQgQOyRyYQjlFkpirclGyb",
    client_id_staging="lwhkGNn5FAXPCCcbIFrgZWk0i7Qolg5WBMFM4UYjZAbaOXQyq6",
    client_id_prod="neik5y7udnvZJAhfGrtH6I8iu02vcUoBhFixau5OWfGvZPrVfq",
    organisation_id="Barclays",

)
