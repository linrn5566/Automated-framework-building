import allure

from core.logger import log
from core.mobile.locator import Locator


class MobileAssertion:
    @staticmethod
    @allure.step("断言元素可见")
    def assert_element_visible(page, locator: Locator, timeout: int = 15, message: str = ''):
        msg = message or f"元素不可见: {locator.display_name}"
        assert page.is_visible(locator, timeout=timeout), msg
        log.info(f"✓ 元素可见断言通过: {locator.display_name}")

    @staticmethod
    @allure.step("断言文本包含预期内容")
    def assert_text_contains(page, locator: Locator, expected_text: str, timeout: int = 15):
        actual_text = page.get_text(locator, timeout=timeout)
        assert expected_text in actual_text, f"期望文本包含 {expected_text}, 实际为 {actual_text}"
        log.info(f"✓ 文本断言通过: {locator.display_name} -> {expected_text}")

    @staticmethod
    @allure.step("断言当前Activity")
    def assert_current_activity_contains(driver, expected_text: str):
        actual_activity = getattr(driver, 'current_activity', '') or ''
        assert expected_text in actual_activity, f"期望Activity包含 {expected_text}, 实际为 {actual_activity}"
        log.info(f"✓ Activity断言通过: {actual_activity}")

    @staticmethod
    @allure.step("断言页面源码包含文本")
    def assert_page_contains_text(driver, expected_text: str):
        page_source = driver.page_source or ''
        assert expected_text in page_source, f"页面源码中未找到文本: {expected_text}"
        log.info(f"✓ 页面文本断言通过: {expected_text}")
