import os
import datetime

from . import utils
from .cmake_parser import CMakeParser
from .user_query import UserQuery


class Project:
    """Class that represents a cmake project on the disk"""

    def __init__(self, path=None, query=None):
        """Default Constructor"""

        # Initialize data
        self.path = path or '.' # Path to project directory
        self.query = query or UserQuery()
        self.cmake_file = None  # The main cmake file
        self.cmake_file_source = None  # The cmake file in source/
        self.project_name = '' # The name of the project

        # Scan project directory
        self.scan()

    def scan(self):
        """Scan the project files"""

        # Reset data
        self.cmake_file = None
        self.cmake_file_source = None

        # Parse main cmake file
        parser = CMakeParser()
        self.cmake_file = parser.load(os.path.join(self.path, 'CMakeLists.txt'))
        if self.cmake_file:
            # Get project name
            self.project_name = self.get_prop('name')

        # Parse cmake file in source
        self.cmake_file_source = parser.load(os.path.join(self.path, 'source', 'CMakeLists.txt'))

    def is_valid(self):
        """Check if the project is a valid cmake_init project"""

        # Check if main cmake file exists
        return self.cmake_file != None and self.cmake_file_source

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

    def initialize(self, name=None, description=None, author_name=None, author_domain=None,
                         author_maintainer=None, version=None, dry=True):
        """Initialize the cmake project"""

        # Create directory if necessary
        if not utils.ensure_dir(self.path):
            print('Could not create directory "{}".'.format(self.path))
            return False

        # Abort if directory is not empty
        if not utils.dir_empty(self.path):
            print('Directory "{}" is not empty.'.format(self.path))
            return False

        # Ask for missing information
        if name == None:
            name = self.query.ask('Project name', os.path.basename(os.path.realpath(self.path)))
        if description == None:
            description = self.query.ask('Project description', 'My new project')
        if author_name == None:
            author_name = self.query.ask('Author name', 'Unknown')
        if author_domain == None:
            author_domain = self.query.ask('Author domain', 'https://example.com')
        if author_maintainer == None:
            author_maintainer = self.query.ask('Maintainer email address', 'example@example.com')
        if version == None:
            version = self.query.ask('Version number', '1.0.0')

        # Copy project template
        if not utils.copy_template(os.path.join(utils.data_dir(), 'templates/core'), self.path, dry):
            print('Could not initialize project.')
            return False

        # Rescan project
        self.scan()

        # Update project information
        self.set_prop('name', name)
        self.set_prop('description', description)
        self.set_prop('author_name', author_name)
        self.set_prop('author_domain', author_domain)
        self.set_prop('author_maintainer', author_maintainer)
        self.set_prop('version', version)

        # Generate README.md
        readme_file = open(os.path.join(self.path, 'README.md'), 'w')
        readme_file.write('# {}\n'.format(name))
        readme_file.write('\n')
        readme_file.write('{}\n'.format(description))
        readme_file.close()

        # Generate LICENSE
        license_file = open(os.path.join(self.path, 'LICENSE'), 'w')
        license_file.write('Copyright (c) {} {}\n'.format(datetime.datetime.now().year, author_name))
        license_file.close()

        # Generate AUTHORS
        authors_file = open(os.path.join(self.path, 'AUTHORS'), 'w')
        authors_file.write('{} <{}>\n'.format(author_name, author_maintainer))
        authors_file.close()

        # Done
        return True

    def generate_library(self, name, dry=True):
        """Generate library"""

        # Check name
        if not name:
            # Invalid name
            print('Please specify a name')
            return False

        # Copy library template
        dst_dir = os.path.join(self.path, 'source', name)
        if not utils.copy_template(os.path.join(utils.data_dir(), 'templates/library'), dst_dir, dry):
            print('Could not generate library.')
            return False

        if not dry:
            # Get important file names
            include_dir_src = os.path.join(dst_dir, 'include', 'lib')
            include_dir_dst = os.path.join(dst_dir, 'include', name)
            header_src = os.path.join(include_dir_dst, 'lib.h')
            header_dst = os.path.join(include_dir_dst, name + '.h')
            impl_src = os.path.join(dst_dir, 'source', 'lib.cpp')
            impl_dst = os.path.join(dst_dir, 'source', name + '.cpp')
            cmake_lists = os.path.join(dst_dir, 'CMakeLists.txt')

            # Rename files
            os.rename(include_dir_src, include_dir_dst)
            os.rename(header_src, header_dst)
            os.rename(impl_src, impl_dst)

            # Replace values in source files
            utils.replace_in_file(header_dst, [
                ( 'proj_name', self.project_name ),
                ( 'lib_name', name ),
                ( 'LIB_NAME', name.upper() )
            ], dry)
            utils.replace_in_file(impl_dst, [
                ( 'proj_name', self.project_name ),
                ( 'lib_name', name ),
                ( 'LIB_NAME', name.upper() )
            ], dry)

            # Replace values in cmake file
            parser = CMakeParser()
            cmake_file = parser.load(cmake_lists)
            if cmake_file:
                cmake_file.set_command_arg([ 'set', 'target' ], 1, name)
                cmake_file.set_command_arg([ 'set', 'headers' ], 1, '${include_path}/' + name + '.h')
                cmake_file.set_command_arg([ 'set', 'sources' ], 1, '${source_path}/' + name + '.cpp')
                cmake_file.save()

            # Add project to main cmake file
            if self.cmake_file_source:
                marker = self.cmake_file_source.find_commands([ 'set', 'IDE_FOLDER', '""'])
                if len(marker) > 0:
                    self.cmake_file_source.add_command([ 'add_subdirectory', name ], after=marker[0])
                    self.cmake_file_source.save()

        # Done
        return True

    def generate_executable(self, name, dry=True):
        """Generate executable"""

        # Check name
        if not name:
            # Invalid name
            print('Please specify a name')
            return False

        # [TODO] Generate executable
        print('Generating executable \'{}\''.format(name))
        return True
