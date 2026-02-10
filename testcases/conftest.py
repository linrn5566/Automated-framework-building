import pytest
from api.auth_api import AuthAPI
from api.coupon_api import CouponAPI
from api.activity_api import ActivityAPI
from api.user_api import UserAPI
from core.database import DatabaseHelper
from config.settings import settings
from utils.data_generator import data_generator
from core.logger import log
import allure


@pytest.fixture(scope="session")
def auth_api():
    api = AuthAPI()
    yield api


@pytest.fixture(scope="session")
def coupon_api():
    api = CouponAPI()
    yield api


@pytest.fixture(scope="session")
def activity_api():
    api = ActivityAPI()
    yield api


@pytest.fixture(scope="session")
def user_api():
    api = UserAPI()
    yield api


@pytest.fixture(scope="session")
def db_helper():
    if not settings.db_database:
        log.warning("数据库配置未设置，跳过数据库fixture")
        yield None
        return
    
    helper = DatabaseHelper(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_database
    )
    yield helper


@pytest.fixture(scope="function")
def test_user(auth_api):
    user_data = data_generator.generate_user_data()
    response = auth_api.register(user_data)
    
    if response.status_code == 201:
        user_info = response.json()
        log.info(f"创建测试用户成功: {user_info.get('username')}")
        yield user_info
    else:
        log.error(f"创建测试用户失败: {response.text}")
        yield None


@pytest.fixture(scope="function")
def login_token(auth_api, test_user):
    if not test_user:
        yield None
        return
    
    response = auth_api.login(test_user['username'], test_user['password'])
    
    if response.status_code == 200:
        token = response.json().get('token')
        log.info(f"用户登录成功，获取token: {token[:20]}...")
        yield token
    else:
        log.error(f"用户登录失败: {response.text}")
        yield None


@pytest.fixture(scope="function")
def test_coupon(coupon_api):
    coupon_data = data_generator.generate_coupon_data()
    response = coupon_api.create_coupon(coupon_data)
    
    if response.status_code == 201:
        coupon_info = response.json()
        log.info(f"创建测试卡券成功: {coupon_info.get('id')}")
        yield coupon_info
        
        coupon_api.delete_coupon(coupon_info['id'])
        log.info(f"清理测试卡券: {coupon_info['id']}")
    else:
        log.error(f"创建测试卡券失败: {response.text}")
        yield None


@pytest.fixture(scope="function")
def test_activity(activity_api):
    activity_data = data_generator.generate_activity_data()
    response = activity_api.create_activity(activity_data)
    
    if response.status_code == 201:
        activity_info = response.json()
        log.info(f"创建测试活动成功: {activity_info.get('id')}")
        yield activity_info
        
        activity_api.delete_activity(activity_info['id'])
        log.info(f"清理测试活动: {activity_info['id']}")
    else:
        log.error(f"创建测试活动失败: {response.text}")
        yield None


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        log.error(f"测试用例失败: {item.nodeid}")
        
        if hasattr(item, 'funcargs'):
            allure.attach(
                str(item.funcargs),
                name="测试参数",
                attachment_type=allure.attachment_type.TEXT
            )


def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
