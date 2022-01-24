import logging

import requests

from marsbots_core.config import IFTTT_KEY


def ifttt_get(event_name: str, key: str = IFTTT_KEY):
    url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{key}"
    logging.info(f"Calling IFTTT get with url: {url}")
    response = requests.get(url)
    return response


def ifttt_post(event_name: str, payload: dict, key: str = IFTTT_KEY):
    url = f"https://maker.ifttt.com/trigger/{event_name}/json/with/key/{key}"
    logging.info(f"Calling IFTTT post with url: {url}")
    response = requests.post(url, data=payload)
    return response
