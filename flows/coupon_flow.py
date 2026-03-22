import allure

from pages.coupon_page import CouponPage
from pages.home_page import HomePage


class CouponFlow:
    def __init__(self, driver):
        self.driver = driver
        self.home_page = HomePage(driver)
        self.coupon_page = CouponPage(driver)

    @allure.step('进入卡券中心并领取卡券')
    def receive_first_coupon(self):
        self.home_page.wait_until_ready()
        self.home_page.open_coupon_center()
        self.coupon_page.wait_until_ready()
        self.coupon_page.receive_coupon()
        self.coupon_page.attach_screenshot('领取卡券结果截图')
        return self.coupon_page
