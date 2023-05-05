
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By;
from selenium.webdriver import Chrome, Firefox
from typing import Tuple;
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from typing import Tuple, Union


class BasePage:
    def __init__(self,driver: Union[Chrome, Firefox]):
        self.driver=driver
        self.wait= WebDriverWait(driver,30)

    def click(self,locator:Tuple[By,str])->None:
        element: WebElement = self.wait.until(expected_conditions.visibility_of_element_located(locator))
        element: WebElement = self.wait.until(expected_conditions.element_to_be_clickable(locator))

        element.click()

    def fill_text(self,locator:Tuple[By,str],text:str)->None:
        element: WebElement = self.wait.until(expected_conditions.visibility_of_element_located(locator))
        element.clear()
        element.click()
        element.send_keys(text)
    def get_text(self,locator:Tuple[By,str])->str:
        element: WebElement = self.wait.until(expected_conditions.visibility_of_element_located(locator))
        return element.text
    def get_image_url(self,locator:Tuple[By,str])->str:
        element: WebElement = self.wait.until(expected_conditions.visibility_of_element_located(locator))
        return element.get_attribute("src")