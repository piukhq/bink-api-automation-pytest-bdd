
# BinkAPI-TestAutomation-pytest-bdd
- This is a framework design in Python for the test automation of Bink's APIs.
- The framework has been designed using the Pytest-BDD plugin to implement  the BDD approach. 
- Modules of the framework are designed in such a way that it can be reused by all merchants in any channels
- This framework will provide a Regression testing suite for all available API endpoints, and also serve for Sanity, 
  Smoke testing & In- Sprint testing for all channels & merchants.


#  Set Up
This project requires an up-to-date version of Python 3 (Currently using Python 3.8)
 It also uses [pipenv](https://pipenv.readthedocs.io/) to manage packages.

To set up this project on your local machine:

    1. Clone it from this GitLab repository [QA GitLab](https://git.bink.com/QA/bink-api-automation-pytest-bdd)
    2. Run `pipenv install` from the project's root directory.
    3. * Optional Step : For Django Web UI tests, install the appropriate browser and WebDriver executable
        * Current Django tests use Chrome and
         [chromedriver](https://chromedriver.chromium.org/downloads) 
    4. Install Azure CLI and login to Azure for Key Vault access
        `brew install azure-cli`
        `az login`

       
# Running Tests
    1. Test Execution:
        - Use `pytest` command 
        - Use markers '-m' to fileter tests by BDD tags
        - Pass variables '--env' and '--channel' to set current environment and channel
        - The default environment is dev and default channel is bink
      
    2. A few sample execution commands:
        - pytest -m "add" --env staging --channel barclays : Execute Add Journey for all merchants in staging-barclays 
        - pytest -m "add" --env staging                    : Execute Add Journey for all merchants in staging-bink
        - pytest -m "add and iceland" --env staging        : Execute Add Journey for Iceland in staging-bink
        - pytest -m "add and enrol"                        : Execute Add & Enrol Journey for all merchants in dev-bink 
    
    3. Commands used for nighly regression in bink in staging
        - pytest -m "bink_regression" --env staging 
       Commands used for nighly regression in bink in staging
        - pytest -m "bmb_regression" --env staging --channel barclays     

# Running Allure Reports

Ensure you have the following installed:

- allure-pytest-bdd==2.943 or  (latest stable version)
- allure-python-commons==2.9.43 or (latest stable version)

Please ensure you are in the root directory before running any reports to avoid path issues.

Step 1 - Create Test Run with Allure:

In the terminal, enter test command - Example Test Command Run:

    1. Commands used for nighly regression in bink in staging
    - pytest -m "bink_regression" --env staging --alluredir=<new_destination_folder_name>
     Commands used for nighly regression in bink in staging
    - pytest -m "bmb_regression" --env staging --channel barclays  --alluredir=<new_destination_folder_name> 

Step 2 - Spin up the Allure results in the Browser

In the terminal, enter: 

- allure serve <new_destination_folder_name>

This should automatically collect the generated results from the destination folder, then 
open a browser window displaying the allure report.


*IMPORTANT*
if you have issues with using the allure command e.g. 'allure commnad not found' - you may need do brew install allure.
If issues persist you may need to check your path, project interpreter.

# Running inside Kubernetes

The project requires the following Environment Variables to function correctly:

- `NAME` - The Human Readable Name which should be sent with reports
  - Example: `Dev - Barclays`
- `TEAMS_WEBHOOK` - The Location to Alert to on Success/Failure
-  "Solutions Delivery/Alerts - Production" - https://hellobink.webhook.office.com/webhookb2/bf220ac8-d509-474f-a568-148982784d19@a6e2367a-92ea-4e5a-b565-723830bcc095/IncomingWebhook/7ae4116d366e4e5a92a65d9135a0664d/48aca6b1-4d56-4a15-bc92-8aa9d97300df
-  "Solutions Delivery/Alerts - QA" - https://hellobink.webhook.office.com/webhookb2/bf220ac8-d509-474f-a568-148982784d19@a6e2367a-92ea-4e5a-b565-723830bcc095/IncomingWebhook/0856493823a1484b9adfa37c942d2da4/48aca6b1-4d56-4a15-bc92-8aa9d97300df
- `SCHEDULE` - Uses Cron Syntax, use [crontab guru](https://crontab.guru) for help
  - Run at 22:05: `5 22 * * *`
  - Run at 22:00 on Mondays: `0 22 * * 1`
- `COMMAND` - The command to run
  - Barclays dev run: `pytest --html report.html --self-contained-html -s -m dev --channel barclays`
  - Bink dev run: `pytest --html report.html --self-contained-html -s -m dev --channel bink --env dev`
- `ALERT_ON_SUCCESS` - if run is successful, send report to Webhook
  - Default: `True`
- `ALERT_ON_FAILURE` - if run fails, send report to Webhook
  - Default: `True`
