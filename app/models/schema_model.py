from app.database.connection import get_mysql_connection

from pymysql.cursors import DictCursor

import json

class SearchSchemaModel:
    def __init__(self, name: str, redis_index_name: str, fields: str):
        self.name = name
        self.redis_index_name = redis_index_name
        self.fields = fields

    def save(self):
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO search_schemas (name, redis_index_name, fields)
            VALUES (%s, %s, %s)
        """, (self.name, self.redis_index_name, self.fields))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_by_redis_index_name(redis_index_name: str):
        conn = get_mysql_connection()
        cursor = conn.cursor(cursor=DictCursor)
        cursor.execute("""
            SELECT name, redis_index_name, fields
            FROM search_schemas
            WHERE redis_index_name = %s
        """, (redis_index_name,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
            
        if result:
            return SearchSchemaModel(
                name=result["name"],
                redis_index_name=result["redis_index_name"],
                fields=json.loads(result["fields"])
            )
        
        return None

    @staticmethod
    def get_by_name(redis_index_name: str):
        conn = get_mysql_connection()
        cursor = conn.cursor(cursor=DictCursor)
        cursor.execute("""
            SELECT name, redis_index_name, fields
            FROM search_schemas
            WHERE name = %s
        """, (redis_index_name,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
            
        if result:
            return SearchSchemaModel(
                name=result["name"],
                redis_index_name=result["redis_index_name"],
                fields=json.loads(result["fields"])
            )
        
        return None
