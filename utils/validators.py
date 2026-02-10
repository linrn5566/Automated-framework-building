import re
from typing import Any
from core.logger import log


class Validators:
    @staticmethod
    def is_mobile(mobile: str) -> bool:
        pattern = r'^1[3-9]\d{9}$'
        result = bool(re.match(pattern, mobile))
        if not result:
            log.warning(f"手机号格式验证失败: {mobile}")
        return result
    
    @staticmethod
    def is_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        result = bool(re.match(pattern, email))
        if not result:
            log.warning(f"邮箱格式验证失败: {email}")
        return result
    
    @staticmethod
    def is_id_card(id_card: str) -> bool:
        pattern = r'^\d{17}[\dXx]$'
        result = bool(re.match(pattern, id_card))
        if not result:
            log.warning(f"身份证号格式验证失败: {id_card}")
        return result
    
    @staticmethod
    def is_bank_card(bank_card: str) -> bool:
        pattern = r'^\d{16,19}$'
        result = bool(re.match(pattern, bank_card))
        if not result:
            log.warning(f"银行卡号格式验证失败: {bank_card}")
        return result
    
    @staticmethod
    def is_password_strong(password: str, min_length: int = 8) -> bool:
        if len(password) < min_length:
            log.warning(f"密码长度不足: {len(password)} < {min_length}")
            return False
        
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        
        result = has_upper and has_lower and has_digit
        if not result:
            log.warning("密码强度不足: 需要包含大小写字母和数字")
        return result
    
    @staticmethod
    def is_url(url: str) -> bool:
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        result = bool(re.match(pattern, url))
        if not result:
            log.warning(f"URL格式验证失败: {url}")
        return result
    
    @staticmethod
    def is_positive_number(value: Any) -> bool:
        try:
            num = float(value)
            result = num > 0
            if not result:
                log.warning(f"数值不是正数: {value}")
            return result
        except ValueError:
            log.warning(f"无法转换为数值: {value}")
            return False
    
    @staticmethod
    def is_in_range(value: float, min_val: float, max_val: float) -> bool:
        result = min_val <= value <= max_val
        if not result:
            log.warning(f"数值 {value} 不在范围 [{min_val}, {max_val}] 内")
        return result
    
    @staticmethod
    def is_not_empty(value: Any) -> bool:
        if value is None:
            log.warning("值为None")
            return False
        
        if isinstance(value, (str, list, dict)) and len(value) == 0:
            log.warning("值为空")
            return False
        
        return True


validators = Validators()
