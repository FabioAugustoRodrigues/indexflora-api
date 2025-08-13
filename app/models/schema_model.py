from app.database.connection import get_mysql_connection

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
