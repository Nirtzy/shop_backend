from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from .logger import logger

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from . import models  # импорт моделей, чтобы SQLAlchemy их знал
        db.create_all()
        logger.info("Таблицы успешно созданы (если их не было).")

        from .routes import bp as routes_bp
        app.register_blueprint(routes_bp)

        from .api_fetcher import APIFetcherThread
        fetcher = APIFetcherThread(app)
        fetcher.start()
        logger.info("Фоновый поток для загрузки API запущен.")

    return app
