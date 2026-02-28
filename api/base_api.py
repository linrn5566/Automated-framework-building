from typing import Optional, Dict
from requests import Response
from core.http_client import HttpClient
from core.logger import log
from config.settings import settings


class BaseAPI:
    def __init__(self, client: Optional[HttpClient] = None, use_session: bool = True):
        self.client = client or HttpClient(
            base_url=settings.base_url,
            timeout=settings.timeout,
            use_session=use_session,
        )
    
    def set_token(self, token: str, token_type: str = "Bearer"):
        self.client.set_token(token, token_type)
    
    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Response:
        return self.client.get(endpoint, params=params, **kwargs)
    
    def post(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs) -> Response:
        return self.client.post(endpoint, data=data, json=json, **kwargs)
    
    def put(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs) -> Response:
        return self.client.put(endpoint, data=data, json=json, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> Response:
        return self.client.delete(endpoint, **kwargs)
    
    def patch(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs) -> Response:
        return self.client.patch(endpoint, data=data, json=json, **kwargs)
