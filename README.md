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
    4. Install Azure CLI and login to Azure for Key Vault access
        `brew install azure-cli`
        `az login`
   
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
        
Check 