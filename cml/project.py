import os

from . import utils
from . import CMakeParser


class Project:
    """Class that represents a cmake project on the disk"""

    def __init__(self, path=None):
        """Default Constructor"""

        # Initialize data
        self.path = path or '.' # Path to project directory
        self.cmake_file = None  # The main cmake file

        # Scan project directory
        self.scan()

    def scan(self):
        """Scan the project files"""

        # Reset data
        self.cmake_file = None

        # Parse main cmake file
        parser = CMakeParser()
        self.cmake_file = parser.load(os.path.join(self.path, 'CMakeLists.txt'))

    def is_valid(self):
        """Check if the project is a valid cmake_init project"""
        return self.cmake_file != None

    def initialize(self, name, dry=True):
        """Initialize the cmake project"""

        # Create directory if necessary
        if not utils.ensure_dir(self.path):
            print('Could not create directory "{}".'.format(self.path))
            return False

        # Abort if directory is not empty
        if not utils.dir_empty(self.path):
            print('Directory "{}" is not empty.'.format(self.path))
            return False

        # Copy project template
        if not utils.apply_template(os.path.join(utils.data_dir(), 'templates/core'), self.path, dry):
            print('Could not initialize project.')
            return False

        # Rescan project
        self.scan()

        # Done
        return True

    def test_cmd(self):
        """Execute test operation (for development)"""

        self.cmake_file.set_command_arg([ 'set', 'META_PROJECT_NAME' ], 1, '"test"')

        cmd = self.cmake_file.find_commands([ 'add_subdirectory' ])[0]
        self.cmake_file.add_command([ 'found', 'here' ], before=cmd)
        self.cmake_file.add_command([ 'found', 'here' ], after=cmd)
        self.cmake_file.add_command([ 'found', 'here' ])

        self.cmake_file.save()
