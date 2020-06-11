from databases import DatabaseURL
from starlette.config import Config

config = Config(".env")

DB_URL = config("DB_URL", cast=DatabaseURL)
APP_NAME = config("APP_NAME", cast=str, default="Todo App")
