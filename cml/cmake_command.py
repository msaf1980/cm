import os

from .cmake_element import CMakeElement
from .cmake import ElementType, TokenType


class CMakeCommand(CMakeElement):
    """A section of a cmake file that represents a command"""

    def __init__(self, tokens):
        """Constructor"""
        super().__init__(ElementType.COMMAND)
        self.tokens = tokens

    def print(self):
        """Print element to terminal"""

        print('CMD:')
        for (token_type, token) in self.tokens:
            if token_type in [ TokenType.DEFAULT, TokenType.STRING, TokenType.SPECIAL_CHAR ]:
                print('- {}'.format(token))
        print('')
