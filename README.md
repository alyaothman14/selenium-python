About
This is a test project to setup selenium wiht python and server report using allure on Github
Project Setup
brew install allure
pipenv install
pipenv run pytest -k "chrome" or pipenv run pytest -k "firefox" or pipenv run pytest
allure serve to generate report locally