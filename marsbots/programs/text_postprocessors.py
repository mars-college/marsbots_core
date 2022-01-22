import re


def remove_empty_lines(response):
    response = re.sub(r"[\n]+", "\\n", response)
    return response


def include_preface(response, settings):
    if settings.preface:
        response = settings.preface + response
    return response
