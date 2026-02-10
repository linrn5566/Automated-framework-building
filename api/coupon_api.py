from typing import Dict, Optional
from requests import Response
from api.base_api import BaseAPI
import allure


class CouponAPI(BaseAPI):
    @allure.step("创建卡券")
    def create_coupon(self, coupon_data: Dict) -> Response:
        return self.post("/api/v1/coupons", json=coupon_data)
    
    @allure.step("领取卡券")
    def receive_coupon(self, coupon_id: int, user_id: int) -> Response:
        payload = {
            "user_id": user_id
        }
        return self.post(f"/api/v1/coupons/{coupon_id}/receive", json=payload)
    
    @allure.step("使用卡券")
    def use_coupon(self, coupon_code: str, order_data: Optional[Dict] = None) -> Response:
        payload = {
            "coupon_code": coupon_code,
            "order_data": order_data or {}
        }
        return self.post("/api/v1/coupons/use", json=payload)
    
    @allure.step("查询卡券详情")
    def get_coupon_detail(self, coupon_id: int) -> Response:
        return self.get(f"/api/v1/coupons/{coupon_id}")
    
    @allure.step("查询卡券列表")
    def get_coupon_list(self, params: Optional[Dict] = None) -> Response:
        return self.get("/api/v1/coupons", params=params)
    
    @allure.step("查询用户卡券")
    def get_user_coupons(self, user_id: int, status: Optional[str] = None) -> Response:
        params = {"user_id": user_id}
        if status:
            params["status"] = status
        return self.get("/api/v1/coupons/user", params=params)
    
    @allure.step("更新卡券")
    def update_coupon(self, coupon_id: int, update_data: Dict) -> Response:
        return self.put(f"/api/v1/coupons/{coupon_id}", json=update_data)
    
    @allure.step("删除卡券")
    def delete_coupon(self, coupon_id: int) -> Response:
        return self.delete(f"/api/v1/coupons/{coupon_id}")
    
    @allure.step("查询卡券库存")
    def get_coupon_stock(self, coupon_id: int) -> Response:
        return self.get(f"/api/v1/coupons/{coupon_id}/stock")
    
    @allure.step("批量领取卡券")
    def batch_receive_coupons(self, coupon_ids: list, user_id: int) -> Response:
        payload = {
            "coupon_ids": coupon_ids,
            "user_id": user_id
        }
        return self.post("/api/v1/coupons/batch-receive", json=payload)
