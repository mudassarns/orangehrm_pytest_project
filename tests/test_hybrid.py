import pytest

pytestmark = pytest.mark.hybrid

def test_api_created_employee_visible_in_ui(
    dashboard,
    create_employee_api
):
    employee_data, employee_details = create_employee_api

    employee_id = employee_details["data"]["employeeId"]

    # UI verification will go here
    employee_list = dashboard.go_to_pim()
    result_count = employee_list.search_employee_by_id(employee_id)

    assert result_count == 1


def test_ui_created_employee_visible_in_api(
    create_employee,
    orangehrm_api
):
    employee_data, employee_details = create_employee

    emp_number = employee_details.get_employee_number()

    response = orangehrm_api.get_employee(emp_number)

    assert response.status_code == 200
    assert response.json()["data"]["employeeId"] == employee_data["employee_id"]

def test_api_updated_employee_visible_in_ui(
    orangehrm_api,
    create_employee_api,
    dashboard
):
    employee_data, employee_details = create_employee_api

    emp_number = employee_details["data"]["empNumber"]

    updated_first_name = "UpdatedName"
    updated_middle_name = "UpdatedMiddle"
    updated_last_name = "UpdatedLast"

    response = orangehrm_api.update_employee(
        emp_number,
        employee_data["employee_id"],
        updated_first_name,
        updated_middle_name,
        updated_last_name
    )

    assert response.status_code == 200

    employee_list = dashboard.go_to_pim()
    result_count = employee_list.search_employee_by_id(
        employee_data["employee_id"]
    )

    assert result_count == 1

    row_text = employee_list.get_first_result_text()

    assert "UpdatedName" in row_text
    assert "UpdatedMiddle" in row_text
    assert "UpdatedLast" in row_text
    assert employee_data["employee_id"] in row_text

def test_ui_deleted_employee_not_found_in_api(
    create_employee,
    orangehrm_api
):
    employee_data, employee_details = create_employee

    emp_number = employee_details.get_employee_number()

    employee_list = employee_details.go_to_employee_list()

    result_count = employee_list.search_employee_by_id(
        employee_data["employee_id"]
    )

    assert result_count == 1

    employee_list.delete_first_employee()

    result_count = employee_list.search_employee_by_id(
        employee_data["employee_id"]
    )

    assert result_count == 0

    response = orangehrm_api.get_employee(emp_number)

    assert response.status_code == 422