import os

from .cmake_element import CMakeElement
from .cmake import ElementType, TokenType


class CMakeCommand(CMakeElement):
    """A section of a cmake file that represents a command"""

    def __init__(self, tokens):
        """Constructor"""
        super().__init__(ElementType.COMMAND)

        # Initialize
        self.tokens = tokens
        self.name = ''
        self.args = []

        # Parse command
        self.parse()

    def write(self, stream):
        """Print element to stream"""

        for (_, token) in self.tokens:
            stream.write(token)

    def parse(self):
        """Parse the elements of the command"""

        for token in self.tokens:
            if token[0] in [ TokenType.DEFAULT, TokenType.STRING ]:
                if self.name == '':
                    self.name = token[1]
                else:
                    self.args.append(token)

    def signature(self, numargs = -1):
        """Get command signature (name and arguments)"""

        # Get complete signature
        cmd = [ self.name ]
        for (_, arg) in self.args:
            cmd.append(arg)

        # Return name and specified number of arguments
        if numargs >= 0:
            return cmd[0:numargs + 1]
        else:
            return cmd

    def get_arg(self, index):
        """Get command argument"""

        if index >= 0 and index < len(self.args):
            return self.args[index]
        else:
            return None

    def set_arg(self, index, value):
        """Set command argument"""

        arg = self.get_arg(index)
        if arg:
            arg[1] = value
