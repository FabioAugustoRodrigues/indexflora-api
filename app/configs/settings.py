import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
    MYSQL_DB = os.getenv("MYSQL_DB", "search_engine")

    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = os.getenv("REDIS_PORT", "6379")

settings = Settings()
