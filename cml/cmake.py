import os

from enum import Enum


class TokenType(Enum):
    """Type of token

    - DEFAULT: Keyword or symbol
    - WHITESPACE: Whitespace
    - COMMENT: Comment block
    - STRING: String value
    - SPECIAL_CHAR: Opening or closing bracket
    - EOL: End of line
    - EOF: End of file

    """
    DEFAULT = 1
    WHITESPACE = 2
    COMMENT = 3
    STRING = 4
    SPECIAL_CHAR = 5
    EOL = 6
    EOF = 7

class ElementType(Enum):
    """Type of structural element

    - COMMAND: Element containing a cmake command
    - COMMENT: Element containing comments
    - WHITESPACE: Element containing only whitespace tokens
    """
    WHITESPACE = 0
    COMMAND = 1
    COMMENT = 2
