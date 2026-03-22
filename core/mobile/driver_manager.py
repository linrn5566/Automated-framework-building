from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from config.settings import settings
from core.logger import log

try:
    from appium import webdriver
    from appium.options.android import UiAutomator2Options
    from appium.options.ios import XCUITestOptions
except ImportError:  # pragma: no cover - 运行环境未安装Appium时降级
    webdriver = None
    UiAutomator2Options = None
    XCUITestOptions = None


class DriverManager:
    def __init__(self, platform: str = '', command_executor: str = '', capability_overrides: Optional[Dict[str, Any]] = None):
        self.platform = (platform or settings.mobile_platform or 'android').lower()
        self.command_executor = command_executor or settings.mobile_appium_server
        self.capability_overrides = capability_overrides or {}
        self.driver = None

    def _build_options(self, capabilities: Dict[str, Any]):
        if self.platform == 'ios':
            if XCUITestOptions is None:
                raise RuntimeError('未安装 Appium-Python-Client，请先执行 pip install -r requirements.txt')
            options = XCUITestOptions()
        else:
            if UiAutomator2Options is None:
                raise RuntimeError('未安装 Appium-Python-Client，请先执行 pip install -r requirements.txt')
            options = UiAutomator2Options()

        options.load_capabilities(capabilities)
        return options

    def get_capabilities(self) -> Dict[str, Any]:
        capabilities = settings.get_mobile_capabilities(self.platform)
        capabilities.update(self.capability_overrides)

        app_package = settings.mobile_env_config.get('app_package')
        app_activity = settings.mobile_env_config.get('app_activity')
        if self.platform == 'android' and app_package:
            capabilities.setdefault('appPackage', app_package)
        if self.platform == 'android' and app_activity:
            capabilities.setdefault('appActivity', app_activity)

        return capabilities

    def create_driver(self):
        if webdriver is None:
            raise RuntimeError('未安装 Appium-Python-Client，请先执行 pip install -r requirements.txt')

        capabilities = self.get_capabilities()
        options = self._build_options(capabilities)
        self.driver = webdriver.Remote(self.command_executor, options=options)
        self.driver.implicitly_wait(settings.mobile_implicit_wait)
        log.info(f"移动端Driver已创建: platform={self.platform}, device={capabilities.get('deviceName')}")
        return self.driver

    def get_driver(self):
        if self.driver is None:
            return self.create_driver()
        return self.driver

    def save_screenshot(self, name: str = 'failure') -> Path:
        if self.driver is None:
            raise RuntimeError('Driver 尚未初始化')

        file_path = settings.screenshots_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}.png"
        self.driver.save_screenshot(str(file_path))
        return file_path

    def save_page_source(self, name: str = 'failure') -> Path:
        if self.driver is None:
            raise RuntimeError('Driver 尚未初始化')

        file_path = settings.page_source_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}.xml"
        file_path.write_text(self.driver.page_source, encoding='utf-8')
        return file_path

    def quit_driver(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None
            log.info('移动端Driver已关闭')
