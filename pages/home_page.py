from core.mobile.base_page import BasePage
from core.mobile.locator import Locator
from config.settings import settings


APP_PACKAGE = settings.mobile_env_config.get('app_package', 'com.demo.mobile')


class HomePage(BasePage):
    home_tab = Locator('id', f'{APP_PACKAGE}:id/tab_home', '首页Tab')
    coupon_entry = Locator('id', f'{APP_PACKAGE}:id/entry_coupon', '卡券入口')
    login_success_flag = Locator('id', f'{APP_PACKAGE}:id/tv_user_name', '登录成功标识')

    def wait_until_ready(self):
        return self.wait_for_page_ready(self.home_tab)

    def open_coupon_center(self):
        self.click(self.coupon_entry)

    def is_login_successful(self, timeout: int = 10) -> bool:
        return self.is_visible(self.login_success_flag, timeout=timeout)
