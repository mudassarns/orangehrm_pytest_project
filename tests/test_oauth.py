import base64
import hashlib
import secrets
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

import requests

from config import Config
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.test_data import generate_employee_data


class CallbackHandler(BaseHTTPRequestHandler):
    authorization_code = None

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        CallbackHandler.authorization_code = query.get("code", [None])[0]

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OAuth callback received.")

    def log_message(self, format, *args):
        return


def test_orangehrm_oauth_flow(driver):
    redirect_uri = "http://127.0.0.1:8765/callback"

    verifier = secrets.token_urlsafe(64)

    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()
    ).rstrip(b"=").decode()

    server = HTTPServer(("127.0.0.1", 8765), CallbackHandler)

    server_thread = threading.Thread(
        target=server.serve_forever,
        daemon=True
    )
    server_thread.start()

    try:
        params = {
            "response_type": "code",
            "client_id": "ci_oauth_probe",
            "redirect_uri": redirect_uri,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "state": "ci-test"
        }

        authorize_url = (
            f"{Config.get('ORANGEHRM_BASE_URL')}/web/index.php/oauth2/authorize?"
            f"{urlencode(params)}"
        )

        driver.get(authorize_url)

        login_page = LoginPage(driver)
        login_page.login(
            Config.get("ORANGEHRM_USERNAME"),
            Config.get("ORANGEHRM_PASSWORD")
        )
        print(f"OAUTH INVALID REDIRECT URL: {driver.current_url}")
        print(f"OAUTH INVALID REDIRECT TITLE: {driver.title}")
        print(f"OAUTH INVALID REDIRECT SOURCE: {driver.page_source[:3000]}")

        allow_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                ("xpath", "//button[normalize-space()='Allow Access']")
            )
        )
        allow_button.click()

        WebDriverWait(driver, 30).until(
            lambda d: d.current_url.startswith(redirect_uri)
        )

        authorization_code = parse_qs(
            urlparse(driver.current_url).query
        ).get("code", [None])[0]

        assert authorization_code is not None, (
            f"OAuth authorization code was not found in callback URL: "
            f"{driver.current_url}"
        )

        token_response = requests.post(
            f"{Config.get('ORANGEHRM_BASE_URL')}/web/index.php/oauth2/token",
            data={
                "grant_type": "authorization_code",
                "client_id": "ci_oauth_probe",
                "redirect_uri": redirect_uri,
                "code": authorization_code,
                "code_verifier": verifier
            },
            timeout=15
        )

        assert token_response.status_code == 200, (
            f"Token request failed: "
            f"{token_response.status_code} {token_response.text}"
        )

        token_data = token_response.json()
        access_token = token_data["access_token"]

        api_response = requests.get(
            f"{Config.get('ORANGEHRM_BASE_URL')}/web/index.php/api/v2/pim/employees",
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            timeout=15
        )

        assert api_response.status_code == 200, (
            f"Authenticated API request failed: "
            f"{api_response.status_code} {api_response.text}"
        )

        employee_data = generate_employee_data()

        create_response = requests.post(
            f"{Config.get('ORANGEHRM_BASE_URL')}/web/index.php/api/v2/pim/employees",
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            json={
                "firstName": employee_data["first_name"],
                "middleName": employee_data["middle_name"],
                "lastName": employee_data["last_name"],
                "empPicture": None,
                "employeeId": employee_data["employee_id"]
            },
            timeout=15
        )

        assert create_response.status_code == 200, (
            f"OAuth create employee failed: "
            f"{create_response.status_code} {create_response.text}"
        )

        created_employee = create_response.json()["data"]

        assert created_employee["empNumber"] > 0
        assert created_employee["employeeId"] == employee_data["employee_id"]

    finally:
        server.shutdown()
        server.server_close()

def test_orangehrm_oauth_rejects_invalid_redirect_uri(driver):
    invalid_redirect_uri = "http://127.0.0.1:9999/callback"

    verifier = secrets.token_urlsafe(64)

    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()
    ).rstrip(b"=").decode()

    params = {
        "response_type": "code",
        "client_id": "ci_oauth_probe",
        "redirect_uri": invalid_redirect_uri,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": "ci-test"
    }

    authorize_url = (
        f"{Config.get('ORANGEHRM_BASE_URL')}/web/index.php/oauth2/authorize?"
        f"{urlencode(params)}"
    )

    driver.get(authorize_url)

    login_page = LoginPage(driver)
    login_page.login(
        Config.get("ORANGEHRM_USERNAME"),
        Config.get("ORANGEHRM_PASSWORD")
    )
    print(f"INVALID REDIRECT FINAL URL: {driver.current_url}")
    print(f"INVALID REDIRECT TITLE: {driver.title}")

    WebDriverWait(driver, 15).until(
        lambda d: "This request is invalid" in d.page_source
    )

    assert "This request is invalid" in driver.page_source


def test_orangehrm_api_rejects_invalid_access_token():
    api_response = requests.get(
        f"{Config.get('ORANGEHRM_BASE_URL')}/web/index.php/api/v2/pim/employees",
        headers={
            "Authorization": "Bearer invalid-token-for-test"
        },
        timeout=15,
        allow_redirects=False
    )

    assert api_response.status_code == 302
    assert "/auth/login" in api_response.headers.get("Location", "")
