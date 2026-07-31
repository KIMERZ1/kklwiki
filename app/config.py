import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
    DB_NAME = os.environ.get("DB_NAME", "wiki_db")

    ES_HOST = os.environ.get("ES_HOST", "http://localhost:9200")
    ES_INDEX = "wiki_pages"
