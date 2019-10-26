import os

from .cmake_element import CMakeElement
from .cmake import ElementType, TokenType


class CMakeWhitespace(CMakeElement):
    """A section of a cmake file that contains only whitespace"""

    def __init__(self, tokens):
        """Constructor"""
        super().__init__(ElementType.WHITESPACE)
        self.tokens = tokens

    def write(self, stream):
        """Print element to stream"""

        for (_, token) in self.tokens:
            stream.write(token)
