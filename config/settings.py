import os
from pathlib import Path
from typing import Dict, Any
import yaml
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

ENV = os.getenv('TEST_ENV', 'test')

class Settings:
    def __init__(self):
        self.env = ENV
        self.base_dir = BASE_DIR
        self.config_dir = BASE_DIR / 'config'
        self.data_dir = BASE_DIR / 'data'
        self.reports_dir = BASE_DIR / 'reports'
        self.logs_dir = BASE_DIR / 'logs'
        self.screenshots_dir = self.reports_dir / 'screenshots'
        self.page_source_dir = self.reports_dir / 'page_source'
        
        self.env_config = self._load_env_config()
        self.db_config = self._load_db_config()
        self.mobile_env_config = self._load_mobile_env_config()
        self.mobile_caps_config = self._load_mobile_caps_config()

        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.page_source_dir.mkdir(parents=True, exist_ok=True)

    def _load_yaml_config(self, file_name: str) -> Dict[str, Any]:
        config_file = self.config_dir / file_name
        if not config_file.exists():
            return {}

        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}

        if not isinstance(config, dict):
            return {}

        return config
    
    def _load_env_config(self) -> Dict[str, Any]:
        all_config = self._load_yaml_config('env_config.yaml')
        return all_config.get(self.env, {})
    
    def _load_db_config(self) -> Dict[str, Any]:
        all_config = self._load_yaml_config('db_config.yaml')
        return all_config.get(self.env, {})

    def _load_mobile_env_config(self) -> Dict[str, Any]:
        all_config = self._load_yaml_config('mobile_env.yaml')
        common_config = all_config.get('common', {})
        env_config = all_config.get(self.env, {})
        return {**common_config, **env_config}

    def _load_mobile_caps_config(self) -> Dict[str, Any]:
        return self._load_yaml_config('mobile_caps.yaml')
    
    @property
    def base_url(self) -> str:
        return self.env_config.get('base_url', '')
    
    @property
    def timeout(self) -> int:
        return self.env_config.get('timeout', 30)
    
    @property
    def db_host(self) -> str:
        return self.db_config.get('host', 'localhost')
    
    @property
    def db_port(self) -> int:
        return self.db_config.get('port', 3306)
    
    @property
    def db_user(self) -> str:
        return self.db_config.get('user', 'root')
    
    @property
    def db_password(self) -> str:
        return self.db_config.get('password', '')
    
    @property
    def db_database(self) -> str:
        return self.db_config.get('database', '')

    @property
    def mobile_platform(self) -> str:
        return os.getenv('MOBILE_PLATFORM', self.mobile_env_config.get('platform', 'android'))

    @property
    def mobile_appium_server(self) -> str:
        return os.getenv('APPIUM_SERVER', self.mobile_env_config.get('appium_server', 'http://127.0.0.1:4723'))

    @property
    def mobile_app_path(self) -> str:
        return os.getenv('MOBILE_APP_PATH', self.mobile_env_config.get('app_path', ''))

    @property
    def mobile_udid(self) -> str:
        return os.getenv('MOBILE_UDID', self.mobile_env_config.get('udid', ''))

    @property
    def mobile_device_name(self) -> str:
        return os.getenv('MOBILE_DEVICE_NAME', self.mobile_env_config.get('device_name', ''))

    @property
    def mobile_no_reset(self) -> bool:
        value = os.getenv('MOBILE_NO_RESET')
        if value is not None:
            return value.lower() in {'1', 'true', 'yes', 'on'}
        return bool(self.mobile_env_config.get('no_reset', False))

    @property
    def mobile_implicit_wait(self) -> int:
        value = os.getenv('MOBILE_IMPLICIT_WAIT')
        if value is not None:
            return int(value)
        return int(self.mobile_env_config.get('implicit_wait', 5))

    @property
    def mobile_explicit_wait(self) -> int:
        value = os.getenv('MOBILE_EXPLICIT_WAIT')
        if value is not None:
            return int(value)
        return int(self.mobile_env_config.get('explicit_wait', 15))

    def get_mobile_capabilities(self, platform: str = '') -> Dict[str, Any]:
        target_platform = (platform or self.mobile_platform or 'android').lower()
        common_caps = self.mobile_caps_config.get('common', {})
        platform_caps = self.mobile_caps_config.get(target_platform, {})
        capabilities = {**common_caps, **platform_caps}

        if self.mobile_device_name:
            capabilities['deviceName'] = self.mobile_device_name
        if self.mobile_udid:
            capabilities['udid'] = self.mobile_udid
        if self.mobile_app_path:
            capabilities['app'] = self.mobile_app_path

        capabilities.setdefault('platformName', target_platform.capitalize())
        capabilities['noReset'] = self.mobile_no_reset
        return capabilities


settings = Settings()
