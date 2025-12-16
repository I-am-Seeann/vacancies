import requests
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('CatAPI')
file_handler = RotatingFileHandler(filename='logs/cat_api.log', maxBytes=10_000, backupCount=5)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s CatAPI %(message)s'))
logger.addHandler(hdlr=file_handler)
logger.setLevel(level=logging.INFO)
logger.propagate = False  # Important: don't duplicate to basic config handlers

def get_random_cat():
    try:
        url = "https://api.thecatapi.com/v1/images/search"

        response = requests.get(url=url, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data and len(data) > 0:
            logger.info(f"Cat pic generated successfully: {data}")
            return data[0]['url']
        return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Cat API request failed: {e}")
        return None