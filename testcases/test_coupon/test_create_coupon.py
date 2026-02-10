import pytest
import allure
from utils.data_generator import data_generator
from core.assertion import EnhancedAssertion


@allure.feature("卡券模块")
@allure.story("创建卡券")
class TestCreateCoupon:
    
    @allure.title("创建折扣卡券")
    @pytest.mark.smoke
    @pytest.mark.coupon
    def test_create_discount_coupon(self, coupon_api):
        coupon_data = data_generator.generate_coupon_data(coupon_type="discount")
        
        response = coupon_api.create_coupon(coupon_data)
        
        EnhancedAssertion.assert_response_code(response, 201)
        EnhancedAssertion.assert_contains_fields(response, ["id", "name", "type", "amount"])
        EnhancedAssertion.assert_field_value(response, "type", "discount")
        
        coupon_api.delete_coupon(response.json()['id'])
    
    @allure.title("创建不同类型的卡券")
    @pytest.mark.parametrize("coupon_type", ["discount", "cashback", "full_reduction"])
    @pytest.mark.normal
    @pytest.mark.coupon
    def test_create_different_types_coupon(self, coupon_api, coupon_type):
        coupon_data = data_generator.generate_coupon_data(coupon_type=coupon_type)
        
        response = coupon_api.create_coupon(coupon_data)
        
        EnhancedAssertion.assert_response_code(response, 201)
        EnhancedAssertion.assert_field_value(response, "type", coupon_type)
        
        coupon_api.delete_coupon(response.json()['id'])
    
    @allure.title("创建卡券-缺少必填字段")
    @pytest.mark.normal
    @pytest.mark.coupon
    def test_create_coupon_missing_required_field(self, coupon_api):
        invalid_data = {
            "name": "测试卡券"
        }
        
        response = coupon_api.create_coupon(invalid_data)
        
        EnhancedAssertion.assert_response_code(response, 400)
    
    @allure.title("创建卡券-无效的金额")
    @pytest.mark.normal
    @pytest.mark.coupon
    def test_create_coupon_invalid_amount(self, coupon_api):
        coupon_data = data_generator.generate_coupon_data()
        coupon_data['amount'] = -10
        
        response = coupon_api.create_coupon(coupon_data)
        
        EnhancedAssertion.assert_response_code(response, 400)
