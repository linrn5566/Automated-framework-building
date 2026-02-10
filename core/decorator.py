import time
import functools
import allure
from typing import Callable
from core.logger import log


def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """
    重试装饰器
    :param max_attempts: 最大重试次数
    :param delay: 重试间隔时间（秒）
    :param exceptions: 需要捕获的异常类型
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        log.error(f"函数 {func.__name__} 执行失败，已重试 {max_attempts} 次: {str(e)}")
                        raise
                    log.warning(f"函数 {func.__name__} 执行失败，第 {attempts} 次重试: {str(e)}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


def log_request_response(func: Callable):
    """
    记录请求和响应的装饰器
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        method = kwargs.get('method', args[1] if len(args) > 1 else 'UNKNOWN')
        endpoint = kwargs.get('endpoint', args[2] if len(args) > 2 else '')
        
        log.info(f"发送请求: {method} {endpoint}")
        log.debug(f"请求参数: {kwargs}")
        
        start_time = time.time()
        try:
            response = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            
            log.info(f"响应状态码: {response.status_code}, 耗时: {elapsed_time:.3f}s")
            log.debug(f"响应内容: {response.text[:500]}")
            
            with allure.step(f"{method} {endpoint}"):
                allure.attach(
                    f"{method} {endpoint}\n参数: {kwargs}",
                    name="请求信息",
                    attachment_type=allure.attachment_type.TEXT
                )
                allure.attach(
                    f"状态码: {response.status_code}\n耗时: {elapsed_time:.3f}s\n响应: {response.text}",
                    name="响应信息",
                    attachment_type=allure.attachment_type.TEXT
                )
            
            return response
        except Exception as e:
            elapsed_time = time.time() - start_time
            log.error(f"请求失败: {method} {endpoint}, 耗时: {elapsed_time:.3f}s, 错误: {str(e)}")
            raise
    return wrapper


def performance_monitor(threshold=3.0):
    """
    性能监控装饰器
    :param threshold: 性能阈值（秒），超过则告警
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            
            if elapsed_time > threshold:
                log.warning(f"性能告警: {func.__name__} 执行时间 {elapsed_time:.3f}s 超过阈值 {threshold}s")
            
            return result
        return wrapper
    return decorator


def exception_handler(default_return=None):
    """
    异常处理装饰器
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log.error(f"函数 {func.__name__} 执行异常: {str(e)}", exc_info=True)
                return default_return
        return wrapper
    return decorator
