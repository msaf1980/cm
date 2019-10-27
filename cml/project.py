import os

from . import utils
from .cmake_parser import CMakeParser


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

        # Check if main cmake file exists
        return self.cmake_file != None

    def get_prop(self, prop):
        """Get property value"""

        # Helper function to get the parameter value of a cmake command
        def get_command_arg_value(signature, index):
            cmds = self.cmake_file.find_commands(signature)
            if len(cmds) == 1:
                return cmds[0].get_arg_value(index)
            else:
                return None

        # Determine property
        if prop == 'name':
            # Project name
            return get_command_arg_value([ 'set', 'META_PROJECT_NAME' ], 1).strip('\"')
        elif prop == 'description':
            # Project description
            return get_command_arg_value([ 'set', 'META_PROJECT_DESCRIPTION' ], 1).strip('\"')
        elif prop == 'author_name':
            # Author name
            return get_command_arg_value([ 'set', 'META_AUTHOR_ORGANIZATION' ], 1).strip('\"')
        elif prop == 'author_domain':
            # Author domain
            return get_command_arg_value([ 'set', 'META_AUTHOR_DOMAIN' ], 1).strip('\"')
        elif prop == 'author_maintainer':
            # Author maintainer
            return get_command_arg_value([ 'set', 'META_AUTHOR_MAINTAINER' ], 1).strip('\"')
        elif prop == 'version':
            # Project Version
            major = get_command_arg_value([ 'set', 'META_VERSION_MAJOR' ], 1).strip('\"')
            minor = get_command_arg_value([ 'set', 'META_VERSION_MINOR' ], 1).strip('\"')
            patch = get_command_arg_value([ 'set', 'META_VERSION_PATCH' ], 1).strip('\"')
            return '{}.{}.{}'.format(major, minor, patch)

        # Property not found
        return None

    def set_prop(self, prop, value):
        """Set property value"""

        # Helper function to set the parameter value of a cmake command
        def set_command_arg_value(signature, index, value):
            cmds = self.cmake_file.find_commands(signature)
            if len(cmds) == 1:
                cmds[0].set_arg_value(index, value)

        # Determine property
        if prop == 'name':
            # Project name
            set_command_arg_value([ 'set', 'META_PROJECT_NAME' ], 1, '"{}"'.format(value))
        elif prop == 'description':
            # Project name
            set_command_arg_value([ 'set', 'META_PROJECT_DESCRIPTION' ], 1, '"{}"'.format(value))
        elif prop == 'author_name':
            # Author name
            set_command_arg_value([ 'set', 'META_AUTHOR_ORGANIZATION' ], 1, '"{}"'.format(value))
        elif prop == 'author_domain':
            # Author name
            set_command_arg_value([ 'set', 'META_AUTHOR_DOMAIN' ], 1, '"{}"'.format(value))
        elif prop == 'author_maintainer':
            # Author name
            set_command_arg_value([ 'set', 'META_AUTHOR_MAINTAINER' ], 1, '"{}"'.format(value))
        elif prop == 'version':
            # Project Version
            values = value.split('.')
            if len(values) == 3:
                set_command_arg_value([ 'set', 'META_VERSION_MAJOR' ], 1, '"{}"'.format(values[0]))
                set_command_arg_value([ 'set', 'META_VERSION_MINOR' ], 1, '"{}"'.format(values[1]))
                set_command_arg_value([ 'set', 'META_VERSION_PATCH' ], 1, '"{}"'.format(values[2]))

        # Save cmake file
        self.cmake_file.save()

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
        """Execute test command (for development)"""

        # Rename project to 'testproject'
        self.set_prop('project_name', 'testproject')

        # Save cmake file
        self.cmake_file.save()
