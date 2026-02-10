import pytest
import allure
from utils.data_generator import data_generator
from core.assertion import EnhancedAssertion


@allure.feature("活动模块")
@allure.story("创建活动")
class TestCreateActivity:
    
    @allure.title("正常创建活动")
    @pytest.mark.smoke
    @pytest.mark.activity
    def test_create_activity_success(self, activity_api):
        activity_data = data_generator.generate_activity_data()
        
        response = activity_api.create_activity(activity_data)
        
        EnhancedAssertion.assert_response_code(response, 201)
        EnhancedAssertion.assert_contains_fields(response, ["id", "title", "status"])
        
        activity_api.delete_activity(response.json()['id'])
    
    @allure.title("创建活动-验证活动详情")
    @pytest.mark.normal
    @pytest.mark.activity
    def test_create_activity_verify_details(self, activity_api):
        activity_data = data_generator.generate_activity_data()
        
        create_response = activity_api.create_activity(activity_data)
        EnhancedAssertion.assert_response_code(create_response, 201)
        
        activity_id = create_response.json()['id']
        detail_response = activity_api.get_activity_detail(activity_id)
        
        EnhancedAssertion.assert_response_code(detail_response, 200)
        EnhancedAssertion.assert_field_value(detail_response, "title", activity_data["title"])
        
        activity_api.delete_activity(activity_id)
    
    @allure.title("创建活动-缺少必填字段")
    @pytest.mark.normal
    @pytest.mark.activity
    def test_create_activity_missing_field(self, activity_api):
        invalid_data = {
            "title": "测试活动"
        }
        
        response = activity_api.create_activity(invalid_data)
        
        EnhancedAssertion.assert_response_code(response, 400)
