import os

from .cmake import ElementType, TokenType
from .cmake_command import CMakeCommand
from .cmake_comment import CMakeComment
from .cmake_whitespace import CMakeWhitespace


class CMakeFile:
    """Class that represents the contents of a CMakeLists.txt file"""

    def __init__(self, path):
        """Constructor"""
        self.path = path
        self.elements = []

    def add(self, element):
        """Add element to file"""
        self.elements.append(element)

    def save(self, path = None):
        """Save file back to disk"""

        try:
            # Open file
            f = open(path or self.path, 'w')

            # Write elements to file
            for element in self.elements:
                element.write(f)

            # Done
            return True
        except:
            # Error
            return False

    def print(self):
        """Print content of cmake file to terminal"""
        for element in self.elements:
            element.print()

    def find_commands(self, signature):
        """Find commands with a specific signature"""

        # Bail out if there is not even a name in the signature
        if len(signature) <= 0:
            return []

        # Find commands that have the given signature
        cmds = []
        for element in self.elements:
            if element.is_command():
                if element.signature(len(signature) - 1) == signature:
                    cmds.append(element)

        # Return list of commands
        return cmds

    def set_command_arg(self, signature, index, value):
        """Set argument of all commands that match a certain signature"""

        # Find commands
        cmds = self.find_commands(signature)

        # Set argument on those commands
        for cmd in cmds:
            cmd.set_arg_value(index, value)

    def add_command(self, cmd, before = None, after = None):
        """Add new command"""

        # Create new command
        tokens = []
        for name in cmd:
            tokens.append([ TokenType.DEFAULT, name ])
            if len(tokens) == 1:
                tokens.append([ TokenType.SPECIAL_CHAR, '(' ])
        tokens.append([ TokenType.SPECIAL_CHAR, ')' ])
        tokens.append([ TokenType.EOL, '\n' ])
        command = CMakeCommand(tokens)

        # Insert command into file
        if before != None:
            self.elements.insert(self.elements.index(before), command)
        elif after != None:
            self.elements.insert(self.elements.index(after) + 1, command)
        else:
            self.elements.append(command)
