import requests
from typing import Dict, Optional
from requests.exceptions import RequestException

from core.decorator import log_request_response, retry
from core.logger import log


class HttpClient:
    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        token: Optional[str] = None,
        use_session: bool = True,
    ):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.use_session = use_session

        self.session: Optional[requests.Session] = None
        if self.use_session:
            self.session = requests.Session()
            self.session.headers.update({
                'Content-Type': 'application/json',
                'User-Agent': 'Automated-Test-Framework/1.0'
            })

        if token:
            self.set_token(token)

    def set_token(self, token: str, token_type: str = "Bearer"):
        if not self.use_session or not self.session:
            raise RuntimeError("HttpClient(use_session=False) 不支持 set_token，请在请求层显式传 headers")
        self.session.headers['Authorization'] = f"{token_type} {token}"
        log.info(f"Token已设置: {token_type} {token[:20]}...")

    def remove_token(self):
        if self.session and 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
            log.info("Token已移除")

    def set_headers(self, headers: Dict[str, str]):
        if not self.use_session or not self.session:
            raise RuntimeError("HttpClient(use_session=False) 不支持 set_headers，请在请求层显式传 headers")
        self.session.headers.update(headers)

    @retry(max_attempts=3, delay=1, exceptions=(RequestException,))
    @log_request_response
    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}" if not endpoint.startswith('http') else endpoint
        kwargs.setdefault('timeout', self.timeout)

        headers = kwargs.get('headers') or {}
        headers.setdefault('Content-Type', 'application/json')
        headers.setdefault('User-Agent', 'Automated-Test-Framework/1.0')
        kwargs['headers'] = headers

        try:
            if self.use_session and self.session:
                return self.session.request(method, url, **kwargs)
            return requests.request(method, url, **kwargs)
        except RequestException as e:
            log.error(f"请求异常: {method} {url}, 错误: {str(e)}")
            raise

    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        return self.request('GET', endpoint, params=params, **kwargs)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        json: Optional[Dict] = None,
        **kwargs,
    ) -> requests.Response:
        return self.request('POST', endpoint, data=data, json=json, **kwargs)

    def put(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        json: Optional[Dict] = None,
        **kwargs,
    ) -> requests.Response:
        return self.request('PUT', endpoint, data=data, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request('DELETE', endpoint, **kwargs)

    def patch(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        json: Optional[Dict] = None,
        **kwargs,
    ) -> requests.Response:
        return self.request('PATCH', endpoint, data=data, json=json, **kwargs)

    def close(self):
        if self.session:
            self.session.close()
        log.info("HTTP会话已关闭")

