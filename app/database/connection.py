import pymysql
from app.configs.settings import settings

def get_mysql_connection():
    connection = pymysql.connect(
        host=settings.MYSQL_HOST,
        port=int(settings.MYSQL_PORT),
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        database=settings.MYSQL_DB,
        autocommit=True,
        charset='utf8mb4'
    )
    return connection
