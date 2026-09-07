from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class EmployeeDetailsPage(BasePage):

    EMPLOYEE_LIST_TAB = (
        By.XPATH,
        "//a[normalize-space()='Employee List']"
    )

    PERSONAL_DETAILS_TAB = (
        By.XPATH,
        "//a[normalize-space()='Personal Details' and contains(@class,'--active')]"
    )

    FIRST_NAME = (
        By.CSS_SELECTOR,
        "input[name='firstName']"
    )

    MIDDLE_NAME = (
        By.CSS_SELECTOR,
        "input[name='middleName']"
    )

    LAST_NAME = (
        By.CSS_SELECTOR,
        "input[name='lastName']"
    )

    SAVE_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'horizontal-padding')]//button[@type='submit']"
    )

    SUCCESS_TOAST = (
        By.CSS_SELECTOR,
        "#oxd-toaster_1"
    )

    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_form_loader()
        self.wait_for_visible(self.PERSONAL_DETAILS_TAB)

    def go_to_employee_list(self):
        self.click(self.EMPLOYEE_LIST_TAB)

        from pages.employee_list_page import EmployeeListPage
        return EmployeeListPage(self.driver)

    def enter_first_name(self, first_name):
        self.enter_text(self.FIRST_NAME, first_name)

    def enter_middle_name(self, middle_name):
        self.enter_text(self.MIDDLE_NAME, middle_name)

    def enter_last_name(self, last_name):
        self.enter_text(self.LAST_NAME, last_name)

    def save(self):
        self.click(self.SAVE_BUTTON)
        self.wait_for_visible(self.SUCCESS_TOAST)
        return EmployeeDetailsPage(self.driver)

    def get_employee_number(self):
        url = self.driver.current_url
        return url.split("/empNumber/")[1]