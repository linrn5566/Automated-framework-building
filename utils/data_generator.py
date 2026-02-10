from faker import Faker
import random
import string
from datetime import datetime, timedelta
from typing import Dict, Any


class DataGenerator:
    def __init__(self, locale='zh_CN'):
        self.faker = Faker(locale)
    
    def generate_username(self, prefix: str = "user") -> str:
        return f"{prefix}_{self.faker.user_name()}_{random.randint(1000, 9999)}"
    
    def generate_mobile(self) -> str:
        return self.faker.phone_number()
    
    def generate_email(self) -> str:
        return self.faker.email()
    
    def generate_id_card(self) -> str:
        return self.faker.ssn()
    
    def generate_password(self, length: int = 12) -> str:
        chars = string.ascii_letters + string.digits + "!@#$%"
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_coupon_code(self, prefix: str = "CPN", length: int = 12) -> str:
        chars = string.ascii_uppercase + string.digits
        code = ''.join(random.choice(chars) for _ in range(length))
        return f"{prefix}{code}"
    
    def generate_coupon_data(self, coupon_type: str = "discount") -> Dict[str, Any]:
        return {
            "name": f"测试卡券_{self.faker.word()}",
            "type": coupon_type,
            "amount": random.choice([10, 20, 50, 100]),
            "total_stock": random.randint(100, 1000),
            "available_stock": random.randint(100, 1000),
            "start_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
            "description": self.faker.text(max_nb_chars=50),
            "min_order_amount": random.choice([0, 100, 200, 500]),
            "status": "active"
        }
    
    def generate_activity_data(self) -> Dict[str, Any]:
        return {
            "title": f"测试活动_{self.faker.catch_phrase()}",
            "description": self.faker.text(max_nb_chars=100),
            "start_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S'),
            "max_participants": random.randint(100, 1000),
            "status": "draft",
            "rules": {
                "max_per_user": random.randint(1, 5),
                "conditions": self.faker.text(max_nb_chars=50)
            }
        }
    
    def generate_user_data(self) -> Dict[str, Any]:
        return {
            "username": self.generate_username(),
            "password": self.generate_password(),
            "mobile": self.generate_mobile(),
            "email": self.generate_email(),
            "real_name": self.faker.name(),
            "id_card": self.generate_id_card(),
            "gender": random.choice(["male", "female"]),
            "birthday": self.faker.date_of_birth(minimum_age=18, maximum_age=60).strftime('%Y-%m-%d')
        }
    
    def generate_order_data(self, amount: float = None) -> Dict[str, Any]:
        return {
            "order_no": f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}",
            "amount": amount or round(random.uniform(10, 1000), 2),
            "product_name": self.faker.word(),
            "quantity": random.randint(1, 10),
            "user_id": random.randint(1, 10000)
        }


data_generator = DataGenerator()
