import pytest
import allure


@allure.feature('移动端冒烟')
@allure.story('应用启动')
@pytest.mark.mobile
@pytest.mark.android
@pytest.mark.ui_smoke
@pytest.mark.p0
class TestAppLaunch:
    @allure.title('成功创建移动端会话')
    def test_create_mobile_session(self, driver, home_page):
        assert driver.session_id, '移动端Driver会话创建失败'
        home_page.dismiss_popups()
        home_page.attach_screenshot('应用启动首页截图')
