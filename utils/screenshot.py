import base64
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import platform

from pytest_html import extras


def capture_failure_screenshot(driver):
    screenshot_bytes = driver.get_screenshot_as_png()

    image = Image.open(BytesIO(screenshot_bytes)).convert("RGB")

    url_height = 60
    output = Image.new(
        "RGB",
        (image.width, image.height + url_height),
        "white"
    )

    output.paste(image, (0, url_height))

    draw = ImageDraw.Draw(output)

    if platform.system() == "Windows":
        font_path = Path("C:/Windows/Fonts/arial.ttf")
    else:
        font_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")

    if font_path.exists():
        font = ImageFont.truetype(str(font_path), 22)
    else:
        font = ImageFont.load_default()

    draw.text(
        (10, 15),
        f"URL: {driver.current_url}",
        fill="black",
        font=font
    )

    output_bytes = BytesIO()
    output.save(output_bytes, format="PNG")

    return output_bytes.getvalue()


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
