import os
import shutil

from os import path

def script_dir():
    """Get path to directory the script resides in."""
    return path.realpath(path.join(path.dirname(__file__), '../'))

def data_dir():
    """Get path to cm's data directory."""
    return path.realpath(path.join(path.dirname(__file__), '../data/'))

def dir_empty(path):
    """Check if directory is empty.
    
    Returns True if directory exists and is empty, else False.
    """
    if os.path.exists(path) and os.path.isdir(path):
        return not os.listdir(path)
    else:
        return False

def ensure_dir(path, dry=True):
    """Check if a directory exists and create it if necessary.

    Returns True if directory exists afterwards, else False.
    """

    # Ignore call on dry-run
    if dry:
        return True

    # Create directory if necessary
    if not os.path.isdir(path):
        print('MKDIR {}'.format(path))
        os.mkdir(path)

    # Check again if directory exists
    return os.path.isdir(path)

def copy_template(src, dst, dry=True):
    """Copy template from source to destination directory"""

    # Ensure that destination directory exists
    if not ensure_dir(dst, dry):
        return False

    # List files and directories
    entries = os.listdir(src)

    # Process files and directories
    for entry in entries:
        # Get source and destination path
        src_file = os.path.join(src, entry)
        dst_file = os.path.join(dst, entry)

        # Check if this is a file or a directory
        if os.path.isfile(src_file):
            # Copy file
            print('GENERATE {}'.format(dst_file))
            if not dry:
                shutil.copy(src_file, dst_file)

            # Ensure file exists
            if not dry and not os.path.isfile(dst_file):
                return False
        elif os.path.isdir(src_file):
            # Recurse into subdirectory
            if not copy_template(src_file, dst_file, dry):
                return False

    # Done
    return True

def replace_in_file(path, variables, dry=True):
    """Replace variables in a file"""

    try:
        # Read file content
        f = open(path, 'r')
        content = f.read()
        f.close()

        # Replace variables
        for (key, value) in variables:
            content = content.replace('${' + key + '}', value)

        # Write back file
        f = open(path, 'w')
        f.write(content)
        f.close()

        # Done
        return True
    except:
        # Error
        return False
