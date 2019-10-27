import argparse

from cml import utils
from cml import Project


# Create argument parser
parser = argparse.ArgumentParser(description='Modern CMake project generator.')
subparsers = parser.add_subparsers(title='subcommands', dest='command')

# General options
parser.add_argument('-d', '--dry-run', help='Do not modify project on disk', action='store_true')

# Command 'get'
sub_parser = subparsers.add_parser('get', help='Get project property')
sub_parser.add_argument('name', help='Property name')

# Command 'set'
sub_parser = subparsers.add_parser('set', help='Set project property')
sub_parser.add_argument('name', help='Property name')
sub_parser.add_argument('value', help='Property value')

# Command 'init'
sub_parser = subparsers.add_parser('init', aliases=['i'], help='Initialize cmake project')
sub_parser.add_argument('-d', '--dry-run', help='Do not modify project on disk', action='store_true')
sub_parser.add_argument('--name', help='Project name')
sub_parser.add_argument('--description', help='Project description')
sub_parser.add_argument('--author-name', help='Author name')
sub_parser.add_argument('--author-domain', help='Author domain')
sub_parser.add_argument('--author-maintainer', help='Author maintainer')
sub_parser.add_argument('--version', help='Version number')

# Command 'generate'
sub_parser = subparsers.add_parser('generate', aliases=['g'], help='Generate sub-project')
sub_parser.add_argument('-d', '--dry-run', help='Do not modify project on disk', action='store_true')
sub_parser.add_argument('type', help='Project type (lib, app, doc)')
sub_parser.add_argument('name', help='Project name')

# Command 'remove'
sub_parser = subparsers.add_parser('remove', aliases=['rm'], help='Remove sub-project')
sub_parser.add_argument('-d', '--dry-run', help='Do not modify project on disk', action='store_true')
sub_parser.add_argument('name', help='Project name')

# Create project
project = Project()
dry_run = True

# Parse command line arguments
args = parser.parse_args()

# Execute commands
if args.command == 'get':
    # Print property value
    value = project.get_prop(args.name)
    if value != None:
        print(value)
if args.command == 'set':
    # Set property value
    project.set_prop(args.name, args.value)
elif args.command == 'init' or args.command == 'i':
    # Initialize project
    project.initialize(name=args.name, description=args.description, author_name=args.author_name,
                       author_domain=args.author_domain, author_maintainer=args.author_maintainer,
                       version=args.version, dry=args.dry_run)
elif args.command == 'generate' or args.command == 'g':
    # Check project type
    if args.type in [ 'lib', 'l' ]:
        # Generate library
        project.generate_library(name=args.name, dry=args.dry_run)
    elif args.type in [ 'exe', 'e' ]:
        # Generate executable
        project.generate_executable(name=args.name, dry=args.dry_run)
    else:
        # Invalid type
        print('Unknown type \'{}\''.format(args.type))
elif args.command == 'remove' or args.command == 'rm':
    # Remove sub-project
    project.remove_subproject(name=args.name, dry=args.dry_run)
