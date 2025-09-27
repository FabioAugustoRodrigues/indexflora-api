from app.database.connection import get_mysql_connection

from pymysql.cursors import DictCursor

import json

class SearchLogModel:
    def __init__(self, redis_index_name: str, parameters: str, duration_ms: int):
        self.redis_index_name = redis_index_name
        self.parameters = parameters
        self.duration_ms = duration_ms

    def save(self):
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO search_logs (redis_index_name, parameters, duration_ms)
            VALUES (%s, %s, %s)
        """, (self.redis_index_name, self.parameters, self.duration_ms))
        conn.commit()
        cursor.close()
        conn.close()
