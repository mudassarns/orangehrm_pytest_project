from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.employee_list_page import EmployeeListPage
from selenium.common.exceptions import TimeoutException


class DashboardPage(BasePage):

    DASHBOARD_HEADER = (By.XPATH, "//h6[normalize-space()='Dashboard']")
    PIM_MENU = (By.CSS_SELECTOR, "a[href='/web/index.php/pim/viewPimModule']")


    def is_dashboard_displayed(self):
        try:
            return self.wait_for_visible(self.DASHBOARD_HEADER).is_displayed()
        except TimeoutException:
            return False

    def go_to_pim(self):
        self.click(self.PIM_MENU)
        return EmployeeListPage(self.driver)
    