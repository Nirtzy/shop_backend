import threading
import time
from flask import current_app
from .utils import fetch_all_products, update_database
from .logger import logger

class APIFetcherThread(threading.Thread):
    def __init__(self, app):
        super().__init__(daemon=True)
        self.app = app

    def run(self):
        with self.app.app_context():
            interval = self.app.config["FETCH_INTERVAL"]
            while True:
                logger.info("Fetching data from API...")
                products = fetch_all_products()
                update_database(products)
                time.sleep(interval)
