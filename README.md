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
    * Using `pipenv`, run tests as `pipenv run python -m pytest`.
    * Use the "-m" option to filter tests by bdd tags.
    * Use --channel to pass 'barclays' /  'bink' channels. Default is bink
        eg: pytest -s --channel barclays -m "add"
    * Use --env to execute the tests in 'dev' / 'staging'. Default is dev
        eg: pytest -s --env staging -m "add"
        
#####   For further details, the confluence link will be provided once migration started.