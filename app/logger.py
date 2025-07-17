import logging

logger = logging.getLogger("shop_backend")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler) 