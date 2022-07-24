from enum import Enum


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class BustType(str, Enum):
    """
    Тип бюста.
    """

    NATURAL = "Natural"
    IMPLANTS = "Implants"
