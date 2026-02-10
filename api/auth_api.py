from typing import Dict
from requests import Response
from api.base_api import BaseAPI
import allure


class AuthAPI(BaseAPI):
    @allure.step("用户登录")
    def login(self, username: str, password: str) -> Response:
        payload = {
            "username": username,
            "password": password
        }
        return self.post("/api/v1/auth/login", json=payload)
    
    @allure.step("用户注册")
    def register(self, user_data: Dict) -> Response:
        return self.post("/api/v1/auth/register", json=user_data)
    
    @allure.step("刷新Token")
    def refresh_token(self, refresh_token: str) -> Response:
        payload = {
            "refresh_token": refresh_token
        }
        return self.post("/api/v1/auth/refresh", json=payload)
    
    @allure.step("用户登出")
    def logout(self) -> Response:
        return self.post("/api/v1/auth/logout")
    
    @allure.step("获取用户信息")
    def get_user_info(self) -> Response:
        return self.get("/api/v1/auth/userinfo")
    
    @allure.step("修改密码")
    def change_password(self, old_password: str, new_password: str) -> Response:
        payload = {
            "old_password": old_password,
            "new_password": new_password
        }
        return self.post("/api/v1/auth/change-password", json=payload)
