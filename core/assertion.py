import jsonschema
from typing import Dict, Any, List
from requests import Response
from core.logger import log
import allure


class EnhancedAssertion:
    
    @staticmethod
    @allure.step("断言响应状态码")
    def assert_response_code(response: Response, expected_code: int = 200, message: str = ""):
        actual_code = response.status_code
        msg = message or f"期望状态码 {expected_code}, 实际 {actual_code}"
        
        try:
            assert actual_code == expected_code, msg
            log.info(f"✓ 状态码断言通过: {actual_code}")
        except AssertionError as e:
            log.error(f"✗ 状态码断言失败: {msg}")
            allure.attach(response.text, name="响应内容", attachment_type=allure.attachment_type.TEXT)
            raise e
    
    @staticmethod
    @allure.step("断言响应时间")
    def assert_response_time(response: Response, max_time: float = 3.0):
        elapsed_time = response.elapsed.total_seconds()
        msg = f"响应时间 {elapsed_time:.3f}s 超过阈值 {max_time}s"
        
        try:
            assert elapsed_time <= max_time, msg
            log.info(f"✓ 响应时间断言通过: {elapsed_time:.3f}s")
        except AssertionError as e:
            log.warning(f"✗ 响应时间断言失败: {msg}")
            raise e
    
    @staticmethod
    @allure.step("断言JSON Schema")
    def assert_json_schema(response: Response, schema: Dict[str, Any]):
        try:
            json_data = response.json()
            jsonschema.validate(instance=json_data, schema=schema)
            log.info("✓ JSON Schema验证通过")
        except jsonschema.ValidationError as e:
            log.error(f"✗ JSON Schema验证失败: {e.message}")
            allure.attach(str(e), name="Schema验证错误", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError(f"JSON Schema验证失败: {e.message}")
        except ValueError as e:
            log.error(f"✗ 响应不是有效的JSON格式: {str(e)}")
            raise AssertionError("响应不是有效的JSON格式")
    
    @staticmethod
    @allure.step("断言包含字段")
    def assert_contains_fields(response: Response, fields: List[str], message: str = ""):
        try:
            json_data = response.json()
            missing_fields = [field for field in fields if field not in json_data]
            
            msg = message or f"缺少字段: {missing_fields}"
            assert not missing_fields, msg
            log.info(f"✓ 字段存在断言通过: {fields}")
        except ValueError:
            raise AssertionError("响应不是有效的JSON格式")
        except AssertionError as e:
            log.error(f"✗ 字段存在断言失败: {msg}")
            allure.attach(response.text, name="响应内容", attachment_type=allure.attachment_type.TEXT)
            raise e
    
    @staticmethod
    @allure.step("断言字段值")
    def assert_field_value(response: Response, field: str, expected_value: Any, message: str = ""):
        try:
            json_data = response.json()
            actual_value = EnhancedAssertion._get_nested_value(json_data, field)
            
            msg = message or f"字段 {field} 期望值 {expected_value}, 实际值 {actual_value}"
            assert actual_value == expected_value, msg
            log.info(f"✓ 字段值断言通过: {field} = {actual_value}")
        except (ValueError, KeyError) as e:
            raise AssertionError(f"无法获取字段 {field}: {str(e)}")
        except AssertionError as e:
            log.error(f"✗ 字段值断言失败: {msg}")
            raise e
    
    @staticmethod
    def _get_nested_value(data: Dict, field: str) -> Any:
        keys = field.split('.')
        value = data
        for key in keys:
            if isinstance(value, dict):
                value = value[key]
            else:
                raise KeyError(f"字段 {field} 不存在")
        return value
