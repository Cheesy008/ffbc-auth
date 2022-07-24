import re


def is_valid_phone(number: str) -> bool:
    regex = r"(\+\d{1,3}\s?)?((\(\d{3}\)\s?)|(\d{3})(\s|-?))(\d{3}(\s|-?))(\d{4})(\s?(([E|e]xt[:|.|]?)|x|X)(\s?\d+))?"
    return True if re.match(regex, number) else False


def validate_phone(number: str) -> str:
    if not is_valid_phone(number):
        raise ValueError("Value is not a valid phone number")
    return number
