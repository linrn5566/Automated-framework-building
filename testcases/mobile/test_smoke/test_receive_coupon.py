import allure
import pytest

from config.settings import settings
from core.assertion import EnhancedAssertion
from core.mobile.mobile_assertion import MobileAssertion


@allure.feature('移动端冒烟')
@allure.story('领取卡券')
@pytest.mark.mobile
@pytest.mark.android
@pytest.mark.ui_smoke
@pytest.mark.p1
class TestMobileReceiveCoupon:
    @allure.title('登录后成功领取卡券')
    def test_receive_coupon_success(
        self,
        driver,
        login_flow,
        coupon_flow,
        mobile_smoke_account,
        mobile_coupon_data,
        coupon_api,
    ):
        username = mobile_smoke_account.get('username')
        password = mobile_smoke_account.get('password')
        if not username or not password:
            pytest.skip('未配置移动端冒烟账号')

        login_flow.login(username, password)
        coupon_page = coupon_flow.receive_first_coupon()

        expected_text = mobile_coupon_data.get('expected_success_text', '领取成功')
        MobileAssertion.assert_page_contains_text(driver, expected_text)
        assert coupon_page.is_receive_successful(timeout=10), '未出现领取成功提示'

        backend_check = mobile_coupon_data.get('backend_check', {})
        if backend_check.get('enabled') and settings.base_url:
            user_id = backend_check.get('user_id')
            if not user_id:
                pytest.skip('已开启后端校验但未配置 user_id')
            response = coupon_api.get_user_coupons(user_id=user_id)
            EnhancedAssertion.assert_response_code(response, 200)
