import requests


def get_random_cat(logger):
    try:
        url = "https://api.thecatapi.com/v1/images/search"

        response = requests.get(url=url, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data and len(data) > 0:
            return data[0]['url']
        return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Cat API request failed: {e}")
        return None