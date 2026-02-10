import hashlib
import base64
from cryptography.fernet import Fernet
from core.logger import log


class Encryption:
    @staticmethod
    def md5(text: str) -> str:
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    @staticmethod
    def sha256(text: str) -> str:
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    @staticmethod
    def base64_encode(text: str) -> str:
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def base64_decode(encoded_text: str) -> str:
        return base64.b64decode(encoded_text.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def generate_key() -> bytes:
        return Fernet.generate_key()
    
    @staticmethod
    def encrypt(text: str, key: bytes) -> str:
        f = Fernet(key)
        encrypted_text = f.encrypt(text.encode('utf-8'))
        return encrypted_text.decode('utf-8')
    
    @staticmethod
    def decrypt(encrypted_text: str, key: bytes) -> str:
        f = Fernet(key)
        decrypted_text = f.decrypt(encrypted_text.encode('utf-8'))
        return decrypted_text.decode('utf-8')


encryption = Encryption()
