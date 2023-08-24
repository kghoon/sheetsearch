
import requests
from sheetsearch import config

_cache = {}

def search_images(query: str):
    if _cache.get(query) is not None:
        return _cache[query]

    base_url= "https://customsearch.googleapis.com/customsearch/v1"
    query_data = {
        'cx': config.CUSTOM_SEARCH_CX,
        'q': query,
        'searchType': 'image',
        'key': config.CUSTOM_SEARCH_API_KEY
    }
    headers = {
        'Accept': 'application/json'
    }
    r = requests.get(base_url, params=query_data, headers=headers)
    r.raise_for_status()
    result = r.json()

    _cache[query] = result

    return result
