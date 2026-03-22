import allure
import pytest
import socket
from urllib.parse import urlparse

from api.coupon_api import CouponAPI
from config.settings import settings
from core.logger import log
from core.mobile.driver_manager import DriverManager, webdriver
from flows.coupon_flow import CouponFlow
from flows.login_flow import LoginFlow
from pages.coupon_page import CouponPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.mobile_data import mobile_test_data


def _is_server_reachable(server_url: str, timeout: int = 2) -> bool:
    parsed = urlparse(server_url)
    host = parsed.hostname
    port = parsed.port
    if not host or not port:
        return False

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def pytest_addoption(parser):
    group = parser.getgroup('mobile')
    group.addoption('--platform', action='store', default=settings.mobile_platform, help='移动端平台: android/ios')
    group.addoption('--device-name', action='store', default=settings.mobile_device_name, help='设备名称')
    group.addoption('--app-path', action='store', default=settings.mobile_app_path, help='App 安装包路径')
    group.addoption('--udid', action='store', default=settings.mobile_udid, help='设备UDID')
    group.addoption('--appium-server', action='store', default=settings.mobile_appium_server, help='Appium Server地址')
    group.addoption('--no-reset', action='store_true', default=settings.mobile_no_reset, help='保留App数据')


@pytest.fixture(scope='session')
def mobile_runtime(pytestconfig):
    platform = pytestconfig.getoption('--platform')
    capabilities = settings.get_mobile_capabilities(platform)

    device_name = pytestconfig.getoption('--device-name')
    app_path = pytestconfig.getoption('--app-path')
    udid = pytestconfig.getoption('--udid')

    if device_name:
        capabilities['deviceName'] = device_name
    if app_path:
        capabilities['app'] = app_path
    if udid:
        capabilities['udid'] = udid
    capabilities['noReset'] = pytestconfig.getoption('--no-reset')

    return {
        'platform': platform,
        'appium_server': pytestconfig.getoption('--appium-server'),
        'capabilities': capabilities,
    }


@pytest.fixture(scope='session')
def mobile_test_dataset():
    return mobile_test_data.load(force_reload=True)


@pytest.fixture(scope='session')
def mobile_smoke_account(mobile_test_dataset):
    return mobile_test_dataset.get('accounts', {}).get('smoke_user', {})


@pytest.fixture(scope='session')
def mobile_coupon_data(mobile_test_dataset):
    return mobile_test_dataset.get('coupon', {})


@pytest.fixture(scope='function')
def driver_manager(mobile_runtime):
    if webdriver is None:
        pytest.skip('未安装 Appium-Python-Client，移动端测试已跳过')

    manager = DriverManager(
        platform=mobile_runtime['platform'],
        command_executor=mobile_runtime['appium_server'],
        capability_overrides=mobile_runtime['capabilities'],
    )
    yield manager
    manager.quit_driver()


@pytest.fixture(scope='function')
def driver(driver_manager):
    capabilities = driver_manager.get_capabilities()
    if not capabilities.get('app') and not capabilities.get('appPackage'):
        pytest.skip('未配置 app_path 或 appPackage，移动端测试已跳过')
    if not _is_server_reachable(driver_manager.command_executor):
        pytest.skip(f'Appium Server 不可达: {driver_manager.command_executor}')

    driver = driver_manager.get_driver()
    log.info(f"启动移动端会话: {driver.session_id}")
    return driver


@pytest.fixture(scope='function', autouse=True)
def attach_mobile_artifacts_on_failure(request):
    yield
    rep_call = getattr(request.node, 'rep_call', None)
    if rep_call is None or rep_call.passed:
        return

    manager = request.node.funcargs.get('driver_manager')
    if not manager or manager.driver is None:
        return

    screenshot_path = manager.save_screenshot(request.node.name)
    page_source_path = manager.save_page_source(request.node.name)

    allure.attach.file(str(screenshot_path), name='失败截图', attachment_type=allure.attachment_type.PNG)
    allure.attach.file(str(page_source_path), name='页面源码', attachment_type=allure.attachment_type.TEXT)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f'rep_{rep.when}', rep)


@pytest.fixture(scope='function')
def login_page(driver):
    return LoginPage(driver, timeout=settings.mobile_explicit_wait)


@pytest.fixture(scope='function')
def home_page(driver):
    return HomePage(driver, timeout=settings.mobile_explicit_wait)


@pytest.fixture(scope='function')
def coupon_page(driver):
    return CouponPage(driver, timeout=settings.mobile_explicit_wait)


@pytest.fixture(scope='function')
def login_flow(driver):
    return LoginFlow(driver)


@pytest.fixture(scope='function')
def coupon_flow(driver):
    return CouponFlow(driver)


@pytest.fixture(scope='session')
def mobile_coupon_api():
    return CouponAPI()
