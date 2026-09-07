def test_employee_exists(db):

    employee_id = "0001"

    db.execute_query(
        """
        SELECT emp_number, employee_id, emp_firstname, emp_lastname
        FROM hs_hr_employee
        WHERE employee_id = ?
        """,
        (employee_id,)
    )

    result = db.fetch_one()

    assert result is not None
    print(result)
    assert result["employee_id"] == employee_id


def test_employee_does_not_exist(db):

    employee_id = "9999"

    db.execute_query(
        """
        SELECT emp_number, employee_id, emp_firstname, emp_lastname
        FROM hs_hr_employee
        WHERE employee_id = ?
        """,
        (employee_id,)
    )

    result = db.fetch_one()

    assert result is None


def test_fetch_all_employees(db):

    db.execute_query(
        """
        SELECT emp_number, employee_id, emp_firstname, emp_lastname
        FROM hs_hr_employee
        """
    )

    results = db.fetch_all()
    print(results)

    for row in results:
        employee_id = row["employee_id"]
        print(employee_id)

    assert results


def test_fetch_one_employee(db):

    db.execute_query(
        """
        SELECT emp_number, employee_id, emp_firstname, emp_lastname
        FROM hs_hr_employee
        WHERE employee_id = ?
        """,
        ("0001",)
    )

    result = db.fetch_one()

    assert result is not None
    assert result["employee_id"] == "0001"


def test_ui_created_employee_exists_in_database(create_employee, db):

    employee_data, employee_details = create_employee

    employee_id = employee_data["employee_id"]

    db.execute_query(
        """
        SELECT emp_number, employee_id, emp_firstname, emp_lastname
        FROM hs_hr_employee
        WHERE employee_id = ?
        """,
        (employee_id,)
    )

    result = db.fetch_one()

    assert result is not None
    assert result["employee_id"] == employee_id
    assert result["emp_firstname"] == employee_data["first_name"]
    assert result["emp_lastname"] == employee_data["last_name"]


def test_ui_updated_employee_exists_in_database(create_employee, db):

    employee_data, employee_details = create_employee

    employee_id = employee_data["employee_id"]

    updated_first_name = "Updated"
    updated_middle_name = "Middle"
    updated_last_name = "Employee"

    employee_details.enter_first_name(updated_first_name)
    employee_details.enter_middle_name(updated_middle_name)
    employee_details.enter_last_name(updated_last_name)
    employee_details.save()

    emp_number = employee_details.get_employee_number()

    db.execute_query(
        """
        SELECT emp_number, employee_id, emp_firstname, emp_lastname
        FROM hs_hr_employee
        WHERE emp_number = ?
        AND employee_id = ?
        """,
        (emp_number, employee_id)
    )

    result = db.fetch_one()

    assert result is not None
    assert result["emp_number"] == int(emp_number)
    assert result["employee_id"] == employee_id
    assert result["emp_firstname"] == updated_first_name
    assert result["emp_lastname"] == updated_last_name
    

def test_api_created_employee_exists_in_database(create_employee_api, db):
    employee_data, employee_details = create_employee_api

    emp_number = employee_details["data"]["empNumber"]
    employee_id = employee_data["employee_id"]

    db.execute_query(
        """
        SELECT emp_number, employee_id, emp_firstname, emp_lastname
        FROM hs_hr_employee
        WHERE emp_number = ?
        AND employee_id = ?
        """,
        (emp_number, employee_id)
    )

    result = db.fetch_one()

    assert result is not None
    assert result["emp_number"] == emp_number
    assert result["employee_id"] == employee_id
    assert result["emp_firstname"] == employee_data["first_name"]
    assert result["emp_lastname"] == employee_data["last_name"]


def test_api_updated_employee_exists_in_database(
    create_employee_api,
    orangehrm_api,
    db
):
    employee_data, employee_details = create_employee_api

    emp_number = employee_details["data"]["empNumber"]

    updated_employee_id = employee_data["employee_id"] + "99"
    updated_first_name = "Updated"
    updated_middle_name = "Middle"
    updated_last_name = "Employee"

    update_response = orangehrm_api.update_employee(
        emp_number,
        updated_employee_id,
        updated_first_name,
        updated_middle_name,
        updated_last_name
    )

    assert update_response.status_code == 200

    db.execute_query(
        """
        SELECT emp_number, employee_id, emp_firstname, emp_lastname
        FROM hs_hr_employee
        WHERE emp_number = ?
        """,
        (emp_number,)
    )

    result = db.fetch_one()

    assert result is not None
    assert result["emp_number"] == emp_number
    assert result["employee_id"] == updated_employee_id
    assert result["emp_firstname"] == updated_first_name
    assert result["emp_lastname"] == updated_last_name


def test_api_deleted_employee_does_not_exist_in_database(
    create_employee_api,
    orangehrm_api,
    db
):
    employee_data, employee_details = create_employee_api

    emp_number = employee_details["data"]["empNumber"]

    delete_response = orangehrm_api.delete_employee(emp_number)

    assert delete_response.status_code == 200

    db.execute_query(
        """
        SELECT emp_number, employee_id, emp_firstname, emp_lastname
        FROM hs_hr_employee
        WHERE emp_number = ?
        """,
        (emp_number,)
    )

    result = db.fetch_one()

    assert result is None


def test_employee_count(db):

    db.execute_query(
        """
        SELECT COUNT(*) AS employee_count
        FROM hs_hr_employee
        """
    )

    result = db.fetch_one()

    assert result is not None
    assert result["employee_count"] >= 1