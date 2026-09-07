from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.employee_details_page import EmployeeDetailsPage


class AddEmployeePage(BasePage):

    ADD_EMPLOYEE_HEADER = (
        By.XPATH,
        "//h6[normalize-space()='Add Employee']"
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

    EMPLOYEE_ID = (
        By.XPATH,
        "//label[normalize-space()='Employee Id']/ancestor::div[contains(@class,'oxd-input-group')]//input"
    )

    SAVE_BUTTON = (
        By.CSS_SELECTOR,
        "button[type='submit']"
    )

    SUCCESS_TOAST = (
        By.CSS_SELECTOR,
        "#oxd-toaster_1"
    )

    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_form_loader()
        self.wait_for_visible(self.ADD_EMPLOYEE_HEADER)

    def enter_first_name(self, first_name):
        self.enter_text(self.FIRST_NAME, first_name)

    def enter_middle_name(self, middle_name):
        self.enter_text(self.MIDDLE_NAME, middle_name)

    def enter_last_name(self, last_name):
        self.enter_text(self.LAST_NAME, last_name)

    def enter_employee_id(self, employee_id):
        self.enter_text(self.EMPLOYEE_ID, employee_id)

    def save(self):
        self.click(self.SAVE_BUTTON)
        self.wait_for_visible(self.SUCCESS_TOAST)
        return EmployeeDetailsPage(self.driver)