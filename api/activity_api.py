from typing import Dict, Optional
from requests import Response
from api.base_api import BaseAPI
import allure


class ActivityAPI(BaseAPI):
    @allure.step("创建活动")
    def create_activity(self, activity_data: Dict) -> Response:
        return self.post("/api/v1/activities", json=activity_data)
    
    @allure.step("查询活动详情")
    def get_activity_detail(self, activity_id: int) -> Response:
        return self.get(f"/api/v1/activities/{activity_id}")
    
    @allure.step("查询活动列表")
    def get_activity_list(self, params: Optional[Dict] = None) -> Response:
        return self.get("/api/v1/activities", params=params)
    
    @allure.step("参与活动")
    def participate_activity(self, activity_id: int, user_id: int) -> Response:
        payload = {
            "user_id": user_id
        }
        return self.post(f"/api/v1/activities/{activity_id}/participate", json=payload)
    
    @allure.step("更新活动")
    def update_activity(self, activity_id: int, update_data: Dict) -> Response:
        return self.put(f"/api/v1/activities/{activity_id}", json=update_data)
    
    @allure.step("删除活动")
    def delete_activity(self, activity_id: int) -> Response:
        return self.delete(f"/api/v1/activities/{activity_id}")
    
    @allure.step("查询活动参与人数")
    def get_activity_participants(self, activity_id: int) -> Response:
        return self.get(f"/api/v1/activities/{activity_id}/participants")
    
    @allure.step("发布活动")
    def publish_activity(self, activity_id: int) -> Response:
        return self.post(f"/api/v1/activities/{activity_id}/publish")
    
    @allure.step("下线活动")
    def offline_activity(self, activity_id: int) -> Response:
        return self.post(f"/api/v1/activities/{activity_id}/offline")
    
    @allure.step("查询用户参与的活动")
    def get_user_activities(self, user_id: int) -> Response:
        params = {"user_id": user_id}
        return self.get("/api/v1/activities/user", params=params)
