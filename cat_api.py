import os

import requests
from dotenv import load_dotenv


load_dotenv()

def get_random_cat(logger):
    api_key = os.environ.get('CAT_API_KEY')

    try:
        url = "https://api.thecatapi.com/v1/images/search"
        headers = {'x-api-key': api_key} if api_key else {}

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data and len(data) > 0:
            return data[0]['url']
        return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Cat API request failed: {e}")
        return None