import pymysql
from pymysql.cursors import DictCursor
from flask import g, current_app
from flask_login import LoginManager
from elasticsearch import Elasticsearch

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "로그인이 필요합니다."

es = None


def init_es(app):
    global es
    es = Elasticsearch(app.config["ES_HOST"])


def get_db():
    if "db_conn" not in g:
        g.db_conn = pymysql.connect(
            host=current_app.config["DB_HOST"],
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASSWORD"],
            database=current_app.config["DB_NAME"],
            charset="utf8mb4",
            cursorclass=DictCursor,
            autocommit=False,
        )
    return g.db_conn


def close_db(exception=None):
    conn = g.pop("db_conn", None)
    if conn is not None:
        conn.close()
