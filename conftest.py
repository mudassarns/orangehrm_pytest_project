import pytest
from pages.login_page import LoginPage
from pages.base_page import BasePage
from config import Config
from utils.test_data import generate_employee_data
from pages.dashboard_page import DashboardPage
from api.orangehrm_api import OrangeHRMApi
from utils.logger import get_logger
from datetime import datetime
from utils.screenshot import capture_failure_screenshot
from db.database_client import DatabaseClient
from utils.browser_factory import BrowserFactory
from pytest_html import extras
import base64


logger = get_logger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Environment to run tests against"
    )

    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use for test execution"
    )

    parser.addoption(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when in ("setup", "call") and report.failed:
        driver = item.funcargs.get("driver")

        if driver:
            logger.error(
                f"TEST FAILED: {item.name} | "
                f"PHASE: {report.when} | "
                f"ERROR: {call.excinfo.value}"
            )

            screenshot_bytes = capture_failure_screenshot(driver)

            screenshot_base64 = base64.b64encode(
                screenshot_bytes
            ).decode("utf-8")

            report_extras = getattr(report, "extras", [])

            report_extras.append(
                extras.image(
                    screenshot_base64,
                    mime_type="image/png",
                    name="Failure Screenshot"
                )
            )

            report.extras = report_extras


@pytest.fixture(scope="session", autouse=True)
def set_environment(request):
    Config.environment = request.config.getoption("--env")


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    driver = BrowserFactory.create(
        browser=browser,
        headless=headless
    )
    driver.maximize_window()

    yield driver

    driver.quit()


@pytest.fixture(scope="session")
def auth_cookie(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    driver = BrowserFactory.create(
        browser=browser,
        headless=headless
    )

    driver.get(Config.get("ORANGEHRM_BASE_URL"))

    print(f"Current URL: {driver.current_url}")
    print(f"Page title: {driver.title}")

    login_page = LoginPage(driver)
    dashboard = login_page.login(
        Config.get("ORANGEHRM_USERNAME"),
        Config.get("ORANGEHRM_PASSWORD")
    )

    assert dashboard.is_dashboard_displayed(), "Initial UI login failed"

    cookie = driver.get_cookie("_orangehrm")
    assert cookie is not None

    driver.quit()

    return {"cookie": cookie}


@pytest.fixture
def dashboard(driver, auth_cookie):
    driver.get(Config.get("ORANGEHRM_BASE_URL"))

    page = BasePage(driver)

    # Remove any orangehrm cookies created when visiting the site
    # driver.execute_cdp_cmd("Network.clearBrowserCookies", {})
    # driver.delete_cookie(auth_cookie["cookie"]["name"])

    # Restore cached authentication cookie
    page.restore_cookie(auth_cookie["cookie"])

    dashboard = DashboardPage(driver)

    if not dashboard.is_dashboard_displayed():

        print("\nCookie authentication failed")

        # Start a completely clean session
        # driver.execute_cdp_cmd("Network.clearBrowserCookies", {})
        driver.delete_cookie(auth_cookie["cookie"]["name"])

        # Load the login page with a fresh session
        driver.get(Config.get("ORANGEHRM_BASE_URL"))

        login_page = LoginPage(driver)

        # Fallback to normal UI login
        dashboard = login_page.login(
            Config.get("ORANGEHRM_USERNAME"),
            Config.get("ORANGEHRM_PASSWORD")
        )

        # Capture the new authentication cookie
        new_cookie = driver.get_cookie("_orangehrm")
        assert new_cookie is not None

        # Update the shared session-scoped authentication state
        auth_cookie["cookie"] = new_cookie

    return dashboard

@pytest.fixture
def add_employee(dashboard):
    employee_list = dashboard.go_to_pim()
    return employee_list.go_to_add_employee()


@pytest.fixture
def create_employee(add_employee):
    employee_data = generate_employee_data()
    add_employee.enter_first_name(employee_data["first_name"])
    add_employee.enter_middle_name(employee_data["middle_name"])
    add_employee.enter_last_name(employee_data["last_name"])
    add_employee.enter_employee_id(employee_data["employee_id"])
    employee_details = add_employee.save()

    yield employee_data, employee_details

    employee_list = employee_details.go_to_employee_list()
    employee_id = employee_data["employee_id"]
    result_count = employee_list.search_employee_by_id(employee_id)

    if result_count == 1:
        employee_list.delete_first_employee()
        result_count = employee_list.search_employee_by_id(employee_id)

        if result_count == 0:
            logger.info(f"CLEANUP SUCCESS: Employee {employee_id} deleted")
        else:
            logger.error(f"CLEANUP FAILED: Employee {employee_id} still exists")
    else:
        logger.warning(f"CLEANUP NOT REQUIRED: Employee {employee_id} not found")


@pytest.fixture(scope="session")
def orangehrm_api(auth_cookie):
    return OrangeHRMApi(auth_cookie["cookie"])

@pytest.fixture
def create_employee_api(orangehrm_api):
    employee_data = generate_employee_data()

    create_response = orangehrm_api.create_employee(employee_data)

    assert create_response.status_code == 200

    employee_details = create_response.json()
    emp_number = employee_details["data"]["empNumber"]

    yield employee_data, employee_details

    get_response = orangehrm_api.get_employee(emp_number)

    if get_response.status_code == 200:
        delete_response = orangehrm_api.delete_employee(emp_number)

        if delete_response.status_code == 200:
            logger.info(f"CLEANUP SUCCESS: Employee {emp_number} deleted")
        else:
            logger.error(
                f"CLEANUP FAILED: Employee {emp_number} "
                f"could not be deleted. Status: {delete_response.status_code}"
            )
    else:
        logger.warning(f"CLEANUP NOT REQUIRED: Employee {emp_number} not found")


@pytest.fixture
def db():
    database = DatabaseClient()
    yield database
    database.close()