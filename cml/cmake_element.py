import os
import sys

from .cmake import ElementType


class CMakeElement:
    """Class that represents an element of a cmake file"""

    def __init__(self, element_type):
        """Constructor

        Args:
            element_type (ElementType): Type of element

        """

        self.element_type = element_type
        self.tokens = []

    def get_type(self):
        """Get type of element

        Returns:
            ElementType: Type of element

        """
        return self.element_type

    def is_command(self):
        """Check if element is a command

        Returns:
            Boolean: True if element is a command, else False

        """
        return self.element_type == ElementType.COMMAND

    def is_comment(self):
        """Check if element is a comment

        Returns:
            Boolean: True if element is a comment, else False

        """
        return self.element_type == ElementType.COMMENT

    def is_whitespace(self):
        """Check if element is whitespace

        Returns:
            Boolean: True if element is a whitespace element, else False

        """
        return self.element_type == ElementType.WHITESPACE

    def print(self):
        """Print element to terminal"""
        self.write(sys.stdout)

    def write(self, stream):
        """Print element to stream

        Args:
            stream (file object): Output stream to write to

        """
