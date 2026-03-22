import allure
import pytest

from core.mobile.mobile_assertion import MobileAssertion


@allure.feature('移动端冒烟')
@allure.story('用户登录')
@pytest.mark.mobile
@pytest.mark.android
@pytest.mark.ui_smoke
@pytest.mark.p0
class TestMobileLogin:
    @allure.title('普通用户登录成功')
    def test_login_success(self, driver, login_flow, mobile_smoke_account):
        username = mobile_smoke_account.get('username')
        password = mobile_smoke_account.get('password')
        if not username or not password:
            pytest.skip('未配置移动端冒烟账号')

        home_page = login_flow.login(username, password)
        MobileAssertion.assert_element_visible(home_page, home_page.login_success_flag, timeout=10)
        assert home_page.is_login_successful(timeout=10), '登录后未进入首页'
        home_page.attach_screenshot('登录冒烟验证')
