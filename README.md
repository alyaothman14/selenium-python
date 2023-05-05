# Selenium with Python and Allure on GitHub

This is a test project to set up Selenium with Python and generate a report using Allure.
The project utilize 
- Page object modal to define different pages
- Github actions to run selenium, generate allure reports and upload to github pages
- Test runs on both chrome and firefox
- Reports includes screenshots and console logs for chrome

## Project Setup

1. Install Allure:
```bash
brew install allure
```
2. Install the required Python packages:
```bash
pip install
```
3. Run the tests using one of the following commands:
```bash
pipenv run pytest -k "chrome" to run chrome only
pipenv run pytest -k "firefox" to run firefox only
pipenv run pytest to run all
```
4. Generate the Allure report:
```bash
allure serve
```

#You can find the allure results [here](https://alyaothman14.github.io/selenium-python/37/#suites/e073428b7a30684178c11e51fcc1e40c/504c9285634c38c/)
