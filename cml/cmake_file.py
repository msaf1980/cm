import os

from . import ElementType, TokenType, CMakeCommand, CMakeComment, CMakeWhitespace


class CMakeFile:
    """Class that represents the contents of a CMakeLists.txt file"""

    def __init__(self, path):
        """Constructor"""
        self.elements = []

    def add(self, element):
        """Add element to file"""
        self.elements.append(element)

    def print(self):
        """Print content of cmake file to terminal"""
        for element in self.elements:
            element.print()
