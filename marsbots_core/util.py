from random import random

import numpy as np


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def hex_to_rgb_float(hex_str):
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


def randomly(prob):
    def decorator(function):
        def wrapper(*args, **kwargs):
            if prob > random():
                return function(*args, **kwargs)

        return wrapper

    return decorator


def pythonify_json(json_data):

    correctedDict = {}

    for key, value in json_data.items():
        if isinstance(value, list):
            value = [
                pythonify_json(item) if isinstance(item, dict) else item
                for item in value
            ]
        elif isinstance(value, dict):
            value = pythonify_json(value)
        try:
            key = int(key)
        except Exception:
            pass
        correctedDict[key] = value

    return correctedDict
