import pytest
import allure
from utils.data_generator import data_generator
from core.assertion import EnhancedAssertion


@allure.feature("卡券模块")
@allure.story("使用卡券")
class TestUseCoupon:
    
    @allure.title("正常使用卡券")
    @pytest.mark.smoke
    @pytest.mark.coupon
    def test_use_coupon_success(self, coupon_api, test_coupon):
        if not test_coupon:
            pytest.skip("测试卡券创建失败")
        
        user_id = 12345
        
        with allure.step("先领取卡券"):
            receive_response = coupon_api.receive_coupon(test_coupon['id'], user_id)
            EnhancedAssertion.assert_response_code(receive_response, 200)
            coupon_code = receive_response.json()['coupon_code']
        
        with allure.step("使用卡券"):
            order_data = data_generator.generate_order_data(amount=500)
            use_response = coupon_api.use_coupon(coupon_code, order_data)
        
        with allure.step("验证响应"):
            EnhancedAssertion.assert_response_code(use_response, 200)
            EnhancedAssertion.assert_contains_fields(use_response, ["status", "discount_amount"])
    
    @allure.title("重复使用已使用的卡券")
    @pytest.mark.normal
    @pytest.mark.coupon
    def test_use_coupon_duplicate(self, coupon_api, test_coupon):
        if not test_coupon:
            pytest.skip("测试卡券创建失败")
        
        user_id = 12345
        
        with allure.step("领取并使用卡券"):
            receive_response = coupon_api.receive_coupon(test_coupon['id'], user_id)
            coupon_code = receive_response.json()['coupon_code']
            
            order_data = data_generator.generate_order_data(amount=500)
            use_response1 = coupon_api.use_coupon(coupon_code, order_data)
            EnhancedAssertion.assert_response_code(use_response1, 200)
        
        with allure.step("再次使用同一卡券"):
            use_response2 = coupon_api.use_coupon(coupon_code, order_data)
            EnhancedAssertion.assert_response_code(use_response2, 400)
    
    @allure.title("使用卡券-订单金额不满足最低要求")
    @pytest.mark.normal
    @pytest.mark.coupon
    def test_use_coupon_order_amount_not_meet(self, coupon_api, test_coupon):
        if not test_coupon:
            pytest.skip("测试卡券创建失败")
        
        user_id = 12345
        
        receive_response = coupon_api.receive_coupon(test_coupon['id'], user_id)
        coupon_code = receive_response.json()['coupon_code']
        
        order_data = data_generator.generate_order_data(amount=10)
        use_response = coupon_api.use_coupon(coupon_code, order_data)
        
        EnhancedAssertion.assert_response_code(use_response, 400)
    
    @allure.title("使用卡券-卡券码无效")
    @pytest.mark.normal
    @pytest.mark.coupon
    def test_use_coupon_invalid_code(self, coupon_api):
        invalid_code = "INVALID_CODE_123"
        order_data = data_generator.generate_order_data(amount=500)
        
        response = coupon_api.use_coupon(invalid_code, order_data)
        
        EnhancedAssertion.assert_response_code(response, 404)
