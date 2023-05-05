from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import pytest
from pages.country_code_page import SportyCountryCodePage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By;
from pages.login_page import SportyLoginPage
from pages.nav_bar_page import SportyNavBarPage
import allure
from allure_commons.types import AttachmentType
import json
import os

# read command line options
# allow to define browser
def pytest_addoption(parser:pytest.Parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser available chrome,firefox,chrome_headless")
  
@pytest.fixture(scope="function")
def setup(request:pytest.FixtureRequest):
    browser=request.config.getoption("--browser")
    if(browser in("chrome","chrome_headless")):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.set_capability(
                "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
            )
        chrome_options.add_argument("disable-dev-shm-usage")

    match browser:
        case "chrome":
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
        case "chrome_headless":
            chrome_options.add_argument("headless=new")
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)    
        case "firefox":
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.get("https://sporty.com/news/latest")
    # make sure the page is loaded
    wait= WebDriverWait(driver,30)
    wait.until(expected_conditions.visibility_of_element_located(((By.XPATH,"//*[contains(text(),'Customise your')]"))))
    driver.implicitly_wait(10)
    request.cls.driver=driver
    request.cls.login_page=SportyLoginPage(driver)
    request.cls.nav_bar= SportyNavBarPage(driver)
    request.cls.country_code=SportyCountryCodePage(driver)
    yield driver
      

@pytest.fixture(autouse=True)
def attach_artifacts_on_failure(request):
    yield
    environment_properties = {
        "Browser": request.cls.driver.name,
        "Driver_Version": request.cls.driver.capabilities['browserVersion'],
    }
    allure_env_path = os.path.join("allure-results", 'environment.properties')
    with open(allure_env_path, 'w') as f:
        data = '\n'.join([f'{variable}={value}' for variable, value in environment_properties.items()])
        f.write(data)
    allure.attach(body=json.dumps(request.cls.driver.get_log("browser"), indent=4), name="Console Logs",attachment_type=allure.attachment_type.JSON)
    allure.attach(request.cls.driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
    request.cls.driver.quit()
    request.cls.driver.close()  


