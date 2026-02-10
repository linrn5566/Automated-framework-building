import pytest
import allure
from core.assertion import EnhancedAssertion


@allure.feature("活动模块")
@allure.story("活动流程")
class TestActivityFlow:
    
    @allure.title("完整活动流程-创建发布参与下线")
    @pytest.mark.smoke
    @pytest.mark.activity
    @pytest.mark.integration
    def test_full_activity_flow(self, activity_api, test_activity):
        if not test_activity:
            pytest.skip("测试活动创建失败")
        
        activity_id = test_activity['id']
        user_id = 12345
        
        with allure.step("发布活动"):
            publish_response = activity_api.publish_activity(activity_id)
            EnhancedAssertion.assert_response_code(publish_response, 200)
        
        with allure.step("用户参与活动"):
            participate_response = activity_api.participate_activity(activity_id, user_id)
            EnhancedAssertion.assert_response_code(participate_response, 200)
        
        with allure.step("查询活动参与人数"):
            participants_response = activity_api.get_activity_participants(activity_id)
            EnhancedAssertion.assert_response_code(participants_response, 200)
        
        with allure.step("下线活动"):
            offline_response = activity_api.offline_activity(activity_id)
            EnhancedAssertion.assert_response_code(offline_response, 200)
    
    @allure.title("用户参与未发布的活动")
    @pytest.mark.normal
    @pytest.mark.activity
    def test_participate_unpublished_activity(self, activity_api, test_activity):
        if not test_activity:
            pytest.skip("测试活动创建失败")
        
        activity_id = test_activity['id']
        user_id = 12345
        
        response = activity_api.participate_activity(activity_id, user_id)
        
        EnhancedAssertion.assert_response_code(response, 400)
