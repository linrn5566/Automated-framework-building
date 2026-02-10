import pytest
import allure
from utils.data_generator import data_generator
from core.assertion import EnhancedAssertion


@allure.feature("集成测试")
@allure.story("完整业务场景")
class TestFullScenario:
    
    @allure.title("完整卡券业务流程")
    @pytest.mark.smoke
    @pytest.mark.integration
    def test_full_coupon_scenario(self, coupon_api, auth_api):
        user_id = 12345
        
        with allure.step("1. 创建卡券"):
            coupon_data = data_generator.generate_coupon_data()
            create_response = coupon_api.create_coupon(coupon_data)
            EnhancedAssertion.assert_response_code(create_response, 201)
            coupon_id = create_response.json()['id']
        
        with allure.step("2. 查询卡券详情"):
            detail_response = coupon_api.get_coupon_detail(coupon_id)
            EnhancedAssertion.assert_response_code(detail_response, 200)
        
        with allure.step("3. 领取卡券"):
            receive_response = coupon_api.receive_coupon(coupon_id, user_id)
            EnhancedAssertion.assert_response_code(receive_response, 200)
            coupon_code = receive_response.json()['coupon_code']
        
        with allure.step("4. 查询用户卡券"):
            user_coupons_response = coupon_api.get_user_coupons(user_id, status="unused")
            EnhancedAssertion.assert_response_code(user_coupons_response, 200)
        
        with allure.step("5. 使用卡券"):
            order_data = data_generator.generate_order_data(amount=500)
            use_response = coupon_api.use_coupon(coupon_code, order_data)
            EnhancedAssertion.assert_response_code(use_response, 200)
        
        with allure.step("6. 清理测试数据"):
            coupon_api.delete_coupon(coupon_id)
    
    @allure.title("活动与卡券联动场景")
    @pytest.mark.normal
    @pytest.mark.integration
    def test_activity_coupon_integration(self, activity_api, coupon_api):
        pytest.skip("需要实现活动与卡券的关联逻辑")
