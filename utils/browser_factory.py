from selenium import webdriver


class BrowserFactory:

    _DRIVERS = {
        "chrome": (webdriver.Chrome, webdriver.ChromeOptions),
        "edge": (webdriver.Edge, webdriver.EdgeOptions),
        "firefox": (webdriver.Firefox, webdriver.FirefoxOptions),
    }

    @classmethod
    def create(cls, browser="chrome", headless=False):
        browser = browser.lower()

        if browser not in cls._DRIVERS:
            raise ValueError(f"Unsupported browser: {browser}")

        driver_cls, options_cls = cls._DRIVERS[browser]
        options = options_cls()

        if browser == "firefox":
            if headless:
                options.add_argument("-headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
        else:
            if headless:
                options.add_argument("--headless=new")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")

        driver = driver_cls(options=options)

        if browser == "chrome" and headless:
            driver.execute_cdp_cmd(
                "Emulation.setDeviceMetricsOverride",
                {
                    "width": 1920,
                    "height": 1080,
                    "deviceScaleFactor": 1,
                    "mobile": False,
                },
            )

        return driver