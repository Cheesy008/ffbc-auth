import re


def is_valid_url(url: str) -> bool:
    regex = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
    return True if re.match(regex, url) else False


def validate_url(url: str) -> str:
    if not is_valid_url(url):
        raise ValueError("Value is not a valid url")
    return url
