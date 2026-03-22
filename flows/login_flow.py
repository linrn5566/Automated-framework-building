import allure

from pages.home_page import HomePage
from pages.login_page import LoginPage


class LoginFlow:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.home_page = HomePage(driver)

    @allure.step('移动端用户登录')
    def login(self, username: str, password: str):
        self.login_page.dismiss_popups()
        self.login_page.wait_until_ready()
        self.login_page.input_username(username)
        self.login_page.input_password(password)
        self.login_page.tap_login()
        self.home_page.wait_until_ready()
        self.home_page.attach_screenshot('登录成功截图')
        return self.home_page
