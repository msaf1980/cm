from enum import Enum


class CMakeParser:
    """A parser for cmake files"""

    def __init__(self):
        """Default Constructor"""

    def parse(self, path):
        """Parse cmake file"""
        self.tokenize(path)

    def tokenize(self, path):
        """Parse cmake file into list of tokens"""

        class Mode(Enum):
            DEFAULT = 1
            WHITESPACE = 2
            COMMENT = 3
            STRING = 4
            SPECIAL_CHAR = 5
            EOL = 5
            EOF = 6

        # Tokenizer configuration
        whitespace = [ ' ', '\t' ]
        special = [ '(', ')', ',', ';' ]

        # Open file
        f = open(path)

        # Tokenize stream
        tokens = []
        token = ''
        mode = Mode.DEFAULT
        escape_code = False
        while True:
            # Read next character
            c = f.read(1)

            # Implement finite state machine
            next_mode = mode

            # DEFAULT (parsing words/commands)
            if mode == Mode.DEFAULT:
                if c == '':
                    next_mode = Mode.EOF
                elif c == '\n':
                    next_mode = Mode.EOL
                elif c == '#':
                    next_mode = Mode.COMMENT
                elif c == '"':
                    next_mode = Mode.STRING
                elif c in special:
                    next_mode = Mode.SPECIAL_CHAR
                elif c in whitespace:
                    next_mode = Mode.WHITESPACE

            # WHITESPACE (parsing whitespace)
            elif mode == Mode.WHITESPACE:
                if c == '':
                    next_mode = Mode.EOF
                elif c == '\n':
                    next_mode = Mode.EOL
                elif c == '#':
                    next_mode = Mode.COMMENT
                elif c == '"':
                    next_mode = Mode.STRING
                elif not c in whitespace:
                    next_mode = Mode.DEFAULT

            # COMMENT (parsing commands until end of line)
            elif mode == Mode.COMMENT:
                if c == '':
                    next_mode = Mode.EOF
                elif c == '\n':
                    next_mode = Mode.EOL

            # STRING (parsing strings)
            elif mode == Mode.STRING:
                if c == '':
                    next_mode = Mode.EOF
                elif c == '\n':
                    next_mode = Mode.EOL
                elif c == '"' and not escape_code:
                    next_mode = Mode.DEFAULT
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
                    tokens.append(token)
                token = ''

            # Stop on EOF
            if next_mode == Mode.EOF:
                break

            # Switch mode
            mode = next_mode

            # End EOL and SPECIAL_CHAR modes right away
            if mode == Mode.EOL or mode == Mode.SPECIAL_CHAR:
                # Add token
                tokens.append(c)
                token = ''

                # Switch to default mode
                mode = Mode.DEFAULT
            else:
                # Add character to word
                token += c

        # Display parsed tokens
        for token in tokens:
            print('({})'.format(token), end = '\n')
