from flask import Flask
from dotenv import load_dotenv

from app.config import Config
from app.extensions import login_manager, init_es, close_db

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    init_es(app)

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    app.teardown_appcontext(close_db)

    from app.models.search_log import SearchLog

    @app.context_processor
    def inject_popular_queries():
        return {"popular_queries": SearchLog.top_queries(limit=5, hours=12)}

    from app.blueprints.wiki.routes import wiki_bp
    from app.blueprints.auth.routes import auth_bp
    from app.blueprints.search.routes import search_bp
    from app.blueprints.admin.routes import admin_bp

    app.register_blueprint(wiki_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
