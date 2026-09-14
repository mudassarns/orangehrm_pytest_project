from jsonschema import validate


EMPLOYEE_SCHEMA = {
    "type": "object",
    "required": [
        "empNumber",
        "firstName",
        "lastName",
        "employeeId",
        "terminationId",
    ],
    "properties": {
        "empNumber": {
            "type": "integer"
        },
        "firstName": {
            "type": "string"
        },
        "lastName": {
            "type": "string"
        },
        "middleName": {
            "type": ["string", "null"]
        },
        "employeeId": {
            "type": "string"
        },
        "terminationId": {
            "type": ["integer", "null"]
        }
    }
}


def validate_employee_schema(employee_data):
    validate(
        instance=employee_data,
        schema=EMPLOYEE_SCHEMA
    )

EMPLOYEE_UPDATE_SCHEMA = {
    "type": "object",
    "required": [
        "empNumber",
        "firstName",
        "lastName",
        "middleName",
        "employeeId",
        "otherId",
        "drivingLicenseNo",
        "drivingLicenseExpiredDate",
        "gender",
        "maritalStatus",
        "birthday",
        "terminationId",
        "nationality",
    ],
    "properties": {
        "empNumber": {
            "type": "integer"
        },
        "firstName": {
            "type": "string"
        },
        "lastName": {
            "type": "string"
        },
        "middleName": {
            "type": "string"
        },
        "employeeId": {
            "type": "string"
        },
        "otherId": {
            "type": "string"
        },
        "drivingLicenseNo": {
            "type": "string"
        },
        "drivingLicenseExpiredDate": {
            "type": ["string", "null"]
        },
        "gender": {
            "type": ["string", "null"]
        },
        "maritalStatus": {
            "type": "string"
        },
        "birthday": {
            "type": ["string", "null"]
        },
        "terminationId": {
            "type": ["integer", "null"]
        },
        "nationality": {
            "type": "object",
            "required": [
                "id",
                "name"
            ],
            "properties": {
                "id": {
                    "type": ["integer", "null"]
                },
                "name": {
                    "type": ["string", "null"]
                }
            }
        }
    }
}


def validate_employee_update_schema(employee_data):
    validate(
        instance=employee_data,
        schema=EMPLOYEE_UPDATE_SCHEMA
    )


EMPLOYEE_LIST_SCHEMA = {
    "type": "object",
    "required": [
        "data",
        "meta",
        "rels"
    ],
    "properties": {
        "data": {
            "type": "array",
            "items": EMPLOYEE_SCHEMA
        },
        "meta": {
            "type": "object"
        },
        "rels": {
            "type": "array"
        }
    }
}


def validate_employee_list_schema(response_data):
    validate(
        instance=response_data,
        schema=EMPLOYEE_LIST_SCHEMA
    )


EMPLOYEE_ERROR_SCHEMA = {
    "type": "object",
    "required": [
        "error"
    ],
    "properties": {
        "error": {
            "type": "object",
            "required": [
                "status",
                "message",
                "data"
            ],
            "properties": {
                "status": {
                    "type": "string"
                },
                "message": {
                    "type": "string"
                },
                "data": {
                    "type": "object",
                    "required": [
                        "invalidParamKeys"
                    ],
                    "properties": {
                        "invalidParamKeys": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        }
    }
}


def validate_employee_error_schema(error_data):
    validate(
        instance=error_data,
        schema=EMPLOYEE_ERROR_SCHEMA
    )
