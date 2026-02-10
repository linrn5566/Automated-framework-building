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
        
        self.env_config = self._load_env_config()
        self.db_config = self._load_db_config()
    
    def _load_env_config(self) -> Dict[str, Any]:
        config_file = self.config_dir / 'env_config.yaml'
        if not config_file.exists():
            return {}
        
        with open(config_file, 'r', encoding='utf-8') as f:
            all_config = yaml.safe_load(f)
            return all_config.get(self.env, {})
    
    def _load_db_config(self) -> Dict[str, Any]:
        config_file = self.config_dir / 'db_config.yaml'
        if not config_file.exists():
            return {}
        
        with open(config_file, 'r', encoding='utf-8') as f:
            all_config = yaml.safe_load(f)
            return all_config.get(self.env, {})
    
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


settings = Settings()
