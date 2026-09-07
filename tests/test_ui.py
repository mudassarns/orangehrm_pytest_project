from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config import Config
import pytest

pytestmark = pytest.mark.ui


def test_orangehrm_login(driver):
    driver.get(Config.get("ORANGEHRM_BASE_URL"))

    login_page = LoginPage(driver)
    login_page.login(
        Config.get("ORANGEHRM_USERNAME"),
        Config.get("ORANGEHRM_PASSWORD")
    )
    dashboard = DashboardPage(driver)
    assert dashboard.is_dashboard_displayed()
    

def test_add_employee(create_employee):
    employee_data, employee_details = create_employee
    employee_list = employee_details.go_to_employee_list()

    result_count = employee_list.search_employee_by_id(
        employee_data["employee_id"]
    )

    assert result_count == 1


def test_search_employee_by_id(create_employee):
    employee_data, employee_details = create_employee
    employee_list = employee_details.go_to_employee_list()

    result_count = employee_list.search_employee_by_id(
        employee_data["employee_id"]
    )

    assert result_count == 1


def test_edit_employee(create_employee):
    employee_data, employee_details = create_employee
    employee_list = employee_details.go_to_employee_list()

    employee_list.search_employee_by_id(
        employee_data["employee_id"]
    )

    employee_details = employee_list.open_employee_details()

    employee_details.enter_first_name("Updated")
    employee_details.enter_middle_name("UpdatedMiddle")
    employee_details.enter_last_name("UpdatedLast")
    employee_details.save()

    employee_list = employee_details.go_to_employee_list()

    employee_list.search_employee_by_id(
        employee_data["employee_id"]
    )

    row_text = employee_list.get_first_result_text()

    assert "Updated UpdatedMiddle" in row_text
    assert "UpdatedLast" in row_text
    assert employee_data["employee_id"] in row_text


def test_delete_employee(create_employee):
    employee_data, employee_details = create_employee
    employee_list = employee_details.go_to_employee_list()
    employee_id = employee_data["employee_id"]
    result_count = employee_list.search_employee_by_id(employee_id)
    assert result_count == 1

    employee_list.delete_first_employee()
    result_count = employee_list.search_employee_by_id(employee_id)
    assert result_count == 0