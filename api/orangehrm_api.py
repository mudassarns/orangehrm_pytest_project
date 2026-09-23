import requests
from api.base_api_client import BaseApiClient
from config import Config
import logging


logger = logging.getLogger(__name__)


class OrangeHRMApi(BaseApiClient):
    
    EMPLOYEES_ENDPOINT = "/web/index.php/api/v2/pim/employees"

    def __init__(self, cookie):
        super().__init__()

        self.base_url = Config.get("ORANGEHRM_BASE_URL")

        self.session.cookies.set(
            "_orangehrm",
            cookie["value"]
        )


    def get_employees(self, limit=None, offset=None):
        url = self.base_url + self.EMPLOYEES_ENDPOINT

        params = {}

        if limit is not None:
            params["limit"] = limit

        if offset is not None:
            params["offset"] = offset

        response = self._request(
            "GET",
            url,
            params=params
        )

        return response

    def get_employee(self, emp_number):
        url = f"{self.base_url}{self.EMPLOYEES_ENDPOINT}/{emp_number}"

        response = self._request("GET", url)

        return response

    def create_employee(self, employee_data):
        url = self.base_url + self.EMPLOYEES_ENDPOINT

        payload = {
            "firstName": employee_data["first_name"],
            "middleName": employee_data["middle_name"],
            "lastName": employee_data["last_name"],
            "empPicture": None,
            "employeeId": employee_data["employee_id"]
        }

        response = self._request(
            "POST",
            url,
            json=payload
        )

        return response

    def update_employee(self, emp_number, employee_id, first_name, middle_name, last_name):
        url = (
            f"{self.base_url}"
            f"{self.EMPLOYEES_ENDPOINT}/{emp_number}/personal-details"
        )

        payload = {
            "firstName": first_name,
            "middleName": middle_name,
            "lastName": last_name,
            "employeeId": employee_id
        }

        response = self._request(
            "PUT",
            url,
            json=payload
        )

        return response

    def delete_employee(self, emp_number):
        url = self.base_url + self.EMPLOYEES_ENDPOINT

        payload = {
            "ids": [emp_number]
        }

        response = self._request(
            "DELETE",
            url,
            json=payload
        )

        return response
