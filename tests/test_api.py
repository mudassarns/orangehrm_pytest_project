from utils.test_data import generate_employee_data
import pytest
from schemas.employee_schema import (
    validate_employee_error_schema,
    validate_employee_list_schema,
    validate_employee_schema,
    validate_employee_update_schema,
)


def test_get_employees(orangehrm_api):
    response = orangehrm_api.get_employees()

    assert response.status_code == 200

    data = response.json()
    validate_employee_list_schema(data)

    assert data["meta"]["total"] >= 1

def test_get_employees_with_limit(orangehrm_api):
    response = orangehrm_api.get_employees(limit=1)

    assert response.status_code == 200

    data = response.json()
    validate_employee_list_schema(data)

    assert len(data["data"]) <= 1


def test_create_employee( create_employee_api):
    employee_data, employee_details = create_employee_api
    validate_employee_schema(employee_details["data"])

    assert employee_details["data"]["empNumber"] > 0
    assert employee_details["data"]["employeeId"] == employee_data["employee_id"]

def test_create_and_get_employee(orangehrm_api, create_employee_api):
    employee_data, employee_details = create_employee_api
    validate_employee_schema(employee_details["data"])

    emp_number = employee_details["data"]["empNumber"]

    assert employee_details["data"]["employeeId"] == employee_data["employee_id"]

    get_response = orangehrm_api.get_employee(emp_number)

    assert get_response.status_code == 200

    get_data = get_response.json()
    validate_employee_schema(get_data["data"])

    assert get_data["data"]["empNumber"] == emp_number
    assert get_data["data"]["employeeId"] == employee_data["employee_id"]
    assert get_data["data"]["firstName"] == employee_data["first_name"]
    assert get_data["data"]["lastName"] == employee_data["last_name"]

def test_employee_crud(orangehrm_api, create_employee_api):
    employee_data, employee_details = create_employee_api
    validate_employee_schema(employee_details["data"])

    emp_number = employee_details["data"]["empNumber"]

    assert employee_details["data"]["employeeId"] == employee_data["employee_id"]

    update_response = orangehrm_api.update_employee(
        emp_number,
        employee_data["employee_id"],
        "ApiUpdated",
        "TestUpdated",
        "EmployeeUpdated"
    )

    assert update_response.status_code == 200

    update_data = update_response.json()

    validate_employee_update_schema(update_data["data"])

    get_response = orangehrm_api.get_employee(emp_number)

    assert get_response.status_code == 200

    get_data = get_response.json()
    validate_employee_schema(get_data["data"])

    assert get_data["data"]["firstName"] == "ApiUpdated"
    assert get_data["data"]["middleName"] == "TestUpdated"
    assert get_data["data"]["lastName"] == "EmployeeUpdated"

def test_get_invalid_employee(orangehrm_api):
    response = orangehrm_api.get_employee(999999)

    assert response.status_code == 422

    data = response.json()
    validate_employee_error_schema(data)

    assert data["error"]["status"] == "422"
    assert data["error"]["message"] == "Invalid Parameter"


@pytest.mark.parametrize(
    "first_name",
    [
        pytest.param(None, id="null"),
        pytest.param("", id="blank"),
        pytest.param(12345, id="wrong_type"),
    ]
)
def test_create_employee_invalid_first_name(orangehrm_api, first_name):
    employee_data = generate_employee_data()
    employee_data["first_name"] = first_name

    response = orangehrm_api.create_employee(employee_data)

    assert response.status_code == 422
    validate_employee_error_schema(response.json())

def test_get_employee_invalid_id_type(orangehrm_api):
    response = orangehrm_api.get_employee("abc")

    assert response.status_code == 404
