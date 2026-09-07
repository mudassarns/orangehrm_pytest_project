from selenium.webdriver.common.by import By


class LocatorUtils:

    @staticmethod
    def input_by_label(label):
        return (
            By.XPATH,
            f"//label[normalize-space()='{label}']/ancestor::div[contains(@class,'oxd-input-group')]//input"
        )