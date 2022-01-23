import requests

from marsbots_core.config import IFTTT_KEY


def ifttt_get(event_name):
    url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{IFTTT_KEY}"
    response = requests.get(url)
    return response


def ifttt_post(event_name, payload):
    url = f"https://maker.ifttt.com/trigger/{event_name}/json/with/key/{IFTTT_KEY}"
    response = requests.post(url, data=payload)
    return response
