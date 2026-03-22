from typing import Iterable

from core.logger import log
from core.mobile.locator import Locator


class PopupWatcher:
    def __init__(self, page):
        self.page = page
        self.default_locators = [
            Locator('id', 'com.android.permissioncontroller:id/permission_allow_button', '允许权限'),
            Locator('id', 'android:id/button1', '系统确认按钮'),
            Locator('xpath', "//*[contains(@text, '同意') or contains(@text, '允许') or contains(@text, '确认')]", '通用确认按钮'),
        ]

    def dismiss_known_popups(self, locators: Iterable[Locator] = ()): 
        handled = 0
        for locator in [*self.default_locators, *list(locators)]:
            if self.page.is_visible(locator, timeout=1):
                self.page.click(locator, timeout=1)
                handled += 1
                log.info(f"已处理弹窗: {locator.display_name}")
        return handled
