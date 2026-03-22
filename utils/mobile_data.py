from typing import Any, Dict

from config.settings import settings
from utils.file_handler import file_handler


class MobileTestData:
    def __init__(self):
        self.file_path = settings.data_dir / 'mobile' / 'test_data.yaml'
        self._cache: Dict[str, Any] = {}

    def load(self, force_reload: bool = False) -> Dict[str, Any]:
        if force_reload or not self._cache:
            if not self.file_path.exists():
                self._cache = {}
            else:
                self._cache = file_handler.read_yaml(str(self.file_path)) or {}
        return self._cache

    def get(self, *keys: str, default: Any = None) -> Any:
        data: Any = self.load()
        for key in keys:
            if not isinstance(data, dict):
                return default
            data = data.get(key)
            if data is None:
                return default
        return data


mobile_test_data = MobileTestData()
