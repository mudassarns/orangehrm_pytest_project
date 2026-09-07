import random


def generate_employee_id():
    return "".join(random.choices("0123456789", k=10))

def generate_employee_data():
    return {
        "first_name": "Mns",
        "middle_name": "Test",
        "last_name": "Emp",
        "employee_id": generate_employee_id()
    }