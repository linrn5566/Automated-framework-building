from core.mobile.base_page import BasePage
from core.mobile.locator import Locator
from config.settings import settings


APP_PACKAGE = settings.mobile_env_config.get('app_package', 'com.demo.mobile')


class LoginPage(BasePage):
    username_input = Locator('id', f'{APP_PACKAGE}:id/input_username', '用户名输入框')
    password_input = Locator('id', f'{APP_PACKAGE}:id/input_password', '密码输入框')
    login_button = Locator('id', f'{APP_PACKAGE}:id/btn_login', '登录按钮')
    page_identifier = Locator('id', f'{APP_PACKAGE}:id/btn_login', '登录页标识')

    def wait_until_ready(self):
        return self.wait_for_page_ready(self.page_identifier)

    def input_username(self, username: str):
        self.input_text(self.username_input, username)

    def input_password(self, password: str):
        self.input_text(self.password_input, password)

    def tap_login(self):
        self.click(self.login_button)
