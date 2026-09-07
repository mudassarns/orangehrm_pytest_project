import requests
from utils.logger import get_logger


logger = get_logger(__name__)


class BaseApiClient:

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "Accept": "application/json"
        })

    def _request(self, method, url, **kwargs):
        try:
            response = self.session.request(
                method,
                url,
                timeout=10,
                **kwargs
            )

            logger.info(f"API {method} | Status: {response.status_code}")

            return response

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise