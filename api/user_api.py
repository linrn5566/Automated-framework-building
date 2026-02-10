from typing import Dict, Optional
from requests import Response
from api.base_api import BaseAPI
import allure


class UserAPI(BaseAPI):
    @allure.step("创建用户")
    def create_user(self, user_data: Dict) -> Response:
        return self.post("/api/v1/users", json=user_data)
    
    @allure.step("查询用户详情")
    def get_user_detail(self, user_id: int) -> Response:
        return self.get(f"/api/v1/users/{user_id}")
    
    @allure.step("更新用户信息")
    def update_user(self, user_id: int, update_data: Dict) -> Response:
        return self.put(f"/api/v1/users/{user_id}", json=update_data)
    
    @allure.step("删除用户")
    def delete_user(self, user_id: int) -> Response:
        return self.delete(f"/api/v1/users/{user_id}")
    
    @allure.step("查询用户列表")
    def get_user_list(self, params: Optional[Dict] = None) -> Response:
        return self.get("/api/v1/users", params=params)
    
    @allure.step("查询用户资产")
    def get_user_assets(self, user_id: int) -> Response:
        return self.get(f"/api/v1/users/{user_id}/assets")
    
    @allure.step("实名认证")
    def verify_identity(self, user_id: int, identity_data: Dict) -> Response:
        return self.post(f"/api/v1/users/{user_id}/verify-identity", json=identity_data)
