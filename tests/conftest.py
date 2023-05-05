from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import pytest
from pages.country_code_page import SportyCountryCodePage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from pages.login_page import SportyLoginPage
from pages.nav_bar_page import SportyNavBarPage
import allure
from allure_commons.types import AttachmentType
import json
# read command line options
# allow to define browser
# To run only one browser pass -k "chrome"


def pytest_generate_tests(metafunc):
    browsers = ["chrome", "firefox"]
    if "browser" in metafunc.fixturenames:
        metafunc.parametrize("browser", browsers)


@pytest.fixture(scope="function")
def setup(request: pytest.FixtureRequest, browser):
    if (browser in ("chrome")):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.set_capability(
            "goog:loggingPrefs", {"browser": "ALL"}
        )

    match browser:
        case "chrome":
            chrome_options.headless = True
            driver = webdriver.Chrome(service=ChromeService(
                ChromeDriverManager().install()), options=chrome_options)
        case "firefox":
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.headless = True
            driver = webdriver.Firefox(service=FirefoxService(
                GeckoDriverManager().install()), options=firefox_options)
    driver.get("https://sporty.com/news/latest")
    # make sure the page is loaded
    wait = WebDriverWait(driver, 30)
    wait.until(expected_conditions.visibility_of_element_located(
        ((By.XPATH, "//*[contains(text(),'Customise your')]"))))
    driver.implicitly_wait(10)
    request.cls.driver = driver
    request.cls.login_page = SportyLoginPage(driver)
    request.cls.nav_bar = SportyNavBarPage(driver)
    request.cls.country_code = SportyCountryCodePage(driver)
    yield driver
    allure.dynamic.tag(driver.capabilities["browserName"])
    if (browser in ("chrome", "chrome_headless")):
        allure.attach(body=json.dumps(driver.get_log("browser"), indent=4),
                      name="Console Logs", attachment_type=allure.attachment_type.JSON)
    allure.attach(driver.get_screenshot_as_png(),
                  name="Screenshot", attachment_type=AttachmentType.PNG)
    driver.quit()
