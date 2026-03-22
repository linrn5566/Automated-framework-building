from typing import List, Optional

from core.logger import log
from core.mobile.locator import Locator

try:
    from appium.webdriver.common.appiumby import AppiumBy
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
except ImportError:  # pragma: no cover - 运行环境未安装Appium时降级
    AppiumBy = None
    TimeoutException = Exception
    EC = None
    WebDriverWait = None


class ElementHelper:
    STRATEGY_MAPPING = {
        'id': 'ID',
        'xpath': 'XPATH',
        'accessibility_id': 'ACCESSIBILITY_ID',
        'class_name': 'CLASS_NAME',
        'android_uiautomator': 'ANDROID_UIAUTOMATOR',
        'ios_predicate': 'IOS_PREDICATE',
        'ios_class_chain': 'IOS_CLASS_CHAIN',
    }

    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.timeout = timeout

    def _resolve(self, locator: Locator):
        if AppiumBy is None:
            raise RuntimeError("未安装 Appium-Python-Client，请先执行 pip install -r requirements.txt")

        strategy_name = self.STRATEGY_MAPPING.get(locator.strategy.lower())
        if not strategy_name or not hasattr(AppiumBy, strategy_name):
            raise ValueError(f"不支持的定位策略: {locator.strategy}")

        return getattr(AppiumBy, strategy_name), locator.value

    def wait_for_visible(self, locator: Locator, timeout: Optional[int] = None):
        by, value = self._resolve(locator)
        wait_timeout = timeout or self.timeout
        return WebDriverWait(self.driver, wait_timeout).until(
            EC.visibility_of_element_located((by, value))
        )

    def wait_for_clickable(self, locator: Locator, timeout: Optional[int] = None):
        by, value = self._resolve(locator)
        wait_timeout = timeout or self.timeout
        return WebDriverWait(self.driver, wait_timeout).until(
            EC.element_to_be_clickable((by, value))
        )

    def find(self, locator: Locator, timeout: Optional[int] = None):
        return self.wait_for_visible(locator, timeout=timeout)

    def find_all(self, locator: Locator) -> List:
        by, value = self._resolve(locator)
        return self.driver.find_elements(by, value)

    def is_visible(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        try:
            self.wait_for_visible(locator, timeout=timeout)
            return True
        except TimeoutException:
            log.info(f"元素不可见: {locator.display_name}")
            return False
