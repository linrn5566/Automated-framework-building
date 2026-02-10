import pytest
import allure
from core.assertion import EnhancedAssertion


@allure.feature("卡券模块")
@allure.story("领取卡券")
class TestReceiveCoupon:
    
    @allure.title("正常领取卡券")
    @pytest.mark.smoke
    @pytest.mark.coupon
    def test_receive_coupon_success(self, coupon_api, test_coupon):
        if not test_coupon:
            pytest.skip("测试卡券创建失败")
        
        user_id = 12345
        
        with allure.step("领取卡券"):
            response = coupon_api.receive_coupon(test_coupon['id'], user_id)
        
        with allure.step("验证响应"):
            EnhancedAssertion.assert_response_code(response, 200)
            EnhancedAssertion.assert_contains_fields(response, ["coupon_code", "user_id", "receive_time"])
            EnhancedAssertion.assert_field_value(response, "user_id", user_id)
    
    @allure.title("重复领取卡券")
    @pytest.mark.normal
    @pytest.mark.coupon
    def test_receive_coupon_duplicate(self, coupon_api, test_coupon):
        if not test_coupon:
            pytest.skip("测试卡券创建失败")
        
        user_id = 12345
        
        with allure.step("第一次领取卡券"):
            response1 = coupon_api.receive_coupon(test_coupon['id'], user_id)
            EnhancedAssertion.assert_response_code(response1, 200)
        
        with allure.step("第二次领取同一卡券"):
            response2 = coupon_api.receive_coupon(test_coupon['id'], user_id)
            EnhancedAssertion.assert_response_code(response2, 400)
    
    @allure.title("领取不存在的卡券")
    @pytest.mark.normal
    @pytest.mark.coupon
    def test_receive_coupon_not_exist(self, coupon_api):
        user_id = 12345
        non_exist_coupon_id = 999999
        
        response = coupon_api.receive_coupon(non_exist_coupon_id, user_id)
        
        EnhancedAssertion.assert_response_code(response, 404)
    
    @allure.title("库存不足时领取卡券")
    @pytest.mark.normal
    @pytest.mark.coupon
    def test_receive_coupon_out_of_stock(self, coupon_api):
        pytest.skip("需要模拟库存不足场景")
