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

        allow_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                ("xpath", "//button[normalize-space()='Allow Access']")
            )
        )
        allow_button.click()

        for _ in range(30):
            if CallbackHandler.authorization_code:
                break

            threading.Event().wait(1)

        assert CallbackHandler.authorization_code is not None, (
            "OAuth authorization code was not received"
        )

        token_response = requests.post(
            f"{Config.get('ORANGEHRM_BASE_URL')}/web/index.php/oauth2/token",
            data={
                "grant_type": "authorization_code",
                "client_id": "ci_oauth_probe",
                "redirect_uri": redirect_uri,
                "code": CallbackHandler.authorization_code,
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

    finally:
        server.shutdown()
        server.server_close()
