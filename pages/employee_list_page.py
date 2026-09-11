
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.add_employee_page import AddEmployeePage
from pages.employee_details_page import EmployeeDetailsPage
from utils.locator_utils import LocatorUtils
from utils.logger import get_logger
from selenium.common.exceptions import (StaleElementReferenceException)

logger = get_logger(__name__)


class EmployeeListPage(BasePage):

    EMPLOYEE_LIST_TAB = (
        By.XPATH,
        "//a[normalize-space()='Employee List']"
    )

    ADD_EMPLOYEE_TAB = (
        By.XPATH,
        "//a[normalize-space()='Add Employee']"
    )

    EMPLOYEE_INFORMATION_TOGGLE = (
        By.XPATH,
        "//h5[normalize-space()='Employee Information']"
        "/ancestor::div[contains(@class,'oxd-table-filter-header')]"
        "//button"
    )

    SEARCH_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Search']"
    )

    EMPLOYEE_RESULT_ROWS = (
        By.CSS_SELECTOR,
        ".oxd-table-body .oxd-table-card"
    )

    EMPLOYEE_ROW = (
        By.CSS_SELECTOR,
        ".oxd-table-body .oxd-table-card:first-child"
    )

    DELETE_EMPLOYEE_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'oxd-table-card')][1]//button[.//i[contains(@class,'bi-trash')]]"
    )

    CONFIRM_DELETE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Yes, Delete']"
    )
    NO_RECORDS_FOUND = (
    By.XPATH,
    "//span[normalize-space()='No Records Found']"
)

    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_visible(self.EMPLOYEE_LIST_TAB)

    # def go_to_add_employee(self):
    #     self.click(self.ADD_EMPLOYEE_TAB)
    #     return AddEmployeePage(self.driver)

    def go_to_add_employee(self):
        print("Browser:", self.driver.capabilities.get("browserName"))
        print("Browser version:", self.driver.capabilities.get("browserVersion"))
        print("Window size:", self.driver.get_window_size())
        print("Viewport width:", self.driver.execute_script("return window.innerWidth"))

        nav = self.driver.find_element(
            By.CSS_SELECTOR,
            ".oxd-topbar-body-nav"
        )

        ul = self.driver.find_element(
            By.CSS_SELECTOR,
            ".oxd-topbar-body-nav > ul"
        )

        print("NAV width:", nav.size["width"])
        print("UL width:", ul.size["width"])
        print(
            "UL clientWidth:",
            self.driver.execute_script(
                "return arguments[0].clientWidth", ul
            )
        )
        print(
            "UL scrollWidth:",
            self.driver.execute_script(
                "return arguments[0].scrollWidth", ul
            )
        )

        items = self.driver.find_elements(
            By.CSS_SELECTOR,
            ".oxd-topbar-body-nav > ul > li"
        )

        for index, item in enumerate(items):
            print(
                f"ITEM {index}: "
                f"text='{item.text}', "
                f"width={item.size['width']}, "
                f"displayed={item.is_displayed()}"
            )

        elements = self.driver.find_elements(
            By.XPATH,
            "//span[normalize-space()='More']"
        )

        print("MORE elements found:", len(elements))

        for index, element in enumerate(elements):
            print(
                f"MORE {index}: "
                f"displayed={element.is_displayed()}, "
                f"enabled={element.is_enabled()}"
            )

        self.click(self.ADD_EMPLOYEE_TAB)
        return AddEmployeePage(self.driver)

    def search_employee_by_id(self, employee_id):
        self.ensure_employee_information_expanded()
        employee_id_locator = LocatorUtils.input_by_label("Employee Id")
        logger.info(f"SEARCH START: Employee {employee_id}")

        self.enter_text(employee_id_locator, employee_id)
        self.click(self.SEARCH_BUTTON)

        WebDriverWait(self.driver, 15).until(
            lambda driver:
            self.is_employee_present(employee_id)
            or driver.find_elements(*self.NO_RECORDS_FOUND)
        )

        result_count = self.get_result_count()

        if result_count == 1:
            logger.info(
                f"UI VERIFICATION SUCCESS: Employee {employee_id} found"
            )

        return result_count

    def wait_for_result_count(self, expected_count):
        WebDriverWait(self.driver, 15).until(
            lambda driver: len(
                driver.find_elements(*self.EMPLOYEE_RESULT_ROWS)
            ) == expected_count
        )

    def get_result_count(self):
        return len(
            self.driver.find_elements(*self.EMPLOYEE_RESULT_ROWS)
        )

    def is_employee_present(self, employee_id):
        try:
            cells = self.driver.find_elements(
                By.CSS_SELECTOR,
                "[role='cell']"
            )

            for cell in cells:
                if cell.find_elements(
                    By.XPATH,
                    f".//div[normalize-space()='{employee_id}']"
                ):
                    return True

            return False

        except StaleElementReferenceException:
            return False

    def get_first_result_text(self):
        rows = self.driver.find_elements(*self.EMPLOYEE_RESULT_ROWS)
        return rows[0].text

    def open_employee_details(self):
        self.click(self.EMPLOYEE_ROW)
        return EmployeeDetailsPage(self.driver)

    def delete_first_employee(self):
        self.click(self.DELETE_EMPLOYEE_BUTTON)
        self.click(self.CONFIRM_DELETE_BUTTON)


    def ensure_employee_information_expanded(self):
        filter_area = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".oxd-table-filter-area")
            )   
        )

        if filter_area.value_of_css_property("display") == "none":
            self.click(self.EMPLOYEE_INFORMATION_TOGGLE)