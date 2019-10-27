#!/bin/env python3
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

# Command 'generate'
sub_parser = subparsers.add_parser('generate', aliases=['g'], help='Generate sub-project')
sub_parser.add_argument('-d', '--dry-run', help='Do not modify project on disk', action='store_true')
sub_parser.add_argument('type', help='Project type (lib, app, doc)')
sub_parser.add_argument('name', help='Project name')

# Command 'test'
# [TODO] Remove
sub_parser = subparsers.add_parser('test', aliases=['i'], help='Execute test operation')

# Create project
project = Project()
dry_run = True

# Parse command line arguments
args = parser.parse_args()

# Execute commands
if args.command == 'get':
    value = project.get_prop(args.name)
    if value != None:
        print(value)
if args.command == 'set':
    project.set_prop(args.name, args.value)
elif args.command == 'init' or args.command == 'i':
    project.initialize(dry=args.dry_run)
elif args.command == 'generate' or args.command == 'g':
    print('Generate project {} ({})'.format(args.name, args.type))
elif args.command == 'test':
    project.test_cmd()
