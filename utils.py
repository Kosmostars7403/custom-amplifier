import requests


def handle_request(url, payload):
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()