import os

from .cmake_element import CMakeElement
from .cmake import ElementType, TokenType


class CMakeCommand(CMakeElement):
    """A section of a cmake file that represents a command"""

    def __init__(self, tokens):
        """Constructor

        Args:
            tokens (list): List of tokens that belong to the command

        """
        super().__init__(ElementType.COMMAND)

        # Initialize
        self.tokens = tokens
        self.name = ''
        self.args = []

        # Parse command
        self.parse()

    def write(self, stream):
        """Print element to stream

        Args:
            stream (file object): Output stream to write to

        """

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
        """Get command signature (name and arguments)

        Args:
            numargs (int): Number of arguments to include of the signature
        
        Returns:
            list: List of name and arguments of the command

        """

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
        """Get command argument

        Args:
            index (int): Index of argument to get
        
        Returns:
            (TokenType, token): Argument at the given index, or None

        """

        # Return argument at given index or None
        if index >= 0 and index < len(self.args):
            return self.args[index]
        else:
            return None

    def get_arg_value(self, index):
        """Get command argument value

        Args:
            index (int): Index of argument to get
        
        Returns:
            string: Argument value at the given index, or None

        """

        # Get argument at given index
        arg = self.get_arg(index)
        if arg:
            # Return value
            return arg[1]
        else:
            # Does not exist
            return None

    def set_arg_value(self, index, value):
        """Set command argument value

        Args:
            index (int): Index of argument to get
            value (string) Argument value
        
        """

        # Get argument at given index
        arg = self.get_arg(index)
        if arg:
            # Set value
            arg[1] = value
