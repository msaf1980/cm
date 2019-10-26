import os

from .cmake_element import CMakeElement
from .cmake import ElementType, TokenType


class CMakeComment(CMakeElement):
    """A section of a cmake file that represents a comment"""

    def __init__(self, tokens):
        """Constructor"""
        super().__init__(ElementType.COMMENT)
        self.tokens = tokens

    def print(self):
        """Print element to terminal"""

        print('CMT:')
        for (token_type, token) in self.tokens:
            if token_type == TokenType.COMMENT:
                print(token)
        print('')
