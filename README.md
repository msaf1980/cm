# cm
Modern CMake project generator.

This application provides a command line tool, `cm`, which enables users to generate and manage projects using C++ and modern CMake-based build systems.

It is based on `cmake-init`, a project template for modern CMake
(https://github.com/cginternals/cmake-init), using its components as
templates for automatically generating cmake projects using a CLI.

At its core, it contains a Python library, `cmi`, which provides functions to parse and manipulate cmake files programmatically. It can be used for example to query if a cmake file contains a specific command, to modify the command parameters, or to add new commands.

`cm` is written in Python3.

## Installation

This project is organized as a Python package and can therefore be installed using the standard Python tools (`pip`, etc.).

To install the library and command line tool to your local package repository, run:

```
> pip install -e .
```

[TODO]: Include package data in setup.py for normal package installation

Afterwards, you can run `cm` in the shell like this:

```
> cm --help
```

## Command line tool

The command line tool `cm` allows you to generate and modify CMake-based C++ projects automatically.

### Initialize project

To initialize a new project, create a directory, enter that directory and run

```
> cm init
```

The application will ask some questions about the project you want to generate:

```
Project name ('test'): 
Project description ('My new project'): 
Author name ('Unknown'): 
Author domain ('https://example.com'): 
Maintainer email address ('example@example.com'): 
Version number ('1.0.0'): 
```

The options can also be specified as command-line parameters. See `cm init --help` for a list of available options.

Afterwards, the project is generated:

```
MKDIR ./cmake
GENERATE ./cmake/Custom.cmake
GENERATE ./cmake/Coverage.cmake
GENERATE ./cmake/GenerateTemplateExportHeader.cmake
GENERATE ./cmake/Cppcheck.cmake
GENERATE ./cmake/Findclang_tidy.cmake
GENERATE ./cmake/Findcppcheck.cmake
GENERATE ./cmake/GetGitRevisionDescription.cmake
GENERATE ./cmake/HealthCheck.cmake
GENERATE ./cmake/CompileOptions.cmake
GENERATE ./cmake/ComponentInstall.cmake
GENERATE ./cmake/GetGitRevisionDescription.cmake.in
GENERATE ./cmake/RuntimeDependencies.cmake
GENERATE ./cmake/Gcov.cmake
GENERATE ./cmake/ClangTidy.cmake
GENERATE ./configure
GENERATE ./AUTHORS
GENERATE ./LICENSE
MKDIR ./data
GENERATE ./data/README.md
GENERATE ./README.md
MKDIR ./source
MKDIR ./source/codegeneration
GENERATE ./source/codegeneration/template_api.h.in
GENERATE ./source/codegeneration/template_msvc_api.h.in
GENERATE ./source/version.h.in
GENERATE ./source/CMakeLists.txt
GENERATE ./CMakeLists.txt
GENERATE ./.gitignore
```

You can now modify the generated project by editing the `CMakeLists.txt` file manually, or generate and build the project by standard CMake procedure. Not however that the project does not contain any targets to build, yet.

```
> mkdir build
> cd build
> make
```

### Project attributes

A project has a number of properties, such as project name, auther, and version, which are encoded inside the `CMakeLists.txt`. They can be accessed either directly by editing the file, or using the command line:

```
> cm get name
test

> cm get description
My new project

> cm get version
1.0.0

> cm get author_name
Unknown

> cm get author_domain
https://example.com

> cm get author_maintainer
example@example.com

```

For example, to modify the name of the project, run:

```
> cm set name myproject
```

This will update the `CMakeLists.txt` file accordingly.

### Adding sub-projects

To add sub-projects such as libraries or executables to the project, the command `generate` can be used. It requires the type ("lib" or "exe") and name of the sub-project.

To add a library to the project, run:

```
> cm generate lib testlib
MKDIR ./source/testlib
MKDIR ./source/testlib/include
MKDIR ./source/testlib/include/lib
GENERATE ./source/testlib/include/lib/lib.h
MKDIR ./source/testlib/source
GENERATE ./source/testlib/source/lib.cpp
GENERATE ./source/testlib/CMakeLists.txt
```

To add an executable to the project, run:

```
> cm generate exe sample
MKDIR ./source/sample
GENERATE ./source/sample/main.cpp
GENERATE ./source/sample/CMakeLists.txt
```

This automatically generates new directories for the sub-projects with the `source`-directory and updates `CMakeLists.txt` accordingly.

### Removing sub-projects

A sub-project can also be removed, deleting all it's directory content and removing it from the `CMakeListst.txt` file in `source`.

```
> cm rm testlib
RM ./source/testlib/include/testlib/testlib.h
RMDIR ./source/testlib/include/testlib
RMDIR ./source/testlib/include
RM ./source/testlib/source/testlib.cpp
RMDIR ./source/testlib/source
RM ./source/testlib/CMakeLists.txt
RMDIR ./source/testlib

> cm rm sample
RM ./source/sample/main.cpp
RM ./source/sample/CMakeLists.txt
RMDIR ./source/sample
```

## Library

In addition to the command line tool, this projects contains a Python library, `cml`, to work with CMake files programmatically. It can be used for example to load and parse cmake files, query and modify their commands, and write the back to disk. In the following, the individual parts of the library are described in more detail.

The class `CMakeParser` provides an interface to load and parse a cmake file. As a result, an object of type `CMakeFile` is created, which can be used to query and modify the contents of the cmake file.

To load a cmake file from disk and print its contents:

```
>>> import cml
>>> parser = cml.CMakeParser()
>>> cmake = parser.load('/projects/test/CMakeLists.txt')
>>> cmake.print()
```

The class `CMakeFile` provides an interface for querying and modifying the contents of a cmake file.
For this, cmake commands are matched by a `signature`, i.e., a list of arbitrary length containing the name and first arguments of the commands to match.

For example, to show us all `install`-directives within the cmake file, we could use the following:

```
>>> cmds = cmake.find_commands([ 'install' ])
>>> for cmd in cmds:
...     cmd.print()
```

Or, to list only `install(FILES)` directives:

```
>>> cmds = cmake.find_commands([ 'install', 'FILES' ])
>>> for cmd in cmds:
...     cmd.print()
```

The function `find_commands` returns a list of `CMakeCommand` instances. This class contains an interface also to edit the command at hand. For example, to find and modify the name of the project, we could do:

```
>>> cmds = cmake.find_commands([ 'set', 'META_PROJECT_NAME' ])
>>> cmds[0].set_arg_value(1, '"newproject"')
>>> cmake.save()
```

Notice that the index of the argument does not include the command name, which cannot be modified using this function. Also, quotes have to be included if the argument is supposed to be a string.

As another example, let's modify the required cmake version for our `CMakeLists.txt`:

```
>>> cmds = cmake.find_commands([ 'cmake_minimum_required' ])
>>> cmds[0].set_arg_value(1, '3.8')
>>> cmake.save()
```

Finally, new commands can be added to the cmake file with the function `add_command`. For example, let's search for the command `add_subdirectory(source)` in our cmake file, and insert a `set`-command right before that, and an additional `include_subdirectory` right after:

```
>>> cmds = cmake.find_commands([ 'add_subdirectory', 'source' ])
>>> cmake.add_command([ 'set', 'IDE_FOLDER', '""' ], before=cmds[0])
>>> cmake.add_command([ 'add_subdirectory', 'docs' ], after=cmds[0])
>>> cmake.save()
```

Now we have two occurrences of `add_subdirectory` in our cmake file. Let's delete the second one:

```
>>> cmds = cmake.find_commands([ 'add_subdirectory' ])
>>> cmds[0].print()
>>> cmds[1].print()
>>> cmake.remove_command(cmds[1])
>>> cmake.save()
```

For a full documentation of all classes and functions, please refer to the generated reference documentation of the library (see `docs`).
