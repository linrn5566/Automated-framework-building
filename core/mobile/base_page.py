from pathlib import Path
from typing import Optional

import allure

from core.logger import log
from core.mobile.element import ElementHelper
from core.mobile.gesture import MobileGesture
from core.mobile.locator import Locator
from core.mobile.watcher import PopupWatcher


class BasePage:
    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.timeout = timeout
        self.element = ElementHelper(driver, timeout=timeout)
        self.gesture = MobileGesture(driver)
        self.watcher = PopupWatcher(self)

    def click(self, locator: Locator, timeout: Optional[int] = None):
        element = self.element.wait_for_clickable(locator, timeout=timeout)
        element.click()
        log.info(f"点击元素: {locator.display_name}")
        return element

    def input_text(self, locator: Locator, text: str, clear_first: bool = True, timeout: Optional[int] = None):
        element = self.element.wait_for_visible(locator, timeout=timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
        log.info(f"输入文本: {locator.display_name}")
        return element

    def get_text(self, locator: Locator, timeout: Optional[int] = None) -> str:
        element = self.element.wait_for_visible(locator, timeout=timeout)
        return element.text

    def is_visible(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        return self.element.is_visible(locator, timeout=timeout)

    def find_elements(self, locator: Locator):
        return self.element.find_all(locator)

    def swipe_up(self):
        self.gesture.swipe_vertical(0.8, 0.2)

    def swipe_down(self):
        self.gesture.swipe_vertical(0.2, 0.8)

    def attach_screenshot(self, name: str = '页面截图'):
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)

    def save_screenshot(self, path: Path):
        self.driver.save_screenshot(str(path))

    def wait_for_page_ready(self, locator: Locator, timeout: Optional[int] = None):
        return self.element.wait_for_visible(locator, timeout=timeout)

    def dismiss_popups(self):
        return self.watcher.dismiss_known_popups()
