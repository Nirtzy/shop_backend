from app import create_app
from app.api_fetcher import APIFetcherThread
from app.logger import logger

app = create_app()

if __name__ == "__main__":
    logger.info("Запуск Flask-приложения...")
    # Запуск фоновой задачи загрузки API
    fetcher = APIFetcherThread(app)
    fetcher.start()
    logger.info("Фоновый поток для загрузки API запущен.")

    # Запуск веб-сервера
    app.run(host="0.0.0.0", port=5555, threaded=True)
