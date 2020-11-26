[Draft - Will enhance further during migration process]

# BinkAPI-TestAutomation-pytest-bdd
This is a framework design in Python for the test automation of Bink's APIs.
Currently, the codebase contains classes required for migration
Once migration started, this repository will contain test automation scripts for Bink API's testing 
and Django UI verifications

#  Set Up
This project requires an up-to-date version of Python 3 (Currently using Python 3.8)
 It also uses [pipenv](https://pipenv.readthedocs.io/) to manage packages.

To set up this project on your local machine:

    1. Clone it from this GitLab repository.
    2. Run `pipenv install` from the terminal in the project's root directory.
    3. For Django Web UI tests, install the appropriate browser and WebDriver executable
        * Current Django tests use Chrome and
         [chromedriver](https://chromedriver.chromium.org/downloads) 
       
# Running Tests
    * Run tests simply using the `pytest` command.
    
    * Use the "-m" option to filter tests by bdd tags. 
        eg1: pytest -m "enrol" : Execute Enrol Journey for all merchants
        eg2: pytest -m "enrol and iceland" :  Execute Enrol Journey for Iceland only
        eg3: pytest -m "enrol or add" : Execute Enrol, Add Journey for all merchants
        
    * Pass '--channel' argument in execution command to pass 'barclays' /  'bink' channels. Default is bink
        eg: pytest -m "enrol" --channel barclays
        
    * Pass '--env' argument in execution command to determine the test environment as 'dev' / 'staging'. Default is dev
        eg: pytest -m "enrol" --env staging --channel barclays
        
# Running inside Kubernetes

The project requires the following Environment Variables to function correctly:

- `NAME` - The Human Readable Name which should be sent with reports
  - Example: `Dev - Barclays`
- `TEAMS_WEBHOOK` - The Location to Alert to on Success/Failure
  - "Solutions Delivery/Alerts - Production" - `https://outlook.office.com/webhook/bf220ac8-d509-474f-a568-148982784d19@a6e2367a-92ea-4e5a-b565-723830bcc095/IncomingWebhook/7ae4116d366e4e5a92a65d9135a0664d/48aca6b1-4d56-4a15-bc92-8aa9d97300df`
  - "Solutions Delivery/Alerts - QA" - `https://outlook.office.com/webhook/bf220ac8-d509-474f-a568-148982784d19@a6e2367a-92ea-4e5a-b565-723830bcc095/IncomingWebhook/0856493823a1484b9adfa37c942d2da4/48aca6b1-4d56-4a15-bc92-8aa9d97300df`
  - "Solutions Delivery/QA" - `https://outlook.office.com/webhook/bf220ac8-d509-474f-a568-148982784d19@a6e2367a-92ea-4e5a-b565-723830bcc095/IncomingWebhook/5d25733db5994811b6ee4049ef74713e/48aca6b1-4d56-4a15-bc92-8aa9d97300df`
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
