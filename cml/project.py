import os

from . import utils


class Project:
    """Class that represents a cmake project on the disk"""

    def __init__(self, path=None):
        """Default Constructor"""
        self.path = path or '.'
        self.scan()

    def scan(self):
        """Scan the project files"""
        self.entries = os.listdir(self.path)

    def exists(self):
        """Check if the project directory exists"""
        return os.path.isdir(self.path)

    def is_initialized(self):
        """Check if the project has been initialized and is a valid cmake-init project"""
        return os.path.isfile(os.path.join(self.path, 'CMakeLists.txt'))

    def initialize(self, name, dry=True):
        """Initialize the cmake project"""

        # Abort if project has already been initialized
        if self.is_initialized():
            print('Project is already initialized.')
            return False

        # Copy project template
        if not utils.apply_template(os.path.join(utils.data_dir(), 'templates/core'), self.path, dry):
            print('Could not initialize project.')
            return False

        # Rescan project
        self.scan()

        # Done
        return True
