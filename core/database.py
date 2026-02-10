import pymysql
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
from core.logger import log


class DatabaseHelper:
    def __init__(self, host: str, port: int, user: str, password: str, database: str, charset: str = 'utf8mb4'):
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'charset': charset
        }
        self.connection = None
    
    @contextmanager
    def get_connection(self):
        try:
            self.connection = pymysql.connect(**self.config)
            yield self.connection
        except Exception as e:
            log.error(f"数据库连接失败: {str(e)}")
            raise
        finally:
            if self.connection:
                self.connection.close()
    
    def execute_query(self, sql: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            try:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute(sql, params)
                    results = cursor.fetchall()
                    log.info(f"查询成功: {sql}, 返回 {len(results)} 条记录")
                    return results
            except Exception as e:
                log.error(f"查询失败: {sql}, 错误: {str(e)}")
                raise
    
    def execute_update(self, sql: str, params: Optional[tuple] = None) -> int:
        with self.get_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    affected_rows = cursor.execute(sql, params)
                    conn.commit()
                    log.info(f"更新成功: {sql}, 影响 {affected_rows} 行")
                    return affected_rows
            except Exception as e:
                conn.rollback()
                log.error(f"更新失败: {sql}, 错误: {str(e)}")
                raise
    
    def execute_many(self, sql: str, params_list: List[tuple]) -> int:
        with self.get_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    affected_rows = cursor.executemany(sql, params_list)
                    conn.commit()
                    log.info(f"批量执行成功: {sql}, 影响 {affected_rows} 行")
                    return affected_rows
            except Exception as e:
                conn.rollback()
                log.error(f"批量执行失败: {sql}, 错误: {str(e)}")
                raise
    
    def query_one(self, sql: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
        results = self.execute_query(sql, params)
        return results[0] if results else None
    
    def query_coupon(self, coupon_id: int) -> Optional[Dict[str, Any]]:
        sql = "SELECT * FROM coupons WHERE id = %s"
        return self.query_one(sql, (coupon_id,))
    
    def query_user_coupons(self, user_id: int) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM user_coupons WHERE user_id = %s"
        return self.execute_query(sql, (user_id,))
    
    def delete_test_data(self, table: str, condition: str, params: Optional[tuple] = None):
        sql = f"DELETE FROM {table} WHERE {condition}"
        return self.execute_update(sql, params)
