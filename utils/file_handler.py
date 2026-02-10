import json
import yaml
from pathlib import Path
from typing import Dict, Any, List
from core.logger import log


class FileHandler:
    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            log.info(f"读取JSON文件成功: {file_path}")
            return data
        except Exception as e:
            log.error(f"读取JSON文件失败: {file_path}, 错误: {str(e)}")
            raise
    
    @staticmethod
    def write_json(file_path: str, data: Dict[str, Any], indent: int = 2):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)
            log.info(f"写入JSON文件成功: {file_path}")
        except Exception as e:
            log.error(f"写入JSON文件失败: {file_path}, 错误: {str(e)}")
            raise
    
    @staticmethod
    def read_yaml(file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            log.info(f"读取YAML文件成功: {file_path}")
            return data
        except Exception as e:
            log.error(f"读取YAML文件失败: {file_path}, 错误: {str(e)}")
            raise
    
    @staticmethod
    def write_yaml(file_path: str, data: Dict[str, Any]):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
            log.info(f"写入YAML文件成功: {file_path}")
        except Exception as e:
            log.error(f"写入YAML文件失败: {file_path}, 错误: {str(e)}")
            raise
    
    @staticmethod
    def read_text(file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            log.info(f"读取文本文件成功: {file_path}")
            return content
        except Exception as e:
            log.error(f"读取文本文件失败: {file_path}, 错误: {str(e)}")
            raise
    
    @staticmethod
    def write_text(file_path: str, content: str):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            log.info(f"写入文本文件成功: {file_path}")
        except Exception as e:
            log.error(f"写入文本文件失败: {file_path}, 错误: {str(e)}")
            raise
    
    @staticmethod
    def ensure_dir(dir_path: str):
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        log.debug(f"确保目录存在: {dir_path}")
    
    @staticmethod
    def list_files(dir_path: str, pattern: str = "*") -> List[Path]:
        path = Path(dir_path)
        if not path.exists():
            log.warning(f"目录不存在: {dir_path}")
            return []
        
        files = list(path.glob(pattern))
        log.debug(f"列出文件: {dir_path}/{pattern}, 共 {len(files)} 个")
        return files


file_handler = FileHandler()
