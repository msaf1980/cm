import os

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

    def print(self):
        """Print element to terminal"""
