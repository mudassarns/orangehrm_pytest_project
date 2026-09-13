import base64

from pytest_html import extras

from utils.screenshot import capture_failure_screenshot


def attach_failure_screenshot(report, driver):
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