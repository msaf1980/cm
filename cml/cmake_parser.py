from enum import Enum


class TokenType(Enum):
    """Type of token"""
    DEFAULT = 1
    WHITESPACE = 2
    COMMENT = 3
    STRING = 4
    SPECIAL_CHAR = 5
    EOL = 6
    EOF = 7

class ElementType(Enum):
    """Type of structurel element"""
    UNKNOWN = 0
    COMMAND = 1
    COMMENT = 2

class CMakeParser:
    """A parser for cmake files"""

    def __init__(self):
        """Default Constructor"""

    def load(self, path):
        """Load cmake file"""
        self.tokenize(path)
        self.parse_structure()

    def tokenize(self, path):
        """Parse cmake file into list of tokens"""

        # Tokenizer configuration
        whitespace = [ ' ', '\t' ]
        special = [ '(', ')' ]

        # Open file
        f = open(path)

        # Tokenize stream
        self.tokens = []
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
                    self.tokens.append((mode, token))
                token = ''

            # Stop on EOF
            if next_mode == TokenType.EOF:
                break

            # Switch mode
            mode = next_mode

            # End EOL and SPECIAL_CHAR modes right away
            if mode == TokenType.EOL or mode == TokenType.SPECIAL_CHAR:
                # Add token
                self.tokens.append((mode, c))
                token = ''

                # Switch to default mode
                mode = TokenType.DEFAULT
            else:
                # Add character to word
                token += c

    def parse_structure(self):
        """Parse structure of cmake file after loading"""

        # Type of the current element
        element = ElementType.UNKNOWN
        command_status = 0

        # Tokens that belong to the current element
        current = []

        # Parse tokens
        for (token_type, token) in self.tokens:
            # Take token
            current.append((token_type, token))

            # If we don't know what we are parsing, yet:
            if element == ElementType.UNKNOWN:
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
                    self.found_whitespace(current)

                    # Start next element
                    element = ElementType.UNKNOWN
                    current = []
                elif token_type != TokenType.WHITESPACE:
                    # Syntax error
                    return False

            # If we are parsing a comment:
            elif element == ElementType.COMMENT:
                # Only accept more comments and whitespace
                if token_type == TokenType.EOL:
                    # End comment
                    self.found_comment(current)

                    # Start next element
                    element = ElementType.UNKNOWN
                    current = []
                elif token_type != TokenType.COMMENT and token_type != TokenType.WHITESPACE:
                    # Syntax error
                    return False

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
                        return False

                # <command_name> '(' ...
                elif command_status == 1:
                    # Everything allowed except open bracket
                    if token_type == TokenType.SPECIAL_CHAR and token == ')':
                        # Command has ended
                        command_status = 2
                    elif token_type == TokenType.SPECIAL_CHAR and token == '(':
                        # Syntax error
                        return False

                # <command_name> '(' ... ')'
                elif command_status == 2:
                    # Expect only whitespace, comments, or newline from now on
                    if token_type == TokenType.EOL:
                        # End command
                        self.found_command(current)

                        # Start next element
                        element = ElementType.UNKNOWN
                        current = []
                    elif not token_type in [ TokenType.WHITESPACE, TokenType.COMMENT ]:
                        # Syntax error
                        return False

    def found_command(self, tokens):
        print('CMD:')
        for (token_type, token) in tokens:
            if token_type in [ TokenType.DEFAULT, TokenType.STRING, TokenType.SPECIAL_CHAR ]:
                print('- {}'.format(token))
        print('')

    def found_comment(self, tokens):
        print('CMT: ', end = '')
        for (token_type, token) in tokens:
            if token_type == TokenType.COMMENT:
                print(token, end = '')
        print('')

    def found_whitespace(self, tokens):
        return

    def print(self):
        """Print structure of cmake to terminal"""

        # Display parsed tokens
        for (token_type, token) in self.tokens:
            if token_type in [ TokenType.DEFAULT, TokenType.STRING, TokenType.SPECIAL_CHAR ]:
                print('- ' + token)
