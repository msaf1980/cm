import os

from .cmake import ElementType, TokenType
from .cmake_file import CMakeFile
from .cmake_command import CMakeCommand
from .cmake_comment import CMakeComment
from .cmake_whitespace import CMakeWhitespace


class CMakeParser:
    """A parser for cmake files"""

    def __init__(self):
        """Default Constructor"""

    def load(self, path):
        """Load cmake file"""

        # Tokenize cmake file
        tokens = self.tokenize(path)
        if tokens == None:
            return None

        # Parse structure of cmake file
        cmake_file = self.parse_structure(path, tokens)
        if cmake_file == None:
            return None

        # Done
        return cmake_file

    def tokenize(self, path):
        """Parse cmake file into list of tokens"""

        # Check if file exists
        if not os.path.isfile(path):
            return None

        # Open file
        f = open(path)

        # Tokenizer configuration
        whitespace = [ ' ', '\t' ]
        special = [ '(', ')' ]

        # Tokenize stream
        tokens = []
        token = ''
        mode = TokenType.DEFAULT
        escape_code = False
        while True:
            # Read next character
            c = f.read(1)

            # Implement finite state machine
            next_mode = mode

            # DEFAULT (parsing words/commands)
            if mode == TokenType.DEFAULT:
                if c == '':
                    next_mode = TokenType.EOF
                elif c == '\n':
                    next_mode = TokenType.EOL
                elif c == '#':
                    next_mode = TokenType.COMMENT
                elif c == '"':
                    next_mode = TokenType.STRING
                elif c in special:
                    next_mode = TokenType.SPECIAL_CHAR
                elif c in whitespace:
                    next_mode = TokenType.WHITESPACE

            # WHITESPACE (parsing whitespace)
            elif mode == TokenType.WHITESPACE:
                if c == '':
                    next_mode = TokenType.EOF
                elif c == '\n':
                    next_mode = TokenType.EOL
                elif c == '#':
                    next_mode = TokenType.COMMENT
                elif c == '"':
                    next_mode = TokenType.STRING
                elif c in special:
                    next_mode = TokenType.SPECIAL_CHAR
                elif not c in whitespace:
                    next_mode = TokenType.DEFAULT

            # COMMENT (parsing commands until end of line)
            elif mode == TokenType.COMMENT:
                if c == '':
                    next_mode = TokenType.EOF
                elif c == '\n':
                    next_mode = TokenType.EOL

            # STRING (parsing strings)
            elif mode == TokenType.STRING:
                if c == '':
                    next_mode = TokenType.EOF
                elif c == '\n':
                    next_mode = TokenType.EOL
                elif c == '"' and not escape_code:
                    next_mode = TokenType.DEFAULT
                    token += '"'
                    c = ''

                # Toggle escape-mode
                if c == '\\' and not escape_code:
                    escape_code = True
                else:
                    escape_code = False

            # Finish old word if mode has changed
            if mode != next_mode:
                if len(token) > 0:
                    tokens.append((mode, token))
                token = ''

            # Stop on EOF
            if next_mode == TokenType.EOF:
                break

            # Switch mode
            mode = next_mode

            # End EOL and SPECIAL_CHAR modes right away
            if mode == TokenType.EOL or mode == TokenType.SPECIAL_CHAR:
                # Add token
                tokens.append((mode, c))
                token = ''

                # Switch to default mode
                mode = TokenType.DEFAULT
            else:
                # Add character to word
                token += c

        # Done parsing
        return tokens

    def parse_structure(self, path, tokens):
        """Parse structure of cmake file after loading"""

        # Create object
        cmake_file = CMakeFile(path)

        # Type of the current element
        element = ElementType.WHITESPACE
        command_status = 0

        # Tokens that belong to the current element
        current = []

        # Parse tokens
        for (token_type, token) in tokens:
            # Take token
            current.append((token_type, token))

            # If we don't know what we are parsing, yet:
            if element == ElementType.WHITESPACE:
                # Determine type of element (if possible)
                if token_type == TokenType.DEFAULT:
                    # We are parsing a command
                    element = ElementType.COMMAND
                    command_status = 0
                elif token_type == TokenType.COMMENT:
                    # We are parsing a comment
                    element = ElementType.COMMENT
                elif token_type == TokenType.EOL:
                    # We got an EOL and only whitespace before
                    cmake_file.add(CMakeWhitespace(current))

                    # Start next element
                    element = ElementType.WHITESPACE
                    current = []
                elif token_type != TokenType.WHITESPACE:
                    # Syntax error
                    return None

            # If we are parsing a comment:
            elif element == ElementType.COMMENT:
                # Only accept more comments and whitespace
                if token_type == TokenType.EOL:
                    # End comment
                    cmake_file.add(CMakeComment(current))

                    # Start next element
                    element = ElementType.WHITESPACE
                    current = []
                elif token_type != TokenType.COMMENT and token_type != TokenType.WHITESPACE:
                    # Syntax error
                    return None

            # If we are parsing a command:
            elif element == ElementType.COMMAND:
                # <command_name> '('
                if command_status == 0:
                    # Expect open bracket
                    if token_type == TokenType.SPECIAL_CHAR and token == '(':
                        # Switch to parsing the command arguments
                        command_status = 1
                    elif token_type != TokenType.WHITESPACE:
                        # Syntax error
                        return None

                # <command_name> '(' ...
                elif command_status == 1:
                    # Everything allowed except open bracket
                    if token_type == TokenType.SPECIAL_CHAR and token == ')':
                        # Command has ended
                        command_status = 2
                    elif token_type == TokenType.SPECIAL_CHAR and token == '(':
                        # Syntax error
                        return None

                # <command_name> '(' ... ')'
                elif command_status == 2:
                    # Expect only whitespace, comments, or newline from now on
                    if token_type == TokenType.EOL:
                        # End command
                        cmake_file.add(CMakeCommand(current))

                        # Start next element
                        element = ElementType.WHITESPACE
                        current = []
                    elif not token_type in [ TokenType.WHITESPACE, TokenType.COMMENT ]:
                        # Syntax error
                        return None

        # Done parsing
        return cmake_file
