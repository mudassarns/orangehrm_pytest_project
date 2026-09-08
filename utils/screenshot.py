from PIL import Image, ImageDraw, ImageFont
import platform


def capture_failure_screenshot(driver, file_path):
    driver.save_screenshot(file_path)

    image = Image.open(file_path).convert("RGB")

    url_height = 60
    output = Image.new(
        "RGB",
        (image.width, image.height + url_height),
        "white"
    )

    output.paste(image, (0, url_height))

    draw = ImageDraw.Draw(output)

    if platform.system() == "Windows":
        font_path = "C:/Windows/Fonts/arial.ttf"
    else:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    font = ImageFont.truetype(font_path, 22)

    draw.text(
        (10, 15),
        f"URL: {driver.current_url}",
        fill="black",
        font=font
    )

    output.save(file_path)