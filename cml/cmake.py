import os

from enum import Enum


class TokenType(Enum):
    """Type of token"""
    DEFAULT = 1
    WHITESPACE = 2
    COMMENT = 3
    STRING = 4
    SPECIAL_CHAR = 5
    EOL = 6
    EOF = 7

class ElementType(Enum):
    """Type of structurel element"""
    WHITESPACE = 0
    COMMAND = 1
    COMMENT = 2
