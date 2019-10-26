import os
import sys

from .cmake import ElementType


class CMakeElement:
    """Class that represents an element of a cmake file"""

    def __init__(self, element_type):
        """Constructor"""
        self.element_type = element_type
        self.tokens = []

    def get_type(self):
        """Get type of element"""
        return self.element_type

    def is_command(self):
        """Check if element is a command"""
        return self.element_type == ElementType.COMMAND

    def is_comment(self):
        """Check if element is a comment"""
        return self.element_type == ElementType.COMMENT

    def is_whitespace(self):
        """Check if element is whitespace"""
        return self.element_type == ElementType.WHITESPACE

    def print(self):
        """Print element to terminal"""
        self.write(sys.stdout)

    def write(self, stream):
        """Print element to stream"""
