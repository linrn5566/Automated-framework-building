from core.mobile.base_page import BasePage
from core.mobile.locator import Locator
from config.settings import settings


APP_PACKAGE = settings.mobile_env_config.get('app_package', 'com.demo.mobile')


class CouponPage(BasePage):
    page_identifier = Locator('id', f'{APP_PACKAGE}:id/tv_coupon_title', '卡券页标识')
    receive_button = Locator('id', f'{APP_PACKAGE}:id/btn_receive', '立即领取按钮')
    receive_success_toast = Locator('xpath', "//*[contains(@text, '领取成功') or contains(@label, '领取成功')]", '领取成功提示')

    def wait_until_ready(self):
        return self.wait_for_page_ready(self.page_identifier)

    def receive_coupon(self):
        self.click(self.receive_button)

    def is_receive_successful(self, timeout: int = 10) -> bool:
        return self.is_visible(self.receive_success_toast, timeout=timeout)
