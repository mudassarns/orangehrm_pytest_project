from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException
)
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:

    FORM_LOADER = (
        By.CSS_SELECTOR,
        ".oxd-form-loader"
    )

    SIDEPANEL = (
        By.CSS_SELECTOR,
        ".oxd-sidepanel"
    )

    HAMBURGER = (
        By.CSS_SELECTOR,
        ".oxd-topbar-header-hamburger"
    )

    def __init__(self, driver):
        self.driver = driver

    def wait_for_form_loader(self):
        self.wait_for_invisible(self.FORM_LOADER)

    def wait_for_visible(self, locator):
        return WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_invisible(self, locator):
        return WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator):
        return WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(locator)
        )

    def scroll_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )

    def click(self, locator):
        element = self.wait_for_clickable(locator)
        self.scroll_into_view(element)
        element.click()

    def enter_text(self, locator, text):
        def click_input(driver):
            try:
                element = driver.find_element(*locator)
                if not element.is_displayed() or not element.is_enabled():
                    return False

                self.scroll_into_view(element)
                element.click()
                return element

            except (
                StaleElementReferenceException,
                ElementClickInterceptedException
            ):
                return False

        element = WebDriverWait(self.driver, 15).until(click_input)

        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(text)

    def get_input_value(self, locator):
        element = self.wait_for_visible(locator)
        return element.get_attribute("value")

    def restore_cookie(self, cookie):
        self.driver.delete_cookie(cookie["name"])
        self.driver.add_cookie(cookie)
        self.driver.refresh()
        logger.info("SESSION COOKIE RESTORED")

    def ensure_sidepanel_expanded(self):
        sidepanel = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SIDEPANEL)
        )

        if sidepanel.size["width"] == 0:
            hamburger = self.wait_for_visible(self.HAMBURGER)

            self.driver.execute_script(
                "arguments[0].click();",
                hamburger
            )

            WebDriverWait(self.driver, 10).until(
                lambda _:
                self.wait_for_visible(self.SIDEPANEL).size["width"] > 0
            )