from os import environ
from tests_resources.test_data import testdata_dev
from tests_resources.test_data import testdata_staging
from tests_resources.test_data import testdata_prod
from tests_resources.test_data import testdata_sit
from tests_resources.test_data import testdata_oat
from tests_resources.test_data import testdata_preprod


class EnvironmentDetails:
    def __init__(self, base_url, test_data):
        self.base_url = base_url
        self.test_data = test_data


if "KUBERNETES_SERVICE_HOST" in environ:
    DEV = EnvironmentDetails(
        base_url="http://hermes-api",
        test_data=testdata_dev,
    )
    STAGING = EnvironmentDetails(
        base_url="http://hermes-api",
        test_data=testdata_staging,
    )
    PROD = EnvironmentDetails(
        base_url="http://hermes-api",
        test_data=testdata_prod,
    )
else:
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
    OAT = EnvironmentDetails(
        base_url="https://oat.sandbox.gb.bink.com",
        test_data=testdata_oat,
    )
    PREPROD = EnvironmentDetails(
        base_url="https://api.preprod.gb.bink.com",
        test_data=testdata_preprod,
    )


class ChannelDetails:
    def __init__(self, channel_name, bundle_id, client_id, organisation_id):
        self.channel_name = channel_name
        self.bundle_id = bundle_id
        self.client_id = client_id
        self.organisation_id = organisation_id


BINK = ChannelDetails(
    channel_name="bink",
    bundle_id="com.bink.wallet",
    client_id="MKd3FfDGBi1CIUQwtahmPap64lneCa2R6GvVWKg6dNg4w9Jnpd",
    organisation_id="",
)

BARCLAYS = ChannelDetails(
    channel_name="barclays",
    bundle_id="com.barclays.bmb",
    client_id="not using for Barclays jwt token creation",
    organisation_id="Barclays",

)
